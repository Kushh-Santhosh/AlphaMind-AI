"""
AlphaMind AI - LangGraph Foundation: Registries, Builder, Metadata & Execution Context

Provides WorkflowRegistry, NodeRegistry, EdgeRegistry, GraphBuilder, ExecutionContext,
and ExecutionMetadata for versioned workflow orchestration.
"""

from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, Field

from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class ExecutionMetadata(BaseModel):
    """Metadata tracking workflow graph execution, versioning, and node timings."""

    workflow_id: str = Field(default_factory=lambda: f"wf_{uuid.uuid4().hex[:8]}")
    session_id: str
    workflow_name: str
    version: str = "1.0.0"
    trace_id: str = Field(default_factory=lambda: f"tr_{uuid.uuid4().hex[:12]}")
    start_timestamp: float = Field(default_factory=time.time)
    end_timestamp: float | None = None
    duration_ms: float = 0.0
    total_steps: int = 0
    active_node: str | None = None
    completed_nodes: list[str] = Field(default_factory=list)
    failed_nodes: list[str] = Field(default_factory=list)
    execution_cost_usd: float = 0.0


class ExecutionContext(BaseModel):
    """Execution context carrying runtime flags, state snapshots, and cancellation signals."""

    metadata: ExecutionMetadata
    is_cancelled: bool = False
    is_paused: bool = False
    requires_human_approval: bool = False
    approval_reason: str | None = None
    max_execution_seconds: float = 60.0
    step_timeout_seconds: float = 10.0


class NodeRegistry:
    """Registry managing executable agent node functions."""

    def __init__(self) -> None:
        self._nodes: dict[str, Callable[[AlphaMindAgentState], Any]] = {}

    def register_node(self, node_id: str, handler: Callable[[AlphaMindAgentState], Any]) -> None:
        """Register an agent node handler."""
        self._nodes[node_id] = handler
        logger.info("Registered agent node '%s' in NodeRegistry.", node_id)

    def get_node(self, node_id: str) -> Callable[[AlphaMindAgentState], Any] | None:
        """Fetch node handler callback."""
        return self._nodes.get(node_id)

    def list_nodes(self) -> list[str]:
        """List registered node IDs."""
        return list(self._nodes.keys())


class EdgeRegistry:
    """Registry managing directed and conditional graph edges."""

    def __init__(self) -> None:
        self._directed_edges: list[tuple[str, str]] = []
        self._conditional_edges: dict[str, Callable[[AlphaMindAgentState], str]] = {}

    def add_edge(self, source_node: str, target_node: str) -> None:
        """Add a directed transition edge between two nodes."""
        self._directed_edges.append((source_node, target_node))

    def add_conditional_edge(
        self, source_node: str, router_func: Callable[[AlphaMindAgentState], str]
    ) -> None:
        """Add a dynamic router function edge for state-based branching."""
        self._conditional_edges[source_node] = router_func

    def get_next_target(self, source_node: str, state: AlphaMindAgentState) -> str | None:
        """Evaluate next target node for a given source node."""
        if source_node in self._conditional_edges:
            return self._conditional_edges[source_node](state)

        for src, target in self._directed_edges:
            if src == source_node:
                return target
        return None


class GraphBuilder:
    """Builder pattern for constructing multi-agent execution graphs."""

    def __init__(self, workflow_name: str, version: str = "1.0.0") -> None:
        self.workflow_name = workflow_name
        self.version = version
        self.node_registry = NodeRegistry()
        self.edge_registry = EdgeRegistry()
        self.start_node: str | None = None
        self.end_nodes: set[str] = set()

    def set_start_node(self, node_id: str) -> GraphBuilder:
        """Define initial graph entry node."""
        self.start_node = node_id
        return self

    def add_node(self, node_id: str, handler: Callable[[AlphaMindAgentState], Any]) -> GraphBuilder:
        """Add node handler to graph."""
        self.node_registry.register_node(node_id, handler)
        return self

    def add_edge(self, source_node: str, target_node: str) -> GraphBuilder:
        """Add static directed edge."""
        self.edge_registry.add_edge(source_node, target_node)
        return self

    def add_conditional_edge(
        self, source_node: str, router_func: Callable[[AlphaMindAgentState], str]
    ) -> GraphBuilder:
        """Add dynamic conditional router edge."""
        self.edge_registry.add_conditional_edge(source_node, router_func)
        return self

    def add_end_node(self, node_id: str) -> GraphBuilder:
        """Mark node as terminal end node."""
        self.end_nodes.add(node_id)
        return self


class WorkflowRegistry:
    """Centralized registry storing compiled GraphBuilder instances."""

    _workflows: dict[str, GraphBuilder] = {}

    @classmethod
    def register(cls, builder: GraphBuilder) -> None:
        """Register compiled graph workflow definition."""
        cls._workflows[builder.workflow_name] = builder
        logger.info(
            "Registered workflow '%s' (v%s) in WorkflowRegistry.",
            builder.workflow_name,
            builder.version,
        )

    @classmethod
    def get(cls, workflow_name: str) -> GraphBuilder | None:
        """Fetch graph builder by workflow name."""
        return cls._workflows.get(workflow_name)

    @classmethod
    def list_workflows(cls) -> list[str]:
        """List registered workflow names."""
        return list(cls._workflows.keys())
