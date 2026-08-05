# ADR-004: LangGraph for Multi-Agent Orchestration

## Context
AlphaMind AI requires orchestrating 11 specialized autonomous AI agents (Market Research, Company Research, SEC, News, Technical, Fundamental, Macro, Risk, Prediction, Portfolio, Report Generator). The agent framework must support cyclical execution loops, state persistence, conditional branch routing, and strict state-driven communication.

## Decision
We decide to adopt **LangGraph** (built on LangChain) as the multi-agent graph orchestration engine.

## Alternatives Considered
1. **AutoGen (Microsoft)**: Rejected due to unstructured conversational agent loops, lack of strict graph state typing, and difficulty in enforcing zero-direct-agent-call rules.
2. **CrewAI**: Rejected due to high abstraction limits that hinder granular control over state mutations and custom circuit breaker error recovery.
3. **Custom Async State Machine**: Rejected due to reinvention of persistence, checkpointing, and graph visualization primitives.

## Pros
- **State-Driven Directed Graphs**: Enforces strict `Shared LangGraph State` transitions and isolated node execution.
- **Built-in Checkpointing & Persistence**: Allows pausing, resuming, and auditing multi-agent research runs.
- **Supervisor Pattern Native Support**: Clean isolation between Supervisor Agent controller and execution worker nodes.

## Cons
- Requires disciplined schema design for the `TypedDict` / Pydantic state object.

## Consequences
All multi-agent definitions and graphs MUST reside in `packages/agents/` and adhere strictly to state-driven isolation rules.
