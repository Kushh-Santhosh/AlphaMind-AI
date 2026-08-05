"""
AlphaMind AI - Agent Runtime Lifecycle Engine

Manages state machine transitions: INITIALIZED -> VALIDATED -> EXECUTING -> CHECKPOINTING -> PAUSED -> RESUMED -> CANCELLED -> RETRIED -> SHUTDOWN.
Abstract lifecycle runner with zero financial domain logic.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class AgentLifecycleState(str, Enum):  # noqa: UP042
    INITIALIZED = "initialized"
    VALIDATED = "validated"
    EXECUTING = "executing"
    CHECKPOINTING = "checkpointing"
    PAUSED = "paused"
    RESUMED = "resumed"
    CANCELLED = "cancelled"
    RETRIED = "retried"
    COMPLETED = "completed"
    FAILED = "failed"
    SHUTDOWN = "shutdown"


class AgentLifecycleStatus(BaseModel):
    agent_id: str
    current_state: AgentLifecycleState = AgentLifecycleState.INITIALIZED
    state_history: list[AgentLifecycleState] = Field(default_factory=list)
    start_time: float = Field(default_factory=time.time)
    end_time: float | None = None
    retry_count: int = 0
    error_message: str | None = None


class AgentRuntimeRunner:
    """Abstract Agent Lifecycle Runner executing lifecycle hooks around agent nodes."""

    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id
        self.status = AgentLifecycleStatus(agent_id=agent_id)
        self._transition(AgentLifecycleState.INITIALIZED)

    def _transition(self, new_state: AgentLifecycleState) -> None:
        """Record lifecycle state transition."""
        self.status.current_state = new_state
        self.status.state_history.append(new_state)
        logger.info("Agent '%s' lifecycle transition -> %s", self.agent_id, new_state.value)

    def validate_inputs(self, state: AlphaMindAgentState) -> bool:
        """Lifecycle Hook: Validate state input required payload keys."""
        self._transition(AgentLifecycleState.VALIDATED)
        return "session_id" in state and "symbol" in state

    async def execute(
        self,
        handler: Callable[[AlphaMindAgentState], Any],
        state: AlphaMindAgentState,
    ) -> dict[str, Any]:
        """
        Execute agent handler through complete lifecycle state sequence.
        """
        if not self.validate_inputs(state):
            self._transition(AgentLifecycleState.FAILED)
            self.status.error_message = "State validation failed (missing session_id or symbol)."
            raise ValueError(self.status.error_message)

        self._transition(AgentLifecycleState.EXECUTING)
        start_t = time.monotonic()

        try:
            # Execute node handler
            result = await handler(state) if callable(handler) else {}

            self._transition(AgentLifecycleState.CHECKPOINTING)
            self._transition(AgentLifecycleState.COMPLETED)
            self.status.end_time = time.time()
            logger.info(
                "Agent '%s' execution completed successfully in %.2fms.",
                self.agent_id,
                (time.monotonic() - start_t) * 1000.0,
            )
            return result if isinstance(result, dict) else {}

        except Exception as exc:
            self._transition(AgentLifecycleState.FAILED)
            self.status.error_message = str(exc)
            logger.error("Agent '%s' execution failed: %s", self.agent_id, exc)
            raise exc

    def pause(self) -> None:
        """Pause agent execution."""
        self._transition(AgentLifecycleState.PAUSED)

    def resume(self) -> None:
        """Resume agent execution."""
        self._transition(AgentLifecycleState.RESUMED)

    def cancel(self) -> None:
        """Cancel agent execution."""
        self._transition(AgentLifecycleState.CANCELLED)

    def retry(self) -> None:
        """Increment retry count and trigger retry transition."""
        self.status.retry_count += 1
        self._transition(AgentLifecycleState.RETRIED)

    def shutdown(self) -> None:
        """Shutdown agent runner."""
        self._transition(AgentLifecycleState.SHUTDOWN)
