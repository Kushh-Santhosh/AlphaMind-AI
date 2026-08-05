"""
Unit and Integration Tests for SEC-02 Rate Limiting Middleware
"""

import pytest
from fastapi.testclient import TestClient

from apps.backend.app.main import app
from apps.backend.app.middleware.rate_limit import reset_rate_limits

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_rate_limit_bucket():
    reset_rate_limits()


def test_rate_limiting_headers_on_successful_request():
    """Verify rate limiting headers are returned on valid API requests."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert "X-RateLimit-Reset" in response.headers


def test_auth_rate_limiting_policy_enforcement():
    """Verify rate limiting enforcement on authentication endpoints (10 req/min limit)."""
    # Send requests to consume auth limit
    for _ in range(12):
        res = client.post(
            "/api/v1/auth/login",
            json={"email": "analyst@alphamind.ai", "password": "WrongPassword"},
        )
    # The last request should be rate limited with HTTP 429
    assert res.status_code == 429
    data = res.json()
    assert data["policy"] == "auth"
    assert "Retry-After" in res.headers


def test_heavy_ai_rate_limiting_policy_enforcement():
    """Verify rate limiting enforcement on heavy AI endpoints (5 req/min limit)."""
    for _ in range(7):
        res = client.get("/api/v1/reasoning/rec_01")
    assert res.status_code == 429
    data = res.json()
    assert data["policy"] == "heavy_ai"
    assert "Retry-After" in res.headers
