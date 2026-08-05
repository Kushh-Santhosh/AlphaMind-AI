"""
Data Foundation Test Suite — Event Bus, DLQ & Task Scheduler Tests
"""

import pytest

from apps.backend.app.events.bus import EventBus
from apps.backend.app.events.contracts import EventMessage
from apps.backend.app.events.dlq import DeadLetterQueue
from apps.backend.app.events.scheduler import TaskScheduler


@pytest.mark.asyncio
async def test_event_bus_pub_sub() -> None:
    """Publish event to registered handler callback."""
    dlq = DeadLetterQueue()
    bus = EventBus(dlq)
    received_events = []

    async def sample_handler(event: EventMessage) -> None:
        received_events.append(event)

    bus.subscribe("market.data.ingested", sample_handler)

    msg = EventMessage(
        event_type="market.data.ingested",
        source="test",
        payload={"symbol": "NVDA"},
    )

    await bus.publish(msg)
    assert len(received_events) == 1
    assert received_events[0].payload["symbol"] == "NVDA"


@pytest.mark.asyncio
async def test_dlq_capture_on_handler_exhaustion() -> None:
    """Failing handler retries and routes to DLQ upon exhaustion."""
    dlq = DeadLetterQueue()
    bus = EventBus(dlq)

    async def failing_handler(event: EventMessage) -> None:
        raise ValueError("Handler processing failed")

    bus.subscribe("test.failure", failing_handler)

    msg = EventMessage(
        event_type="test.failure",
        source="test",
        payload={},
        max_retries=1,
    )

    await bus.publish(msg)
    assert dlq.size() == 1
    assert dlq.list_dlq()[0].event_type == "test.failure"


def test_task_scheduler_one_shot() -> None:
    """TaskScheduler one-shot timer registration."""
    scheduler = TaskScheduler()
    task = scheduler.schedule_one_shot("timer-1", 60.0, "Run data validation ping")
    assert task.task_id == "timer-1"
    assert len(scheduler.list_tasks()) == 1
