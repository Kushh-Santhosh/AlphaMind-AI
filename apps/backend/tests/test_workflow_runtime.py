"""
Workflow Runtime Test Suite — LangGraph Foundation, State Management, Checkpoints,
Parallel Fan-Out, Supervisor Routing & Agent Lifecycles.
"""

from __future__ import annotations

import pytest

from packages.agents.checkpoint_manager import CheckpointManager, HumanApprovalInterrupt
from packages.agents.execution_engine import WorkflowExecutionEngine
from packages.agents.lifecycle import AgentLifecycleState, AgentRuntimeRunner
from packages.agents.registry import GraphBuilder, WorkflowRegistry
from packages.agents.state import AlphaMindAgentState
from packages.agents.state_manager import StateManager
from packages.agents.supervisor import SupervisorOrchestrator


@pytest.mark.asyncio
async def test_graph_builder_and_registries() -> None:
    """Test GraphBuilder, node registration, edge registration, and WorkflowRegistry."""
    builder = GraphBuilder(workflow_name="TestResearchWorkflow")

    def node_a(state: AlphaMindAgentState) -> dict:
        return {"step_a": "complete"}

    def node_b(state: AlphaMindAgentState) -> dict:
        return {"step_b": "complete"}

    builder.set_start_node("node_a")
    builder.add_node("node_a", node_a)
    builder.add_node("node_b", node_b)
    builder.add_edge("node_a", "node_b")
    builder.add_end_node("node_b")

    WorkflowRegistry.register(builder)
    retrieved = WorkflowRegistry.get("TestResearchWorkflow")

    assert retrieved is not None
    assert retrieved.workflow_name == "TestResearchWorkflow"
    assert len(retrieved.node_registry.list_nodes()) == 2


@pytest.mark.asyncio
async def test_state_manager_immutable_updates_diff_and_rollback() -> None:
    """Test StateManager versioning, immutable updates, diff calculation, and rollback."""
    initial: AlphaMindAgentState = {
        "session_id": "s_001",
        "symbol": "AAPL",
        "asset_class": "equity",
        "target_horizon_days": 30,
        "user_id": "u_100",
        "completed_agent_nodes": [],
        "current_node": "start",
        "circuit_breaker_active": False,
        "error_logs": [],
    }

    mgr = StateManager(initial)
    assert mgr.get_version() == 1

    # Version 2 mutation
    mgr.update_state("node_a", {"market_data": {"price": 150.0}})
    assert mgr.get_version() == 2

    # Version 3 mutation
    mgr.update_state("node_b", {"news_sentiment_data": {"polarity": 0.8}})
    assert mgr.get_version() == 3

    # Diff calculation
    diff = mgr.compute_diff(1, 3)
    assert "market_data" in diff.added_keys
    assert "news_sentiment_data" in diff.added_keys

    # Rollback to Version 2
    rolled_back = mgr.rollback(2)
    assert mgr.get_version() == 2
    assert "market_data" in rolled_back
    assert "news_sentiment_data" not in rolled_back


@pytest.mark.asyncio
async def test_checkpoint_manager_and_human_approval_interrupt() -> None:
    """Test automatic checkpointing, recovery, and human approval interrupts."""
    cp_mgr = CheckpointManager(session_id="s_999", workflow_name="ResearchWf")
    state: AlphaMindAgentState = {"session_id": "s_999", "symbol": "NVDA"}

    # Automatic checkpoint
    rec1 = cp_mgr.create_checkpoint("node_1", state, requires_human_approval=False)
    assert rec1.checkpoint_number == 1
    assert rec1.approval_status == "approved"

    # Human Approval Interrupt
    with pytest.raises(HumanApprovalInterrupt) as excinfo:
        cp_mgr.create_checkpoint("node_2", state, requires_human_approval=True)

    assert "node_2" in excinfo.value.reason
    cp_id = excinfo.value.checkpoint_id

    # Resolve Human Approval
    resolved = cp_mgr.resolve_human_approval(cp_id, approve=True)
    assert resolved.approval_status == "approved"

    # State Recovery
    recovered = cp_mgr.recover_state(cp_id)
    assert recovered["symbol"] == "NVDA"


@pytest.mark.asyncio
async def test_supervisor_planning_and_routing() -> None:
    """Test Supervisor plan creation, target routing, and result aggregation."""
    supervisor = SupervisorOrchestrator("plan_001")
    state: AlphaMindAgentState = {"session_id": "s_100", "completed_agent_nodes": []}

    plan = supervisor.create_plan(state, ["node_1", "node_2"])
    assert len(plan.steps) == 2

    # Route 1
    t1 = supervisor.route_next(plan, state)
    assert t1 == "node_1"

    # Aggregate 1
    state = supervisor.aggregate_result(state, "node_1", {"key1": "val1"})

    # Route 2
    t2 = supervisor.route_next(plan, state)
    assert t2 == "node_2"

    # Aggregate 2
    state = supervisor.aggregate_result(state, "node_2", {"key2": "val2"})

    # Route 3 (End)
    t3 = supervisor.route_next(plan, state)
    assert t3 is None
    assert plan.is_complete is True


@pytest.mark.asyncio
async def test_parallel_fan_out_fan_in_execution() -> None:
    """Test parallel Fan-Out execution and Fan-In state aggregation."""
    builder = GraphBuilder(workflow_name="ParallelWf")

    async def node_fast(state: AlphaMindAgentState) -> dict:
        return {"fast_result": "done"}

    async def node_slow(state: AlphaMindAgentState) -> dict:
        return {"slow_result": "done"}

    builder.add_node("node_fast", node_fast)
    builder.add_node("node_slow", node_slow)

    engine = WorkflowExecutionEngine(builder, session_id="s_parallel")
    initial: AlphaMindAgentState = {"session_id": "s_parallel", "symbol": "TSLA"}

    final_state = await engine.execute_parallel_fan_out(initial, ["node_fast", "node_slow"])

    assert final_state["fast_result"] == "done"
    assert final_state["slow_result"] == "done"


@pytest.mark.asyncio
async def test_agent_lifecycle_runner() -> None:
    """Test AgentRuntimeRunner state machine transitions."""
    runner = AgentRuntimeRunner("MarketAgent")

    async def sample_handler(state: AlphaMindAgentState) -> dict:
        return {"market_out": "ok"}

    state: AlphaMindAgentState = {"session_id": "s_lc", "symbol": "MSFT"}
    out = await runner.execute(sample_handler, state)

    assert out["market_out"] == "ok"
    assert runner.status.current_state == AgentLifecycleState.COMPLETED
    assert AgentLifecycleState.EXECUTING in runner.status.state_history
