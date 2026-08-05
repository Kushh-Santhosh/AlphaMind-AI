"""
API v1 — Live Operating System Core Router
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from packages.os_core.asset_registry import CanonicalAssetRegistry
from packages.os_core.event_bus import EventBusManager, EventType, SystemEvent
from packages.os_core.event_replay import EventReplayEngine
from packages.os_core.live_scheduler import LiveScheduler
from packages.os_core.system_health import SystemHealthMonitor
from packages.os_core.unified_timeline import UnifiedImmutableTimeline
from packages.os_core.worker_pool import WorkerPoolManager

router = APIRouter(prefix="/api/v1/os", tags=["Live OS Core"])

asset_registry = CanonicalAssetRegistry()
event_bus = EventBusManager()
timeline = UnifiedImmutableTimeline()
scheduler = LiveScheduler(event_bus)
health_monitor = SystemHealthMonitor()
worker_pool = WorkerPoolManager()
replay_engine = EventReplayEngine(timeline)

# Subscribe timeline to event bus
event_bus.subscribe(EventType.MARKET_TICK_INGESTED, timeline.append_event)
event_bus.subscribe(EventType.SEC_FILING_PROCESSED, timeline.append_event)
event_bus.subscribe(EventType.FORECAST_UPDATED, timeline.append_event)
event_bus.subscribe(EventType.PORTFOLIO_REBALANCED, timeline.append_event)


@router.get("/status")
async def get_os_status() -> dict[str, Any]:
    """Fetch Live OS Core kernel runtime status and registered assets count."""
    return {
        "os_version": "2.0.0",
        "kernel_status": "RUNNING_24X7",
        "canonical_assets_count": len(asset_registry.list_all_assets()),
        "timeline_events_count": len(timeline.timeline_events),
        "scheduler_active_tasks": len(scheduler.schedules),
    }


@router.get("/assets")
async def list_canonical_assets() -> list[dict[str, Any]]:
    """Fetch canonical assets from Asset Registry."""
    assets = asset_registry.list_all_assets()
    return [a.model_dump() for a in assets]


@router.get("/timeline")
async def query_unified_timeline(
    event_type: EventType | None = None,
    asset_uuid: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Fetch events from Unified Immutable Timeline."""
    events = timeline.query_timeline(event_type, asset_uuid, limit)
    return [e.model_dump() for e in events]


@router.get("/health")
async def get_system_health() -> dict[str, Any]:
    """Fetch AI System Health Monitor snapshot."""
    snapshot = health_monitor.update_metrics(queue_depth=len(worker_pool.tasks))
    return snapshot.model_dump()


@router.post("/events/publish")
async def publish_system_event(
    event_type: EventType = EventType.MARKET_TICK_INGESTED,
    headline: str = "Market Tick Ingested — AAPL",
    details: str = "Live quote processed for AAPL @ $155.00",
    symbol: str = "AAPL",
) -> dict[str, Any]:
    """Publish custom SystemEvent to EventBus."""
    asset = asset_registry.get_by_symbol(symbol)
    evt = SystemEvent(
        event_type=event_type,
        source_subsystem="api_gateway",
        headline=headline,
        details=details,
        related_asset_uuid=asset.asset_uuid if asset else None,
    )
    event_bus.publish(evt)
    return evt.model_dump()


@router.post("/replay/start")
async def start_event_replay(asset_uuid: str | None = None) -> dict[str, Any]:
    """Initialize chess-style historical event replay session."""
    count = replay_engine.initialize_replay(asset_uuid)
    first_step = replay_engine.step_forward()
    return {
        "replay_initialized": True,
        "total_events_count": count,
        "first_step": first_step.model_dump() if first_step else None,
    }
