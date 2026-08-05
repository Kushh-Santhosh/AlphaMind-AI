"""
AlphaMind AI - Async Task Scheduler Engine (One-shot & Cron Timers)
"""

from __future__ import annotations

import logging
import time

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ScheduledTask(BaseModel):
    task_id: str
    cron_expression: str | None = None
    duration_seconds: float | None = None
    prompt: str
    next_run_timestamp: float


class TaskScheduler:
    """Async Scheduler for one-shot timers and recurring cron background tasks."""

    def __init__(self) -> None:
        self.scheduled_tasks: dict[str, ScheduledTask] = {}
        self._is_running = False

    def schedule_one_shot(
        self, task_id: str, duration_seconds: float, prompt: str
    ) -> ScheduledTask:
        """Schedule a one-shot background timer."""
        next_run = time.time() + duration_seconds
        task = ScheduledTask(
            task_id=task_id,
            duration_seconds=duration_seconds,
            prompt=prompt,
            next_run_timestamp=next_run,
        )
        self.scheduled_tasks[task_id] = task
        logger.info(
            "Scheduled one-shot timer '%s' for %.1fs: %s", task_id, duration_seconds, prompt
        )
        return task

    def list_tasks(self) -> list[ScheduledTask]:
        """List active scheduled tasks."""
        return list(self.scheduled_tasks.values())
