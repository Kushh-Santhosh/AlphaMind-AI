"""
Data Foundation Test Suite — Observability & Prometheus Metrics Exporter Tests
"""

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.core.telemetry import TelemetryMetricsManager
from apps.backend.app.main import app


def test_prometheus_metrics_formatting() -> None:
    """TelemetryMetricsManager formats Prometheus output string correctly."""
    TelemetryMetricsManager.record_provider_request("polygon_io", True, 45.2)
    output = TelemetryMetricsManager.export_prometheus_metrics()

    assert "alphamind_provider_requests_total" in output
    assert "alphamind_ingestion_latency_ms" in output


@pytest.mark.asyncio
async def test_metrics_endpoint() -> None:
    """GET /metrics returns 200 plain text metrics response."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/metrics")

    assert response.status_code == 200
    assert "alphamind_provider_requests_total" in response.text
