"""
AlphaMind AI - Dead Letter Queue (DLQ) & Retry Policy Engine
"""

from __future__ import annotations

import logging

from apps.backend.app.events.contracts import EventMessage

logger = logging.getLogger(__name__)


class DeadLetterQueue:
    """Dead Letter Queue (DLQ) for failed event message captures."""

    def __init__(self) -> None:
        self._dlq_messages: list[EventMessage] = []

    def push(self, message: EventMessage, failure_reason: str) -> None:
        """Push a failed message to DLQ after retries are exhausted."""
        logger.error(
            "DLQ PUSH: Event %s (type: %s) failed retries (%d/%d). Reason: %s",
            message.event_id,
            message.event_type,
            message.retry_count,
            message.max_retries,
            failure_reason,
        )
        self._dlq_messages.append(message)

    def list_dlq(self) -> list[EventMessage]:
        """Return all failed messages currently in DLQ."""
        return list(self._dlq_messages)

    def size(self) -> int:
        """Return total size of DLQ."""
        return len(self._dlq_messages)

    def clear(self) -> None:
        """Clear DLQ messages."""
        self._dlq_messages.clear()
