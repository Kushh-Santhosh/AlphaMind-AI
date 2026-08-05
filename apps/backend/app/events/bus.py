"""
AlphaMind AI - In-Memory & Redis Pub/Sub Event Bus Engine
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from typing import Any

from apps.backend.app.events.contracts import EventMessage
from apps.backend.app.events.dlq import DeadLetterQueue

logger = logging.getLogger(__name__)


class EventBus:
    """Event Bus managing topic subscriptions, event publication, and DLQ fallbacks."""

    def __init__(self, dlq: DeadLetterQueue) -> None:
        self.dlq = dlq
        self._subscribers: dict[str, list[Callable[[EventMessage], Any]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[EventMessage], Any]) -> None:
        """Subscribe a handler callback to a specific event_type topic."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.info("Subscribed handler '%s' to event topic '%s'", handler.__name__, event_type)

    async def publish(self, event: EventMessage) -> None:
        """Publish event message to all registered subscriber callbacks."""
        handlers = self._subscribers.get(event.event_type, [])
        if not handlers:
            logger.debug("No subscribers registered for event type '%s'", event.event_type)
            return

        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as exc:
                event.retry_count += 1
                if event.retry_count > event.max_retries:
                    self.dlq.push(event, str(exc))
                else:
                    logger.warning(
                        "Event %s handler '%s' failed (retry %d/%d): %s",
                        event.event_id,
                        handler.__name__,
                        event.retry_count,
                        event.max_retries,
                        exc,
                    )
                    # Re-publish for retry
                    await self.publish(event)
