"""
AlphaMind AI - Custom Exception Definitions.

Note: Exception names use 'Exception' suffix (not 'Error') to distinguish
domain-level checked conditions from programming errors per AlphaMind convention.
"""  # noqa: N818


class AlphaMindBaseException(Exception):  # noqa: N818
    """Base exception class for all AlphaMind AI domain errors."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DataProviderException(AlphaMindBaseException):  # noqa: N818
    """Raised when all data provider tiers fail (Primary, Secondary, Fallback)."""

    def __init__(self, provider: str, asset: str) -> None:
        super().__init__(
            f"All provider tiers exhausted for asset '{asset}' via '{provider}'.",
            status_code=503,
        )


class AgentExecutionException(AlphaMindBaseException):  # noqa: N818
    """Raised when a LangGraph agent node fails and circuit breaker trips."""

    def __init__(self, agent_id: str, reason: str) -> None:
        super().__init__(
            f"Agent '{agent_id}' failed execution. Circuit breaker active. Reason: {reason}",
            status_code=500,
        )


class HallucinationVerificationException(AlphaMindBaseException):  # noqa: N818
    """Raised when AI Hallucination Verifier detects numerical discrepancy > 0.01%."""

    def __init__(self, field: str, reported: float, source: float) -> None:
        super().__init__(
            f"Hallucination detected in field '{field}': reported={reported}, source={source}.",
            status_code=422,
        )


class PredictionSafetyViolationException(AlphaMindBaseException):  # noqa: N818
    """Raised when a prediction function attempts to return a deterministic target price."""

    def __init__(self) -> None:
        super().__init__(
            "Prediction Safety Violation: deterministic single-point target price not permitted.",
            status_code=422,
        )


class UnauthorizedException(AlphaMindBaseException):  # noqa: N818
    """Raised when JWT authentication fails."""

    def __init__(self) -> None:
        super().__init__("Unauthorized. Invalid or expired JWT token.", status_code=401)


class ForbiddenException(AlphaMindBaseException):  # noqa: N818
    """Raised when RBAC check denies access."""

    def __init__(self, role_required: str) -> None:
        super().__init__(
            f"Forbidden. Required role: '{role_required}'.",
            status_code=403,
        )
