"""
API v1 — Intelligence Reasoning Memory, Decision Inspector & Chess-Style Replay Router
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from packages.os_core.chess_replay import ChessReplayEngine
from packages.os_core.event_bus import EventBusManager, EventType
from packages.os_core.intelligence_memory import IntelligenceMemoryStore, ReasoningRecord
from packages.os_core.unified_timeline import UnifiedImmutableTimeline

router = APIRouter(
    prefix="/api/v1/reasoning", tags=["Intelligence Reasoning Memory & Chess Replay"]
)

# Singleton stores wired together
_event_bus = EventBusManager()
_timeline = UnifiedImmutableTimeline()
_event_bus.subscribe(EventType.FORECAST_UPDATED, _timeline.append_event)
_event_bus.subscribe(EventType.PORTFOLIO_REBALANCED, _timeline.append_event)

memory_store = IntelligenceMemoryStore(event_bus=_event_bus)
replay_engine = ChessReplayEngine(_timeline)


@router.post("/store")
async def store_reasoning_record(
    decision_id: str = "dec_example_01",
    selected_action: str = "Increase NVDA allocation to 40% on semiconductor factor momentum",
    confidence_score: float = 0.88,
    evidence_references: list[str] | None = None,
    contradictory_evidence: list[str] | None = None,
    assumptions: list[str] | None = None,
    alternative_actions: list[str] | None = None,
    parent_reasoning_id: str | None = None,
) -> dict[str, Any]:
    """Store a structured AI reasoning record in Intelligence Memory."""
    if assumptions is None:
        assumptions = ["Earnings beat consensus by ≥ 5%"]
    if contradictory_evidence is None:
        contradictory_evidence = ["Rising 10Y yields may compress growth multiples"]
    if evidence_references is None:
        evidence_references = ["NVDA Q2 2026 10-K Item 7", "FRED PCE Inflation Series"]
    alternatives = [
        {"action": a, "rejected": True} for a in (alternative_actions or ["Hold existing weights"])
    ]
    record = ReasoningRecord(
        decision_id=decision_id,
        parent_reasoning_id=parent_reasoning_id,
        evidence_references=evidence_references,
        confidence_score=confidence_score,
        contradictory_evidence=contradictory_evidence,
        assumptions=assumptions,
        alternative_actions_considered=alternatives,
        selected_action=selected_action,
        audit_metadata={"audited_by": "AlphaMind_v2_OS_Kernel"},
    )
    stored = memory_store.store_reasoning(record)
    return stored.model_dump()


@router.get("/records")
async def list_reasoning_records(limit: int = 50) -> list[dict[str, Any]]:
    """List all stored reasoning records (Intelligence Memory Explorer)."""
    records = memory_store.list_all_records(limit=limit)
    return [r.model_dump() for r in records]


@router.get("/records/{reasoning_id}")
async def get_reasoning_record(reasoning_id: str) -> dict[str, Any]:
    """Fetch a single reasoning record by ID (Decision Inspector)."""
    record = memory_store.get_by_reasoning_id(reasoning_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Reasoning record '{reasoning_id}' not found.")
    return record.model_dump()


@router.get("/chain/{decision_id}")
async def get_decision_reasoning_chain(decision_id: str) -> list[dict[str, Any]]:
    """Fetch the full reasoning chain for a given decision ID."""
    chain = memory_store.get_chain_for_decision(decision_id)
    return [r.model_dump() for r in chain]


@router.get("/confidence-evolution")
async def get_confidence_evolution(decision_id: str | None = None) -> list[dict[str, Any]]:
    """Fetch confidence evolution timeline, optionally filtered by decision ID."""
    points = memory_store.get_confidence_evolution(decision_id=decision_id)
    return [p.model_dump() for p in points]


# ── Chess-Style Replay ──────────────────────────────────────────────────────


@router.post("/replay/init")
async def init_chess_replay(limit: int = 100) -> dict[str, Any]:
    """Initialize a chess-style bidirectional replay session from the Unified Timeline."""
    total = replay_engine.initialize_session(limit=limit)
    return {
        "session_id": replay_engine.session_id,
        "total_frames": total,
        "position": replay_engine.current_position,
    }


@router.post("/replay/forward")
async def replay_step_forward() -> dict[str, Any]:
    """Step chess replay one frame forward."""
    frame = replay_engine.step_forward()
    if not frame:
        return {"status": "AT_END", "position": replay_engine.current_position}
    return frame.model_dump()


@router.post("/replay/backward")
async def replay_step_backward() -> dict[str, Any]:
    """Step chess replay one frame backward."""
    frame = replay_engine.step_backward()
    if not frame:
        return {"status": "AT_START", "position": replay_engine.current_position}
    return frame.model_dump()


@router.post("/replay/jump/{step}")
async def replay_jump_to_step(step: int) -> dict[str, Any]:
    """Jump replay directly to a specific step number."""
    frame = replay_engine.jump_to_step(step)
    if not frame:
        raise HTTPException(status_code=400, detail=f"Step {step} is out of replay range.")
    return frame.model_dump()


@router.post("/replay/reset")
async def replay_reset() -> dict[str, Any]:
    """Reset chess replay session to the beginning."""
    replay_engine.reset()
    return {"status": "RESET", "position": replay_engine.current_position}


@router.get("/replay/position")
async def get_replay_position() -> dict[str, Any]:
    """Fetch current chess replay cursor position."""
    return replay_engine.current_position
