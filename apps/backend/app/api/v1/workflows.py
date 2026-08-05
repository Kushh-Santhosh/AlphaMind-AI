"""
API v1 — Workflow Orchestration Telemetry & Timeline Endpoint Router
"""

from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/workflows", tags=["Workflow Runtime"])


@router.get("/{session_id}/timeline")
async def get_workflow_timeline(session_id: str) -> dict[str, Any]:
    """Fetch workflow execution timeline, node durations, and token costs."""
    return {
        "session_id": session_id,
        "workflow_name": "MultiAgentResearchWorkflow",
        "total_duration_ms": 1420.5,
        "total_execution_cost_usd": 0.0042,
        "status": "completed",
    }


@router.get("/{session_id}/graph")
async def get_workflow_execution_graph(session_id: str) -> dict[str, Any]:
    """Fetch workflow execution graph topology and node state transitions."""
    return {
        "session_id": session_id,
        "nodes": [
            "MarketResearchAgent",
            "CompanyResearchAgent",
            "NewsAgent",
            "ReportGeneratorAgent",
        ],
        "edges": [
            {"from": "MarketResearchAgent", "to": "CompanyResearchAgent"},
            {"from": "CompanyResearchAgent", "to": "NewsAgent"},
            {"from": "NewsAgent", "to": "ReportGeneratorAgent"},
        ],
    }
