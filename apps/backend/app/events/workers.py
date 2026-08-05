"""
AlphaMind AI - Background Worker Pool & Task Queue Consumers
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from apps.backend.app.events.contracts import EventMessage

logger = logging.getLogger(__name__)


class BackgroundWorkerPool:
    """Async Background Worker Pool for consumer task processing."""

    def __init__(self, num_workers: int = 4) -> None:
        self.num_workers = num_workers
        self.queue: asyncio.Queue[EventMessage] = asyncio.Queue()
        self._workers: list[asyncio.Task[Any]] = []
        self.is_running = False

    async def start(self) -> None:
        """Start worker pool consumer tasks."""
        self.is_running = True
        for i in range(self.num_workers):
            task = asyncio.create_task(self._worker_loop(i))
            self._workers.append(task)
        logger.info("Started %d background workers in worker pool.", self.num_workers)

    async def enqueue_task(self, event: EventMessage) -> None:
        """Enqueue task into background worker queue."""
        await self.queue.put(event)

    async def _worker_loop(self, worker_id: int) -> None:
        """Worker event consumption loop."""
        while self.is_running:
            try:
                event = await self.queue.get()
                logger.info(
                    "Worker %d processing event %s (%s)",
                    worker_id,
                    event.event_id,
                    event.event_type,
                )
                await asyncio.sleep(0.01)  # Process task stub
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.error("Worker %d encountered error: %s", worker_id, exc)

    async def stop(self) -> None:
        """Stop worker pool consumer tasks."""
        self.is_running = False
        for task in self._workers:
            task.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
