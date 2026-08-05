"""
Dedicated Risk Engine Interfaces
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class DedicatedRiskEngineInterface(Protocol):
    """Interface for VaR/CVaR calculations and AI Hallucination Verification."""

    async def compute_var_cvar(
        self, returns: list[float], confidence: float = 0.95
    ) -> dict[str, float]: ...

    async def verify_ai_hallucinations(
        self, generated_text: str, source_data: dict[str, Any]
    ) -> dict[str, Any]: ...
