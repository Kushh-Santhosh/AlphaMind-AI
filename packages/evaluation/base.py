"""
Continuous Evaluation Metric Interfaces
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class EvaluationEngineInterface(Protocol):
    """Interface for Brier score, MAE, RMSE, and Agent Success Rate evaluations."""

    async def compute_brier_score(
        self, forecast_probs: list[float], outcomes: list[int]
    ) -> float: ...

    async def compute_regression_metrics(
        self, y_true: list[float], y_pred: list[float]
    ) -> dict[str, float]: ...
