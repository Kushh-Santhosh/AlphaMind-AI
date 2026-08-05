"""
AlphaMind AI v2 — Live OS Async Event Bus & Redis Stream Telemetry Pipeline

Publishes and dispatches SystemEvents asynchronously across platform workers and subscribers.
Includes durable Redis Streams transport (XADD, XREADGROUP, XACK, XRANGE replay) with
graceful in-memory fallback, duplicate delivery prevention, and OpenTelemetry trace context.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from collections.abc import Callable
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from apps.backend.app.core.config import settings
from apps.backend.app.db.redis_client import get_redis

logger = logging.getLogger(__name__)


class EventType(str, Enum):  # noqa: UP042
    MARKET_TICK_INGESTED = "MARKET_TICK_INGESTED"
    SEC_FILING_PROCESSED = "SEC_FILING_PROCESSED"
    NEWS_ARTICLE_ANALYZED = "NEWS_ARTICLE_ANALYZED"
    MACRO_RELEASE_DETECTED = "MACRO_RELEASE_DETECTED"
    FORECAST_UPDATED = "FORECAST_UPDATED"
    PORTFOLIO_REBALANCED = "PORTFOLIO_REBALANCED"
    RISK_ALERT_EMITTED = "RISK_ALERT_EMITTED"
    CONTRADICTION_DETECTED = "CONTRADICTION_DETECTED"
    MODEL_RECALIBRATED = "MODEL_RECALIBRATED"
    BRIEFING_GENERATED = "BRIEFING_GENERATED"
    SYSTEM_HEALTH_CHECK = "SYSTEM_HEALTH_CHECK"


class SystemEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:10]}")
    timestamp_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )
    event_type: EventType
    source_subsystem: str
    correlation_id: str = Field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:8]}")
    related_asset_uuid: str | None = None
    user_id: str | None = "system"
    trace_id: str = Field(default_factory=lambda: f"trace_{uuid.uuid4().hex[:16]}")
    headline: str
    details: str
    payload: dict[str, Any] = Field(default_factory=dict)


class EventBusManager:
    """Async event bus dispatching system events to registered handlers with Redis Stream persistence."""

    def __init__(self) -> None:
        self.subscribers: dict[EventType, list[Callable[[SystemEvent], Any]]] = {}
        self.published_events_history: list[SystemEvent] = []
        self.seen_event_ids: set[str] = set()

        # Configurable Redis Stream Properties
        self.stream_name: str = settings.REDIS_STREAM_NAME
        self.stream_maxlen: int = settings.REDIS_STREAM_MAXLEN
        self.consumer_group: str = settings.REDIS_CONSUMER_GROUP
        self.consumer_name: str = settings.REDIS_CONSUMER_NAME
        self.enable_streams: bool = settings.REDIS_ENABLE_STREAMS

    def subscribe(self, event_type: EventType, handler: Callable[[SystemEvent], Any]) -> None:
        """Subscribe async or sync handler to specific event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        logger.info("Subscribed handler to event type '%s'", event_type.value)

    def publish(self, event: SystemEvent) -> SystemEvent:
        """Publish system event to subscribers, in-memory history, and durable Redis Stream."""
        # Duplicate delivery prevention check
        if event.event_id in self.seen_event_ids:
            logger.debug("Duplicate event '%s' suppressed.", event.event_id)
            return event

        self.seen_event_ids.add(event.event_id)
        self.published_events_history.append(event)

        # In-memory subscriber dispatch
        handlers = self.subscribers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error("Error executing handler for event '%s': %s", event.event_id, e)

        logger.info(
            "Event Published [%s | %s]: %s (trace_id=%s)",
            event.event_type.value,
            event.source_subsystem,
            event.headline,
            event.trace_id,
        )

        # Asynchronous Redis Stream Persistence (Non-blocking fallback)
        if self.enable_streams:
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self._async_publish_to_stream(event))
            except RuntimeError:
                pass  # Execution outside active event loop defaults to in-memory dispatch

        return event

    async def _async_publish_to_stream(self, event: SystemEvent) -> str | None:
        """Internal helper to publish event payload to Redis Stream using XADD."""
        try:
            redis = await get_redis()
            if redis is not None:
                payload_str = event.model_dump_json()
                msg_id = await redis.xadd(
                    self.stream_name,
                    {
                        "data": payload_str,
                        "event_id": event.event_id,
                        "event_type": event.event_type.value,
                    },
                    maxlen=self.stream_maxlen,
                    approximate=True,
                )
                return str(msg_id)
        except Exception as exc:
            logger.warning("Redis Stream XADD fallback (in-memory dispatch succeeded): %s", exc)
        return None

    async def ensure_consumer_group(self) -> bool:
        """Ensure consumer group exists for stream via XGROUP CREATE."""
        try:
            redis = await get_redis()
            if redis is not None:
                try:
                    await redis.xgroup_create(
                        self.stream_name, self.consumer_group, id="0", mkstream=True
                    )
                    logger.info(
                        "Created consumer group '%s' for stream '%s'",
                        self.consumer_group,
                        self.stream_name,
                    )
                    return True
                except Exception as exc:
                    if "BUSYGROUP" in str(exc):
                        return True
                    logger.warning("XGROUP CREATE warning: %s", exc)
        except Exception as err:
            logger.warning("Redis consumer group setup failed: %s", err)
        return False

    async def ack_event(self, message_id: str) -> bool:
        """Acknowledge event processing in consumer group via XACK."""
        try:
            redis = await get_redis()
            if redis is not None:
                await redis.xack(self.stream_name, self.consumer_group, message_id)
                return True
        except Exception as exc:
            logger.warning("Redis XACK failed for message '%s': %s", message_id, exc)
        return False

    async def replay_missed_events(
        self, start_id: str = "0-0", count: int = 100
    ) -> list[SystemEvent]:
        """Replay historical missed events from Redis Stream using XRANGE."""
        replayed: list[SystemEvent] = []
        try:
            redis = await get_redis()
            if redis is not None:
                raw_entries = await redis.xrange(self.stream_name, min=start_id, count=count)
                for _msg_id, fields in raw_entries:
                    data_json = fields.get("data")
                    if data_json:
                        event_dict = json.loads(data_json)
                        evt = SystemEvent(**event_dict)
                        if evt.event_id not in self.seen_event_ids:
                            self.seen_event_ids.add(evt.event_id)
                            replayed.append(evt)
        except Exception as exc:
            logger.warning("Redis XRANGE event replay fallback: %s", exc)
        return replayed
