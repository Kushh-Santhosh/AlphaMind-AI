# ADR-007: Neo4j for Financial Knowledge Graph

## Context
AlphaMind AI requires mapping complex non-linear relationships across companies, executives, products, competitors, supply chain dependencies, patents, lawsuits, and macroeconomic shocks.

## Decision
We decide to adopt **Neo4j** (supported by NetworkX in-memory Python utility) as the Knowledge Graph engine.

## Alternatives Considered
1. **Relational Foreign Key Joins**: Rejected due to query degradation and complex multi-join SQL queries when exploring multi-hop supply chain connections.
2. **Amazon Neptune**: Rejected due to AWS cloud vendor lock-in.

## Pros
- **Cypher Query Language**: Powerful declarative query syntax for multi-hop graph traversal (e.g. `MATCH (c:Company)-[:SUPPLIES_TO*1..3]->(...)`).
- **Graph Algorithms**: Built-in PageRank, Centrality, and Community Detection algorithms for financial network risk.
- **Visualizer Compatibility**: Native compatibility with 2D/3D WebGL graph rendering components in Next.js UI.

## Cons
- Requires dedicated graph schema index management.

## Consequences
All graph queries and node/edge schemas MUST be maintained in `packages/research/knowledge_graph.py` and documented in `docs/15_KNOWLEDGE_GRAPH.md`.
