"""
API v1 — Execution Simulation Platform Router
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from packages.portfolio.market_replay import MarketReplayEngine, ReplayScenario
from packages.portfolio.paper_exchange import PaperExchange, SimulatedOrderSide, SimulatedOrderType
from packages.portfolio.paper_portfolio import PortfolioSimulator
from packages.portfolio.risk_controls import PreTradeRiskEngine

router = APIRouter(prefix="/api/v1/simulation", tags=["Execution Simulation Platform"])

paper_exchange = PaperExchange()
portfolio_simulator = PortfolioSimulator()
pre_trade_risk = PreTradeRiskEngine()
replay_engine = MarketReplayEngine()


@router.post("/order")
async def submit_simulated_order(
    symbol: str = "AAPL",
    side: SimulatedOrderSide = SimulatedOrderSide.BUY,
    order_type: SimulatedOrderType = SimulatedOrderType.MARKET,
    quantity: float = 10.0,
    limit_price: float | None = None,
    stop_price: float | None = None,
    market_price: float = 150.0,
) -> dict[str, Any]:
    """Submit order to virtual paper exchange following pre-trade risk checks."""
    # Pre-trade risk validation
    risk_res = pre_trade_risk.validate_pre_trade(
        symbol, side, quantity, market_price, portfolio_simulator.state
    )
    if not risk_res.is_approved:
        raise HTTPException(status_code=400, detail=risk_res.rejection_reason)

    # Submit virtual order
    order = paper_exchange.submit_order(
        symbol, side, order_type, quantity, limit_price, stop_price, market_price
    )

    # Process simulated trade in portfolio state
    if paper_exchange.trades:
        portfolio_simulator.process_trade(paper_exchange.trades[-1])

    return {
        "order": order.model_dump(),
        "portfolio_state": portfolio_simulator.state.model_dump(),
    }


@router.delete("/order/{order_id}")
async def cancel_simulated_order(order_id: str) -> dict[str, Any]:
    """Cancel pending virtual order."""
    order = paper_exchange.cancel_order(order_id)
    return order.model_dump()


@router.get("/orders")
async def list_simulated_orders() -> list[dict[str, Any]]:
    """List virtual exchange order history."""
    return [o.model_dump() for o in paper_exchange.orders.values()]


@router.get("/trades")
async def list_simulated_trades() -> list[dict[str, Any]]:
    """List virtual exchange executed trade history."""
    return [t.model_dump() for t in paper_exchange.trades]


@router.get("/positions")
async def get_portfolio_positions() -> dict[str, Any]:
    """Fetch virtual portfolio positions, cash, and P/L."""
    return portfolio_simulator.state.model_dump()


@router.get("/performance")
async def get_simulation_performance() -> dict[str, Any]:
    """Fetch virtual execution analytics, slippage, and fill statistics."""
    return {
        "initial_cash_usd": portfolio_simulator.state.initial_cash_usd,
        "total_market_value_usd": portfolio_simulator.state.total_market_value_usd,
        "realized_pnl_usd": portfolio_simulator.state.realized_pnl_usd,
        "unrealized_pnl_usd": portfolio_simulator.state.unrealized_pnl_usd,
        "total_trades_count": len(paper_exchange.trades),
        "disclaimer": portfolio_simulator.state.disclaimer,
    }


@router.post("/replay/start")
async def start_market_replay(
    symbol: str = "AAPL",
    scenario: ReplayScenario = ReplayScenario.FINANCIAL_CRISIS_2008,
    ticks_count: int = 50,
) -> dict[str, Any]:
    """Start accelerated historical market replay simulation."""
    ticks = await replay_engine.run_replay(symbol, scenario, ticks_count)
    return {
        "symbol": symbol.upper(),
        "scenario": scenario.value,
        "ticks_generated_count": len(ticks),
        "ticks": [
            {
                "timestamp_utc": t.timestamp_utc,
                "symbol": t.symbol,
                "price": t.price,
                "volume": t.volume,
                "event_flag": t.event_flag,
            }
            for t in ticks
        ],
    }
