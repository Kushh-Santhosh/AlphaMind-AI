"""
Comprehensive Unit and Integration Tests for Production Database-Backed Auth System
"""

from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from apps.backend.app.core.auth import (
    UserRole,
    UserSession,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from apps.backend.app.db.postgres import get_db
from apps.backend.app.main import app
from apps.backend.app.middleware.rate_limit import reset_rate_limits

app.dependency_overrides[get_db] = lambda: None
client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_rate_limit_bucket():
    reset_rate_limits()


def test_password_hashing_and_verification():
    """Verify password hashing and verification."""
    pwd = "EnterprisePassword2026!"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_access_token_creation_and_decoding():
    """Verify JWT access token creation and decoding."""
    user = UserSession(
        user_id="usr_prod_01",
        email="prod_analyst@alphamind.ai",
        role=UserRole.ADMIN,
    )
    token = create_access_token(user)
    assert isinstance(token, str)

    decoded = decode_token(token)
    assert decoded["sub"] == "usr_prod_01"
    assert decoded["email"] == "prod_analyst@alphamind.ai"
    assert decoded["role"] == "ADMIN"
    assert decoded["type"] == "access"


def test_jwt_refresh_token_creation_and_decoding():
    """Verify JWT refresh token creation and decoding."""
    user = UserSession(
        user_id="usr_prod_02",
        email="quant_prod@alphamind.ai",
        role=UserRole.QUANT_ANALYST,
    )
    token = create_refresh_token(user)
    assert isinstance(token, str)

    decoded = decode_token(token)
    assert decoded["sub"] == "usr_prod_02"
    assert decoded["type"] == "refresh"


def test_expired_token_rejected():
    """Verify that an expired JWT token returns 401 Unauthorized."""
    user = UserSession(user_id="usr_exp_01", email="expired@alphamind.ai", role=UserRole.RESEARCHER)
    expired_token = create_access_token(user, expires_delta=timedelta(seconds=-10))

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401


def test_invalid_token_rejected():
    """Verify that a malformed JWT token returns 401 Unauthorized."""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid_malformed_jwt_token_xyz"},
    )
    assert response.status_code == 401


def test_multiple_users_register_and_login_flow():
    """Integration test: Register multiple unique users and verify separate logins."""
    users_data = [
        {"email": "user_alpha@alphamind.ai", "password": "PasswordAlpha123!"},
        {"email": "user_beta@alphamind.ai", "password": "PasswordBeta123!"},
    ]

    for u in users_data:
        # Register
        reg_resp = client.post("/api/v1/auth/register", json=u)
        assert reg_resp.status_code == 201
        data = reg_resp.json()
        assert data["user"]["email"] == u["email"]

        # Login
        log_resp = client.post("/api/v1/auth/login", json=u)
        assert log_resp.status_code == 200
        token = log_resp.json()["access_token"]

        # /me check
        me_resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_resp.status_code == 200
        assert me_resp.json()["email"] == u["email"]


def test_duplicate_user_registration_blocked():
    """Verify duplicate user registration returns 400 Bad Request."""
    email = "dup_test@alphamind.ai"
    payload = {"email": email, "password": "DupPassword123!"}

    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]


def test_token_refresh_flow():
    """Integration test: Refresh access token using valid refresh token."""
    user = UserSession(
        user_id="usr_ref_99", email="refresh_test@alphamind.ai", role=UserRole.RESEARCHER
    )
    refresh_tok = create_refresh_token(user)

    response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_tok})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
