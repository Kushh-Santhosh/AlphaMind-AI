"""
AlphaMind AI - Configurable Scoring Framework Interfaces

Defines abstract Protocol contracts for scoring pipelines:
GrowthScore, FinancialHealthScore, RiskScore, QualityScore, InnovationScore, MarketPositionScore.
STRICT RULE: Infrastructure interfaces ONLY — zero investment ratings or buy/sell advice.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, Field


class ScoreResult(BaseModel):
    score_id: str
    score_type: (
        str  # "growth", "financial_health", "risk", "quality", "innovation", "market_position"
    )
    normalized_score: float  # Bounded 0.0 to 100.0
    confidence: float
    factors_used: list[str] = Field(default_factory=list)
    lineage: str = ""


@runtime_checkable
class GrowthScoreProtocol(Protocol):
    async def compute_growth_score(self, symbol: str, data: dict[str, Any]) -> ScoreResult: ...


@runtime_checkable
class FinancialHealthScoreProtocol(Protocol):
    async def compute_health_score(self, symbol: str, data: dict[str, Any]) -> ScoreResult: ...


@runtime_checkable
class RiskScoreProtocol(Protocol):
    async def compute_risk_score(self, symbol: str, data: dict[str, Any]) -> ScoreResult: ...


@runtime_checkable
class QualityScoreProtocol(Protocol):
    async def compute_quality_score(self, symbol: str, data: dict[str, Any]) -> ScoreResult: ...


@runtime_checkable
class InnovationScoreProtocol(Protocol):
    async def compute_innovation_score(self, symbol: str, data: dict[str, Any]) -> ScoreResult: ...


@runtime_checkable
class MarketPositionScoreProtocol(Protocol):
    async def compute_position_score(self, symbol: str, data: dict[str, Any]) -> ScoreResult: ...
