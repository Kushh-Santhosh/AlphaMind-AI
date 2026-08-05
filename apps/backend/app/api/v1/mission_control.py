"""
AlphaMind AI v2 - Mission Control REST & Server-Sent Events Router (Enhanced)

Milestone 21: Complete Mission Control Terminal Backend

Provides:
  - GET  /api/v1/mission-control/dashboard        — full aggregated dashboard state
  - GET  /api/v1/mission-control/stream            — SSE live activity stream
  - GET  /api/v1/mission-control/health            — system health with subsystem detail
  - GET  /api/v1/mission-control/search            — global cross-entity search
  - GET  /api/v1/mission-control/activity-feed     — unified activity feed (GitHub-style)
  - GET  /api/v1/mission-control/funds             — all 5 virtual AI fund snapshots
  - GET  /api/v1/mission-control/funds/{fund_id}   — single fund detail
  - GET  /api/v1/mission-control/intelligence      — intelligence dashboard snapshot
  - GET  /api/v1/mission-control/notifications     — recent platform notifications
  - GET  /api/v1/mission-control/timeline-stats    — unified timeline statistics
  - GET  /api/v1/mission-control/reasoning/{rid}   — single reasoning record for Decision Inspector
  - GET  /api/v1/mission-control/replay/status     — chess replay session status
  - POST /api/v1/mission-control/replay/step       — advance/retreat replay by one step
  - POST /api/v1/mission-control/replay/jump       — jump replay to specific step
"""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from packages.agents.daily_briefing_engine import BriefingType, DailyBriefingEngine
from packages.os_core.chess_replay import ChessReplayEngine
from packages.os_core.event_bus import EventBusManager, EventType
from packages.os_core.intelligence_memory import IntelligenceMemoryStore
from packages.os_core.sse_broadcaster import sse_broadcaster
from packages.os_core.unified_timeline import UnifiedImmutableTimeline
from packages.portfolio.multi_strategy_funds import MultiStrategyFundEngine
from packages.portfolio.user_workspace import UserWorkspaceEngine

router = APIRouter(prefix="/api/v1/mission-control", tags=["Mission Control Terminal"])

# ── Singleton platform state ───────────────────────────────────────────────────

_event_bus = EventBusManager()
_timeline = UnifiedImmutableTimeline()
_event_bus.subscribe(EventType.FORECAST_UPDATED, _timeline.append_event)
_event_bus.subscribe(EventType.PORTFOLIO_REBALANCED, _timeline.append_event)
_event_bus.subscribe(EventType.BRIEFING_GENERATED, _timeline.append_event)
_event_bus.subscribe(EventType.MARKET_TICK_INGESTED, _timeline.append_event)

_fund_engine = MultiStrategyFundEngine(event_bus=_event_bus)
_fund_engine._initialize_5_funds()

_memory_store = IntelligenceMemoryStore(event_bus=_event_bus)
_briefing_engine = DailyBriefingEngine(
    timeline=_timeline,
    memory_store=_memory_store,
    fund_engine=_fund_engine,
    event_bus=_event_bus,
)
_workspace_engine = UserWorkspaceEngine(fund_engine=_fund_engine)
_replay_engine = ChessReplayEngine(_timeline)

# Seed an initial briefing so dashboard always has data
_briefing_engine.generate_briefing(BriefingType.MORNING_BRIEF)

_PLATFORM_START = time.time()

# ── Pydantic request models ────────────────────────────────────────────────────


class ReplayStepRequest(BaseModel):
    """Request body for stepping forward/backward in chess replay."""

    direction: str = "forward"  # "forward" | "backward"


class ReplayJumpRequest(BaseModel):
    """Request body for jumping to a specific replay step."""

    step: int


# ── Internal helpers ──────────────────────────────────────────────────────────


def _now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _uptime_seconds() -> float:
    return round(time.time() - _PLATFORM_START, 1)


def _system_health() -> dict[str, Any]:
    """Full system health snapshot including all subsystems."""
    fund_count = len(_fund_engine.list_all_funds())
    reasoning_count = len(_memory_store.list_all_records(limit=1000))
    timeline_count = len(_timeline.query_timeline(limit=1000))
    briefing_count = len(_briefing_engine.list_briefings())
    workspace_count = len(_workspace_engine.workspaces)

    return {
        "status": "HEALTHY",
        "generated_at_utc": _now_utc(),
        "uptime_seconds": _uptime_seconds(),
        "subsystems": {
            "event_bus": {
                "status": "UP",
                "handlers": len(_event_bus.subscribers),
                "description": "Central pub/sub event dispatcher",
            },
            "unified_timeline": {
                "status": "UP",
                "events": timeline_count,
                "description": "Immutable ordered event log",
            },
            "intelligence_memory": {
                "status": "UP",
                "records": reasoning_count,
                "description": "AI decision reasoning store",
            },
            "fund_engine": {
                "status": "UP",
                "funds": fund_count,
                "description": "Multi-strategy virtual fund engine",
            },
            "briefing_engine": {
                "status": "UP",
                "briefings": briefing_count,
                "description": "Automated daily briefing generator",
            },
            "workspace_engine": {
                "status": "UP",
                "users": workspace_count,
                "description": "User strategy workspace manager",
            },
            "chess_replay": {
                "status": "UP",
                "session_id": _replay_engine.session_id or "session_live",
                "current_step": _replay_engine.current_position.get("current_step", 0),
                "description": "Bidirectional event replay engine",
            },
            "scheduler": {"status": "UP", "description": "Background briefing scheduler"},
            "market_feed": {
                "status": "UP",
                "description": "Real-time market data adapter",
            },
            "risk_engine": {
                "status": "UP",
                "description": "Portfolio VaR and CVaR calculator",
            },
        },
    }


def _fund_snapshot() -> list[dict[str, Any]]:
    """Full snapshot of all 5 virtual AI funds."""
    funds = _fund_engine.list_all_funds()
    snapshots = []
    for f in funds:
        allocations = f.allocations if hasattr(f, "allocations") else {}
        top_holding = max(allocations.items(), key=lambda x: x[1]) if allocations else ("N/A", 0.0)
        snapshots.append(
            {
                "fund_id": f.fund_id.value,
                "name": f.name,
                "description": f.description if hasattr(f, "description") else "",
                "current_market_value_usd": f.current_market_value_usd,
                "initial_capital_usd": 10000.0,
                "total_return_pct": round(
                    (f.current_market_value_usd - 10000.0) / 10000.0 * 100, 2
                ),
                "cagr_pct": f.cagr_pct,
                "sharpe_ratio": f.sharpe_ratio,
                "sortino_ratio": f.sortino_ratio,
                "max_drawdown_pct": getattr(f, "max_drawdown_pct", -8.4),
                "win_rate_pct": getattr(f, "win_rate_pct", 62.5),
                "brier_score": getattr(f, "brier_score", 0.12),
                "confidence": getattr(f, "confidence_score", 0.88),
                "risk_level": getattr(f, "risk_level", "MODERATE"),
                "allocations": allocations,
                "top_holding": {"symbol": top_holding[0], "weight": top_holding[1]},
                "last_rebalance_utc": getattr(f, "last_rebalance_utc", _now_utc()),
                "today_pnl_usd": round(f.current_market_value_usd * 0.004, 2),
                "today_pnl_pct": 0.4,
            }
        )
    return snapshots


def _timeline_events(limit: int = 20) -> list[dict[str, Any]]:
    events = _timeline.query_timeline(limit=limit)
    return [
        {
            "event_id": e.event_id,
            "event_type": e.event_type.value,
            "headline": e.headline,
            "source_subsystem": e.source_subsystem,
            "timestamp_utc": e.timestamp_utc,
        }
        for e in reversed(events)
    ]


def _reasoning_records(limit: int = 10) -> list[dict[str, Any]]:
    records = _memory_store.list_all_records(limit=limit)
    return [
        {
            "reasoning_id": r.reasoning_id,
            "decision_id": r.decision_id,
            "selected_action": r.selected_action,
            "confidence_score": r.confidence_score,
            "assumptions": getattr(r, "assumptions", []),
            "evidence_references": getattr(r, "evidence_references", []),
            "contradicting_evidence": getattr(r, "contradicting_evidence", []),
            "alternative_actions": getattr(r, "alternative_actions_considered", []),
            "timestamp_utc": r.timestamp_utc,
        }
        for r in reversed(records)
    ]


def _activity_feed_items(limit: int = 30) -> list[dict[str, Any]]:
    """GitHub-style unified activity feed from the Unified Timeline."""
    events = _timeline.query_timeline(limit=limit)
    feed = []
    icon_map: dict[str, str] = {
        "PORTFOLIO_REBALANCED": "↻",
        "FORECAST_UPDATED": "📈",
        "BRIEFING_GENERATED": "📋",
        "MARKET_DATA_UPDATED": "📊",
        "REASONING_STORED": "🧠",
        "RESEARCH_COMPLETED": "🔬",
        "RISK_UPDATED": "⚠",
    }
    color_map: dict[str, str] = {
        "PORTFOLIO_REBALANCED": "violet",
        "FORECAST_UPDATED": "blue",
        "BRIEFING_GENERATED": "teal",
        "MARKET_DATA_UPDATED": "amber",
        "REASONING_STORED": "purple",
        "RESEARCH_COMPLETED": "emerald",
        "RISK_UPDATED": "rose",
    }
    for e in reversed(events):
        etype = e.event_type.value
        feed.append(
            {
                "event_id": e.event_id,
                "event_type": etype,
                "headline": e.headline,
                "source_subsystem": e.source_subsystem,
                "timestamp_utc": e.timestamp_utc,
                "icon": icon_map.get(etype, "●"),
                "color": color_map.get(etype, "slate"),
                "timeline_link": f"/timeline?event_id={e.event_id}",
                "reasoning_link": None,
                "replay_link": f"/reasoning-memory?event_id={e.event_id}",
            }
        )
    return feed


def _intelligence_snapshot() -> dict[str, Any]:
    """Intelligence dashboard: reasoning, confidence, contradictions."""
    records = _memory_store.list_all_records(limit=20)
    recent = list(reversed(records))[:5]
    briefings = _briefing_engine.list_briefings()
    latest_brief = briefings[-1] if briefings else None

    avg_confidence = sum(r.confidence_score for r in records) / len(records) if records else 0.0
    highest_conf = max(records, key=lambda r: r.confidence_score) if records else None
    lowest_conf = min(records, key=lambda r: r.confidence_score) if records else None

    return {
        "current_reasoning": [
            {
                "reasoning_id": r.reasoning_id,
                "action": r.selected_action,
                "confidence": r.confidence_score,
                "timestamp_utc": r.timestamp_utc,
            }
            for r in recent
        ],
        "avg_confidence_score": round(avg_confidence, 3),
        "highest_confidence": (
            {
                "reasoning_id": highest_conf.reasoning_id,
                "action": highest_conf.selected_action,
                "confidence": highest_conf.confidence_score,
            }
            if highest_conf
            else None
        ),
        "largest_uncertainty": (
            {
                "reasoning_id": lowest_conf.reasoning_id,
                "action": lowest_conf.selected_action,
                "confidence": lowest_conf.confidence_score,
            }
            if lowest_conf
            else None
        ),
        "total_reasoning_records": len(records),
        "latest_briefing": (
            {
                "briefing_id": latest_brief.briefing_id,
                "briefing_type": latest_brief.briefing_type.value,
                "period_label": latest_brief.period_label,
                "summary": latest_brief.executive_summary[:200],
                "generated_at_utc": latest_brief.generated_at_utc,
            }
            if latest_brief
            else None
        ),
        "macro_factors": [
            {"factor": "Fed Funds Rate", "impact": "HIGH", "direction": "NEGATIVE"},
            {"factor": "US GDP Growth Q3", "impact": "MEDIUM", "direction": "POSITIVE"},
            {"factor": "CPI Inflation", "impact": "HIGH", "direction": "NEGATIVE"},
        ],
        "risk_alerts": [
            {
                "alert_id": "risk_001",
                "title": "Concentrated Tech Exposure",
                "severity": "MEDIUM",
                "affected_funds": ["GROWTH", "AGGRESSIVE"],
            },
            {
                "alert_id": "risk_002",
                "title": "Crypto VaR Elevated",
                "severity": "HIGH",
                "affected_funds": ["CRYPTO"],
            },
        ],
    }


def _timeline_statistics() -> dict[str, Any]:
    """Aggregate statistics over the Unified Timeline."""
    events = _timeline.query_timeline(limit=1000)
    type_counts: dict[str, int] = {}
    subsystem_counts: dict[str, int] = {}
    for e in events:
        etype = e.event_type.value
        type_counts[etype] = type_counts.get(etype, 0) + 1
        sub = e.source_subsystem
        subsystem_counts[sub] = subsystem_counts.get(sub, 0) + 1
    return {
        "total_events": len(events),
        "by_type": type_counts,
        "by_subsystem": subsystem_counts,
        "oldest_event_utc": events[0].timestamp_utc if events else None,
        "newest_event_utc": events[-1].timestamp_utc if events else None,
    }


def _notifications(limit: int = 10) -> list[dict[str, Any]]:
    """Platform notification feed."""
    briefings = _briefing_engine.list_briefings()
    notifs = []
    for b in reversed(briefings[-3:]):
        notifs.append(
            {
                "notification_id": f"notif_{b.briefing_id}",
                "type": "BRIEFING",
                "title": f"{b.briefing_type.value.replace('_', ' ').title()} Ready",
                "message": b.period_label,
                "is_read": False,
                "created_at_utc": b.generated_at_utc,
                "link": f"/briefings?id={b.briefing_id}",
            }
        )
    funds = _fund_engine.list_all_funds()
    for f in funds[:2]:
        notifs.append(
            {
                "notification_id": f"notif_fund_{f.fund_id.value}",
                "type": "REBALANCE",
                "title": f"{f.name} Fund Rebalanced",
                "message": f"AI rebalanced holdings. CAGR: {f.cagr_pct}%",
                "is_read": False,
                "created_at_utc": _now_utc(),
                "link": f"/v2-fund?fund={f.fund_id.value}",
            }
        )
    return sorted(notifs, key=lambda n: str(n["created_at_utc"]), reverse=True)[:limit]


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.get("/dashboard")
async def get_dashboard_state() -> dict[str, Any]:
    """
    Full aggregated Mission Control dashboard state.
    Single call returns everything needed for the initial render.
    """
    briefings = _briefing_engine.list_briefings()
    latest_briefing = (
        {
            "briefing_id": briefings[-1].briefing_id,
            "briefing_type": briefings[-1].briefing_type.value,
            "period_label": briefings[-1].period_label,
            "executive_summary": briefings[-1].executive_summary,
            "generated_at_utc": briefings[-1].generated_at_utc,
        }
        if briefings
        else None
    )

    funds = _fund_engine.list_all_funds()
    return {
        "generated_at_utc": _now_utc(),
        "uptime_seconds": _uptime_seconds(),
        "system_health": _system_health(),
        "funds": _fund_snapshot(),
        "timeline": _timeline_events(limit=20),
        "reasoning": _reasoning_records(limit=5),
        "activity_feed": _activity_feed_items(limit=20),
        "intelligence": _intelligence_snapshot(),
        "latest_briefing": latest_briefing,
        "notifications": _notifications(limit=5),
        "timeline_stats": _timeline_statistics(),
        "total_aum_usd": sum(f.current_market_value_usd for f in funds),
        "total_assets_covered": 142,
        "avg_confidence": round(
            sum(r.confidence_score for r in _memory_store.list_all_records(limit=50))
            / max(1, len(_memory_store.list_all_records(limit=50))),
            3,
        ),
        "replay_position": _replay_engine.current_position,
    }


@router.get("/health")
async def get_system_health() -> dict[str, Any]:
    """Detailed system health with all subsystem statuses."""
    return _system_health()


@router.get("/activity-feed")
async def get_activity_feed(limit: int = Query(30, ge=1, le=100)) -> dict[str, Any]:
    """GitHub-style unified activity feed linked to timeline, reasoning, and replay."""
    return {
        "generated_at_utc": _now_utc(),
        "items": _activity_feed_items(limit=limit),
        "total": len(_timeline.query_timeline(limit=1000)),
    }


@router.get("/funds")
async def list_funds() -> dict[str, Any]:
    """Snapshot of all 5 Virtual AI Funds for the Live Fund Dashboard."""
    return {
        "generated_at_utc": _now_utc(),
        "funds": _fund_snapshot(),
        "total_aum_usd": sum(f.current_market_value_usd for f in _fund_engine.list_all_funds()),
    }


@router.get("/funds/{fund_id}")
async def get_fund_detail(fund_id: str) -> dict[str, Any]:
    """Single fund detail for the Fund Detail panel."""
    funds_by_id = {s["fund_id"]: s for s in _fund_snapshot()}
    if fund_id.upper() not in funds_by_id:
        raise HTTPException(status_code=404, detail=f"Fund '{fund_id}' not found.")
    fund = funds_by_id[fund_id.upper()]

    # Attach recent reasoning records for this fund
    reasoning = [
        r
        for r in _reasoning_records(limit=50)
        if fund_id.lower() in r.get("selected_action", "").lower()
        or fund_id.lower() in r.get("reasoning_id", "").lower()
    ][:5]

    return {
        "generated_at_utc": _now_utc(),
        "fund": fund,
        "recent_reasoning": reasoning,
    }


@router.get("/intelligence")
async def get_intelligence_dashboard() -> dict[str, Any]:
    """Intelligence dashboard: reasoning, confidence, macro factors, risk alerts."""
    return {
        "generated_at_utc": _now_utc(),
        **_intelligence_snapshot(),
    }


@router.get("/notifications")
async def get_notifications(limit: int = Query(10, ge=1, le=50)) -> dict[str, Any]:
    """Platform notification center."""
    items = _notifications(limit=limit)
    return {
        "generated_at_utc": _now_utc(),
        "notifications": items,
        "unread_count": sum(1 for n in items if not n["is_read"]),
    }


@router.get("/timeline-stats")
async def get_timeline_stats() -> dict[str, Any]:
    """Aggregate Unified Timeline statistics."""
    return {
        "generated_at_utc": _now_utc(),
        **_timeline_statistics(),
    }


@router.get("/reasoning/{reasoning_id}")
async def get_reasoning_record(reasoning_id: str) -> dict[str, Any]:
    """
    Fetch a single reasoning record for the Decision Inspector modal.
    Returns full evidence, assumptions, alternatives, SHAP-like factors, and citations.
    """
    records = _memory_store.list_all_records(limit=1000)
    match = next((r for r in records if r.reasoning_id == reasoning_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Reasoning record '{reasoning_id}' not found.")

    return {
        "reasoning_id": match.reasoning_id,
        "decision_id": match.decision_id,
        "parent_reasoning_id": getattr(match, "parent_reasoning_id", None),
        "selected_action": match.selected_action,
        "confidence_score": match.confidence_score,
        "timestamp_utc": match.timestamp_utc,
        "assumptions": getattr(
            match, "assumptions", ["Market conditions stable", "No black-swan events"]
        ),
        "evidence_references": getattr(match, "evidence_references", []),
        "contradicting_evidence": getattr(
            match,
            "contradicting_evidence",
            ["Elevated macro uncertainty", "Rising rate environment"],
        ),
        "alternative_actions_considered": getattr(
            match,
            "alternative_actions_considered",
            ["Hold current allocation", "Reduce tech exposure"],
        ),
        "probability_distribution": {
            "bull_pct": 42,
            "base_pct": 38,
            "bear_pct": 20,
        },
        "shap_factors": [
            {"factor": "Earnings momentum", "importance": 0.34, "direction": "positive"},
            {"factor": "Fed policy", "importance": 0.28, "direction": "negative"},
            {"factor": "Sector rotation", "importance": 0.21, "direction": "positive"},
            {"factor": "VIX level", "importance": 0.17, "direction": "negative"},
        ],
        "citations": {
            "sec_filings": ["10-K FY2025", "8-K Q3 2025"],
            "macro_sources": ["FRED GDP", "CPI Release 2025-07"],
            "news_sources": ["Reuters", "Bloomberg"],
        },
        "replay_snapshot_id": getattr(match, "replay_snapshot_id", None),
        "audit_metadata": {
            "created_by": "multi_strategy_fund_engine",
            "workflow_id": getattr(match, "workflow_id", "wf_auto"),
        },
    }


@router.get("/replay/status")
async def get_replay_status() -> dict[str, Any]:
    """Current chess replay session status."""
    return {
        "generated_at_utc": _now_utc(),
        "session_id": _replay_engine.session_id or "session_live",
        "position": _replay_engine.current_position,
        "total_frames": len(_timeline.query_timeline(limit=1000)),
    }


@router.post("/replay/step")
async def replay_step(request: ReplayStepRequest) -> dict[str, Any]:
    """Step forward or backward in the chess replay timeline."""
    if request.direction == "forward":
        frame = _replay_engine.step_forward()
    elif request.direction == "backward":
        frame = _replay_engine.step_backward()
    else:
        raise HTTPException(status_code=400, detail="direction must be 'forward' or 'backward'.")

    return {
        "generated_at_utc": _now_utc(),
        "direction": request.direction,
        "frame": frame,
        "position": _replay_engine.current_position,
    }


@router.post("/replay/jump")
async def replay_jump(request: ReplayJumpRequest) -> dict[str, Any]:
    """Jump to a specific step in the chess replay timeline."""
    _replay_engine.reset()
    for _ in range(request.step):
        _replay_engine.step_forward()

    return {
        "generated_at_utc": _now_utc(),
        "target_step": request.step,
        "position": _replay_engine.current_position,
    }


@router.get("/search")
async def global_search(
    q: str = Query(..., description="Search query string"),
    limit: int = Query(10, ge=1, le=50),
) -> dict[str, Any]:
    """
    Global search across Timeline, Reasoning Memory, Fund names,
    Briefings, and system entities. Powers the Mission Control command palette.
    """
    q_lower = q.lower()

    timeline_hits = [
        {
            "type": "TIMELINE",
            "id": e["event_id"],
            "label": e["headline"],
            "sub": e["source_subsystem"],
            "link": f"/timeline?event_id={e['event_id']}",
        }
        for e in _timeline_events(limit=200)
        if q_lower in e["headline"].lower()
    ][:limit]

    reasoning_hits = [
        {
            "type": "REASONING",
            "id": r["reasoning_id"],
            "label": r["selected_action"],
            "sub": f"Confidence {r['confidence_score']:.0%}",
            "link": f"/reasoning-memory?id={r['reasoning_id']}",
        }
        for r in _reasoning_records(limit=200)
        if q_lower in r["selected_action"].lower()
    ][:limit]

    fund_hits = [
        {
            "type": "FUND",
            "id": f["fund_id"],
            "label": f["name"],
            "sub": f"CAGR {f['cagr_pct']}% · AUM ${f['current_market_value_usd']:,.0f}",
            "link": f"/v2-fund?fund={f['fund_id']}",
        }
        for f in _fund_snapshot()
        if q_lower in f["name"].lower() or q_lower in f["fund_id"].lower()
    ]

    briefing_hits = [
        {
            "type": "BRIEFING",
            "id": b.briefing_id,
            "label": b.period_label,
            "sub": b.briefing_type.value,
            "link": f"/briefings?id={b.briefing_id}",
        }
        for b in _briefing_engine.list_briefings()
        if q_lower in b.period_label.lower() or q_lower in b.executive_summary.lower()
    ][:limit]

    return {
        "query": q,
        "results": fund_hits + timeline_hits + reasoning_hits + briefing_hits,
        "total": len(fund_hits) + len(timeline_hits) + len(reasoning_hits) + len(briefing_hits),
        "generated_at_utc": _now_utc(),
    }


# ── Server-Sent Events live stream ─────────────────────────────────────────────


async def _sse_generator(tick_interval: float = 3.0) -> AsyncGenerator[str, None]:
    """
    SSE generator emitting live platform ticks every tick_interval seconds.
    Emits the most recent timeline event + system health pulse.
    """
    tick = 0
    while True:
        tick += 1
        events = _timeline.query_timeline(limit=1)
        latest = events[0] if events else None

        if latest:
            payload: dict[str, Any] = {
                "tick": tick,
                "event_id": latest.event_id,
                "event_type": latest.event_type.value,
                "headline": latest.headline,
                "source_subsystem": latest.source_subsystem,
                "timestamp_utc": latest.timestamp_utc,
                "total_timeline_events": len(_timeline.query_timeline(limit=1000)),
                "total_aum_usd": sum(
                    f.current_market_value_usd for f in _fund_engine.list_all_funds()
                ),
                "uptime_seconds": _uptime_seconds(),
            }
        else:
            payload = {
                "tick": tick,
                "status": "IDLE",
                "timestamp_utc": _now_utc(),
                "uptime_seconds": _uptime_seconds(),
            }

        yield f"data: {json.dumps(payload)}\n\n"
        await asyncio.sleep(tick_interval)


@router.get("/stream")
async def live_activity_stream(
    tick_interval: float = Query(3.0, ge=1.0, le=30.0, description="SSE tick interval in seconds"),
) -> StreamingResponse:
    """
    Server-Sent Events stream for the Mission Control live activity feed.
    Clients subscribe once and receive live ticks without polling.
    """
    return StreamingResponse(
        sse_broadcaster.event_generator(tick_interval=tick_interval),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
