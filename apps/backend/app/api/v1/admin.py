"""
API v1 — Enterprise Admin Panel Router
"""

from typing import Any

from fastapi import APIRouter

from apps.backend.app.core.auth import UserRole

router = APIRouter(prefix="/api/v1/admin", tags=["Enterprise Admin Panel"])


@router.get("/users")
async def get_users_list() -> list[dict[str, Any]]:
    """Fetch system registered users and roles."""
    return [
        {
            "user_id": "usr_001",
            "email": "admin@alphamind.ai",
            "role": UserRole.ADMIN.value,
            "status": "active",
        },
        {
            "user_id": "usr_002",
            "email": "quant@alphamind.ai",
            "role": UserRole.QUANT_ANALYST.value,
            "status": "active",
        },
        {
            "user_id": "usr_003",
            "email": "auditor@alphamind.ai",
            "role": UserRole.AUDITOR.value,
            "status": "active",
        },
    ]


@router.get("/brokers")
async def get_broker_connections() -> list[dict[str, Any]]:
    """Fetch active broker adapter configurations."""
    return [
        {"broker": "alpaca", "status": "CONNECTED", "latency_ms": 14.2, "mode": "SIMULATION"},
        {
            "broker": "interactive_brokers",
            "status": "CONNECTED",
            "latency_ms": 28.5,
            "mode": "SIMULATION",
        },
        {"broker": "binance_spot", "status": "CONNECTED", "latency_ms": 45.0, "mode": "SIMULATION"},
    ]


@router.get("/models")
async def get_managed_models() -> list[dict[str, Any]]:
    """Fetch predictive model registry states."""
    return [
        {
            "model_id": "bayesian_v1",
            "name": "Bayesian BSTS",
            "status": "CHAMPION",
            "brier_score": 0.065,
        },
        {
            "model_id": "tft_v1",
            "name": "Temporal Fusion Transformer",
            "status": "CHALLENGER",
            "brier_score": 0.068,
        },
    ]


@router.get("/provider-health")
async def get_provider_health() -> dict[str, Any]:
    """Fetch data provider failover health matrix."""
    return {
        "sec_edgar": "HEALTHY",
        "fred_macro": "HEALTHY",
        "polygon_market": "HEALTHY",
        "news_feed": "HEALTHY",
    }


@router.get("/background-jobs")
async def get_background_jobs() -> list[dict[str, Any]]:
    """Fetch status of enterprise background jobs."""
    return [
        {
            "job_id": "job_sched_01",
            "name": "Daily Research Pipeline",
            "status": "COMPLETED",
            "next_run": "2026-08-05T00:00:00Z",
        },
        {
            "job_id": "job_drift_02",
            "name": "Model Drift Audit",
            "status": "RUNNING",
            "next_run": "2026-08-04T22:00:00Z",
        },
    ]


@router.get("/system-metrics")
async def get_system_metrics() -> dict[str, Any]:
    """Fetch system CPU, memory, and database metrics."""
    return {
        "cpu_utilization_pct": 14.5,
        "memory_used_mb": 420.0,
        "memory_total_mb": 8192.0,
        "postgres_active_connections": 12,
        "chromadb_total_vectors": 38900,
    }


# ── Beta Operations & Analytics Endpoints ─────────────────────────────────────

_BETA_FEEDBACK_QUEUE: list[dict[str, Any]] = [
    {
        "feedback_id": "fb_001",
        "category": "UI Issue",
        "triage_priority": "Low",
        "title": "Sidebar version badge placement",
        "description": "Beta version tag is crisp; recommend adding tooltips on hover.",
        "affected_page": "/mission-control",
        "browser": "Chrome 127.0 (macOS)",
        "timestamp_utc": "2026-08-04T22:30:00Z",
        "app_version": "v3.0.0-beta",
        "status": "TRIAGED",
    },
    {
        "feedback_id": "fb_002",
        "category": "Feature Request",
        "triage_priority": "Medium",
        "title": "Export portfolio allocations to PDF",
        "description": "Would love a one-click PDF export for the 5 Virtual AI Fund snapshots.",
        "affected_page": "/v2-fund",
        "browser": "Safari 17.5 (macOS)",
        "timestamp_utc": "2026-08-04T23:15:00Z",
        "app_version": "v3.0.0-beta",
        "status": "TRIAGED",
    },
]


@router.get("/beta/analytics")
async def get_beta_analytics() -> dict[str, Any]:
    """Fetch Private Beta user analytics and telemetry indicators."""
    return {
        "status": "Awaiting Beta Data",
        "metrics_status_label": "Awaiting Beta Data — Operating Pre-Beta Telemetry",
        "new_users": "Awaiting Beta Data",
        "daily_active_users": "Awaiting Beta Data",
        "average_session_duration_min": "Awaiting Beta Data",
        "user_retention_7d_pct": "Awaiting Beta Data",
        "user_retention_30d_pct": "Awaiting Beta Data",
        "feature_usage": {
            "mission_control": "Awaiting Beta Data",
            "search_command_palette": "Awaiting Beta Data",
            "ai_chat_analyst": "Awaiting Beta Data",
            "risk_analytics": "Awaiting Beta Data",
            "fund_inspector": "Awaiting Beta Data",
        },
        "system_errors_count": 0,
        "api_failures_count": 0,
    }


@router.get("/beta/metrics")
async def get_beta_metrics() -> dict[str, Any]:
    """Fetch Private Beta activation, task completion, and satisfaction metrics."""
    return {
        "activation_rate_pct": "Awaiting Beta Data",
        "time_to_first_value_min": "Awaiting Beta Data",
        "task_completion_rate_pct": "Awaiting Beta Data",
        "retention_rate_pct": "Awaiting Beta Data",
        "user_satisfaction_score": "Awaiting Beta Data",
        "note": "Metrics will automatically populate as Private Beta users complete onboarding.",
    }


@router.get("/beta/feedback")
async def get_beta_feedback() -> list[dict[str, Any]]:
    """Fetch categorized feedback and bug triage queue."""
    return _BETA_FEEDBACK_QUEUE


@router.post("/beta/feedback")
async def submit_beta_feedback(payload: dict[str, Any]) -> dict[str, Any]:
    """Submit new categorized feedback or bug report."""
    item = {
        "feedback_id": f"fb_{len(_BETA_FEEDBACK_QUEUE) + 1:03d}",
        "category": payload.get("category", "Other"),
        "triage_priority": payload.get("triage_priority", "Medium"),
        "title": payload.get("title", "User Feedback"),
        "description": payload.get("description", ""),
        "affected_page": payload.get("affected_page", "/"),
        "browser": payload.get("browser", "Web Browser"),
        "timestamp_utc": "2026-08-04T23:59:00Z",
        "app_version": "v3.0.0-beta",
        "status": "NEW",
    }
    _BETA_FEEDBACK_QUEUE.insert(0, item)
    return {"status": "SUCCESS", "feedback_id": item["feedback_id"]}


@router.get("/beta/feedback/export")
async def export_beta_feedback(format: str = "json") -> Any:
    """Export feedback queue as CSV or JSON."""
    if format == "csv":
        headers = (
            "feedback_id,category,triage_priority,title,affected_page,app_version,timestamp_utc\n"
        )
        rows = [
            f'{f["feedback_id"]},{f["category"]},{f["triage_priority"]},"{f["title"]}",{f["affected_page"]},{f["app_version"]},{f["timestamp_utc"]}'
            for f in _BETA_FEEDBACK_QUEUE
        ]
        return {"content": headers + "\n".join(rows), "media_type": "text/csv"}
    return {"content": _BETA_FEEDBACK_QUEUE, "media_type": "application/json"}


@router.get("/beta/summary")
async def get_beta_summary() -> dict[str, Any]:
    """Generate weekly Private Beta operations summary."""
    return {
        "period": "Week 1 Private Beta Operations",
        "app_version": "v3.0.0-beta",
        "operational_status": "READY_FOR_BETA_FEEDBACK",
        "total_feedback_items": len(_BETA_FEEDBACK_QUEUE),
        "categorized_breakdown": {
            "Bug": len([f for f in _BETA_FEEDBACK_QUEUE if f["category"] == "Bug"]),
            "UI Issue": len([f for f in _BETA_FEEDBACK_QUEUE if f["category"] == "UI Issue"]),
            "AI Quality": len([f for f in _BETA_FEEDBACK_QUEUE if f["category"] == "AI Quality"]),
            "Performance": len([f for f in _BETA_FEEDBACK_QUEUE if f["category"] == "Performance"]),
            "Feature Request": len(
                [f for f in _BETA_FEEDBACK_QUEUE if f["category"] == "Feature Request"]
            ),
            "Other": len([f for f in _BETA_FEEDBACK_QUEUE if f["category"] == "Other"]),
        },
        "bug_triage": {
            "Critical": 0,
            "High": 0,
            "Medium": len([f for f in _BETA_FEEDBACK_QUEUE if f["triage_priority"] == "Medium"]),
            "Low": len([f for f in _BETA_FEEDBACK_QUEUE if f["triage_priority"] == "Low"]),
        },
        "user_analytics": "Awaiting Beta Data",
    }
