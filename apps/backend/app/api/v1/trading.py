"""
AlphaMind AI - Multi-Asset Paper Trading API Router (v4.1)

Exposes paper order placement, positions management, execution trade logs,
portfolio state, and autonomous paper trader execution in [PAPER MODE].
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from packages.agents.agents.autonomous_paper_trader import autonomous_paper_trader
from packages.market.provider_registry import market_data_registry
from packages.portfolio.paper_exchange import (
    PaperExchange,
    SimulatedOrderSide,
    SimulatedOrderStatus,
    SimulatedOrderType,
)
from packages.portfolio.paper_portfolio import PortfolioSimulator
from packages.portfolio.risk_controls import PreTradeRiskEngine

paper_trading_router = APIRouter(prefix="/api/v1/trading", tags=["Paper Trading"])
backtest_router = APIRouter(prefix="/api/v1/backtest-legacy", tags=["Backtesting Legacy"])
risk_router = APIRouter(prefix="/api/v1/risk-legacy", tags=["Risk Legacy"])
logger = logging.getLogger(__name__)

# Shared global paper trading state instances
_exchange = autonomous_paper_trader.exchange
_portfolio = autonomous_paper_trader.portfolio
_risk = autonomous_paper_trader.risk_engine


class OrderSubmissionRequest(BaseModel):
    symbol: str = Field(..., description="Ticker symbol to trade (e.g. AAPL, NVDA, RELIANCE.NS, BTC-USD, WTI)")
    side: str = Field("BUY", description="BUY or SELL")
    order_type: str = Field("MARKET", description="MARKET, LIMIT, STOP")
    quantity: float = Field(..., gt=0, description="Order quantity in units/shares")
    limit_price: Optional[float] = Field(None, description="Limit price for LIMIT orders")
    stop_price: Optional[float] = Field(None, description="Stop price for STOP orders")


@paper_trading_router.post("/orders")
async def submit_paper_order(payload: OrderSubmissionRequest) -> dict[str, Any]:
    """
    Submit a simulated paper trading order backed by live provider market price.
    STRICT MANDATE: Simulated [PAPER MODE] execution with zero real money.
    """
    sym = market_data_registry._normalize_symbol(payload.symbol)
    side_enum = SimulatedOrderSide.BUY if payload.side.upper() == "BUY" else SimulatedOrderSide.SELL
    type_enum = (
        SimulatedOrderType.LIMIT if payload.order_type.upper() == "LIMIT"
        else (SimulatedOrderType.STOP if payload.order_type.upper() == "STOP" else SimulatedOrderType.MARKET)
    )

    # Fetch live price from provider
    snap = await market_data_registry.get_market_snapshot(sym)
    live_price = snap.get("price", 0.0)
    if live_price <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot execute paper order: live price unavailable for '{payload.symbol}'.",
        )

    # Pre-trade risk validation
    risk_res = _risk.validate_pre_trade(
        order_symbol=sym,
        side=side_enum,
        quantity=payload.quantity,
        price=live_price,
        portfolio_state=_portfolio.state,
    )
    if not risk_res.is_approved:
        raise HTTPException(
            status_code=422,
            detail=f"Pre-trade risk rejection: {risk_res.rejection_reason}",
        )

    # Execute fill on virtual exchange
    order = _exchange.submit_order(
        symbol=sym,
        side=side_enum,
        order_type=type_enum,
        quantity=payload.quantity,
        limit_price=payload.limit_price,
        stop_price=payload.stop_price,
        market_price=live_price,
    )

    # Update portfolio state if filled
    if _exchange.trades:
        last_trade = _exchange.trades[-1]
        _portfolio.process_trade(last_trade)

    return {
        "status": "SUCCESS",
        "order": order.model_dump(),
        "live_quote_used": live_price,
        "mode": "PAPER_MODE_SIMULATION",
        "disclaimer": "SIMULATED PAPER EXECUTION ONLY. NO LIVE BROKER ORDER SUBMITTED.",
    }


@paper_trading_router.get("/orders")
async def list_paper_orders() -> dict[str, Any]:
    """Retrieve all simulated orders placed on the paper exchange."""
    return {
        "orders_count": len(_exchange.orders),
        "orders": [o.model_dump() for o in _exchange.orders.values()],
        "mode": "PAPER_MODE",
    }


@paper_trading_router.get("/positions")
async def list_paper_positions() -> dict[str, Any]:
    """Retrieve open multi-asset positions with unrealized P&L and market value."""
    positions_list = []
    for sym, pos in _portfolio.state.positions.items():
        positions_list.append({
            "symbol": sym,
            "quantity": pos.quantity,
            "average_entry_price": pos.average_entry_price,
            "current_market_price": pos.current_market_price,
            "unrealized_pnl_usd": pos.unrealized_pnl_usd,
            "unrealized_return_pct": pos.unrealized_return_pct,
            "market_value_usd": pos.market_value_usd,
        })
    return {
        "positions_count": len(positions_list),
        "positions": positions_list,
        "mode": "PAPER_MODE",
    }


@paper_trading_router.get("/portfolio")
async def get_paper_portfolio_state() -> dict[str, Any]:
    """Retrieve aggregate paper portfolio KPIs, balances, margin, and exposure."""
    st = _portfolio.state
    return {
        "total_portfolio_value_usd": st.total_portfolio_value_usd,
        "cash_balance_usd": st.cash_balance_usd,
        "buying_power_usd": st.buying_power_usd,
        "unrealized_pnl_usd": st.unrealized_pnl_usd,
        "realized_pnl_usd": st.realized_pnl_usd,
        "daily_pnl_usd": st.daily_pnl_usd,
        "maintenance_margin_required_usd": st.maintenance_margin_required_usd,
        "is_margin_call": st.is_margin_call,
        "positions_count": len(st.positions),
        "mode": "PAPER_MODE",
    }


@paper_trading_router.get("/trades")
async def list_paper_trades() -> dict[str, Any]:
    """Retrieve simulated trade execution history log."""
    return {
        "trades_count": len(_exchange.trades),
        "trades": [t.model_dump() for t in _exchange.trades],
        "mode": "PAPER_MODE",
    }


@paper_trading_router.post("/autonomous/cycle")
async def trigger_autonomous_paper_cycle() -> dict[str, Any]:
    """Trigger a one-shot autonomous research -> forecast -> risk -> paper execution loop."""
    res = await autonomous_paper_trader.execute_trading_cycle()
    return {
        "status": res.status,
        "action_taken": res.action_taken,
        "symbol": res.symbol,
        "side": res.side,
        "quantity": res.quantity,
        "fill_price": res.fill_price,
        "opportunity_score": res.opportunity_score,
        "forecast_trend": res.forecast_trend,
        "rejection_reason": res.rejection_reason,
        "timestamp_utc": res.timestamp_utc,
        "mode": res.mode,
    }
