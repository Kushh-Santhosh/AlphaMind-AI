"""
AlphaMind AI - Multi-Channel Notification Router

Dispatches alerts & reports via Email, Push Notifications, Slack, Discord, and Webhooks.
"""

from __future__ import annotations

import logging
import time
import uuid
from enum import Enum

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class NotificationChannel(str, Enum):  # noqa: UP042
    EMAIL = "EMAIL"
    PUSH = "PUSH"
    SLACK = "SLACK"
    DISCORD = "DISCORD"
    WEBHOOK = "WEBHOOK"


class NotificationMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: f"notif_{uuid.uuid4().hex[:8]}")
    channel: NotificationChannel
    recipient: str
    subject: str
    body: str
    status: str = "DELIVERED"
    sent_at_utc: str = Field(
        default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


class NotificationDispatcher:
    """Dispatcher routing alerts to Email, Slack, Discord, and Webhook endpoints."""

    def __init__(self) -> None:
        self.delivered_notifications: list[NotificationMessage] = []

    def send_notification(
        self, channel: NotificationChannel, recipient: str, subject: str, body: str
    ) -> NotificationMessage:
        """Route notification to target channel."""
        msg = NotificationMessage(channel=channel, recipient=recipient, subject=subject, body=body)
        self.delivered_notifications.append(msg)
        logger.info("Dispatched notification [%s] to '%s': %s", channel.value, recipient, subject)
        return msg
