"""
ML & Probability Prediction Engine Interfaces
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class TimeSeriesPredictorInterface(Protocol):
    """Interface for time series ML models (TFT, LSTM, XGBoost)."""

    async def predict_distribution(
        self,
        features: dict[str, Any],
        horizon_days: int,
    ) -> dict[str, Any]: ...


@runtime_checkable
class MonteCarloEngineInterface(Protocol):
    """Interface for Monte Carlo simulation engine."""

    async def run_simulation(
        self,
        symbol: str,
        current_price: float,
        iterations: int = 10000,
        horizon_days: int = 30,
    ) -> dict[str, Any]: ...
