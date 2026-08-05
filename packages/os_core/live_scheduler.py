"""
AlphaMind AI v2 - 24x7 Live Background Scheduler

Triggers continuous background market tick monitoring, filing ingestion,
drift evaluation, and daily briefings.
"""

from __future__ import annotations

import logging
import time
import uuid

from pydantic import BaseModel, Field

from packages.os_core.event_bus import EventBusManager, EventType, SystemEvent

logger = logging.getLogger(__name__)


class ScheduledTask(BaseModel):
    schedule_id: str = Field(default_factory=lambda: f"sch_{uuid.uuid4().hex[:8]}")
    name: str
    interval_seconds: int
    event_type_to_publish: EventType
    is_active: bool = True
    last_triggered_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


class LiveScheduler:
    """24x7 Scheduler triggering live background tasks and event publishing."""

    def __init__(self, event_bus: EventBusManager) -> None:
        self.event_bus = event_bus
        self.schedules: dict[str, ScheduledTask] = {}
        self._seed_default_schedules()

    def _seed_default_schedules(self) -> None:
        """Seed 24x7 continuous background schedules."""
        defaults = [
            ScheduledTask(
                name="24x7 Market Tick Monitor",
                interval_seconds=60,
                event_type_to_publish=EventType.MARKET_TICK_INGESTED,
            ),
            ScheduledTask(
                name="SEC EDGAR 10-K/10-Q Ingestion",
                interval_seconds=300,
                event_type_to_publish=EventType.SEC_FILING_PROCESSED,
            ),
            ScheduledTask(
                name="FRED Macro Release Monitor",
                interval_seconds=600,
                event_type_to_publish=EventType.MACRO_RELEASE_DETECTED,
            ),
            ScheduledTask(
                name="Predictive Model Drift Audit",
                interval_seconds=1800,
                event_type_to_publish=EventType.MODEL_RECALIBRATED,
            ),
        ]
        for sch in defaults:
            self.schedules[sch.schedule_id] = sch

    def trigger_schedule(self, schedule_id: str) -> SystemEvent:
        """Trigger scheduled background task and publish event."""
        sch = self.schedules.get(schedule_id)
        if not sch:
            raise ValueError(f"Schedule '{schedule_id}' not found.")

        sch.last_triggered_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        event = SystemEvent(
            event_type=sch.event_type_to_publish,
            source_subsystem="live_scheduler",
            headline=f"Scheduled Task Execution: {sch.name}",
            details=f"Executed 24x7 background interval task ({sch.interval_seconds}s).",
        )
        self.event_bus.publish(event)
        return event
