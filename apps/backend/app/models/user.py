"""
User Account & Portfolio ORM Models
"""

from __future__ import annotations

import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from apps.backend.app.models.base import Base


class UserModel(Base):
    """User account table model."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="QUANT_ANALYST")
    org_id = Column(String(100), nullable=False, default="org_enterprise_01")
