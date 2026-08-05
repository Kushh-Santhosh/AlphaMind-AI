"""
AlphaMind AI - Supervisor Orchestrator Engine

Responsible ONLY for control plane orchestration:
Task Planning, Task Routing, Dependency Resolution, Execution Ordering, Parallel Scheduling,
Retry Decisions, Timeout Handling, Failure Recovery, Result Aggregation, Workflow Completion.

STRICT RULE: The Supervisor MUST NEVER perform financial analysis or business calculations.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field

from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class TaskPlanStep(BaseModel):
    """Plan step item created by Supervisor."""

    step_index: int
    target_node: str
    dependencies: list[str] = Field(default_factory=list)
    status: str = "pending"  # "pending", "in_progress", "completed", "failed"
    is_parallel: bool = False


class WorkflowPlan(BaseModel):
    """Execution plan containing sequence of task steps."""

    plan_id: str
    session_id: str
    steps: list[TaskPlanStep] = Field(default_factory=list)
    current_step_index: int = 0
    is_complete: bool = False


class SupervisorOrchestrator:
    """
    Supervisor Control Plane Engine.
    Evaluates state, plans task execution dependency order, routes to node targets,
    and aggregates outputs into the shared LangGraph State.
    """

    def __init__(self, plan_id: str = "plan_default") -> None:
        self.plan_id = plan_id

    def create_plan(self, state: AlphaMindAgentState, required_nodes: list[str]) -> WorkflowPlan:
        """
        Create structured execution plan dependency order for worker nodes.
        No financial analysis performed.
        """
        session_id = state.get("session_id", "default_session")
        steps: list[TaskPlanStep] = []

        for idx, node_id in enumerate(required_nodes):
            deps = [required_nodes[i] for i in range(idx)]
            steps.append(
                TaskPlanStep(
                    step_index=idx,
                    target_node=node_id,
                    dependencies=deps,
                )
            )

        logger.info(
            "Supervisor created WorkflowPlan '%s' with %d steps for session '%s'.",
            self.plan_id,
            len(steps),
            session_id,
        )
        return WorkflowPlan(plan_id=self.plan_id, session_id=session_id, steps=steps)

    def route_next(self, plan: WorkflowPlan, state: AlphaMindAgentState) -> str | None:
        """
        Route to next pending node target whose dependencies are satisfied.
        Returns None if workflow is complete.
        """
        completed_nodes = set(state.get("completed_agent_nodes", []))

        for step in plan.steps:
            if step.target_node in completed_nodes:
                step.status = "completed"
                continue

            if step.status == "completed":
                continue

            # Check if all prerequisite dependencies are met
            deps_satisfied = all(dep in completed_nodes for dep in step.dependencies)

            if deps_satisfied:
                step.status = "in_progress"
                logger.info(
                    "Supervisor routing session '%s' to target node '%s'.",
                    plan.session_id,
                    step.target_node,
                )
                return step.target_node

        plan.is_complete = True
        logger.info("Supervisor declared WorkflowPlan '%s' COMPLETE.", plan.plan_id)
        return None

    def evaluate_retry(self, node_id: str, current_retries: int, max_retries: int = 3) -> bool:
        """Decide whether to retry a failed worker node."""
        should_retry = current_retries < max_retries
        logger.info(
            "Supervisor retry decision for node '%s' (attempt %d/%d): %s",
            node_id,
            current_retries,
            max_retries,
            "RETRY" if should_retry else "FAILOVER",
        )
        return should_retry

    def aggregate_result(
        self, state: AlphaMindAgentState, node_id: str, node_output: dict[str, Any]
    ) -> AlphaMindAgentState:
        """
        Aggregate worker node result into shared LangGraph State.
        Pure state mutation — zero business logic computation.
        """
        completed = list(state.get("completed_agent_nodes", []))
        if node_id not in completed:
            completed.append(node_id)

        updated_state = dict(state)
        updated_state.update(node_output)
        updated_state["completed_agent_nodes"] = completed
        updated_state["current_node"] = "supervisor"

        logger.info("Supervisor aggregated output from '%s' into state.", node_id)
        return updated_state  # type: ignore[return-value]
