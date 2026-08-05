"""
AlphaMind AI - Workflow Execution Engine

Supports Sequential Execution, Parallel Execution (Fan-Out), Result Aggregation (Fan-In),
Conditional Branching, Loops, and Dynamic State-Driven Routing.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from packages.agents.checkpoint_manager import CheckpointManager
from packages.agents.lifecycle import AgentRuntimeRunner
from packages.agents.registry import GraphBuilder
from packages.agents.state import AlphaMindAgentState
from packages.agents.state_manager import StateManager
from packages.agents.supervisor import SupervisorOrchestrator

logger = logging.getLogger(__name__)


class WorkflowExecutionEngine:
    """
    Core Execution Engine supporting Sequential, Parallel (Fan-Out/Fan-In),
    Conditional Branching, Loops, and Dynamic Routing.
    """

    def __init__(self, graph_builder: GraphBuilder, session_id: str = "session_001") -> None:
        self.builder = graph_builder
        self.session_id = session_id
        self.supervisor = SupervisorOrchestrator(plan_id=f"plan_{graph_builder.workflow_name}")
        self.checkpoint_manager = CheckpointManager(
            session_id=session_id, workflow_name=graph_builder.workflow_name
        )

    async def execute_sequential(
        self, initial_state: AlphaMindAgentState, node_sequence: list[str]
    ) -> AlphaMindAgentState:
        """Execute sequence of nodes sequentially in order."""
        state_mgr = StateManager(initial_state)

        for node_id in node_sequence:
            handler = self.builder.node_registry.get_node(node_id)
            if not handler:
                logger.warning("Node '%s' not registered in GraphBuilder. Skipping.", node_id)
                continue

            runner = AgentRuntimeRunner(agent_id=node_id)
            current_state = state_mgr.get_current_state()

            # Execute via lifecycle runner
            output = await runner.execute(handler, current_state)

            # State Manager update (Immutable version creation)
            updated_state = state_mgr.update_state(node_id, output)

            # Automatic Checkpoint
            self.checkpoint_manager.create_checkpoint(node_id=node_id, state=updated_state)

        return state_mgr.get_current_state()

    async def execute_parallel_fan_out(
        self,
        initial_state: AlphaMindAgentState,
        parallel_nodes: list[str],
    ) -> AlphaMindAgentState:
        """
        Execute multiple independent nodes in parallel (Fan-Out),
        then aggregate all outputs into state (Fan-In).
        """
        logger.info("Executing parallel Fan-Out for nodes: %s", parallel_nodes)
        state_mgr = StateManager(initial_state)
        current_state = state_mgr.get_current_state()

        async def run_single_node(node_id: str) -> tuple[str, dict[str, Any]]:
            handler = self.builder.node_registry.get_node(node_id)
            if not handler:
                return node_id, {}
            runner = AgentRuntimeRunner(agent_id=node_id)
            output = await runner.execute(handler, current_state)
            return node_id, output

        # Parallel asyncio gathering (Fan-Out)
        tasks = [run_single_node(nid) for nid in parallel_nodes]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Result Aggregation (Fan-In)
        aggregated_updates: dict[str, Any] = {}
        for res in results:
            if isinstance(res, tuple):
                node_id, output = res
                aggregated_updates.update(output)

        final_state = state_mgr.update_state("parallel_fan_in", aggregated_updates)
        self.checkpoint_manager.create_checkpoint(node_id="parallel_fan_in", state=final_state)
        return final_state

    async def execute_dynamic_graph(
        self, initial_state: AlphaMindAgentState
    ) -> AlphaMindAgentState:
        """
        Execute workflow via Supervisor dynamic plan and edge routing.
        """
        state_mgr = StateManager(initial_state)
        registered_nodes = self.builder.node_registry.list_nodes()

        # Step 1: Supervisor creates execution plan
        plan = self.supervisor.create_plan(initial_state, registered_nodes)

        while not plan.is_complete:
            current_state = state_mgr.get_current_state()
            next_target = self.supervisor.route_next(plan, current_state)

            if not next_target:
                break

            handler = self.builder.node_registry.get_node(next_target)
            if not handler:
                continue

            runner = AgentRuntimeRunner(agent_id=next_target)
            output = await runner.execute(handler, current_state)

            # Immutably update state
            updated_state = self.supervisor.aggregate_result(current_state, next_target, output)
            state_mgr.update_state(next_target, dict(updated_state))

            # Checkpoint
            self.checkpoint_manager.create_checkpoint(node_id=next_target, state=updated_state)

        return state_mgr.get_current_state()
