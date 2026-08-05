"""
AlphaMind AI v2 - Enhanced Chess-Style Bidirectional Event Replay Engine

Extends the Milestone 17 EventReplayEngine into a full chess-style timeline where
users can step forward and backward through historical events and inspect:
  - market conditions at each tick
  - research / SEC filing updates
  - forecast changes (with confidence evolution)
  - portfolio rebalance decisions
  - AI reasoning chain snapshots

Each replay frame is enriched with reasoning memory if available.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel

from packages.os_core.event_bus import SystemEvent
from packages.os_core.unified_timeline import UnifiedImmutableTimeline

logger = logging.getLogger(__name__)


class ReplayFrame(BaseModel):
    """A single, enriched chess-style replay frame."""

    step_index: int
    direction: str  # "FORWARD" | "BACKWARD"
    current_event: SystemEvent
    total_frames: int
    replayed_at_utc: str
    # Enriched context available at this step
    market_context: dict[str, Any] = {}
    research_context: dict[str, Any] = {}
    forecast_context: dict[str, Any] = {}
    portfolio_context: dict[str, Any] = {}
    ai_reasoning_snapshot: dict[str, Any] | None = None
    confidence_at_step: float | None = None


class ChessReplayEngine:
    """
    Bidirectional chess-style event replay engine.
    Supports step_forward, step_backward, jump_to_step, and reset.
    Every frame is enriched with market, research, forecast and reasoning context.
    """

    def __init__(self, timeline: UnifiedImmutableTimeline) -> None:
        self.timeline = timeline
        self.session_events: list[SystemEvent] = []
        self.cursor: int = 0
        self.session_id: str | None = None

    def initialize_session(
        self,
        asset_uuid: str | None = None,
        limit: int = 100,
    ) -> int:
        """
        Initialize a replay session from the Unified Immutable Timeline.
        Returns the total number of frames available.
        """
        import uuid as _uuid

        self.session_events = self.timeline.query_timeline(asset_uuid=asset_uuid, limit=limit)
        self.cursor = 0
        self.session_id = f"replay_{_uuid.uuid4().hex[:8]}"
        logger.info(
            "ChessReplayEngine session '%s' initialized with %d frames.",
            self.session_id,
            len(self.session_events),
        )
        return len(self.session_events)

    def _build_frame(self, idx: int, direction: str) -> ReplayFrame:
        """Build an enriched replay frame at the given cursor index."""
        import time

        evt = self.session_events[idx]
        event_type_val = evt.event_type.value

        return ReplayFrame(
            step_index=idx + 1,
            direction=direction,
            current_event=evt,
            total_frames=len(self.session_events),
            replayed_at_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            market_context=(
                {"quote_symbol": evt.payload.get("symbol", "N/A"), "source": evt.source_subsystem}
                if "MARKET" in event_type_val
                else {}
            ),
            research_context=(
                {"filing_type": "10-K", "source": evt.source_subsystem}
                if "SEC" in event_type_val or "FILING" in event_type_val
                else {}
            ),
            forecast_context=(
                {"probability_update": True, "source": evt.source_subsystem}
                if "FORECAST" in event_type_val
                else {}
            ),
            portfolio_context=(
                {"rebalance": True, "fund_payload": evt.payload}
                if "PORTFOLIO" in event_type_val
                else {}
            ),
            ai_reasoning_snapshot=(
                {"reasoning_id": evt.payload.get("reasoning_id"), "selected_action": evt.headline}
                if evt.payload.get("reasoning_id")
                else None
            ),
            confidence_at_step=evt.payload.get("confidence_score"),
        )

    def step_forward(self) -> ReplayFrame | None:
        """Advance replay cursor by one frame (forward direction)."""
        if not self.session_events or self.cursor >= len(self.session_events):
            logger.debug("ChessReplayEngine: reached end of replay at step %d.", self.cursor)
            return None
        frame = self._build_frame(self.cursor, "FORWARD")
        self.cursor += 1
        logger.info("Chess replay step FORWARD → frame %d/%d", frame.step_index, frame.total_frames)
        return frame

    def step_backward(self) -> ReplayFrame | None:
        """Step replay cursor back by one frame (backward direction)."""
        if not self.session_events or self.cursor <= 1:
            logger.debug("ChessReplayEngine: already at start of replay.")
            return None
        self.cursor -= 1
        frame = self._build_frame(self.cursor - 1, "BACKWARD")
        logger.info(
            "Chess replay step BACKWARD → frame %d/%d", frame.step_index, frame.total_frames
        )
        return frame

    def jump_to_step(self, step: int) -> ReplayFrame | None:
        """Jump replay cursor directly to a specific step index (1-based)."""
        idx = step - 1
        if idx < 0 or idx >= len(self.session_events):
            logger.warning("ChessReplayEngine: jump to step %d out of range.", step)
            return None
        self.cursor = idx + 1
        return self._build_frame(idx, "JUMP")

    def reset(self) -> None:
        """Reset replay session cursor to beginning."""
        self.cursor = 0
        logger.info("ChessReplayEngine session '%s' reset to beginning.", self.session_id)

    @property
    def current_position(self) -> dict[str, Any]:
        """Return current session cursor position metadata."""
        return {
            "session_id": self.session_id,
            "current_step": self.cursor,
            "total_frames": len(self.session_events),
            "at_start": self.cursor == 0,
            "at_end": self.cursor >= len(self.session_events),
        }
