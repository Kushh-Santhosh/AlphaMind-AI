"""
Multi-Strategy Virtual AI Funds Test Suite — 5 Strategy Funds, Rebalance Engine,
Decision Lineage Citations, Public Leaderboard Competition, and REST APIs.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from packages.os_core.event_bus import EventBusManager, EventType
from packages.portfolio.fund_competition import FundCompetitionLeaderboard
from packages.portfolio.multi_strategy_funds import MultiStrategyFundEngine, StrategyFundType


def test_5_virtual_ai_funds_initialization() -> None:
    """Test that all 5 permanent virtual AI funds are initialized."""
    engine = MultiStrategyFundEngine()
    funds = engine.list_all_funds()

    assert len(funds) == 5
    fund_ids = {f.fund_id for f in funds}
    assert StrategyFundType.CONSERVATIVE in fund_ids
    assert StrategyFundType.BALANCED in fund_ids
    assert StrategyFundType.GROWTH in fund_ids
    assert StrategyFundType.AGGRESSIVE in fund_ids
    assert StrategyFundType.CRYPTO in fund_ids


def test_fund_rebalance_publishes_event_to_timeline() -> None:
    """Test that fund rebalancing publishes SystemEvents to the EventBus."""
    bus = EventBusManager()
    engine = MultiStrategyFundEngine(event_bus=bus)

    rec = engine.rebalance_fund(
        fund_id=StrategyFundType.GROWTH,
        target_allocations={"NVDA": 0.40, "QQQ": 0.40, "AAPL": 0.20},
        reasoning_summary="Rebalancing Tech Fund for semiconductor factor momentum",
        evidence_citations=["SEC Form 10-K Item 7", "NVIDIA Q2 Earnings"],
    )

    assert rec.fund_id == StrategyFundType.GROWTH
    assert rec.decision_id.startswith("dec_")
    assert len(bus.published_events_history) == 1
    assert bus.published_events_history[0].event_type == EventType.PORTFOLIO_REBALANCED


def test_decision_lineage_citations_and_risk() -> None:
    """Test that decision records contain evidence citations and risk assessments."""
    engine = MultiStrategyFundEngine()
    rec = engine.rebalance_fund(
        fund_id=StrategyFundType.CONSERVATIVE,
        target_allocations={"TLT": 0.50, "CASH": 0.50},
        reasoning_summary="Increasing fixed income allocation to hedge rate risks",
        evidence_citations=["FRED Federal Reserve Interest Rates"],
        confidence_score=0.92,
    )

    assert rec.confidence_score == 0.92
    assert "FRED Federal Reserve Interest Rates" in rec.evidence_citations
    assert "var_95_pct" in rec.risk_assessment


def test_fund_competition_leaderboard_ranking() -> None:
    """Test composite scoring and ranking of the 5 virtual funds on the leaderboard."""
    engine = MultiStrategyFundEngine()
    leaderboard = FundCompetitionLeaderboard(engine)
    rankings = leaderboard.get_leaderboard()

    assert len(rankings) == 5
    assert rankings[0].rank == 1
    assert rankings[0].composite_score >= rankings[1].composite_score


@pytest.mark.asyncio
async def test_funds_rest_api_endpoints() -> None:
    """Test Multi-Strategy Funds REST API endpoints (/funds, /funds/leaderboard, /funds/compare, /funds/{fund_id}, /funds/{fund_id}/rebalance)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_funds = await client.get("/api/v1/funds")
        res_leaderboard = await client.get("/api/v1/funds/leaderboard")
        res_compare = await client.get("/api/v1/funds/compare")
        res_single = await client.get("/api/v1/funds/GROWTH")
        res_rebalance = await client.post(
            "/api/v1/funds/GROWTH/rebalance",
            json={
                "allocations": {"NVDA": 0.5, "QQQ": 0.5},
                "reasoning_summary": "API Test Rebalance",
                "evidence_citations": ["API Citation 1"],
            },
        )

    assert res_funds.status_code == 200
    assert res_leaderboard.status_code == 200
    assert res_compare.status_code == 200
    assert res_single.status_code == 200
    assert res_rebalance.status_code == 200
