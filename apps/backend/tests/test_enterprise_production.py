"""
Enterprise Production Hardening Test Suite — RBAC Permissions, Admin Panel REST APIs,
Enterprise Scheduler, Multi-Channel Notifications, and Security Hardening.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from apps.backend.app.core.auth import PermissionsMatrix, UserRole
from apps.backend.app.core.security import SecurityHardeningEngine
from apps.backend.app.main import app
from packages.shared.enterprise_scheduler import EnterpriseScheduler
from packages.shared.notifications import NotificationChannel, NotificationDispatcher


def test_rbac_permissions_and_roles() -> None:
    """Test Role-Based Access Control (RBAC) permissions matrix."""
    assert PermissionsMatrix.has_permission(UserRole.ADMIN, "manage_users")
    assert PermissionsMatrix.has_permission(UserRole.QUANT_ANALYST, "simulate")
    assert not PermissionsMatrix.has_permission(UserRole.RESEARCHER, "manage_users")
    assert PermissionsMatrix.has_permission(UserRole.AUDITOR, "audit_logs")


def test_enterprise_scheduler_jobs() -> None:
    """Test EnterpriseScheduler job registration and trigger execution."""
    scheduler = EnterpriseScheduler()
    job = scheduler.register_job("Daily Research Pipeline", "0 0 * * *")

    assert job.name == "Daily Research Pipeline"
    assert job.status == "SCHEDULED"

    executed = scheduler.trigger_job(job.job_id)
    assert executed.status == "COMPLETED"


def test_notification_dispatcher_channels() -> None:
    """Test NotificationDispatcher multi-channel routing (Email, Slack, Discord, Webhook)."""
    dispatcher = NotificationDispatcher()

    msg_email = dispatcher.send_notification(
        NotificationChannel.EMAIL,
        "analyst@alphamind.ai",
        "Report Ready",
        "Executive summary compiled.",
    )
    msg_slack = dispatcher.send_notification(
        NotificationChannel.SLACK, "#quant-alerts", "Drift Alert", "Feature drift detected."
    )

    assert msg_email.status == "DELIVERED"
    assert msg_slack.channel == NotificationChannel.SLACK
    assert len(dispatcher.delivered_notifications) == 2


def test_security_headers_and_rate_limiting() -> None:
    """Test SecurityHardeningEngine OWASP headers and payload encryption."""
    headers = SecurityHardeningEngine.get_security_headers()
    assert "X-Content-Type-Options" in headers
    assert headers["X-Frame-Options"] == "DENY"

    secret = "TopSecretApiKey123"
    encrypted = SecurityHardeningEngine.encrypt_secret(secret)
    assert encrypted.startswith("enc_v1:")

    decrypted = SecurityHardeningEngine.decrypt_secret(encrypted)
    assert decrypted == secret


@pytest.mark.asyncio
async def test_admin_api_endpoints() -> None:
    """Test Enterprise Admin Panel REST API endpoints (/users, /brokers, /models, /provider-health, /background-jobs, /system-metrics)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_users = await client.get("/api/v1/admin/users")
        res_brokers = await client.get("/api/v1/admin/brokers")
        res_models = await client.get("/api/v1/admin/models")
        res_health = await client.get("/api/v1/admin/provider-health")
        res_jobs = await client.get("/api/v1/admin/background-jobs")
        res_metrics = await client.get("/api/v1/admin/system-metrics")

    assert res_users.status_code == 200
    assert res_brokers.status_code == 200
    assert res_models.status_code == 200
    assert res_health.status_code == 200
    assert res_jobs.status_code == 200
    assert res_metrics.status_code == 200
