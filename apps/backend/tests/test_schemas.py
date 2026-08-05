"""
Backend Test Suite — Shared Schemas & PredictionSafetySchema Validation
"""

import pytest
from pydantic import ValidationError

from packages.shared.schemas import (
    ConfidenceIntervalSchema,
    PredictionSafetySchema,
    ProbabilityDistributionSchema,
)


def test_probability_distribution_schema_valid() -> None:
    """Valid probability distribution schema instantiation."""
    schema = ProbabilityDistributionSchema(
        bull_scenario_pct=25.0,
        base_scenario_pct=60.0,
        bear_scenario_pct=15.0,
    )
    assert schema.bull_scenario_pct == 25.0


def test_prediction_safety_schema_valid() -> None:
    """Valid PredictionSafetySchema should instantiate correctly."""
    schema = PredictionSafetySchema(
        asset="AAPL",
        prediction_horizon_days=30,
        probability_distribution=ProbabilityDistributionSchema(
            bull_scenario_pct=25.0,
            base_scenario_pct=60.0,
            bear_scenario_pct=15.0,
        ),
        confidence_interval_95=ConfidenceIntervalSchema(
            lower_bound_pct=-5.0,
            expected_return_pct=4.5,
            upper_bound_pct=12.0,
        ),
        model_confidence_score=0.82,
        data_quality_score=0.94,
        prediction_expiry_timestamp="2026-09-04T18:30:00Z",
        supporting_evidence=["Strong Q2 revenue", "Margin expansion"],
        contradicting_evidence=["Antitrust risk"],
        known_unknowns=["DOJ verdict pending"],
        historical_model_accuracy_brier_score=0.14,
    )
    assert schema.asset == "AAPL"
    assert "informational" in schema.disclaimer.lower()


def test_prediction_safety_schema_missing_field() -> None:
    """Missing required field must raise Pydantic ValidationError."""
    with pytest.raises(ValidationError):
        PredictionSafetySchema(  # type: ignore[call-arg]
            asset="AAPL",
            # prediction_horizon_days omitted intentionally
        )
