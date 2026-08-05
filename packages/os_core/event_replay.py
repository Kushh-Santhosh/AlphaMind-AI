"""
AlphaMind AI v2 - Chess-Style Historical Event Replay Engine

Step-by-step event replay engine reconstructing historical market conditions,
AI research reasoning, probability shifts, and portfolio rebalance decisions.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel

from packages.os_core.event_bus import SystemEvent
from packages.os_core.unified_timeline import UnifiedImmutableTimeline

logger = logging.getLogger(__name__)


class ReplayStepState(BaseModel):
    step_index: int
    current_event: SystemEvent
    total_events_in_replay: int
    replayed_at_utc: str


class EventReplayEngine:
    """Replay engine reconstructing historical AI reasoning and system state move-by-move."""

    def __init__(self, timeline: UnifiedImmutableTimeline) -> None:
        self.timeline = timeline
        self.active_replay_events: list[SystemEvent] = []
        self.current_step_cursor: int = 0

    def initialize_replay(self, asset_uuid: str | None = None) -> int:
        """Initialize replay session from timeline history."""
        events = self.timeline.query_timeline(asset_uuid=asset_uuid, limit=100)
        self.active_replay_events = events
        self.current_step_cursor = 0
        logger.info("Initialized EventReplayEngine with %d historical events.", len(events))
        return len(events)

    def step_forward(self) -> ReplayStepState | None:
        """Advance replay by 1 event step forward."""
        if not self.active_replay_events or self.current_step_cursor >= len(
            self.active_replay_events
        ):
            return None

        evt = self.active_replay_events[self.current_step_cursor]
        self.current_step_cursor += 1

        state = ReplayStepState(
            step_index=self.current_step_cursor,
            current_event=evt,
            total_events_in_replay=len(self.active_replay_events),
            replayed_at_utc=evt.timestamp_utc,
        )
        logger.info(
            "Replay Step %d/%d: %s", state.step_index, state.total_events_in_replay, evt.headline
        )
        return state
