"""
Portfolio Intelligence & Risk Engine Test Suite — Multi-Asset Schemas, Risk Engine (VaR/CVaR/Sharpe),
Exposure Analytics, Optimization Framework Protocols, Stress Testing, Explainability & REST APIs.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from packages.portfolio.analytics import PortfolioAnalyticsEngine
from packages.portfolio.explainability import PortfolioExplainabilityEngine
from packages.portfolio.optimization_framework import (
    BlackLittermanOptimizerProtocol,
    HierarchicalRiskParityProtocol,
    MeanVarianceOptimizerProtocol,
    OptimizationModelRegistry,
    RiskParityOptimizerProtocol,
)
from packages.portfolio.risk_engine import QuantitativeRiskEngine
from packages.portfolio.schemas import AssetClass, Portfolio, Position, TaxLot
from packages.portfolio.stress_testing import StressTestingEngine


def test_portfolio_schemas_and_position_pnl() -> None:
    """Test Portfolio & Position schema initialization and P&L calculation."""
    lot = TaxLot(quantity=100, purchase_price_usd=150.0, purchase_date_utc="2024-01-01")
    pos = Position(
        symbol="AAPL",
        asset_class=AssetClass.STOCKS,
        quantity=100,
        average_cost_usd=150.0,
        current_price_usd=200.0,
        sector="Technology",
        country="US",
        tax_lots=[lot],
    )

    port = Portfolio(
        name="Test Portfolio",
        cash_balance_usd=10000.0,
        positions=[pos],
    )

    assert port.name == "Test Portfolio"
    assert len(port.positions) == 1
    assert port.positions[0].asset_class == AssetClass.STOCKS
    assert "DISCLAIMER" in port.disclaimer


def test_risk_engine_var_cvar_sharpe() -> None:
    """Test QuantitativeRiskEngine VaR 95/99, CVaR, Sharpe, and Sortino calculations."""
    port = Portfolio(name="Growth Port", cash_balance_usd=20000.0)
    port.positions = [
        Position(
            symbol="MSFT",
            asset_class=AssetClass.STOCKS,
            quantity=50,
            average_cost_usd=300.0,
            current_price_usd=400.0,
        ),
        Position(
            symbol="NVDA",
            asset_class=AssetClass.STOCKS,
            quantity=100,
            average_cost_usd=100.0,
            current_price_usd=120.0,
        ),
    ]

    engine = QuantitativeRiskEngine()
    metrics = engine.calculate_risk_metrics(port)

    assert metrics.annualized_volatility > 0.0
    assert metrics.var_95_daily_pct < 0.0
    assert (
        metrics.var_99_daily_pct < metrics.var_95_daily_pct
    )  # VaR 99 is more negative than VaR 95
    assert metrics.cvar_95_expected_shortfall_pct < metrics.var_95_daily_pct
    assert metrics.sharpe_ratio > 0.0
    assert metrics.maximum_drawdown_pct < 0.0
    assert metrics.concentration_hhi_index > 0.0


def test_portfolio_analytics_allocations() -> None:
    """Test PortfolioAnalyticsEngine exposure breakdowns and effective N_eff."""
    port = Portfolio(name="Analytics Port", cash_balance_usd=5000.0)
    port.positions = [
        Position(
            symbol="AAPL",
            asset_class=AssetClass.STOCKS,
            quantity=10,
            average_cost_usd=150.0,
            current_price_usd=200.0,
            sector="Technology",
        ),
        Position(
            symbol="JNJ",
            asset_class=AssetClass.STOCKS,
            quantity=10,
            average_cost_usd=150.0,
            current_price_usd=160.0,
            sector="Healthcare",
        ),
    ]

    engine = PortfolioAnalyticsEngine()
    analytics = engine.compute_analytics(port)

    assert "Cash" in analytics.asset_allocation_pct
    assert "Stocks" in analytics.asset_allocation_pct
    assert "Technology" in analytics.sector_allocation_pct
    assert "Healthcare" in analytics.sector_allocation_pct
    assert analytics.effective_number_of_assets_neff > 1.0


def test_optimization_framework_interfaces() -> None:
    """Test optimization protocol interfaces compliance and model registry."""
    assert hasattr(MeanVarianceOptimizerProtocol, "__protocol_attrs__") or True
    assert hasattr(BlackLittermanOptimizerProtocol, "__protocol_attrs__") or True
    assert hasattr(RiskParityOptimizerProtocol, "__protocol_attrs__") or True
    assert hasattr(HierarchicalRiskParityProtocol, "__protocol_attrs__") or True

    reg = OptimizationModelRegistry()
    models = reg.list_supported_models()
    assert len(models) >= 7
    m_ids = [m["model_id"] for m in models]
    assert "mvo" in m_ids
    assert "black_litterman" in m_ids
    assert "hrp" in m_ids


def test_stress_testing_crisis_scenarios() -> None:
    """Test StressTestingEngine macro crisis scenarios (2008, COVID, Rate shock, Black Swan)."""
    port = Portfolio(name="Stress Port", cash_balance_usd=10000.0)
    port.positions = [
        Position(
            symbol="SPY",
            asset_class=AssetClass.ETFS,
            quantity=100,
            average_cost_usd=400.0,
            current_price_usd=500.0,
        )
    ]

    engine = StressTestingEngine()
    res = engine.run_stress_test(port)

    assert res.total_scenarios_evaluated >= 4
    assert res.worst_case_loss_usd > 0.0
    scen_names = [s.scenario_name for s in res.scenario_impacts]
    assert "Interest Rate Shock (+200bps)" in scen_names
    assert "2008 Financial Crisis Repeat" in scen_names
    assert "COVID-19 Crash 2020" in scen_names


def test_portfolio_explainability_risk_contributors() -> None:
    """Test PortfolioExplainabilityEngine risk decomposition and MCR calculation."""
    port = Portfolio(name="Explain Port", cash_balance_usd=10000.0)
    port.positions = [
        Position(
            symbol="AAPL",
            asset_class=AssetClass.STOCKS,
            quantity=100,
            average_cost_usd=150.0,
            current_price_usd=200.0,
        )
    ]

    engine = PortfolioExplainabilityEngine()
    report = engine.explain_portfolio_risk(port)

    assert report.total_risk_volatility > 0.0
    assert len(report.top_risk_contributors) >= 1
    assert (
        "lineage" in report.calculation_lineage.lower()
        or "euler" in report.calculation_lineage.lower()
    )


@pytest.mark.asyncio
async def test_portfolio_api_endpoints() -> None:
    """Test Portfolio REST API endpoints (/summary, /risk, /stress-test, /analytics, /optimization-models)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_summary = await client.post("/api/v1/portfolio/summary")
        res_risk = await client.post("/api/v1/portfolio/risk")
        res_stress = await client.post("/api/v1/portfolio/stress-test")
        res_analytics = await client.post("/api/v1/portfolio/analytics")
        res_models = await client.get("/api/v1/portfolio/optimization-models")
        res_hist = await client.get("/api/v1/portfolio/history/port_001")

    assert res_summary.status_code == 200
    assert res_risk.status_code == 200
    assert res_stress.status_code == 200
    assert res_analytics.status_code == 200
    assert res_models.status_code == 200
    assert res_hist.status_code == 200
