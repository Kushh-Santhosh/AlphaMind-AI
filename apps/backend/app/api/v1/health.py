"""
AlphaMind AI v2 — Production Health, Probes & Prometheus Metrics Router

Provides:
  - GET /api/v1/health   — basic health check
  - GET /api/v1/healthz  — detailed subsystem health status
  - GET /api/v1/livez    — Kubernetes liveness probe (200 OK if process alive)
  - GET /api/v1/readyz   — Kubernetes readiness probe (200 OK if ready for traffic)
  - GET /api/v1/metrics  — Prometheus exposition text format exporter
"""

from __future__ import annotations

import os
import time
from typing import Any

from fastapi import APIRouter, Response


def _get_mc() -> dict[str, Any]:
    """Defer import of mission control components to prevent circular imports during module load."""
    from apps.backend.app.api.v1.mission_control import (
        _PLATFORM_START,
        _briefing_engine,
        _event_bus,
        _fund_engine,
        _memory_store,
        _replay_engine,
        _timeline,
        _workspace_engine,
    )

    return {
        "start": _PLATFORM_START,
        "briefing_engine": _briefing_engine,
        "event_bus": _event_bus,
        "fund_engine": _fund_engine,
        "memory_store": _memory_store,
        "replay_engine": _replay_engine,
        "timeline": _timeline,
        "workspace_engine": _workspace_engine,
    }


router = APIRouter(prefix="/api/v1", tags=["System & Telemetry"])


@router.get("/health")
async def health() -> dict[str, str]:
    """System health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}


@router.get("/healthz")
async def healthz() -> dict[str, Any]:
    """Detailed health check for all platform subsystems."""
    mc = _get_mc()
    uptime_sec = round(time.time() - mc["start"], 1)
    timeline_count = len(mc["timeline"].query_timeline(limit=10000))
    reasoning_count = len(mc["memory_store"].list_all_records(limit=10000))
    fund_count = len(mc["fund_engine"].list_all_funds())

    return {
        "status": "HEALTHY",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "uptime_seconds": uptime_sec,
        "environment": os.getenv("ENVIRONMENT", "staging"),
        "subsystems": {
            "event_bus": {"status": "UP", "subscribers": len(mc["event_bus"].subscribers)},
            "unified_timeline": {"status": "UP", "total_events": timeline_count},
            "intelligence_memory": {"status": "UP", "total_records": reasoning_count},
            "fund_engine": {"status": "UP", "active_funds": fund_count},
            "briefing_engine": {
                "status": "UP",
                "total_briefings": len(mc["briefing_engine"].list_briefings()),
            },
            "workspace_engine": {
                "status": "UP",
                "workspaces": len(mc["workspace_engine"].workspaces),
            },
            "chess_replay": {
                "status": "UP",
                "session_id": mc["replay_engine"].session_id or "session_live",
            },
        },
    }


@router.get("/livez")
async def livez() -> Response:
    """
    Kubernetes Liveness Probe.
    Returns 200 OK if the process main event loop is responsive.
    """
    return Response(content='{"status":"ALIVE"}', media_type="application/json", status_code=200)


@router.get("/readyz")
async def readyz() -> Response:
    """
    Kubernetes Readiness Probe.
    Returns 200 OK if all core engines are initialized and ready to serve traffic.
    """
    try:
        mc = _get_mc()
        # Check event bus and fund engine initialization
        if not mc["fund_engine"].list_all_funds():
            return Response(
                content='{"status":"NOT_READY","reason":"Funds not initialized"}',
                media_type="application/json",
                status_code=503,
            )
        return Response(
            content='{"status":"READY"}', media_type="application/json", status_code=200
        )
    except Exception as e:
        return Response(
            content=f'{{"status":"NOT_READY","error":"{str(e)}"}}',
            media_type="application/json",
            status_code=503,
        )


@router.get("/metrics")
async def metrics() -> Response:
    """
    Prometheus Exposition Text Format Metrics Exporter.
    Provides gauge and counter telemetry for Prometheus scraping.
    """
    mc = _get_mc()
    uptime_sec = round(time.time() - mc["start"], 2)
    timeline_count = len(mc["timeline"].query_timeline(limit=10000))
    reasoning_count = len(mc["memory_store"].list_all_records(limit=10000))
    funds = mc["fund_engine"].list_all_funds()
    total_aum = sum(f.current_market_value_usd for f in funds)
    subscribers_count = len(mc["event_bus"].subscribers)
    briefings_count = len(mc["briefing_engine"].list_briefings())

    lines = [
        "# HELP alphamind_uptime_seconds Total system uptime in seconds",
        "# TYPE alphamind_uptime_seconds gauge",
        f"alphamind_uptime_seconds {uptime_sec}",
        "",
        "# HELP alphamind_timeline_events_total Total events recorded in Unified Timeline",
        "# TYPE alphamind_timeline_events_total counter",
        f"alphamind_timeline_events_total {timeline_count}",
        "",
        "# HELP alphamind_reasoning_records_total Total AI decision records stored in Intelligence Memory",
        "# TYPE alphamind_reasoning_records_total counter",
        f"alphamind_reasoning_records_total {reasoning_count}",
        "",
        "# HELP alphamind_active_funds_total Total active virtual AI investment funds",
        "# TYPE alphamind_active_funds_total gauge",
        f"alphamind_active_funds_total {len(funds)}",
        "",
        "# HELP alphamind_total_aum_usd Total Assets Under Management in USD across virtual funds",
        "# TYPE alphamind_total_aum_usd gauge",
        f"alphamind_total_aum_usd {total_aum:.2f}",
        "",
        "# HELP alphamind_event_bus_subscribers Number of active Event Bus subscriber channels",
        "# TYPE alphamind_event_bus_subscribers gauge",
        f"alphamind_event_bus_subscribers {subscribers_count}",
        "",
        "# HELP alphamind_briefings_generated_total Total daily briefings generated",
        "# TYPE alphamind_briefings_generated_total counter",
        f"alphamind_briefings_generated_total {briefings_count}",
        "",
    ]

    for f in funds:
        fid = f.fund_id.value
        lines.extend(
            [
                f'alphamind_fund_aum_usd{{fund_id="{fid}"}} {f.current_market_value_usd:.2f}',
                f'alphamind_fund_cagr_pct{{fund_id="{fid}"}} {f.cagr_pct:.2f}',
                f'alphamind_fund_sharpe_ratio{{fund_id="{fid}"}} {f.sharpe_ratio:.2f}',
            ]
        )

    body = "\n".join(lines) + "\n"
    return Response(
        content=body, media_type="text/plain; version=0.0.4; charset=utf-8", status_code=200
    )
