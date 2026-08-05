"""
Unit and Integration Tests for HARD-04 Durable Redis Stream EventBus Persistence
"""

import pytest

from packages.os_core.event_bus import EventBusManager, EventType, SystemEvent


def test_event_bus_publish_and_subscribe_in_memory():
    """Verify in-memory publish and subscriber execution backward compatibility."""
    bus = EventBusManager()
    received = []

    def handler(evt: SystemEvent) -> None:
        received.append(evt)

    bus.subscribe(EventType.FORECAST_UPDATED, handler)

    event = SystemEvent(
        event_type=EventType.FORECAST_UPDATED,
        source_subsystem="prediction_engine",
        headline="AAPL Forecast Updated",
        details="95% CI bounds calculated",
    )

    published = bus.publish(event)
    assert published.event_id == event.event_id
    assert len(received) == 1
    assert received[0].headline == "AAPL Forecast Updated"


def test_duplicate_event_suppression():
    """Verify duplicate event ID delivery suppression."""
    bus = EventBusManager()
    received = []

    def handler(evt: SystemEvent) -> None:
        received.append(evt)

    bus.subscribe(EventType.RISK_ALERT_EMITTED, handler)

    event = SystemEvent(
        event_id="evt_duplicate_001",
        event_type=EventType.RISK_ALERT_EMITTED,
        source_subsystem="risk_engine",
        headline="VaR Exceeded",
        details="99% Historical VaR alert",
    )

    bus.publish(event)
    bus.publish(event)  # Second duplicate publish

    assert len(received) == 1
    assert len(bus.published_events_history) == 1


@pytest.mark.asyncio
async def test_redis_stream_methods_fallback_when_offline():
    """Verify consumer group, ack, and replay fallback gracefully when Redis is offline."""
    bus = EventBusManager()
    bus.enable_streams = False

    group_ok = await bus.ensure_consumer_group()
    assert isinstance(group_ok, bool)

    ack_ok = await bus.ack_event("1000-0")
    assert isinstance(ack_ok, bool)

    replayed = await bus.replay_missed_events()
    assert isinstance(replayed, list)
