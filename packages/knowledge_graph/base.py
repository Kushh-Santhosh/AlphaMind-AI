"""
Financial Knowledge Graph Interfaces
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class KnowledgeGraphEngineInterface(Protocol):
    """Interface for Neo4j / NetworkX Financial Knowledge Graph."""

    async def query_supply_chain(self, symbol: str) -> list[dict[str, Any]]: ...

    async def get_executive_network(self, executive_name: str) -> dict[str, Any]: ...
