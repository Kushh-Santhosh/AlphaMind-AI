"""
AlphaMind AI - Workflow Observability & Execution Timeline Tracker
"""

from __future__ import annotations

import logging
import time

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class NodeTimingRecord(BaseModel):
    node_id: str
    agent_id: str
    start_time: float
    end_time: float
    duration_ms: float
    status: str  # "success", "failed", "retried"
    retry_count: int = 0


class WorkflowTimeline(BaseModel):
    workflow_name: str
    session_id: str
    start_timestamp: float = Field(default_factory=time.time)
    end_timestamp: float | None = None
    total_duration_ms: float = 0.0
    total_execution_cost_usd: float = 0.0
    node_timings: list[NodeTimingRecord] = Field(default_factory=list)
    state_version_count: int = 1
    checkpoint_count: int = 0


class WorkflowObservabilityTracker:
    """Tracker capturing node execution timing, agent steps, timelines, and costs."""

    def __init__(self, workflow_name: str, session_id: str) -> None:
        self.timeline = WorkflowTimeline(workflow_name=workflow_name, session_id=session_id)

    def record_node_timing(
        self,
        node_id: str,
        agent_id: str,
        start_time: float,
        end_time: float,
        status: str = "success",
        retry_count: int = 0,
    ) -> None:
        """Record timing telemetry for a completed node step."""
        duration = (end_time - start_time) * 1000.0
        record = NodeTimingRecord(
            node_id=node_id,
            agent_id=agent_id,
            start_time=start_time,
            end_time=end_time,
            duration_ms=duration,
            status=status,
            retry_count=retry_count,
        )
        self.timeline.node_timings.append(record)
        logger.info(
            "Telemetry recorded node '%s' duration: %.2fms (status: %s)",
            node_id,
            duration,
            status,
        )

    def record_cost(self, cost_usd: float) -> None:
        """Accumulate token execution cost."""
        self.timeline.total_execution_cost_usd += cost_usd

    def finalize(self) -> WorkflowTimeline:
        """Finalize workflow timeline and total execution duration."""
        self.timeline.end_timestamp = time.time()
        self.timeline.total_duration_ms = (
            self.timeline.end_timestamp - self.timeline.start_timestamp
        ) * 1000.0
        return self.timeline
