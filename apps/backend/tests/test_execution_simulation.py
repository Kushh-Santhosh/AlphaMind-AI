"""
Execution Simulation Platform Test Suite — Virtual Paper Exchange, Order Lifecycle,
Portfolio Simulator, Market Replay, Pre-Trade Risk Controls, and Simulation APIs.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from packages.portfolio.market_replay import MarketReplayEngine, ReplayScenario
from packages.portfolio.paper_exchange import (
    PaperExchange,
    SimulatedOrderSide,
    SimulatedOrderStatus,
    SimulatedOrderType,
)
from packages.portfolio.paper_portfolio import PortfolioSimulator
from packages.portfolio.risk_controls import PreTradeRiskEngine


def test_paper_exchange_order_types_and_lifecycle() -> None:
    """Test PaperExchange order submission, slippage, and fill lifecycle."""
    exchange = PaperExchange(fixed_commission_usd=1.0, slippage_bps=2.0)
    order = exchange.submit_order(
        symbol="AAPL",
        side=SimulatedOrderSide.BUY,
        order_type=SimulatedOrderType.MARKET,
        quantity=10.0,
        market_price=150.0,
    )

    assert order.symbol == "AAPL"
    assert order.status == SimulatedOrderStatus.FILLED
    assert order.filled_quantity == 10.0
    assert order.filled_avg_price > 150.0  # Buy slippage added
    assert order.commission_usd == 1.0
    assert order.slippage_usd > 0.0


def test_slippage_and_commission_modeling() -> None:
    """Test slippage and commission calculations on virtual SELL order."""
    exchange = PaperExchange(fixed_commission_usd=2.5, slippage_bps=5.0)
    order = exchange.submit_order(
        symbol="NVDA",
        side=SimulatedOrderSide.SELL,
        order_type=SimulatedOrderType.LIMIT,
        quantity=5.0,
        limit_price=120.0,
    )

    assert order.symbol == "NVDA"
    assert order.filled_avg_price < 120.0  # Sell slippage deducted
    assert order.commission_usd == 2.5


def test_portfolio_simulator_margin_and_pnl() -> None:
    """Test PortfolioSimulator buying power, positions, and margin accounting."""
    sim = PortfolioSimulator(initial_cash_usd=100000.0)
    exchange = PaperExchange()

    # Buy trade
    exchange.submit_order(
        "AAPL", SimulatedOrderSide.BUY, SimulatedOrderType.MARKET, 20.0, market_price=150.0
    )
    sim.process_trade(exchange.trades[-1])

    assert "AAPL" in sim.state.positions
    assert sim.state.positions["AAPL"].quantity == 20.0
    assert sim.state.cash_balance_usd < 100000.0
    assert sim.state.buying_power_usd > 0.0
    assert sim.state.maintenance_margin_required_usd > 0.0


@pytest.mark.asyncio
async def test_historical_market_replay_engine() -> None:
    """Test MarketReplayEngine historical crash scenarios and tick generation."""
    replay = MarketReplayEngine(playback_speed_multiplier=10)
    ticks = await replay.run_replay("AAPL", ReplayScenario.FINANCIAL_CRISIS_2008, ticks_count=20)

    assert len(ticks) == 20
    assert ticks[0].symbol == "AAPL"
    assert any(t.event_flag == "CRASH_EVENT" for t in ticks)


def test_pre_trade_risk_controls_rejection() -> None:
    """Test PreTradeRiskEngine position size and leverage pre-trade limit rejections."""
    risk_engine = PreTradeRiskEngine()
    sim = PortfolioSimulator(initial_cash_usd=100000.0)

    # Attempt to place order exceeding max position size (25%)
    res_rejected = risk_engine.validate_pre_trade(
        order_symbol="AAPL",
        side=SimulatedOrderSide.BUY,
        quantity=300.0,
        price=150.0,  # $45,000 order = 45% of portfolio > 25% limit
        portfolio_state=sim.state,
    )

    assert not res_rejected.is_approved
    assert "PRE-TRADE RISK REJECTION" in res_rejected.rejection_reason


@pytest.mark.asyncio
async def test_simulation_api_endpoints() -> None:
    """Test Simulation REST API endpoints (/order, /orders, /trades, /positions, /performance, /replay/start)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_order = await client.post("/api/v1/simulation/order?symbol=AAPL&quantity=5.0")
        res_orders = await client.get("/api/v1/simulation/orders")
        res_trades = await client.get("/api/v1/simulation/trades")
        res_positions = await client.get("/api/v1/simulation/positions")
        res_perf = await client.get("/api/v1/simulation/performance")
        res_replay = await client.post("/api/v1/simulation/replay/start?symbol=AAPL&ticks_count=10")

    assert res_order.status_code == 200
    assert res_orders.status_code == 200
    assert res_trades.status_code == 200
    assert res_positions.status_code == 200
    assert res_perf.status_code == 200
    assert res_replay.status_code == 200
