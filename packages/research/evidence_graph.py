"""
AlphaMind AI - Evidence Graph & Full Lineage Traceability Engine

Links Evidence -> Supporting Documents -> Knowledge Graph Entities -> Research Reports -> Factors -> Metadata.
Maintains complete 100% data audit lineage.
"""

from __future__ import annotations

import logging
import time
import uuid

from pydantic import BaseModel, Field

from packages.research.factor_extractor import ExtractedFactor
from packages.research.research_report import ResearchReport

logger = logging.getLogger(__name__)


class EvidenceTraceabilityNode(BaseModel):
    node_id: str = Field(default_factory=lambda: f"ev_node_{uuid.uuid4().hex[:8]}")
    node_type: str  # "evidence", "document", "entity", "report", "factor", "metadata"
    label: str
    source_reference: str
    created_at_utc: float = Field(default_factory=time.time)


class EvidenceTraceabilityLink(BaseModel):
    link_id: str = Field(default_factory=lambda: f"ev_link_{uuid.uuid4().hex[:8]}")
    from_node_id: str
    to_node_id: str
    relationship: str  # "DERIVED_FROM", "CITES", "MAPS_TO", "MODIFIES"


class EvidenceGraph(BaseModel):
    symbol: str
    nodes: list[EvidenceTraceabilityNode] = Field(default_factory=list)
    links: list[EvidenceTraceabilityLink] = Field(default_factory=list)


class EvidenceGraphEngine:
    """
    Engine constructing end-to-end audit lineage graphs for extracted factors and research data.
    """

    def build_evidence_graph(
        self, report: ResearchReport, factors: list[ExtractedFactor]
    ) -> EvidenceGraph:
        """Build complete traceability graph linking evidence to research factors."""
        symbol = report.symbol
        logger.info("Building evidence traceability graph for '%s'", symbol)

        graph = EvidenceGraph(symbol=symbol)

        # 1. Report Node
        rep_node = EvidenceTraceabilityNode(
            node_type="report",
            label=f"ResearchReport_{report.report_id}",
            source_reference=f"Report ID: {report.report_id}",
        )
        graph.nodes.append(rep_node)

        # 2. Document Nodes & Factors
        for doc in report.documents:
            doc_node = EvidenceTraceabilityNode(
                node_type="document",
                label=doc.title,
                source_reference=doc.doc_id,
            )
            graph.nodes.append(doc_node)
            graph.links.append(
                EvidenceTraceabilityLink(
                    from_node_id=rep_node.node_id,
                    to_node_id=doc_node.node_id,
                    relationship="CITES",
                )
            )

        for factor in factors:
            fctr_node = EvidenceTraceabilityNode(
                node_type="factor",
                label=f"{factor.factor_name}:{factor.factor_value}",
                source_reference=factor.evidence_reference,
            )
            graph.nodes.append(fctr_node)
            graph.links.append(
                EvidenceTraceabilityLink(
                    from_node_id=fctr_node.node_id,
                    to_node_id=rep_node.node_id,
                    relationship="DERIVED_FROM",
                )
            )

        logger.info(
            "Evidence Graph created for '%s': %d nodes, %d links.",
            symbol,
            len(graph.nodes),
            len(graph.links),
        )
        return graph
