"""
AlphaMind AI - Data & LLM Provider Observability API Router
Exposes live health of market data vendors and multi-provider LLM gateways.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from packages.agents.models.llm_gateway import LLMGateway
from packages.market.provider_registry import DataProviderRegistry

router = APIRouter(prefix="/api/v1/providers", tags=["Providers & LLMs"])
_data_registry = DataProviderRegistry()
_llm_gateway = LLMGateway()


@router.get("/status")
async def get_providers_status() -> dict[str, Any]:
    """Retrieve health and configuration status of all connected data providers and LLM gateways."""
    data_health = _data_registry.get_providers_health()
    llm_providers = _llm_gateway.get_supported_providers()
    llm_telemetry = _llm_gateway.get_telemetry_summary()

    return {
        "data_providers": data_health,
        "llm_gateways": {
            "supported_providers": llm_providers,
            "telemetry": llm_telemetry,
        },
    }
