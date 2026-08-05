# Document 03: System Architecture Blueprint

## Purpose
This document provides the definitive architectural blueprint for **AlphaMind AI**, detailing the modular monorepo structure, service interaction topology, data pipeline flows, and component responsibilities across all 13 core expanded modules.

## Responsibilities
- Specify Clean Architecture layer boundaries between presentation, backend API, multi-agent orchestrator, quantitative engines, and data stores.
- Define communication protocols (REST, WebSockets, Server-Sent Events SSE, gRPC/Internal Async calls).
- Detail fault tolerance, multi-provider failover, and zero-trust security controls.

## Master System Topology Diagram

```mermaid
graph TD
    subgraph Client Presentation Layer (Next.js 14)
        WebUI[Next.js App Router]
        TVChart[TradingView Lightweight Charts]
        Dashboards[13 Specialized UI Dashboards]
        StateStore[Zustand & TanStack React Query]
        WebUI --> TVChart & Dashboards & StateStore
    end

    subgraph Security & API Gateway Layer (FastAPI)
        Gateway[FastAPI Reverse Proxy & Gateway]
        JWTAuth[JWT & RBAC Middleware]
        RateLimiter[Redis Token Bucket Rate Limiter]
        Disclaimer[Financial Research Disclaimer Middleware]
        Gateway --> JWTAuth --> RateLimiter --> Disclaimer
    end

    subgraph LangGraph Multi-Agent Orchestration Layer
        Supervisor[Supervisor Agent Node]
        StateGraph[Shared LangGraph State Object]
        Agents[11 Autonomous Research & Execution Agents]
        CircuitBreaker[Agent Circuit Breakers & Failover Handlers]
        Supervisor <--> StateGraph <--> Agents <--> CircuitBreaker
    end

    subgraph Quantitative & Machine Learning Engines
        QuantEngine[Quantitative Analytics Engine\nCAPM, Fama-French, Cointegration, Risk]
        MLEngine[ML Prediction Engine\nTFT, XGBoost, CatBoost, Monte Carlo]
        XAIEngine[Explainable AI Engine\nSHAP, Evidence Matrix, Reasoning]
        ModelRegistry[Multi-LLM Model Registry\nOpenAI, Claude, Gemini, DeepSeek, Ollama]
    end

    subgraph Data Stores & Persistence Layer
        Timescale[(PostgreSQL 16 + TimescaleDB)]
        Chroma[(ChromaDB Vector Store)]
        Neo4j[(Neo4j Financial Knowledge Graph)]
        RedisCache[(Redis Cache & Message Broker)]
    end

    WebUI <-->|HTTP/2 JSON & SSE & WS| Gateway
    Gateway <--> Supervisor
    Agents <--> QuantEngine & MLEngine & XAIEngine & ModelRegistry
    QuantEngine & MLEngine & DataEngine <--> Timescale & Chroma & Neo4j & RedisCache
```

## 13 Core Expanded Architectural Modules

### 1. Market Data Engine
- Pluggable provider architecture with 3-tier redundancy (`Polygon.io` primary $\rightarrow$ `Alpha Vantage` secondary $\rightarrow$ `yfinance` fallback).
- Multi-asset support: Stocks, ETFs, Futures, Options, Forex, Crypto, Bonds, Commodities, Global Indices.

### 2. 9-Stage Ingestion Data Pipeline
`Raw Data` $\rightarrow$ `Cleaning` $\rightarrow$ `Normalization` $\rightarrow$ `Feature Engineering` $\rightarrow$ `Storage` $\rightarrow$ `Vector Index` $\rightarrow$ `AI Agents` $\rightarrow$ `Prediction Engine` $\rightarrow$ `Report Generator`.

### 3. Quantitative Analytics Engine
- Factor Models: Single-index CAPM, Fama-French 3 & 5 Factor Models, Carhart 4-Factor.
- Statistical Arbitrage: Cointegration testing (Engle-Granger, Johansen), Hurst Exponent, Mean Reversion, Pairs Trading.
- Institutional Risk: VaR (95/99), CVaR, Sharpe, Sortino, Treynor, Calmar, MaxDD, Beta.

### 4. ML Prediction Engine
- Time Series Deep Learning: Temporal Fusion Transformers (TFT), Bi-LSTM.
- Gradient Boosting: XGBoost, CatBoost, LightGBM.
- Probabilistic Engine: Bayesian Posterior Probability, 10,000-run Monte Carlo simulations with Student's t heavy-tailed distributions, Prediction Calibration diagrams.

### 5. Financial Knowledge Graph
- 15 node types (`Company`, `Executive`, `Product`, `Competitor`, `Industry`, `Country`, `Investor`, `Subsidiary`, `Patent`, `Lawsuit`, `SupplyChainNode`, `NewsArticle`, `MacroEvent`, `Commodity`, `Currency`) with Neo4j and NetworkX.

### 6. Event Intelligence Engine
- Ingests corporate earnings calendars, dividend payout dates, stock splits, central bank FOMC/MPC meetings, economic calendars, insider trading filings, and Form 13F institutional holdings.

### 7. Hierarchical AI Memory Engine
- Multi-tier memory architecture: Working Memory (LangGraph State), Episodic Memory (Research Sessions), Semantic Memory (Vector Store), and Investment Journal (Rolling Brier Score self-calibration).

### 8. Explainable AI (XAI) Framework
- Generates SHAP feature attributions, Chain-of-Thought summaries, bull/bear argument matrices, known unknowns, and historical model accuracy.

### 9. Agent Marketplace & LangGraph Supervisor Topology
- Isolated agents communicating **exclusively via shared LangGraph State**. Centralized Supervisor Agent controls execution flow. Direct agent-to-agent calls strictly prohibited.

### 10. Plugin Architecture
- Abstract Python protocol interfaces for Swappable Brokers, LLMs, Vector DBs, ML Models, and Custom Technical Indicators.

### 11. Observability, Telemetry & LLM Cost Accounting
- OpenTelemetry tracing, Prometheus metrics, Sentry exception logging, and real-time LLM token cost accounting per research query.

### 12. Security & Compliance Layer
- JWT/RBAC authentication, Vault secret management, encrypted memory at rest, audit logging, and mandatory SEC/FINRA financial research disclaimers.

### 13. 13 Interactive UI Dashboard Modules
- Dedicated UI page layouts for Research, Portfolio, Prediction, Risk, Macro, News, Events, Watchlists, AI Chat, Knowledge Graph, Backtesting, Paper Trading, and Settings.

## Dependencies & Sub-System References
- [04. Database Design](file:///Users/kushal/Desktop/AlphaMind%20AI/docs/04_DATABASE_DESIGN.md)
- [05. API Design](file:///Users/kushal/Desktop/AlphaMind%20AI/docs/05_API_DESIGN.md)
- [06. Agent Architecture](file:///Users/kushal/Desktop/AlphaMind%20AI/docs/06_AGENT_ARCHITECTURE.md)
- [13. Data Pipeline](file:///Users/kushal/Desktop/AlphaMind%20AI/docs/13_DATA_PIPELINE.md)
- [16. Risk Engine](file:///Users/kushal/Desktop/AlphaMind%20AI/docs/16_RISK_ENGINE.md)
- [17. Prediction Engine](file:///Users/kushal/Desktop/AlphaMind%20AI/docs/17_PREDICTION_ENGINE.md)
