"""
Live OS Core Test Suite — Canonical Asset Registry, Live Event Bus, Unified Timeline,
Worker Pool Manager, Live Scheduler, System Health Monitor, Event Replay Engine, and OS REST APIs.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.main import app
from packages.os_core.asset_registry import AssetClass, CanonicalAsset, CanonicalAssetRegistry
from packages.os_core.event_bus import EventBusManager, EventType, SystemEvent
from packages.os_core.event_replay import EventReplayEngine
from packages.os_core.live_scheduler import LiveScheduler
from packages.os_core.system_health import SystemHealthMonitor
from packages.os_core.unified_timeline import UnifiedImmutableTimeline
from packages.os_core.worker_pool import WorkerPoolManager


def test_canonical_asset_registry() -> None:
    """Test CanonicalAssetRegistry asset registration and symbol/UUID lookup."""
    reg = CanonicalAssetRegistry()

    aapl = reg.get_by_symbol("AAPL")
    assert aapl is not None
    assert aapl.asset_class == AssetClass.STOCKS
    assert aapl.asset_uuid.startswith("asset_")

    by_uuid = reg.get_by_uuid(aapl.asset_uuid)
    assert by_uuid is not None
    assert by_uuid.symbol == "AAPL"

    custom_crypto = CanonicalAsset(
        symbol="SOL-USD",
        canonical_name="Solana USD",
        asset_class=AssetClass.CRYPTO,
        exchange="BINANCE",
    )
    reg.register_asset(custom_crypto)
    assert reg.get_by_symbol("SOL-USD") is not None


def test_live_event_bus_and_subscribers() -> None:
    """Test EventBusManager pub/sub dispatching and subscriber execution."""
    bus = EventBusManager()
    received_events = []

    def handler(evt: SystemEvent) -> None:
        received_events.append(evt)

    bus.subscribe(EventType.MARKET_TICK_INGESTED, handler)

    event = SystemEvent(
        event_type=EventType.MARKET_TICK_INGESTED,
        source_subsystem="market_feed",
        headline="Tick AAPL",
        details="Quote @ $155.00",
    )
    bus.publish(event)

    assert len(received_events) == 1
    assert received_events[0].headline == "Tick AAPL"
    assert received_events[0].trace_id.startswith("trace_")


def test_unified_immutable_timeline() -> None:
    """Test UnifiedImmutableTimeline append-only event logging and filtering."""
    timeline = UnifiedImmutableTimeline()
    event = SystemEvent(
        event_type=EventType.SEC_FILING_PROCESSED,
        source_subsystem="research",
        headline="10-K Ingested — AAPL",
        details="Processed Form 10-K Item 7",
        related_asset_uuid="asset_aapl_01",
    )

    timeline.append_event(event)
    assert len(timeline.timeline_events) == 1
    assert timeline.get_event_by_id(event.event_id) is not None

    queried = timeline.query_timeline(event_type=EventType.SEC_FILING_PROCESSED)
    assert len(queried) == 1


def test_worker_pool_manager() -> None:
    """Test WorkerPoolManager background task execution."""
    pool = WorkerPoolManager(max_concurrent_workers=4)

    executed = False

    def dummy_task() -> None:
        nonlocal executed
        executed = True

    task = pool.submit_task("Compute Sharpe Ratio", dummy_task)
    assert executed
    assert task.status == "COMPLETED"
    assert task.duration_ms >= 0.0


def test_live_scheduler_24x7() -> None:
    """Test LiveScheduler interval task triggering and EventBus publication."""
    bus = EventBusManager()
    scheduler = LiveScheduler(bus)

    sch_id = list(scheduler.schedules.keys())[0]
    evt = scheduler.trigger_schedule(sch_id)

    assert evt.source_subsystem == "live_scheduler"
    assert len(bus.published_events_history) == 1


def test_system_health_monitor() -> None:
    """Test SystemHealthMonitor metric updates and OpenTelemetry compatibility."""
    monitor = SystemHealthMonitor()
    snapshot = monitor.update_metrics(queue_depth=2, ingestion_latency=35.0)

    assert snapshot.overall_status == "HEALTHY"
    assert snapshot.queue_depth_count == 2
    assert snapshot.avg_ingestion_latency_ms == 35.0


def test_event_replay_engine() -> None:
    """Test EventReplayEngine chess-style step-by-step event replay."""
    timeline = UnifiedImmutableTimeline()
    evt1 = SystemEvent(
        event_type=EventType.MARKET_TICK_INGESTED,
        source_subsystem="test",
        headline="Step 1 Tick",
        details="Detail 1",
    )
    evt2 = SystemEvent(
        event_type=EventType.FORECAST_UPDATED,
        source_subsystem="test",
        headline="Step 2 Forecast",
        details="Detail 2",
    )
    timeline.append_event(evt1)
    timeline.append_event(evt2)

    replay = EventReplayEngine(timeline)
    count = replay.initialize_replay()
    assert count == 2

    step1 = replay.step_forward()
    assert step1 is not None
    assert step1.step_index == 1
    assert step1.current_event.headline == "Step 1 Tick"

    step2 = replay.step_forward()
    assert step2 is not None
    assert step2.step_index == 2
    assert step2.current_event.headline == "Step 2 Forecast"


@pytest.mark.asyncio
async def test_os_core_api_endpoints() -> None:
    """Test Live OS Core REST API endpoints (/status, /assets, /timeline, /health, /events/publish, /replay/start)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_status = await client.get("/api/v1/os/status")
        res_assets = await client.get("/api/v1/os/assets")
        res_timeline = await client.get("/api/v1/os/timeline")
        res_health = await client.get("/api/v1/os/health")
        res_pub = await client.post("/api/v1/os/events/publish?headline=TestEvent&symbol=AAPL")
        res_replay = await client.post("/api/v1/os/replay/start")

    assert res_status.status_code == 200
    assert res_assets.status_code == 200
    assert res_timeline.status_code == 200
    assert res_health.status_code == 200
    assert res_pub.status_code == 200
    assert res_replay.status_code == 200
