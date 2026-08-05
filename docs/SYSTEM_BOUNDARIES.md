# AlphaMind AI - System Boundaries, Capabilities & Risk Assumptions

This document defines the strict operational boundaries, market scopes, provider integrations, performance SLA targets, failure protocols, and risk assumptions for the **AlphaMind AI** platform.

---

## 1. System Scope & Core Mission

### What AlphaMind AI DOES
- Provides autonomous, multi-agent probabilistic financial research and analysis.
- Computes multi-factor quantitative models (CAPM, Fama-French, Momentum, Value, Quality, Volatility, Cointegration).
- Runs 10,000-iteration Monte Carlo simulations and Bayesian inference for price trajectory probability distributions.
- Ingests and analyzes SEC filings (10-K, 10-Q, 8-K, 13F) with FinBERT / LLM NLP extraction.
- Tracks macroeconomic indicators, central bank policies (Fed, RBI, ECB), and global event calendars.
- Builds and queries a multi-node Financial Knowledge Graph (companies, executives, supply chains, lawsuits, patents).
- Performs portfolio optimization (Markowitz Mean-Variance, Black-Litterman, Hierarchical Risk Parity) and risk calculation (VaR, CVaR).
- Provides VectorBT / Backtrader strategy backtesting and paper trading execution simulation.
- Enforces Explainable AI (XAI) with SHAP feature attribution, confidence scores, known unknowns, and contradicting evidence.

### What AlphaMind AI DOES NOT DO
- **Guaranteed Future Target Prices**: The platform explicitly rejects deterministic single-point target prices (e.g. "$250 by Friday").
- **High-Frequency Trading (HFT)**: The system does not engage in sub-millisecond market making or low-latency arbitrage.
- **Personalized Financial / Tax / Legal Advice**: AlphaMind AI generates objective research intelligence and is not a registered fiduciary or investment advisor.
- **Direct Broker Custody**: AlphaMind AI does not hold client funds or operate as a securities exchange.

---

## 2. Asset Class & Market Coverage

### Supported Markets & Instruments
| Asset Class | Supported Coverage | Primary Data Feed | Secondary / Fallback Feed |
| :--- | :--- | :--- | :--- |
| **US Equities** | NYSE, NASDAQ, AMEX (Large, Mid, Small Cap) | Polygon.io | Alpha Vantage / yfinance |
| **ETFs & Funds** | US & Global Equity, Fixed Income, Sector ETFs | Polygon.io | yfinance |
| **Futures** | Index (ES, NQ), Commodities (CL, GC), Rates (ZN) | Interactive Brokers API | Polygon.io / Yahoo Finance |
| **Options** | US Stock & Index Options (US Chains) | Polygon.io | Interactive Brokers API |
| **Forex** | Major (EUR/USD, GBP/USD, USD/JPY) & Minor Pairs | CCXT / Polygon.io | Alpha Vantage |
| **Crypto** | Top 100 Cryptocurrencies by Market Cap | CCXT (Binance, Kraken) | Polygon.io Crypto |
| **Fixed Income** | US Treasuries (2Y, 5Y, 10Y, 30Y), Corporate Spreads | FRED API | World Bank Data |
| **Commodities** | Gold, Silver, Crude Oil, Natural Gas, Agriculture | Interactive Brokers | Polygon.io / yfinance |
| **Global Indices** | S&P 500, NASDAQ 100, FTSE 100, Nifty 50, Nikkei 225 | Polygon.io | yfinance |

### Unsupported Markets (Out of Scope for Initial Releases)
- Private Equity / Venture Capital early-stage deals.
- Real Estate physical deeds / non-securitized property.
- Exotic derivatives (variance swaps, barrier options, weather derivatives).
- Micro-cap OTC penny stocks (< $5M market cap).

---

## 3. Provider Integration & Redundancy Matrix

AlphaMind AI enforces a mandatory 3-Tier Redundancy Matrix for all market data ingestion:

```
[ Primary Provider ] ---> (Fail? / Timeout > 3s) ---> [ Secondary Provider ] ---> (Fail?) ---> [ Fallback Provider ]
```

- **Equities / Options**: `Polygon.io` (Primary) $\rightarrow$ `Alpha Vantage` (Secondary) $\rightarrow$ `yfinance` (Fallback).
- **Macroeconomic Data**: `FRED API` (Primary) $\rightarrow$ `World Bank API` (Secondary) $\rightarrow$ `OECD Data` (Fallback).
- **Crypto & FX**: `CCXT` (Primary) $\rightarrow$ `Polygon.io Crypto` (Secondary) $\rightarrow$ `Alpha Vantage` (Fallback).
- **SEC Filings**: `SEC EDGAR Direct` (Primary) $\rightarrow$ `Financial Modeling Prep` (Secondary) $\rightarrow$ `SEC RSS Parser` (Fallback).

---

## 4. Latency SLA Targets & Performance Boundaries

| Operation Type | Target Latency SLA | Maximum Acceptable Timeout | Streaming Protocol |
| :--- | :--- | :--- | :--- |
| **Market Ticker Streaming** | < 250ms | 1000ms | WebSockets |
| **REST API Data Endpoints** | < 200ms | 1500ms | HTTP/2 JSON |
| **Single-Agent Research Query** | < 3000ms | 8000ms | Server-Sent Events (SSE) |
| **Multi-Agent Deep Research (11 Agents)** | < 30 seconds | 60 seconds | SSE Log Streaming |
| **Monte Carlo Simulation (10,000 runs)** | < 1500ms | 4000ms | Async Worker / Redis |
| **Backtest Execution (5-year history)** | < 5000ms | 15000ms | Async Worker / Redis |

---

## 5. Offline Capabilities & Degraded Modes

- **Local Redis Caching**: All historical daily bars and static financial statement metrics are cached locally with TTLs ranging from 60 seconds (real-time price bars) to 24 hours (macro indicators).
- **Offline / Disconnected Mode**: If all remote data providers fail or internet connectivity is severed, AlphaMind AI enters **Degraded Read-Only Mode**, operating entirely on cached SQLite / PostgreSQL data and displaying explicit UI warning banners.

---

## 6. Failure Recovery & Risk Assumptions

1. **AI Hallucination Risk Assumption**: LLMs can misquote numbers. All numeric assertions generated by agents are cross-checked against source tabular data in PostgreSQL by the `Risk Engine`. Discrepancies > 0.01% cause automatic report rejection and re-generation.
2. **Provider Outage Assumption**: Data providers will experience downtime. The system maintains automated health checks every 30 seconds and switches endpoints seamlessly.
3. **Model Risk Assumption**: Quantitative models (e.g., Black-Scholes, CAPM) depend on distributional assumptions. Monte Carlo simulations utilize heavy-tailed Student's t distributions rather than pure Gaussian distributions to account for market jump risk.
4. **Market Black Swan Assumption**: Financial markets experience extreme regime shifts. The system embeds real-time volatility spike monitoring (VIX > 35) to trigger conservative risk controls and increase cash allocations in paper trading portfolios.
