"""
API v1 — Multi-Strategy Virtual AI Funds & Competition Router
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from packages.portfolio.fund_competition import FundCompetitionLeaderboard
from packages.portfolio.multi_strategy_funds import MultiStrategyFundEngine, StrategyFundType

router = APIRouter(prefix="/api/v1/funds", tags=["Multi-Strategy Virtual AI Funds"])

fund_engine = MultiStrategyFundEngine()
leaderboard_engine = FundCompetitionLeaderboard(fund_engine)


@router.get("")
async def list_virtual_funds() -> list[dict[str, Any]]:
    """List all 5 permanent virtual strategy AI funds."""
    funds = fund_engine.list_all_funds()
    return [f.model_dump() for f in funds]


@router.get("/leaderboard")
async def get_fund_leaderboard() -> list[dict[str, Any]]:
    """Fetch public fund competition leaderboard ranking virtual funds."""
    rankings = leaderboard_engine.get_leaderboard()
    return [r.model_dump() for r in rankings]


@router.get("/compare")
async def compare_funds_matrix() -> dict[str, Any]:
    """Fetch side-by-side comparison matrix across all 5 virtual funds."""
    funds = fund_engine.list_all_funds()
    return {
        "funds_count": len(funds),
        "comparison": [
            {
                "fund_id": f.fund_id.value,
                "name": f.name,
                "cagr_pct": f.cagr_pct,
                "sharpe_ratio": f.sharpe_ratio,
                "sortino_ratio": f.sortino_ratio,
                "max_drawdown_limit_pct": f.max_drawdown_limit_pct,
                "allocations": f.allocations,
            }
            for f in funds
        ],
    }


@router.get("/{fund_id}")
async def get_virtual_fund(fund_id: StrategyFundType) -> dict[str, Any]:
    """Fetch detailed portfolio and state for specific virtual fund."""
    fund = fund_engine.get_fund(fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail=f"Fund '{fund_id}' not found.")
    return fund.model_dump()


@router.post("/{fund_id}/rebalance")
async def rebalance_virtual_fund(
    fund_id: StrategyFundType,
    allocations: dict[str, float],
    reasoning_summary: str = "Quarterly factor momentum rebalance",
    evidence_citations: list[str] | None = None,
) -> dict[str, Any]:
    """Trigger fund rebalance and publish transparent decision record."""
    try:
        citations = evidence_citations or ["SEC Form 10-K Item 7", "FRED Inflation CPI"]
        record = fund_engine.rebalance_fund(
            fund_id=fund_id,
            target_allocations=allocations,
            reasoning_summary=reasoning_summary,
            evidence_citations=citations,
        )
        return record.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{fund_id}/decisions")
async def get_fund_decision_history(fund_id: StrategyFundType) -> list[dict[str, Any]]:
    """Fetch complete decision history and citations for specific virtual fund."""
    fund = fund_engine.get_fund(fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail=f"Fund '{fund_id}' not found.")
    return [d.model_dump() for d in fund.decision_history]
