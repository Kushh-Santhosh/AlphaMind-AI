"""
AlphaMind AI - Research Engine Data Schemas

Normalized, structured Pydantic schemas for Company Profiles, Financial Statements, News,
Macro Indicators, Events, Documents, Entity Resolution, and Research Reports.
"""

from __future__ import annotations

import uuid

from pydantic import BaseModel, Field


class ExecutiveTeamMember(BaseModel):
    name: str
    title: str
    age: int | None = None
    since_year: int | None = None


class SubsidiarySchema(BaseModel):
    name: str
    jurisdiction: str
    ownership_pct: float = 100.0


class CorporateActionSchema(BaseModel):
    action_type: str  # "stock_split", "dividend", "spinoff", "buyback"
    execution_date: str
    description: str


class ShareStructureSchema(BaseModel):
    shares_outstanding: int
    float_shares: int
    institutional_ownership_pct: float
    insider_ownership_pct: float


class CompanyProfileSchema(BaseModel):
    """Normalized Company Research Profile Schema."""

    company_id: str = Field(default_factory=lambda: f"comp_{uuid.uuid4().hex[:8]}")
    symbol: str
    company_name: str
    business_summary: str
    sector: str
    industry: str
    market_cap_usd: float
    country: str = "US"
    exchange: str = "NASDAQ"
    ceo: str
    products: list[str] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)
    executives: list[ExecutiveTeamMember] = Field(default_factory=list)
    subsidiaries: list[SubsidiarySchema] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list)
    share_structure: ShareStructureSchema | None = None
    corporate_actions: list[CorporateActionSchema] = Field(default_factory=list)
