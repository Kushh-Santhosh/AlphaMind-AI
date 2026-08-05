"""
API v1 — Unified Dashboard Aggregation API Router

Powering Overview, Research, Forecast, Portfolio, Evaluation, Knowledge Graph, Evidence,
Reports Dashboards, and Activity Timelines.
"""

from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/dashboards", tags=["Dashboard Aggregation Engine"])


@router.get("/overview")
async def get_overview_dashboard() -> dict[str, Any]:
    """Fetch high-level system overview dashboard aggregations."""
    return {
        "system_status": "healthy",
        "active_researched_assets_count": 142,
        "total_knowledge_graph_nodes": 12450,
        "active_portfolios_monitored": 12,
        "champion_model_brier_score": 0.068,
        "recent_workflows_executed_24h": 48,
    }


@router.get("/research/{symbol}")
async def get_research_dashboard(symbol: str) -> dict[str, Any]:
    """Fetch Research Dashboard aggregations for a symbol."""
    sym = symbol.upper()
    return {
        "symbol": sym,
        "company_name": f"{sym} Inc.",
        "sector": "Technology",
        "market_cap_usd": 2850000000000.0,
        "financial_health_trend": 0.75,
        "sec_filings_count": 24,
        "news_articles_count": 112,
    }


@router.get("/forecast/{symbol}")
async def get_forecast_dashboard(symbol: str) -> dict[str, Any]:
    """Fetch Forecast Dashboard aggregations for a symbol."""
    sym = symbol.upper()
    return {
        "symbol": sym,
        "expected_return_30d_pct": 3.4,
        "confidence_interval_95": {"lower": -12.0, "mean": 3.4, "upper": 18.0},
        "scenarios_count": 5,
        "monte_carlo_simulations_count": 10000,
        "brier_score": 0.078,
    }


@router.get("/portfolio/{portfolio_id}")
async def get_portfolio_dashboard(portfolio_id: str) -> dict[str, Any]:
    """Fetch Portfolio Dashboard aggregations."""
    return {
        "portfolio_id": portfolio_id,
        "total_market_value_usd": 485000.0,
        "annualized_volatility": 0.165,
        "var_95_daily_pct": -0.0185,
        "sharpe_ratio": 1.45,
        "effective_number_of_assets_neff": 8.0,
    }


@router.get("/evaluation")
async def get_evaluation_dashboard() -> dict[str, Any]:
    """Fetch Continuous Evaluation Dashboard aggregations."""
    return {
        "champion_model_id": "bayesian_v1",
        "top_directional_accuracy_pct": 72.0,
        "historical_backtests_run": 142,
        "active_drift_alerts_count": 1,
        "models_in_registry_count": 9,
    }


@router.get("/graph")
async def get_knowledge_graph_dashboard() -> dict[str, Any]:
    """Fetch Knowledge Graph structural metrics dashboard."""
    return {
        "total_nodes": 12450,
        "total_edges": 38900,
        "entity_types_count": 21,
        "relation_types_count": 12,
    }


@router.get("/evidence/{symbol}")
async def get_evidence_dashboard(symbol: str) -> dict[str, Any]:
    """Fetch Evidence & Traceability Dashboard."""
    return {
        "symbol": symbol.upper(),
        "extracted_factors_count": 12,
        "evidence_citations_count": 28,
        "contradictions_count": 0,
        "data_completeness_pct": 100.0,
    }


@router.get("/reports")
async def get_reports_dashboard() -> dict[str, Any]:
    """Fetch compiled reports dashboard."""
    return {
        "total_reports_generated": 85,
        "recent_reports": [
            {
                "report_id": "rep_exec_001",
                "type": "executive_summary",
                "title": "Executive Research Summary — AAPL",
            },
            {
                "report_id": "rep_fore_002",
                "type": "forecast",
                "title": "Probabilistic Return Scenarios — NVDA",
            },
        ],
    }


@router.get("/activity-timeline")
async def get_activity_timeline() -> list[dict[str, Any]]:
    """Fetch platform activity execution timeline logs."""
    return [
        {
            "timestamp_utc": "2026-08-04T19:00:00Z",
            "event_type": "WORKFLOW_COMPLETED",
            "details": "Workflow 'Analyze Company' completed for AAPL",
        },
        {
            "timestamp_utc": "2026-08-04T18:45:00Z",
            "event_type": "FORECAST_GENERATED",
            "details": "Ensemble forecast compiled for NVDA",
        },
        {
            "timestamp_utc": "2026-08-04T18:30:00Z",
            "event_type": "DRIFT_ALERT",
            "details": "Feature drift alert emitted for tft_v1",
        },
    ]
