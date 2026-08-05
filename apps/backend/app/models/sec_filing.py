"""
SEC Filings, News & Audit Trail ORM Models
"""

from __future__ import annotations

import uuid

from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from apps.backend.app.models.base import Base


class SECFilingModel(Base):
    """SEC Filing Document Table Model."""

    __tablename__ = "sec_filings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(String(20), nullable=False, index=True)
    form_type = Column(String(20), nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)


class NewsArticleModel(Base):
    """News Media Article Table Model."""

    __tablename__ = "news_articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    publisher = Column(String(100), nullable=False)
    url = Column(String(1000), nullable=False)
    sentiment_polarity = Column(Float, nullable=True)


class AuditLogModel(Base):
    """System Operations & LLM Spend Audit Trail Table Model."""

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event = Column(String(100), nullable=False, index=True)
    details = Column(Text, nullable=False)
