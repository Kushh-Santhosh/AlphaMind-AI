"""
API v1 — User Strategy Workspace Router
(Follow funds, clone allocations, compare performance, watchlists, alerts)
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from packages.os_core.event_bus import EventBusManager
from packages.portfolio.multi_strategy_funds import MultiStrategyFundEngine
from packages.portfolio.user_workspace import UserWorkspaceEngine

router = APIRouter(prefix="/api/v1/workspace", tags=["User Strategy Workspace"])

_event_bus = EventBusManager()
_fund_engine = MultiStrategyFundEngine(event_bus=_event_bus)
_fund_engine._initialize_5_funds()
workspace_engine = UserWorkspaceEngine(fund_engine=_fund_engine)


# ── Workspace ─────────────────────────────────────────────────────────────────


@router.get("/{user_id}")
async def get_workspace(user_id: str) -> dict[str, Any]:
    """Retrieve or initialize a user's strategy workspace."""
    ws = workspace_engine.get_or_create_workspace(user_id)
    return ws.model_dump()


# ── Follow / Unfollow Fund ────────────────────────────────────────────────────


@router.post("/{user_id}/follow/{fund_id}")
async def follow_fund(user_id: str, fund_id: str) -> dict[str, Any]:
    """Follow an AI fund in the user's workspace."""
    try:
        ws = workspace_engine.follow_fund(user_id, fund_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ws.model_dump()


@router.delete("/{user_id}/follow/{fund_id}")
async def unfollow_fund(user_id: str, fund_id: str) -> dict[str, Any]:
    """Unfollow an AI fund from the user's workspace."""
    ws = workspace_engine.unfollow_fund(user_id, fund_id)
    return ws.model_dump()


# ── Paper Portfolio ────────────────────────────────────────────────────────────


@router.post("/{user_id}/clone/{fund_id}")
async def clone_fund_allocation(
    user_id: str,
    fund_id: str,
    portfolio_name: str = "",
) -> dict[str, Any]:
    """Clone a live AI fund's allocation into a paper portfolio."""
    try:
        pp = workspace_engine.clone_fund_into_paper_portfolio(user_id, fund_id, portfolio_name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return pp.model_dump()


@router.get("/{user_id}/portfolios/{portfolio_id}")
async def get_paper_portfolio(user_id: str, portfolio_id: str) -> dict[str, Any]:
    """Retrieve a user's paper portfolio by ID."""
    pp = workspace_engine.get_paper_portfolio(user_id, portfolio_id)
    if not pp:
        raise HTTPException(
            status_code=404,
            detail=f"Portfolio '{portfolio_id}' not found for user '{user_id}'.",
        )
    return pp.model_dump()


# ── Performance Comparison ────────────────────────────────────────────────────


@router.get("/{user_id}/compare/{portfolio_id}/vs/{fund_id}")
async def compare_performance(
    user_id: str,
    portfolio_id: str,
    fund_id: str,
) -> dict[str, Any]:
    """Compare a user's paper portfolio performance against an AI fund."""
    try:
        comparison = workspace_engine.compare_with_fund(user_id, portfolio_id, fund_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return comparison.model_dump()


# ── Watchlist ─────────────────────────────────────────────────────────────────


@router.post("/{user_id}/watchlist/{symbol}")
async def add_to_watchlist(
    user_id: str,
    symbol: str,
    asset_class: str = "EQUITY",
    notes: str = "",
) -> dict[str, Any]:
    """Add an asset to the user's watchlist."""
    item = workspace_engine.add_to_watchlist(user_id, symbol, asset_class, notes)
    return item.model_dump()


@router.delete("/{user_id}/watchlist/{symbol}")
async def remove_from_watchlist(user_id: str, symbol: str) -> dict[str, Any]:
    """Remove an asset from the user's watchlist."""
    ws = workspace_engine.remove_from_watchlist(user_id, symbol)
    return ws.model_dump()


# ── Alerts ────────────────────────────────────────────────────────────────────


@router.post("/{user_id}/alerts")
async def create_alert(
    user_id: str,
    title: str = "Market Alert",
    message: str = "NVDA earnings beat consensus by 8%.",
    alert_type: str = "INFO",
) -> dict[str, Any]:
    """Create a non-trading alert for the user."""
    alert = workspace_engine.add_alert(user_id, title, message, alert_type)
    return alert.model_dump()


@router.get("/{user_id}/alerts")
async def get_unread_alerts(user_id: str) -> list[dict[str, Any]]:
    """Fetch unread alerts for a user."""
    alerts = workspace_engine.get_unread_alerts(user_id)
    return [a.model_dump() for a in alerts]


@router.patch("/{user_id}/alerts/{alert_id}/read")
async def mark_alert_read(user_id: str, alert_id: str) -> dict[str, Any]:
    """Mark an alert as read."""
    success = workspace_engine.mark_alert_read(user_id, alert_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Alert '{alert_id}' not found.")
    return {"status": "READ", "alert_id": alert_id}


# ── Supported AI Funds ────────────────────────────────────────────────────────


@router.get("/funds/available")
async def list_available_funds() -> list[dict[str, Any]]:
    """List all AI funds available to follow or clone."""
    funds = _fund_engine.list_all_funds()
    return [
        {
            "fund_id": f.fund_id.value,
            "name": f.name,
            "cagr_pct": f.cagr_pct,
            "sharpe_ratio": f.sharpe_ratio,
            "sortino_ratio": f.sortino_ratio,
            "current_market_value_usd": f.current_market_value_usd,
        }
        for f in funds
    ]
