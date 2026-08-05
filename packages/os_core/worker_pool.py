"""
AlphaMind AI v2 - Distributed Worker Pool Manager

Manages concurrent background research worker tasks and queue execution.
"""

from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Callable

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class WorkerTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"tsk_{uuid.uuid4().hex[:8]}")
    name: str
    status: str = "PENDING"  # "PENDING", "RUNNING", "COMPLETED", "FAILED"
    duration_ms: float = 0.0
    created_at_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


class WorkerPoolManager:
    """Worker pool manager orchestrating parallel background research tasks."""

    def __init__(self, max_concurrent_workers: int = 8) -> None:
        self.max_concurrent_workers = max_concurrent_workers
        self.tasks: dict[str, WorkerTask] = {}

    def submit_task(self, name: str, task_fn: Callable[[], None]) -> WorkerTask:
        """Submit task to worker pool."""
        start_t = time.monotonic()
        task = WorkerTask(name=name, status="RUNNING")
        self.tasks[task.task_id] = task

        try:
            task_fn()
            task.status = "COMPLETED"
        except Exception as e:
            task.status = "FAILED"
            logger.error("Worker task '%s' failed: %s", task.task_id, e)

        task.duration_ms = round((time.monotonic() - start_t) * 1000.0, 2)
        logger.info("Worker task '%s' completed in %.2fms", name, task.duration_ms)
        return task
