"""
AlphaMind AI v2 — Production Health, Probes & Prometheus Metrics Unit Tests
"""

from __future__ import annotations

from app.api.v1.health import router
from fastapi import FastAPI
from fastapi.testclient import TestClient

_app = FastAPI()
_app.include_router(router)
client = TestClient(_app)


def test_health_endpoint() -> None:
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_healthz_detailed_subsystem_health() -> None:
    resp = client.get("/api/v1/healthz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "HEALTHY"
    assert "subsystems" in data
    assert data["subsystems"]["event_bus"]["status"] == "UP"
    assert data["subsystems"]["fund_engine"]["status"] == "UP"


def test_livez_liveness_probe() -> None:
    resp = client.get("/api/v1/livez")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ALIVE"


def test_readyz_readiness_probe() -> None:
    resp = client.get("/api/v1/readyz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "READY"


def test_metrics_prometheus_exposition_format() -> None:
    resp = client.get("/api/v1/metrics")
    assert resp.status_code == 200
    text = resp.text
    assert "alphamind_uptime_seconds" in text
    assert "alphamind_timeline_events_total" in text
    assert "alphamind_reasoning_records_total" in text
    assert "alphamind_active_funds_total" in text
    assert "alphamind_total_aum_usd" in text
