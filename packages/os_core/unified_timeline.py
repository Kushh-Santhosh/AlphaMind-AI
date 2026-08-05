"""
AlphaMind AI v2 - Unified Immutable Event Timeline Engine

Append-only event store capturing all platform activity, research disclosures, AI decisions,
and alerts into a single queryable, immutable timeline.
"""

from __future__ import annotations

import logging

from packages.os_core.event_bus import EventType, SystemEvent

logger = logging.getLogger(__name__)


class UnifiedImmutableTimeline:
    """Append-only immutable timeline recording every platform system event."""

    def __init__(self) -> None:
        self.timeline_events: list[SystemEvent] = []
        self.event_index: dict[str, SystemEvent] = {}

    def append_event(self, event: SystemEvent) -> SystemEvent:
        """Append new event to immutable timeline."""
        self.timeline_events.append(event)
        self.event_index[event.event_id] = event
        logger.info("Timeline Appended [%s]: %s", event.event_id, event.headline)
        return event

    def get_event_by_id(self, event_id: str) -> SystemEvent | None:
        """Fetch event by ID."""
        return self.event_index.get(event_id)

    def query_timeline(
        self,
        event_type: EventType | None = None,
        asset_uuid: str | None = None,
        limit: int = 50,
    ) -> list[SystemEvent]:
        """Query unified timeline with filters."""
        results = self.timeline_events
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        if asset_uuid:
            results = [e for e in results if e.related_asset_uuid == asset_uuid]
        return results[-limit:]
