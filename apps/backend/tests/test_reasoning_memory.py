"""
Intelligence Reasoning Memory & Chess Replay Engine Test Suite.

Covers:
- ReasoningRecord storage, retrieval, and parent-chain linkage
- IntelligenceMemoryStore decision-index and workflow-index
- Confidence evolution timeline
- EventBus publication on store
- ChessReplayEngine: forward, backward, jump, reset, position
- REST API endpoints
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from apps.backend.app.middleware.rate_limit import _IN_MEMORY_BUCKET
from packages.os_core.chess_replay import ChessReplayEngine
from packages.os_core.event_bus import EventBusManager, EventType, SystemEvent
from packages.os_core.intelligence_memory import IntelligenceMemoryStore, ReasoningRecord
from packages.os_core.unified_timeline import UnifiedImmutableTimeline


@pytest.fixture(autouse=True)
def _reset_rate_limit():
    _IN_MEMORY_BUCKET.clear()
    yield
    _IN_MEMORY_BUCKET.clear()

# ── Helpers ────────────────────────────────────────────────────────────────────


def _make_record(
    decision_id: str = "dec_001",
    confidence: float = 0.85,
    parent: str | None = None,
) -> ReasoningRecord:
    return ReasoningRecord(
        decision_id=decision_id,
        parent_reasoning_id=parent,
        evidence_references=["SEC 10-K Item 7", "FRED CPI 2026-07"],
        confidence_score=confidence,
        contradictory_evidence=["Rising yields compress multiples"],
        assumptions=["Fed holds rates through Q4"],
        alternative_actions_considered=[{"action": "Hold weights", "rejected": True}],
        selected_action="Increase NVDA to 40%",
        audit_metadata={"audited_by": "pytest_suite"},
    )


def _seed_timeline(n: int = 5) -> UnifiedImmutableTimeline:
    """Create a timeline pre-seeded with n events."""
    tl = UnifiedImmutableTimeline()
    for i in range(n):
        tl.append_event(
            SystemEvent(
                event_type=EventType.FORECAST_UPDATED,
                source_subsystem="test_seeder",
                headline=f"Seed Event {i + 1}",
                details=f"Detail {i + 1}",
            )
        )
    return tl


# ── Intelligence Memory Store ──────────────────────────────────────────────────


def test_store_and_retrieve_reasoning_record() -> None:
    """Reasoning records are stored and retrievable by reasoning_id."""
    store = IntelligenceMemoryStore()
    rec = store.store_reasoning(_make_record())

    assert rec.reasoning_id.startswith("rsn_")
    fetched = store.get_by_reasoning_id(rec.reasoning_id)
    assert fetched is not None
    assert fetched.selected_action == "Increase NVDA to 40%"


def test_reasoning_chain_parent_linkage() -> None:
    """Parent-child reasoning chains are navigable via decision_id."""
    store = IntelligenceMemoryStore()
    parent = store.store_reasoning(_make_record(decision_id="dec_parent"))
    child = store.store_reasoning(
        _make_record(decision_id="dec_parent", parent=parent.reasoning_id)
    )

    chain = store.get_chain_for_decision("dec_parent")
    assert len(chain) == 2
    assert child.parent_reasoning_id == parent.reasoning_id


def test_workflow_index() -> None:
    """Records sharing a workflow_id are grouped correctly."""
    store = IntelligenceMemoryStore()
    rec1 = _make_record(decision_id="dec_a")
    rec1.workflow_id = "wf_shared_99"
    rec2 = _make_record(decision_id="dec_b")
    rec2.workflow_id = "wf_shared_99"
    store.store_reasoning(rec1)
    store.store_reasoning(rec2)

    chain = store.get_chain_for_workflow("wf_shared_99")
    assert len(chain) == 2


def test_confidence_evolution_timeline() -> None:
    """Confidence evolution points are appended and filterable by decision_id."""
    store = IntelligenceMemoryStore()
    store.store_reasoning(_make_record(decision_id="dec_conf", confidence=0.70))
    store.store_reasoning(_make_record(decision_id="dec_conf", confidence=0.85))
    store.store_reasoning(_make_record(decision_id="dec_other", confidence=0.90))

    evolution = store.get_confidence_evolution(decision_id="dec_conf")
    assert len(evolution) == 2
    assert evolution[0].confidence_score == 0.70
    assert evolution[1].confidence_score == 0.85


def test_reasoning_store_publishes_event_to_bus() -> None:
    """Storing a reasoning record publishes a FORECAST_UPDATED SystemEvent."""
    bus = EventBusManager()
    received: list[SystemEvent] = []
    bus.subscribe(EventType.FORECAST_UPDATED, lambda e: received.append(e))

    store = IntelligenceMemoryStore(event_bus=bus)
    store.store_reasoning(_make_record())

    assert len(received) == 1
    assert received[0].source_subsystem == "intelligence_memory"


# ── Chess Replay Engine ────────────────────────────────────────────────────────


def test_chess_replay_forward_and_backward() -> None:
    """Chess replay steps forward and backward through timeline frames."""
    tl = _seed_timeline(5)
    engine = ChessReplayEngine(tl)
    total = engine.initialize_session()
    assert total == 5

    f1 = engine.step_forward()
    assert f1 is not None and f1.step_index == 1 and f1.direction == "FORWARD"

    f2 = engine.step_forward()
    assert f2 is not None and f2.step_index == 2

    back = engine.step_backward()
    assert back is not None and back.step_index == 1 and back.direction == "BACKWARD"


def test_chess_replay_jump_and_reset() -> None:
    """Chess replay jump_to_step and reset work correctly."""
    tl = _seed_timeline(10)
    engine = ChessReplayEngine(tl)
    engine.initialize_session()

    jumped = engine.jump_to_step(7)
    assert jumped is not None and jumped.step_index == 7 and jumped.direction == "JUMP"

    engine.reset()
    assert engine.current_position["current_step"] == 0
    assert engine.current_position["at_start"] is True


def test_chess_replay_at_boundaries() -> None:
    """Chess replay returns None when stepping past the start or end."""
    tl = _seed_timeline(2)
    engine = ChessReplayEngine(tl)
    engine.initialize_session()

    # At start, backward returns None
    assert engine.step_backward() is None

    engine.step_forward()
    engine.step_forward()
    # Past end, forward returns None
    assert engine.step_forward() is None


# ── REST API Endpoints ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_reasoning_rest_api_endpoints() -> None:
    """All Reasoning Memory & Chess Replay REST endpoints return HTTP 200."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Store a reasoning record
        store_res = await client.post(
            "/api/v1/reasoning/store",
            params={
                "decision_id": "dec_api_test",
                "selected_action": "API test action",
                "confidence_score": 0.80,
            },
        )
        data = store_res.json()
        rid = data.get("reasoning_id", "")

        res_list = await client.get("/api/v1/reasoning/records")
        res_get = await client.get(f"/api/v1/reasoning/records/{rid}")
        res_chain = await client.get("/api/v1/reasoning/chain/dec_api_test")
        res_conf = await client.get("/api/v1/reasoning/confidence-evolution")

        # Replay endpoints
        res_init = await client.post("/api/v1/reasoning/replay/init")
        res_fwd = await client.post("/api/v1/reasoning/replay/forward")
        res_bwd = await client.post("/api/v1/reasoning/replay/backward")
        res_reset = await client.post("/api/v1/reasoning/replay/reset")
        res_pos = await client.get("/api/v1/reasoning/replay/position")

    assert store_res.status_code == 200
    assert res_list.status_code == 200
    assert res_get.status_code == 200
    assert res_chain.status_code == 200
    assert res_conf.status_code == 200
    assert res_init.status_code == 200
    assert res_fwd.status_code == 200
    assert res_bwd.status_code == 200
    assert res_reset.status_code == 200
    assert res_pos.status_code == 200
