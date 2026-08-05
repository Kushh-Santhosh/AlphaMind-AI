"""
Daily Automated Briefings & User Strategy Workspace Test Suite.

Covers:
- DailyBriefingEngine: generate all 5 briefing types, retrieve, list, filter
- BriefingDocument: required fields, evidence links, replay links, disclaimer
- EventBus publication on briefing generation
- UserWorkspaceEngine: create workspace, follow/unfollow, clone, compare, watchlist, alerts
- Performance comparison calculations
- REST API endpoints (briefings + workspace)
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from packages.agents.daily_briefing_engine import BriefingType, DailyBriefingEngine
from packages.os_core.event_bus import EventBusManager, EventType, SystemEvent
from packages.os_core.intelligence_memory import IntelligenceMemoryStore
from packages.os_core.unified_timeline import UnifiedImmutableTimeline
from packages.portfolio.multi_strategy_funds import MultiStrategyFundEngine, StrategyFundType
from packages.portfolio.user_workspace import UserWorkspaceEngine

# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_briefing_engine() -> DailyBriefingEngine:
    bus = EventBusManager()
    tl = UnifiedImmutableTimeline()
    bus.subscribe(EventType.BRIEFING_GENERATED, tl.append_event)
    fund_engine = MultiStrategyFundEngine(event_bus=bus)
    fund_engine._initialize_5_funds()
    memory = IntelligenceMemoryStore(event_bus=bus)
    return DailyBriefingEngine(
        timeline=tl,
        memory_store=memory,
        fund_engine=fund_engine,
        event_bus=bus,
    )


def _make_workspace_engine() -> UserWorkspaceEngine:
    bus = EventBusManager()
    fund_engine = MultiStrategyFundEngine(event_bus=bus)
    fund_engine._initialize_5_funds()
    return UserWorkspaceEngine(fund_engine=fund_engine)


# ── DailyBriefingEngine ───────────────────────────────────────────────────────


def test_generate_morning_brief() -> None:
    """Morning Brief generates a BriefingDocument with all required fields."""
    engine = _make_briefing_engine()
    doc = engine.generate_briefing(BriefingType.MORNING_BRIEF)

    assert doc.briefing_id.startswith("brief_")
    assert doc.briefing_type == BriefingType.MORNING_BRIEF
    assert len(doc.executive_summary) > 10
    assert len(doc.evidence_links) >= 2
    assert doc.disclaimer.startswith("This briefing is generated")
    assert "AlphaMind" in doc.executive_summary


def test_generate_all_five_briefing_types() -> None:
    """All five briefing types generate valid, distinct documents."""
    engine = _make_briefing_engine()
    docs = {bt: engine.generate_briefing(bt) for bt in BriefingType}

    assert len(docs) == 5
    for bt, doc in docs.items():
        assert doc.briefing_type == bt
        assert doc.briefing_id.startswith("brief_")


def test_briefing_list_and_filter() -> None:
    """List briefings filters correctly by type."""
    engine = _make_briefing_engine()
    engine.generate_briefing(BriefingType.MORNING_BRIEF)
    engine.generate_briefing(BriefingType.MORNING_BRIEF)
    engine.generate_briefing(BriefingType.CLOSING_REPORT)

    all_docs = engine.list_briefings()
    morning_docs = engine.list_briefings(briefing_type=BriefingType.MORNING_BRIEF)
    closing_docs = engine.list_briefings(briefing_type=BriefingType.CLOSING_REPORT)

    assert len(all_docs) == 3
    assert len(morning_docs) == 2
    assert len(closing_docs) == 1


def test_briefing_get_by_id() -> None:
    """Generated briefing is retrievable by ID."""
    engine = _make_briefing_engine()
    doc = engine.generate_briefing(BriefingType.WEEKLY_REVIEW)
    fetched = engine.get_briefing(doc.briefing_id)
    assert fetched is not None
    assert fetched.briefing_type == BriefingType.WEEKLY_REVIEW


def test_briefing_publishes_event_to_bus() -> None:
    """Generating a briefing publishes BRIEFING_GENERATED to the EventBus."""
    bus = EventBusManager()
    received: list[SystemEvent] = []
    bus.subscribe(EventType.BRIEFING_GENERATED, lambda e: received.append(e))

    tl = UnifiedImmutableTimeline()
    fund_engine = MultiStrategyFundEngine(event_bus=bus)
    fund_engine._initialize_5_funds()
    memory = IntelligenceMemoryStore()
    engine = DailyBriefingEngine(
        timeline=tl, memory_store=memory, fund_engine=fund_engine, event_bus=bus
    )
    engine.generate_briefing(BriefingType.MIDDAY_UPDATE)

    assert len(received) == 1
    assert received[0].source_subsystem == "daily_briefing_engine"


# ── UserWorkspaceEngine ───────────────────────────────────────────────────────


def test_create_and_get_workspace() -> None:
    """Workspace is created on demand and returned with correct user_id."""
    engine = _make_workspace_engine()
    ws = engine.get_or_create_workspace("user_test_01")
    assert ws.user_id == "user_test_01"
    assert ws.workspace_id.startswith("ws_")


def test_follow_and_unfollow_fund() -> None:
    """Users can follow and unfollow AI funds."""
    engine = _make_workspace_engine()
    engine.follow_fund("user_01", StrategyFundType.GROWTH.value)
    ws = engine.get_or_create_workspace("user_01")
    assert StrategyFundType.GROWTH.value in ws.followed_fund_ids

    engine.unfollow_fund("user_01", StrategyFundType.GROWTH.value)
    assert StrategyFundType.GROWTH.value not in ws.followed_fund_ids


def test_clone_fund_into_paper_portfolio() -> None:
    """Users can clone a live AI fund allocation into a paper portfolio."""
    engine = _make_workspace_engine()
    pp = engine.clone_fund_into_paper_portfolio(
        "user_02", StrategyFundType.GROWTH.value, "My Growth Clone"
    )

    assert pp.portfolio_id.startswith("pp_")
    assert pp.cloned_from_fund_id == StrategyFundType.GROWTH.value
    assert len(pp.allocations) > 0


def test_performance_comparison() -> None:
    """Compare user paper portfolio performance against a live AI fund."""
    engine = _make_workspace_engine()
    pp = engine.clone_fund_into_paper_portfolio("user_03", StrategyFundType.BALANCED.value)
    comparison = engine.compare_with_fund(
        "user_03", pp.portfolio_id, StrategyFundType.BALANCED.value
    )

    assert comparison.user_portfolio_id == pp.portfolio_id
    assert comparison.ai_fund_id == StrategyFundType.BALANCED.value
    assert isinstance(comparison.outperformance_pct, float)


def test_watchlist_add_and_remove() -> None:
    """Users can add and remove items from their watchlist."""
    engine = _make_workspace_engine()
    engine.add_to_watchlist("user_04", "NVDA", "EQUITY", "Semiconductor momentum")
    ws = engine.get_or_create_workspace("user_04")
    assert any(w.symbol == "NVDA" for w in ws.watchlists)

    engine.remove_from_watchlist("user_04", "NVDA")
    ws2 = engine.get_or_create_workspace("user_04")
    assert not any(w.symbol == "NVDA" for w in ws2.watchlists)


def test_alerts_create_and_mark_read() -> None:
    """Non-trading alerts can be created and marked as read."""
    engine = _make_workspace_engine()
    alert = engine.add_alert("user_05", "Test Alert", "NVDA beat by 8%.", "INFO")
    assert not alert.is_read

    success = engine.mark_alert_read("user_05", alert.alert_id)
    assert success

    unread = engine.get_unread_alerts("user_05")
    assert len(unread) == 0


# ── REST API Endpoints ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_briefings_and_workspace_api_endpoints() -> None:
    """All Briefings and Workspace REST endpoints return HTTP 200."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Briefings
        gen_res = await client.post("/api/v1/briefings/generate/MORNING_BRIEF")
        bid = gen_res.json().get("briefing_id", "")
        list_res = await client.get("/api/v1/briefings/list")
        get_res = await client.get(f"/api/v1/briefings/{bid}")

        # Workspace
        ws_res = await client.get("/api/v1/workspace/api_test_user")
        follow_res = await client.post("/api/v1/workspace/api_test_user/follow/GROWTH")
        unfollow_res = await client.delete("/api/v1/workspace/api_test_user/follow/GROWTH")
        clone_res = await client.post("/api/v1/workspace/api_test_user/clone/BALANCED")
        wl_add = await client.post("/api/v1/workspace/api_test_user/watchlist/NVDA")
        wl_del = await client.delete("/api/v1/workspace/api_test_user/watchlist/NVDA")
        alert_res = await client.post("/api/v1/workspace/api_test_user/alerts")
        alert_id = alert_res.json().get("alert_id", "missing_id")
        read_res = await client.patch(f"/api/v1/workspace/api_test_user/alerts/{alert_id}/read")
        unread_res = await client.get("/api/v1/workspace/api_test_user/alerts")
        funds_res = await client.get("/api/v1/workspace/funds/available")

    # Briefings
    assert gen_res.status_code == 200
    assert list_res.status_code == 200
    assert get_res.status_code == 200
    # Workspace
    assert ws_res.status_code == 200
    assert follow_res.status_code == 200
    assert unfollow_res.status_code == 200
    assert clone_res.status_code == 200
    assert wl_add.status_code == 200
    assert wl_del.status_code == 200
    assert alert_res.status_code == 200
    assert read_res.status_code == 200
    assert unread_res.status_code == 200
    assert funds_res.status_code == 200
