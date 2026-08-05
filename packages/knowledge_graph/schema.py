"""
AlphaMind AI - Financial Knowledge Graph Schema Definitions

Defines 21 Graph Entity Types and 12 Typed Relationship Types for semantic financial modeling.
"""

from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class GraphEntityType(str, Enum):  # noqa: UP042
    COMPANY = "Company"
    TICKER = "Ticker"
    EXECUTIVE = "Executive"
    BOARD_MEMBER = "BoardMember"
    INVESTOR = "Investor"
    SUBSIDIARY = "Subsidiary"
    INDUSTRY = "Industry"
    SECTOR = "Sector"
    COUNTRY = "Country"
    EXCHANGE = "Exchange"
    COMMODITY = "Commodity"
    CURRENCY = "Currency"
    ECONOMIC_INDICATOR = "EconomicIndicator"
    ECONOMIC_EVENT = "EconomicEvent"
    PRODUCT = "Product"
    PATENT = "Patent"
    TECHNOLOGY = "Technology"
    NEWS_ARTICLE = "NewsArticle"
    SEC_FILING = "SECFiling"
    RESEARCH_REPORT = "ResearchReport"
    CORPORATE_ACTION = "CorporateAction"


class GraphRelationType(str, Enum):  # noqa: UP042
    OWNS = "OWNS"
    SUPPLIES = "SUPPLIES"
    COMPETES_WITH = "COMPETES_WITH"
    BELONGS_TO = "BELONGS_TO"
    LOCATED_IN = "LOCATED_IN"
    USES = "USES"
    AFFECTS = "AFFECTS"
    MENTIONS = "MENTIONS"
    REPORTS = "REPORTS"
    FILES = "FILES"
    MANUFACTURES = "MANUFACTURES"
    INVESTS_IN = "INVESTS_IN"


class GraphNode(BaseModel):
    """Knowledge Graph Node entity model."""

    node_id: str = Field(default_factory=lambda: f"node_{uuid.uuid4().hex[:8]}")
    entity_type: GraphEntityType
    label: str
    properties: dict[str, Any] = Field(default_factory=dict)
    created_at_utc: float = Field(default_factory=time.time)


class GraphEdge(BaseModel):
    """Knowledge Graph Directed Edge relationship model."""

    edge_id: str = Field(default_factory=lambda: f"edge_{uuid.uuid4().hex[:8]}")
    source_node_id: str
    target_node_id: str
    relation_type: GraphRelationType
    weight: float = 1.0
    properties: dict[str, Any] = Field(default_factory=dict)
    created_at_utc: float = Field(default_factory=time.time)
