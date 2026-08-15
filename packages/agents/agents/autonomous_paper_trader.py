"""
AlphaMind AI - Autonomous Multi-Asset Paper Trader (v4.1)

Executes continuous autonomous paper trading loops:
  1. Screens universe via OpportunityScannerEngine
  2. Runs probabilistic Kronos K-line forecast
  3. Evaluates PreTradeRiskEngine limits (max leverage, concentration, stop loss)
  4. Executes simulated market/limit order on PaperExchange
  5. Records trade decision & context to StrategyLearningMemory

STRICT MANDATE: [PAPER MODE ONLY] Zero real money, zero live broker execution.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from packages.market.provider_registry import market_data_registry
from packages.memory.strategy_learning_memory import strategy_learning_memory
from packages.portfolio.paper_exchange import (
    PaperExchange,
    SimulatedOrder,
    SimulatedOrderSide,
    SimulatedOrderStatus,
    SimulatedOrderType,
)
from packages.portfolio.paper_portfolio import PortfolioSimulator
from packages.portfolio.risk_controls import PreTradeRiskEngine
from packages.prediction.kronos_forecast_engine import ForecastHorizon, kronos_forecast_engine
from packages.research.opportunity_scanner import opportunity_scanner_engine

logger = logging.getLogger(__name__)


@dataclass
class PaperTradeExecutionResult:
    status: str  # "EXECUTED", "REJECTED_RISK", "NO_CONVICTION_OPPORTUNITIES", "MARKET_CLOSED"
    action_taken: str
    symbol: Optional[str] = None
    side: Optional[str] = None
    quantity: Optional[float] = None
    fill_price: Optional[float] = None
    opportunity_score: Optional[float] = None
    forecast_trend: Optional[str] = None
    rejection_reason: Optional[str] = None
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    mode: str = "PAPER_MODE_SIMULATION"


class AutonomousPaperTrader:
    """Autonomous quantitative paper trading engine with continuous research and risk checks."""

    def __init__(
        self,
        exchange: Optional[PaperExchange] = None,
        portfolio: Optional[PortfolioSimulator] = None,
        risk_engine: Optional[PreTradeRiskEngine] = None,
    ) -> None:
        self.exchange = exchange or PaperExchange()
        self.portfolio = portfolio or PortfolioSimulator(initial_cash_usd=100_000.0)
        self.risk_engine = risk_engine or PreTradeRiskEngine()
        self.is_active = False

    async def execute_trading_cycle(self) -> PaperTradeExecutionResult:
        """Run a complete autonomous research -> forecast -> risk -> paper execution cycle."""
        logger.info("Executing Autonomous Paper Trader cycle...")

        # 1. Scan for top opportunities across universe
        opportunities = await opportunity_scanner_engine.scan_opportunities(min_score=60.0, limit=3)
        if not opportunities:
            return PaperTradeExecutionResult(
                status="NO_CONVICTION_OPPORTUNITIES",
                action_taken="Scanner yielded zero opportunities meeting conviction threshold >= 60.0.",
            )

        top_candidate = opportunities[0]
        sym = top_candidate["symbol"]
        score = top_candidate["opportunity_score"]

        # 2. Get live market snapshot
        snap = await market_data_registry.get_market_snapshot(sym)
        price = snap.get("price", 0.0)
        if price <= 0:
            return PaperTradeExecutionResult(
                status="MARKET_CLOSED",
                action_taken=f"Live quote unavailable for {sym}.",
                symbol=sym,
            )

        # 3. Generate Kronos forecast
        fcst = await kronos_forecast_engine.generate_forecast(sym, horizon=ForecastHorizon.SHORT)
        trend = fcst.predicted_trend

        # Decide side: Buy if Bullish & high score, Sell/Short if Bearish
        side = SimulatedOrderSide.BUY if trend == "BULLISH_EXPANSION" else SimulatedOrderSide.SELL

        # Calculate position sizing (max 10% of portfolio)
        allocated_cash = self.portfolio.state.cash_balance_usd * 0.10
        qty = max(1.0, round(allocated_cash / price, 2)) if price > 0 else 1.0

        # 4. Pre-trade risk check
        risk_verdict = self.risk_engine.validate_pre_trade(
            order_symbol=sym,
            side=side,
            quantity=qty,
            price=price,
            portfolio_state=self.portfolio.state,
        )

        if not risk_verdict.is_approved:
            return PaperTradeExecutionResult(
                status="REJECTED_RISK",
                action_taken=f"Pre-trade risk check rejected order for {sym}.",
                symbol=sym,
                rejection_reason=risk_verdict.rejection_reason,
            )

        # 5. Paper order execution
        order = self.exchange.submit_order(
            symbol=sym,
            side=side,
            order_type=SimulatedOrderType.MARKET,
            quantity=qty,
            market_price=price,
        )

        if self.exchange.trades:
            last_trade = self.exchange.trades[-1]
            self.portfolio.process_trade(last_trade)

            # Record reflection to strategy memory
            strategy_learning_memory.record_trade_outcome(
                strategy_name="AI_Multi_Factor_Momentum",
                symbol=sym,
                pnl_usd=0.0,  # initial entry
                return_pct=0.0,
                regime="BULL_EXPANSION" if trend == "BULLISH_EXPANSION" else "VOLATILE",
                alpha_bps=12.5,
                reflection=f"Entered {side.value} position based on opportunity score {score:.1f} and Kronos {trend} forecast.",
            )

        return PaperTradeExecutionResult(
            status="EXECUTED",
            action_taken=f"Filled simulated {side.value} order for {qty} shares of {sym} at ${order.filled_avg_price:.2f}.",
            symbol=sym,
            side=side.value,
            quantity=qty,
            fill_price=order.filled_avg_price,
            opportunity_score=score,
            forecast_trend=trend,
        )


# Singleton Global Autonomous Paper Trader
autonomous_paper_trader = AutonomousPaperTrader()
