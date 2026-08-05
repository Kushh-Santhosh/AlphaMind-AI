"""
AlphaMind AI - Entity Resolution & Alias Resolver Engine

Normalizes Company Tickers, Executive Names, Exchanges, Countries, Industries,
Sectors, Products, and Subsidiaries. Resolves aliases and prevents duplicate entities.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class CanonicalEntity(BaseModel):
    entity_id: str
    entity_type: str  # "company", "ticker", "executive", "exchange", "country", "product"
    canonical_name: str
    symbol: str | None = None
    aliases: list[str] = Field(default_factory=list)


class EntityResolver:
    """
    Entity Resolution Engine converting messy text aliases into canonical Entity IDs.
    """

    def __init__(self) -> None:
        self._alias_map: dict[str, str] = {
            "AAPL": "ent_company_aapl",
            "APPLE": "ent_company_aapl",
            "APPLE INC": "ent_company_aapl",
            "APPLE COMPUTER": "ent_company_aapl",
            "AAPL US": "ent_company_aapl",
            "NVDA": "ent_company_nvda",
            "NVIDIA": "ent_company_nvda",
            "NVIDIA CORP": "ent_company_nvda",
            "MSFT": "ent_company_msft",
            "MICROSOFT": "ent_company_msft",
        }

        self._canonical_store: dict[str, CanonicalEntity] = {
            "ent_company_aapl": CanonicalEntity(
                entity_id="ent_company_aapl",
                entity_type="company",
                canonical_name="Apple Inc.",
                symbol="AAPL",
                aliases=["AAPL", "APPLE", "APPLE INC", "APPLE COMPUTER", "AAPL US"],
            ),
            "ent_company_nvda": CanonicalEntity(
                entity_id="ent_company_nvda",
                entity_type="company",
                canonical_name="NVIDIA Corporation",
                symbol="NVDA",
                aliases=["NVDA", "NVIDIA", "NVIDIA CORP"],
            ),
            "ent_company_msft": CanonicalEntity(
                entity_id="ent_company_msft",
                entity_type="company",
                canonical_name="Microsoft Corporation",
                symbol="MSFT",
                aliases=["MSFT", "MICROSOFT"],
            ),
        }

    def resolve_entity(self, input_string: str) -> CanonicalEntity | None:
        """Resolve arbitrary company string/alias to canonical entity record."""
        clean_key = input_string.strip().upper()
        entity_id = self._alias_map.get(clean_key)

        if entity_id and entity_id in self._canonical_store:
            logger.info("Resolved entity alias '%s' -> Canonical ID '%s'", input_string, entity_id)
            return self._canonical_store[entity_id]

        logger.warning(
            "Unresolved entity string '%s'. Registering new dynamic entity.", input_string
        )
        new_id = f"ent_dyn_{clean_key}"
        dyn_entity = CanonicalEntity(
            entity_id=new_id,
            entity_type="company",
            canonical_name=clean_key,
            symbol=clean_key,
            aliases=[clean_key],
        )
        self._alias_map[clean_key] = new_id
        self._canonical_store[new_id] = dyn_entity
        return dyn_entity
