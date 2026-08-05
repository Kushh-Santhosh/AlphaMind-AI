"""
AlphaMind AI - Autonomous Agent Abstract Interface Definitions

Contains pure abstract protocol interface definitions for all 11 AI Agents.
NO BUSINESS LOGIC OR IMPLEMENTATION CODE IS WRITTEN HERE.
"""

from typing import Any, Protocol, runtime_checkable

from packages.agents.state import AlphaMindAgentState


@runtime_checkable
class BaseAgentInterface(Protocol):
    """Base interface for all autonomous LangGraph agent nodes."""

    agent_id: str
    description: str

    async def execute(self, state: AlphaMindAgentState) -> dict[str, Any]:
        """
        Execute agent node operation on shared state.
        Returns partial state mutation dictionary to be merged into LangGraph state.
        """
        ...


@runtime_checkable
class SupervisorAgentInterface(Protocol):
    """Interface for Supervisor Agent controlling orchestration workflow."""

    async def route_next_node(self, state: AlphaMindAgentState) -> str:
        """Determine next agent node execution target or declare END."""
        ...


@runtime_checkable
class ResearchAgentInterface(BaseAgentInterface, Protocol):
    """Interface for general financial research agents."""

    ...


@runtime_checkable
class PredictionAgentInterface(BaseAgentInterface, Protocol):
    """Interface for Probability Prediction Agent."""

    ...


@runtime_checkable
class PortfolioAgentInterface(BaseAgentInterface, Protocol):
    """Interface for Portfolio Optimization Agent."""

    ...


@runtime_checkable
class RiskAgentInterface(BaseAgentInterface, Protocol):
    """Interface for Dedicated Risk & Hallucination Verification Agent."""

    ...


@runtime_checkable
class NewsAgentInterface(BaseAgentInterface, Protocol):
    """Interface for News Analysis Agent."""

    ...


@runtime_checkable
class MacroAgentInterface(BaseAgentInterface, Protocol):
    """Interface for Macroeconomic Agent."""

    ...


@runtime_checkable
class ReportAgentInterface(BaseAgentInterface, Protocol):
    """Interface for Explainable AI (XAI) Report Generator Agent."""

    ...


@runtime_checkable
class MemoryAgentInterface(BaseAgentInterface, Protocol):
    """Interface for Hierarchical Memory Agent."""

    ...
