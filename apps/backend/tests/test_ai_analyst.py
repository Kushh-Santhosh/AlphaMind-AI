"""
AI Analyst Experience Test Suite — Master Orchestrator, 9 Workflows, Conversational System,
Standardized Report Generator, Dashboard Aggregation APIs, Watchlists & Alerts, and Analyst REST APIs.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from packages.agents.analyst_workflows import AnalystWorkflowsRunner
from packages.agents.conversational_analyst import ConversationalAnalystEngine
from packages.agents.master_orchestrator import MasterAnalystOrchestrator
from packages.agents.report_generator import StandardizedReportGenerator
from packages.agents.watchlist_alerts import WatchlistAlertsManager


def test_master_analyst_orchestrator() -> None:
    """Test MasterAnalystOrchestrator component initialization."""
    orchestrator = MasterAnalystOrchestrator()

    assert orchestrator.company_engine is not None
    assert orchestrator.financial_engine is not None
    assert orchestrator.ensemble_engine is not None
    assert orchestrator.risk_engine is not None


@pytest.mark.asyncio
async def test_end_to_end_analysis_workflows() -> None:
    """Test 9 specialized AI Analyst workflows."""
    runner = AnalystWorkflowsRunner()

    wf1 = await runner.run_analyze_company("AAPL")
    wf2 = await runner.run_compare_companies(["AAPL", "MSFT"])
    wf3 = await runner.run_analyze_sector("Technology")
    wf4 = await runner.run_analyze_portfolio("port_001")
    wf5 = await runner.run_explain_forecast("AAPL")
    wf6 = await runner.run_explain_portfolio_risk("port_001")
    wf7 = await runner.run_review_evidence("AAPL")
    wf8 = await runner.run_review_contradictions("AAPL")
    wf9 = await runner.run_review_model_performance("tft_v1")

    assert wf1.workflow_type == "analyze_company"
    assert wf2.workflow_type == "compare_companies"
    assert wf3.workflow_type == "analyze_sector"
    assert wf4.workflow_type == "analyze_portfolio"
    assert wf5.workflow_type == "explain_forecast"
    assert wf6.workflow_type == "explain_portfolio_risk"
    assert wf7.workflow_type == "review_evidence"
    assert wf8.workflow_type == "review_contradictions"
    assert wf9.workflow_type == "review_model_performance"


def test_conversational_analyst_session_and_context() -> None:
    """Test ConversationalAnalystEngine session management, dialogue, and follow-up suggestions."""
    engine = ConversationalAnalystEngine()
    sess = engine.create_session(initial_symbol="NVDA")

    updated_sess = engine.process_user_query(sess.session_id, "Analyze NVDA gross margins")
    assert len(updated_sess.messages) >= 2
    assert len(updated_sess.suggested_followups) >= 3
    assert "NVDA" in updated_sess.messages[1].content


def test_report_generator_audit_metadata() -> None:
    """Test StandardizedReportGenerator auditability metadata and citations."""
    gen = StandardizedReportGenerator()
    rep = gen.create_report(
        report_type="executive_summary",
        symbol_or_target="AAPL",
        title="Executive Summary AAPL",
        summary_text="High margin cash flow generation.",
    )

    assert rep.symbol_or_target == "AAPL"
    assert rep.audit_metadata.workflow_id is not None
    assert rep.audit_metadata.forecast_version is not None
    assert len(rep.evidence_citations) >= 2
    assert "DISCLAIMER" in rep.disclaimer


def test_watchlists_and_alerts_system() -> None:
    """Test WatchlistAlertsManager watchlist creation and alert emission."""
    mgr = WatchlistAlertsManager()
    wl = mgr.create_watchlist("Tech List", ["AAPL", "MSFT", "NVDA"])

    alert = mgr.emit_alert(
        alert_type="drift_alert",
        severity="warning",
        symbol="AAPL",
        headline="Feature Drift Alert",
        description="Shift in interest rate feature distribution.",
    )

    assert len(wl.symbols) == 3
    assert alert.symbol_or_target == "AAPL"
    active_alerts = mgr.get_active_alerts("AAPL")
    assert len(active_alerts) == 1


@pytest.mark.asyncio
async def test_analyst_and_dashboards_api_endpoints() -> None:
    """Test AI Analyst & Dashboard Aggregation REST APIs."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Dashboard APIs
        res_overview = await client.get("/api/v1/dashboards/overview")
        res_res_dash = await client.get("/api/v1/dashboards/research/AAPL")
        res_fcst_dash = await client.get("/api/v1/dashboards/forecast/AAPL")
        res_port_dash = await client.get("/api/v1/dashboards/portfolio/port_001")
        res_eval_dash = await client.get("/api/v1/dashboards/evaluation")
        res_graph_dash = await client.get("/api/v1/dashboards/graph")
        res_ev_dash = await client.get("/api/v1/dashboards/evidence/AAPL")
        res_rep_dash = await client.get("/api/v1/dashboards/reports")
        res_timeline = await client.get("/api/v1/dashboards/activity-timeline")

        # Analyst APIs
        res_chat = await client.post("/api/v1/analyst/chat?message=Analyze%20AAPL")
        res_wf = await client.post(
            "/api/v1/analyst/workflows/run?workflow_type=analyze_company&target=AAPL"
        )
        res_gen_rep = await client.post(
            "/api/v1/analyst/reports/generate?report_type=executive_summary&target=AAPL"
        )
        res_wl = await client.post("/api/v1/analyst/watchlists?name=Core&symbols=AAPL,NVDA")
        res_alerts = await client.get("/api/v1/analyst/alerts")

    assert res_overview.status_code == 200
    assert res_res_dash.status_code == 200
    assert res_fcst_dash.status_code == 200
    assert res_port_dash.status_code == 200
    assert res_eval_dash.status_code == 200
    assert res_graph_dash.status_code == 200
    assert res_ev_dash.status_code == 200
    assert res_rep_dash.status_code == 200
    assert res_timeline.status_code == 200

    assert res_chat.status_code == 200
    assert res_wf.status_code == 200
    assert res_gen_rep.status_code == 200
    assert res_wl.status_code == 200
    assert res_alerts.status_code == 200
