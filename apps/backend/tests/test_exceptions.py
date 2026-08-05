"""
Backend Test Suite — Exception Hierarchy Tests
"""

from apps.backend.app.exceptions import (
    AgentExecutionException,
    DataProviderException,
    ForbiddenException,
    HallucinationVerificationException,
    PredictionSafetyViolationException,
    UnauthorizedException,
)


def test_data_provider_exception() -> None:
    exc = DataProviderException(provider="Polygon.io", asset="AAPL")
    assert exc.status_code == 503
    assert "AAPL" in exc.message


def test_agent_execution_exception() -> None:
    exc = AgentExecutionException(agent_id="PredictionAgent", reason="TFT timeout")
    assert exc.status_code == 500
    assert "PredictionAgent" in exc.message


def test_hallucination_exception() -> None:
    exc = HallucinationVerificationException(field="revenue", reported=30.04, source=30.10)
    assert exc.status_code == 422
    assert "revenue" in exc.message


def test_prediction_safety_violation() -> None:
    exc = PredictionSafetyViolationException()
    assert exc.status_code == 422
    assert "deterministic" in exc.message.lower()


def test_unauthorized_exception() -> None:
    exc = UnauthorizedException()
    assert exc.status_code == 401


def test_forbidden_exception() -> None:
    exc = ForbiddenException(role_required="Quant Analyst")
    assert exc.status_code == 403
    assert "Quant Analyst" in exc.message
