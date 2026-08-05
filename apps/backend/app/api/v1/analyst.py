"""
API v1 — AI Analyst Orchestrator & Conversational Experience Router
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from packages.agents.analyst_workflows import AnalystWorkflowsRunner
from packages.agents.conversational_analyst import ConversationalAnalystEngine
from packages.agents.report_generator import StandardizedReportGenerator
from packages.agents.watchlist_alerts import WatchlistAlertsManager

router = APIRouter(prefix="/api/v1/analyst", tags=["AI Analyst Experience"])

conversational_engine = ConversationalAnalystEngine()
workflow_runner = AnalystWorkflowsRunner()
report_generator = StandardizedReportGenerator()
alerts_manager = WatchlistAlertsManager()


@router.post("/chat")
async def chat_with_analyst(session_id: str = "", message: str = "Analyze AAPL") -> dict[str, Any]:
    """Conversational AI Analyst dialogue interface."""
    sess = conversational_engine.process_user_query(session_id, message)
    return sess.model_dump()


@router.post("/workflows/run")
async def run_analyst_workflow(
    workflow_type: str = "analyze_company", target: str = "AAPL"
) -> dict[str, Any]:
    """Execute end-to-end multi-engine analysis workflow."""
    if workflow_type == "analyze_company":
        res = await workflow_runner.run_analyze_company(target)
    elif workflow_type == "compare_companies":
        res = await workflow_runner.run_compare_companies(target.split(","))
    elif workflow_type == "analyze_sector":
        res = await workflow_runner.run_analyze_sector(target)
    elif workflow_type == "analyze_portfolio":
        res = await workflow_runner.run_analyze_portfolio(target)
    elif workflow_type == "explain_forecast":
        res = await workflow_runner.run_explain_forecast(target)
    elif workflow_type == "explain_portfolio_risk":
        res = await workflow_runner.run_explain_portfolio_risk(target)
    elif workflow_type == "review_evidence":
        res = await workflow_runner.run_review_evidence(target)
    elif workflow_type == "review_contradictions":
        res = await workflow_runner.run_review_contradictions(target)
    else:
        res = await workflow_runner.run_review_model_performance(target)

    return res.model_dump()


@router.post("/reports/generate")
async def generate_standardized_report(
    report_type: str = "executive_summary", target: str = "AAPL"
) -> dict[str, Any]:
    """Generate standardized research report with complete auditability metadata."""
    rep = report_generator.create_report(
        report_type=report_type,
        symbol_or_target=target.upper(),
        title=f"Standardized {report_type.title()} Report — {target.upper()}",
        summary_text=f"Aggregated multi-engine research findings for {target.upper()}.",
    )
    return rep.model_dump()


@router.post("/watchlists")
async def create_watchlist(
    name: str = "Tech Favorites", symbols: str = "AAPL,NVDA,MSFT"
) -> dict[str, Any]:
    """Create user research watchlist."""
    w = alerts_manager.create_watchlist(name, symbols.split(","))
    return w.model_dump()


@router.get("/alerts")
async def get_platform_alerts(symbol: str | None = None) -> list[dict[str, Any]]:
    """Fetch active research, drift, and data quality alerts."""
    alerts = alerts_manager.get_active_alerts(symbol)
    return [a.model_dump() for a in alerts]
