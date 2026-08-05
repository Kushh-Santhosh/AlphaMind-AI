"""
AlphaMind AI - Typed State Management, Versioning, Snapshots, Rollback & Diff Engine

Enforces immutable state updates, version tracking, state diff computation,
checkpoint snapshots, and rollback functionality.
"""

from __future__ import annotations

import copy
import logging
import time
from typing import Any

from pydantic import BaseModel, Field

from packages.agents.state import AlphaMindAgentState

logger = logging.getLogger(__name__)


class StateSnapshot(BaseModel):
    """Immutable state snapshot wrapper with version number and timestamp."""

    version: int
    timestamp: float = Field(default_factory=time.time)
    mutated_by_node: str
    state_payload: dict[str, Any]


class StateDiff(BaseModel):
    """Diff summary between two state versions."""

    from_version: int
    to_version: int
    added_keys: list[str] = Field(default_factory=list)
    modified_keys: list[str] = Field(default_factory=list)
    removed_keys: list[str] = Field(default_factory=list)


class StateManager:
    """
    Manager governing state versioning, immutable mutations, snapshots, diff tracking, and rollback.
    """

    def __init__(self, initial_state: AlphaMindAgentState) -> None:
        self._current_version = 1
        self._snapshots: dict[int, StateSnapshot] = {}
        self._audit_history: list[dict[str, Any]] = []

        # Record initial version 1 snapshot
        snap = StateSnapshot(
            version=1,
            mutated_by_node="initialization",
            state_payload=copy.deepcopy(dict(initial_state)),
        )
        self._snapshots[1] = snap
        self._audit_history.append(
            {"version": 1, "node": "initialization", "timestamp": snap.timestamp}
        )

    def get_current_state(self) -> AlphaMindAgentState:
        """Get deep copy of current state version payload."""
        payload = self._snapshots[self._current_version].state_payload
        return copy.deepcopy(payload)  # type: ignore[return-value]

    def get_version(self) -> int:
        """Get current state version number."""
        return self._current_version

    def update_state(self, mutating_node: str, updates: dict[str, Any]) -> AlphaMindAgentState:
        """
        Immutably apply state updates, creating next version snapshot.
        Original state snapshot remains untouched.
        """
        current_payload = dict(self.get_current_state())

        # Immutably merge updates
        new_payload = copy.deepcopy(current_payload)
        new_payload.update(updates)

        self._current_version += 1
        new_snap = StateSnapshot(
            version=self._current_version,
            mutated_by_node=mutating_node,
            state_payload=new_payload,
        )
        self._snapshots[self._current_version] = new_snap
        self._audit_history.append(
            {
                "version": self._current_version,
                "node": mutating_node,
                "timestamp": new_snap.timestamp,
            }
        )

        logger.info(
            "State updated by '%s' -> Version %d created.",
            mutating_node,
            self._current_version,
        )
        return copy.deepcopy(new_payload)  # type: ignore[return-value]

    def rollback(self, target_version: int) -> AlphaMindAgentState:
        """
        Rollback current active state to target_version snapshot.
        Raises ValueError if version does not exist.
        """
        if target_version not in self._snapshots:
            raise ValueError(f"State version {target_version} does not exist.")

        self._current_version = target_version
        logger.warning("Rolled back state to version %d.", target_version)
        return self.get_current_state()

    def compute_diff(self, from_version: int, to_version: int) -> StateDiff:
        """Compute key-level diff between two state versions."""
        if from_version not in self._snapshots or to_version not in self._snapshots:
            raise ValueError("Invalid state version numbers for diff calculation.")

        v_from = self._snapshots[from_version].state_payload
        v_to = self._snapshots[to_version].state_payload

        from_keys = set(v_from.keys())
        to_keys = set(v_to.keys())

        added = list(to_keys - from_keys)
        removed = list(from_keys - to_keys)
        modified = [k for k in (from_keys & to_keys) if v_from[k] != v_to[k]]

        return StateDiff(
            from_version=from_version,
            to_version=to_version,
            added_keys=added,
            modified_keys=modified,
            removed_keys=removed,
        )

    def get_audit_history(self) -> list[dict[str, Any]]:
        """Fetch audit log history of all state version mutations."""
        return list(self._audit_history)
