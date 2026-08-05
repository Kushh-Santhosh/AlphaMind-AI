"""
Shared Pydantic Schemas & Global Constants
"""

from pydantic import BaseModel, Field


class ProbabilityDistributionSchema(BaseModel):
    bull_scenario_pct: float = Field(..., description="Bull scenario percentage probability")
    base_scenario_pct: float = Field(..., description="Base scenario percentage probability")
    bear_scenario_pct: float = Field(..., description="Bear scenario percentage probability")


class ConfidenceIntervalSchema(BaseModel):
    lower_bound_pct: float
    expected_return_pct: float
    upper_bound_pct: float


class PredictionSafetySchema(BaseModel):
    asset: str
    prediction_horizon_days: int
    probability_distribution: ProbabilityDistributionSchema
    confidence_interval_95: ConfidenceIntervalSchema
    model_confidence_score: float
    data_quality_score: float
    prediction_expiry_timestamp: str
    supporting_evidence: list[str]
    contradicting_evidence: list[str]
    known_unknowns: list[str]
    historical_model_accuracy_brier_score: float
    disclaimer: str = (
        "DISCLAIMER: For informational and educational research purposes only. "
        "Does not constitute financial or investment advice."
    )
