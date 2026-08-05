"""
AlphaMind AI - Checkpoint Manager & Human-in-the-Loop Interrupt Engine

Supports automatic checkpointing, failure recovery, execution replay, and human approval interrupts.
"""

from __future__ import annotations

import copy
import logging
import time
from typing import Any

from pydantic import BaseModel, Field

from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class CheckpointRecord(BaseModel):
    """Checkpoint snapshot stored in persistent memory/database."""

    checkpoint_id: str
    session_id: str
    workflow_name: str
    checkpoint_number: int
    active_node: str
    timestamp: float = Field(default_factory=time.time)
    state_payload: dict[str, Any]
    requires_human_approval: bool = False
    approval_status: str = "pending"  # "pending", "approved", "rejected"


class HumanApprovalInterrupt(Exception):
    """Raised when a workflow hits a human approval checkpoint interrupt."""

    def __init__(self, checkpoint_id: str, reason: str) -> None:
        self.checkpoint_id = checkpoint_id
        self.reason = reason
        super().__init__(f"Human approval required for checkpoint '{checkpoint_id}': {reason}")


class CheckpointManager:
    """
    Manager governing automatic state checkpoints, failure recovery, replay,
    and Human-in-the-Loop approval interrupts.
    """

    def __init__(self, session_id: str, workflow_name: str) -> None:
        self.session_id = session_id
        self.workflow_name = workflow_name
        self._checkpoints: dict[str, CheckpointRecord] = {}
        self._counter = 0

    def create_checkpoint(
        self,
        node_id: str,
        state: AlphaMindAgentState,
        requires_human_approval: bool = False,
    ) -> CheckpointRecord:
        """Create automatic checkpoint of current workflow state."""
        self._counter += 1
        cp_id = f"cp_{self.session_id}_{self._counter}"

        record = CheckpointRecord(
            checkpoint_id=cp_id,
            session_id=self.session_id,
            workflow_name=self.workflow_name,
            checkpoint_number=self._counter,
            active_node=node_id,
            state_payload=copy.deepcopy(dict(state)),
            requires_human_approval=requires_human_approval,
            approval_status="pending" if requires_human_approval else "approved",
        )
        self._checkpoints[cp_id] = record
        logger.info(
            "Created Checkpoint '%s' (number %d) at node '%s'.",
            cp_id,
            self._counter,
            node_id,
        )

        if requires_human_approval:
            raise HumanApprovalInterrupt(
                checkpoint_id=cp_id,
                reason=f"Human review flag triggered at node '{node_id}'.",
            )

        return record

    def resolve_human_approval(self, checkpoint_id: str, approve: bool) -> CheckpointRecord:
        """Resolve human approval interrupt (Approve or Reject)."""
        if checkpoint_id not in self._checkpoints:
            raise ValueError(f"Checkpoint '{checkpoint_id}' not found.")

        record = self._checkpoints[checkpoint_id]
        record.approval_status = "approved" if approve else "rejected"
        record.requires_human_approval = False

        logger.info(
            "Human approval for Checkpoint '%s' resolved -> %s",
            checkpoint_id,
            record.approval_status,
        )
        return record

    def get_latest_checkpoint(self) -> CheckpointRecord | None:
        """Fetch latest saved checkpoint for recovery."""
        if not self._checkpoints:
            return None
        latest_id = max(
            self._checkpoints.keys(), key=lambda k: self._checkpoints[k].checkpoint_number
        )
        return self._checkpoints[latest_id]

    def recover_state(self, checkpoint_id: str) -> AlphaMindAgentState:
        """Recover workflow state from specified checkpoint."""
        if checkpoint_id not in self._checkpoints:
            raise ValueError(f"Checkpoint '{checkpoint_id}' not found for recovery.")

        record = self._checkpoints[checkpoint_id]
        logger.warning("Recovered state from checkpoint '%s'.", checkpoint_id)
        return copy.deepcopy(record.state_payload)  # type: ignore[return-value]

    def list_checkpoints(self) -> list[CheckpointRecord]:
        """List all recorded checkpoints."""
        return sorted(self._checkpoints.values(), key=lambda c: c.checkpoint_number)
