"""
AlphaMind AI - Portfolio Optimization Infrastructure Protocols

Defines Protocol interfaces for Mean-Variance (MVO), Black-Litterman, Risk Parity,
Minimum Variance, Hierarchical Risk Parity (HRP), Maximum Diversification, and Equal Weight.
STRICT RULE: Infrastructure contracts ONLY — zero optimization advice or rebalancing signals.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, Field


class OptimizationConstraint(BaseModel):
    min_weight: float = 0.0
    max_weight: float = 0.25  # Max 25% single asset allocation
    max_sector_weight: float = 0.40  # Max 40% sector allocation


class OptimizationResult(BaseModel):
    model_name: str
    target_weights: dict[str, float] = Field(default_factory=dict)
    expected_return_annual: float = 0.08
    expected_volatility_annual: float = 0.14
    sharpe_ratio: float = 1.60
    lineage: str = ""


@runtime_checkable
class MeanVarianceOptimizerProtocol(Protocol):
    async def optimize_mvo(
        self, symbols: list[str], covariance_matrix: dict[str, dict[str, float]]
    ) -> OptimizationResult: ...


@runtime_checkable
class BlackLittermanOptimizerProtocol(Protocol):
    async def optimize_black_litterman(
        self,
        symbols: list[str],
        market_caps: dict[str, float],
        investor_views: list[dict[str, Any]],
    ) -> OptimizationResult: ...


@runtime_checkable
class RiskParityOptimizerProtocol(Protocol):
    async def optimize_risk_parity(
        self, symbols: list[str], covariance_matrix: dict[str, dict[str, float]]
    ) -> OptimizationResult: ...


@runtime_checkable
class HierarchicalRiskParityProtocol(Protocol):
    async def optimize_hrp(
        self, symbols: list[str], price_history: dict[str, list[float]]
    ) -> OptimizationResult: ...


class OptimizationModelRegistry:
    """Registry listing supported portfolio optimization algorithms."""

    def list_supported_models(self) -> list[dict[str, str]]:
        return [
            {"model_id": "mvo", "name": "Mean-Variance Optimization (Markowitz)"},
            {"model_id": "black_litterman", "name": "Black-Litterman Asset Allocation"},
            {"model_id": "risk_parity", "name": "Equal Risk Contribution (Risk Parity)"},
            {"model_id": "min_var", "name": "Minimum Variance Optimization"},
            {"model_id": "hrp", "name": "Hierarchical Risk Parity (De Prado)"},
            {"model_id": "max_div", "name": "Maximum Diversification Portfolio"},
            {"model_id": "equal_weight", "name": "Equal Weight 1/N Portfolio"},
        ]
