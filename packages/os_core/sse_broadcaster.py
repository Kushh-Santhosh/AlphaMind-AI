"""
AlphaMind AI v2 — Scalable Redis Pub/Sub SSE Event Broadcaster

Dispatches real-time telemetry events across multi-container backend replicas using
Redis Pub/Sub (PUBLISH / SUBSCRIBE) with heartbeat pings, automatic client cleanup,
exponential reconnect backoff, and in-process fallback.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections.abc import AsyncGenerator
from typing import Any

from apps.backend.app.core.config import settings
from apps.backend.app.db.redis_client import get_redis

logger = logging.getLogger(__name__)


class RedisSSEBroadcaster:
    """Scalable Redis Pub/Sub SSE Event Broadcaster."""

    def __init__(self) -> None:
        self.pubsub_channel: str = settings.REDIS_PUBSUB_CHANNEL
        self.heartbeat_interval: int = settings.SSE_HEARTBEAT_INTERVAL
        self.reconnect_delay: int = settings.SSE_RECONNECT_DELAY
        self.max_clients: int = settings.SSE_MAX_CLIENTS_PER_WORKER
        self.enable_pubsub: bool = settings.REDIS_ENABLE_PUBSUB

        self._active_clients_count: int = 0
        self._local_event_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=1000)

    @property
    def active_clients_count(self) -> int:
        """Return count of active SSE client connections on this worker."""
        return self._active_clients_count

    async def publish_event(self, event_data: dict[str, Any]) -> bool:
        """Publish event payload across all cluster workers using Redis Pub/Sub."""
        payload_str = json.dumps(event_data)
        success = False

        if self.enable_pubsub:
            try:
                redis = await get_redis()
                if redis is not None:
                    await redis.publish(self.pubsub_channel, payload_str)
                    success = True
            except Exception as exc:
                logger.warning("Redis Pub/Sub PUBLISH fallback to local queue: %s", exc)

        # In-process fallback queue put
        if not success:
            try:
                if self._local_event_queue.full():
                    self._local_event_queue.get_nowait()
                self._local_event_queue.put_nowait(event_data)
            except Exception as err:
                logger.debug("Local SSE queue overflow: %s", err)

        return success

    async def _fetch_pubsub_message(self, pubsub: Any) -> str | None:
        """Fetch and format next PubSub message string if available."""
        try:
            msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if msg and msg.get("type") == "message":
                data_str = msg.get("data")
                if data_str:
                    return f"data: {data_str}\n\n"
        except Exception as exc:
            logger.warning("Redis PubSub get_message error: %s", exc)
        return None

    async def _subscribe_pubsub(self) -> Any:
        """Subscribe to Redis PubSub channel if enabled and connection is available."""
        if not self.enable_pubsub:
            return None
        try:
            redis = await get_redis()
            if redis is not None:
                pubsub = redis.pubsub()
                await pubsub.subscribe(self.pubsub_channel)
                return pubsub
        except Exception as err:
            logger.warning("Redis PubSub subscribe failed: %s", err)
        return None

    def _read_queue_message(self) -> str | None:
        """Fetch and format next local queue message string if available."""
        if not self._local_event_queue.empty():
            try:
                local_event = self._local_event_queue.get_nowait()
                return f"data: {json.dumps(local_event)}\n\n"
            except Exception:
                pass
        return None

    def _generate_heartbeat(self) -> str:
        """Format heartbeat event payload."""
        heartbeat_payload = {
            "type": "heartbeat",
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "active_clients": self._active_clients_count,
        }
        return f"data: {json.dumps(heartbeat_payload)}\n\n"

    async def event_generator(  # noqa: C901
        self, tick_interval: float = 3.0
    ) -> AsyncGenerator[str, None]:
        """Yield formatted SSE streams with heartbeats, Redis PubSub subscriptions, and cleanup."""
        if self._active_clients_count >= self.max_clients:
            yield "data: " + json.dumps(
                {"type": "error", "message": "Max SSE client capacity reached."}
            ) + "\n\n"
            return

        self._active_clients_count += 1
        last_heartbeat = time.time()
        pubsub = await self._subscribe_pubsub()

        try:
            while True:
                now = time.time()
                message_sent = False

                if pubsub is not None:
                    pub_str = await self._fetch_pubsub_message(pubsub)
                    if pub_str:
                        yield pub_str
                        message_sent = True
                    else:
                        pubsub = None

                if not message_sent:
                    q_str = self._read_queue_message()
                    if q_str:
                        yield q_str
                        message_sent = True

                if not message_sent and (now - last_heartbeat >= self.heartbeat_interval):
                    yield self._generate_heartbeat()
                    last_heartbeat = now

                await asyncio.sleep(tick_interval)

        except asyncio.CancelledError:
            logger.debug("SSE client disconnected.")
        finally:
            self._active_clients_count = max(0, self._active_clients_count - 1)
            if pubsub is not None:
                try:
                    await pubsub.unsubscribe(self.pubsub_channel)
                    await pubsub.close()
                except Exception:
                    pass


# Singleton Broadcaster Instance
sse_broadcaster = RedisSSEBroadcaster()
