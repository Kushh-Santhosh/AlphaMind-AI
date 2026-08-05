"""
Portfolio Optimization & Paper Trading Engine Interfaces
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class PortfolioOptimizerInterface(Protocol):
    """Interface for Mean-Variance, Black-Litterman, HRP solvers."""

    async def optimize(
        self,
        symbols: list[str],
        returns_history: dict[str, list[float]],
        method: str = "black_litterman",
    ) -> dict[str, float]: ...


@runtime_checkable
class PaperTraderInterface(Protocol):
    """Interface for simulated paper trade execution."""

    async def execute_simulated_trade(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
    ) -> dict[str, Any]: ...
