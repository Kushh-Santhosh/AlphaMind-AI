"""
AlphaMind AI - Institutional Backtester API Router
Exposes walk-forward backtest simulations with out-of-sample attribution.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from packages.research.backtest_engine import BacktestConfig, BacktestingEngine

router = APIRouter(prefix="/api/v1/backtest_v4", tags=["Backtesting v4"])
_engine = BacktestingEngine()


class BacktestRunRequest(BaseModel):
    strategy_name: str = Field(default="Alpha Multi-Factor Long/Short", description="Strategy identifier")
    universe: list[str] = Field(default_factory=lambda: ["NVDA", "MSFT", "AAPL", "GOOGL", "SPY"], description="Asset universe")
    start_date: str = Field(default="2024-01-01", description="Simulation start date")
    end_date: str = Field(default="2025-12-31", description="Simulation end date")
    initial_capital: float = Field(default=100000.0, ge=1000.0)
    commission_bps: float = Field(default=5.0)
    slippage_bps: float = Field(default=8.0)
    rebalance_frequency: str = Field(default="MONTHLY")
    benchmark: str = Field(default="SPY")
    walk_forward_enabled: bool = Field(default=True)


@router.post("/run", response_model=dict[str, Any])
async def run_strategy_backtest(payload: BacktestRunRequest) -> dict[str, Any]:
    """Execute walk-forward out-of-sample backtest simulation."""
    config = BacktestConfig(
        strategy_name=payload.strategy_name,
        universe=payload.universe,
        start_date=payload.start_date,
        end_date=payload.end_date,
        initial_capital=payload.initial_capital,
        commission_bps=payload.commission_bps,
        slippage_bps=payload.slippage_bps,
        rebalance_frequency=payload.rebalance_frequency,
        benchmark_symbol=payload.benchmark,
        walk_forward_enabled=payload.walk_forward_enabled,
    )
    return _engine.run_backtest(config)
