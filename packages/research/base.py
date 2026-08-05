"""
Quantitative Research Library Interfaces
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class FactorModelInterface(Protocol):
    """Interface for CAPM and Fama-French factor models."""

    async def compute_factors(
        self, returns: list[float], benchmark_returns: list[float]
    ) -> dict[str, float]: ...


@runtime_checkable
class CointegrationInterface(Protocol):
    """Interface for statistical arbitrage and cointegration testing."""

    async def test_cointegration(
        self, series_a: list[float], series_b: list[float]
    ) -> dict[str, Any]: ...
