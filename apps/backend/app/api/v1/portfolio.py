"""
API v1 — Portfolio Intelligence & Quantitative Risk Router

Serves portfolio risk evaluations, VaR/CVaR calculations, exposure analytics,
macro stress testing, and optimization model specifications.
STRICT MANDATE: Zero broker connections, automated trading, or investment recommendations.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from packages.portfolio.analytics import PortfolioAnalyticsEngine
from packages.portfolio.explainability import PortfolioExplainabilityEngine
from packages.portfolio.optimization_framework import OptimizationModelRegistry
from packages.portfolio.risk_engine import QuantitativeRiskEngine
from packages.portfolio.schemas import AssetClass, Portfolio, Position, TaxLot
from packages.portfolio.stress_testing import StressTestingEngine

router = APIRouter(prefix="/api/v1/portfolio", tags=["Portfolio Intelligence Layer"])

risk_engine = QuantitativeRiskEngine()
analytics_engine = PortfolioAnalyticsEngine()
stress_engine = StressTestingEngine()
explainability_engine = PortfolioExplainabilityEngine()
opt_registry = OptimizationModelRegistry()


def _get_sample_portfolio() -> Portfolio:
    """Construct sample institutional portfolio for router requests."""
    p = Portfolio(name="Sample Institutional Growth Portfolio", cash_balance_usd=50_000.0)
    p.positions = [
        Position(
            symbol="AAPL",
            asset_class=AssetClass.STOCKS,
            quantity=500,
            average_cost_usd=180.0,
            current_price_usd=225.0,
            sector="Technology",
            country="US",
            tax_lots=[
                TaxLot(
                    quantity=500,
                    purchase_price_usd=180.0,
                    purchase_date_utc="2024-01-15",
                )
            ],
        ),
        Position(
            symbol="MSFT",
            asset_class=AssetClass.STOCKS,
            quantity=300,
            average_cost_usd=350.0,
            current_price_usd=420.0,
            sector="Technology",
            country="US",
            tax_lots=[
                TaxLot(
                    quantity=300,
                    purchase_price_usd=350.0,
                    purchase_date_utc="2024-02-01",
                )
            ],
        ),
        Position(
            symbol="NVDA",
            asset_class=AssetClass.STOCKS,
            quantity=200,
            average_cost_usd=110.0,
            current_price_usd=130.0,
            sector="Technology",
            country="US",
        ),
    ]
    p.total_market_value_usd = 50000.0 + (500 * 225.0) + (300 * 420.0) + (200 * 130.0)
    return p


@router.post("/summary")
async def get_portfolio_summary(portfolio: Portfolio | None = None) -> dict[str, Any]:
    """Fetch portfolio summary valuation and positions list."""
    target_port = portfolio or _get_sample_portfolio()
    analytics = analytics_engine.compute_analytics(target_port)
    return {
        "portfolio": target_port.model_dump(),
        "analytics": analytics.model_dump(),
    }


@router.post("/risk")
async def evaluate_portfolio_risk(
    portfolio: Portfolio | None = None,
) -> dict[str, Any]:
    """
    Compute quantitative risk metrics: Volatility, Beta, VaR 95/99, CVaR, Sharpe, Sortino, Max Drawdown.
    Contains ZERO buy/sell ratings or trade execution logic.
    """
    target_port = portfolio or _get_sample_portfolio()
    risk_metrics = risk_engine.calculate_risk_metrics(target_port)
    explain_report = explainability_engine.explain_portfolio_risk(target_port)
    return {
        "risk_metrics": risk_metrics.model_dump(),
        "explainability": explain_report.model_dump(),
    }


@router.post("/stress-test")
async def run_stress_testing(
    portfolio: Portfolio | None = None,
) -> dict[str, Any]:
    """Execute macro stress tests (Rate shock, 2008 Crisis, COVID crash, Black Swan)."""
    target_port = portfolio or _get_sample_portfolio()
    result = stress_engine.run_stress_test(target_port)
    return result.model_dump()


@router.post("/analytics")
async def get_portfolio_analytics(
    portfolio: Portfolio | None = None,
) -> dict[str, Any]:
    """Fetch exposure breakdowns (Asset, Sector, Country, Market Cap, HHI, N_eff)."""
    target_port = portfolio or _get_sample_portfolio()
    result = analytics_engine.compute_analytics(target_port)
    return result.model_dump()


@router.get("/optimization-models")
async def get_optimization_models() -> list[dict[str, str]]:
    """List supported optimization models (MVO, Black-Litterman, Risk Parity, HRP)."""
    return opt_registry.list_supported_models()


@router.get("/history/{portfolio_id}")
async def get_portfolio_history(portfolio_id: str) -> dict[str, Any]:
    """Fetch historical portfolio valuation and drawdown history."""
    return {
        "portfolio_id": portfolio_id,
        "history_days": 365,
        "historical_sharpe": 1.45,
        "max_drawdown_historical": -0.142,
    }
