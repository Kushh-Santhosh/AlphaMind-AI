"""
AlphaMind AI - Knowledge Graph Ingestion & Incremental Merge Engine

Converts Company Profiles, Financial Statements, News Articles, Events, Documents,
and Research Reports into Graph Nodes & Edges.
Includes duplicate detection and incremental graph merges.
"""

from __future__ import annotations

import logging
from typing import Any

from packages.knowledge_graph.schema import (
    GraphEdge,
    GraphEntityType,
    GraphNode,
    GraphRelationType,
)
from packages.research.research_report import ResearchReport

logger = logging.getLogger(__name__)


class GraphIngestionEngine:
    """
    Ingestion engine mapping research artifacts to Knowledge Graph nodes and edges.
    Enforces uniqueness and duplicate prevention.
    """

    def __init__(self) -> None:
        self.nodes: dict[str, GraphNode] = {}
        self.edges: dict[tuple[str, str, str], GraphEdge] = {}  # (src, target, relation)

    def add_node(
        self, entity_type: GraphEntityType, label: str, properties: dict[str, Any]
    ) -> GraphNode:
        """Add or merge node into graph without duplicates."""
        node_key = f"{entity_type.value}:{label.upper()}"
        if node_key in self.nodes:
            # Update properties incrementally
            self.nodes[node_key].properties.update(properties)
            return self.nodes[node_key]

        node = GraphNode(
            node_id=node_key,
            entity_type=entity_type,
            label=label,
            properties=properties,
        )
        self.nodes[node_key] = node
        return node

    def add_edge(
        self,
        source_node_id: str,
        target_node_id: str,
        relation_type: GraphRelationType,
        weight: float = 1.0,
        properties: dict[str, Any] | None = None,
    ) -> GraphEdge:
        """Add or update edge in graph without duplicates."""
        edge_key = (source_node_id, target_node_id, relation_type.value)
        if edge_key in self.edges:
            self.edges[edge_key].weight = max(self.edges[edge_key].weight, weight)
            return self.edges[edge_key]

        edge = GraphEdge(
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            relation_type=relation_type,
            weight=weight,
            properties=properties or {},
        )
        self.edges[edge_key] = edge
        return edge

    def ingest_research_report(self, report: ResearchReport) -> tuple[int, int]:
        """Ingest complete unified ResearchReport into graph nodes and relationships."""
        symbol = report.symbol
        co = report.company_profile

        # 1. Company & Ticker Nodes
        comp_node = self.add_node(
            GraphEntityType.COMPANY, co.company_name, {"market_cap": co.market_cap_usd}
        )
        ticker_node = self.add_node(GraphEntityType.TICKER, symbol, {"exchange": co.exchange})
        self.add_edge(comp_node.node_id, ticker_node.node_id, GraphRelationType.REPORTS)

        # 2. Sector & Industry Nodes
        sec_node = self.add_node(GraphEntityType.SECTOR, co.sector, {})
        ind_node = self.add_node(GraphEntityType.INDUSTRY, co.industry, {})
        self.add_edge(comp_node.node_id, ind_node.node_id, GraphRelationType.BELONGS_TO)
        self.add_edge(ind_node.node_id, sec_node.node_id, GraphRelationType.BELONGS_TO)

        # 3. Executives
        for exec_mem in co.executives:
            exec_node = self.add_node(
                GraphEntityType.EXECUTIVE, exec_mem.name, {"title": exec_mem.title}
            )
            self.add_edge(exec_node.node_id, comp_node.node_id, GraphRelationType.BELONGS_TO)

        # 4. News Articles
        for article in report.news_articles:
            news_node = self.add_node(
                GraphEntityType.NEWS_ARTICLE, article.title, {"url": article.url}
            )
            self.add_edge(news_node.node_id, comp_node.node_id, GraphRelationType.MENTIONS)

        logger.info(
            "Graph ingestion complete for '%s': %d nodes, %d edges.",
            symbol,
            len(self.nodes),
            len(self.edges),
        )
        return len(self.nodes), len(self.edges)
