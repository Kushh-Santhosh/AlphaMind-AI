"""
API v1 — Prometheus Metrics & Infrastructure Health Endpoint Router
"""

from typing import Any

from fastapi import APIRouter, Response

from apps.backend.app.core.telemetry import TelemetryMetricsManager
from apps.backend.app.db.health import DatabaseHealthAggregator

router = APIRouter(tags=["Observability"])


@router.get("/metrics", response_class=Response)
async def get_prometheus_metrics() -> Response:
    """Prometheus metrics endpoint."""
    content = TelemetryMetricsManager.export_prometheus_metrics()
    return Response(content=content, media_type="text/plain; version=0.0.4")


@router.get("/api/v1/health/databases")
async def get_database_health() -> dict[str, Any]:
    """Database infrastructure multi-store health status."""
    return await DatabaseHealthAggregator.check_all_databases()
