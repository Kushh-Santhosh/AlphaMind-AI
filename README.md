<div align="center">

# AlphaMind AI — Institutional Quantitative Trading OS (v4.1)

**An autonomous multi-agent intelligence and paper trading operating system featuring real multi-asset feeds, Kronos foundation K-line forecasting, interactive candlestick charting, dialectical research debate, 7 portfolio solvers, and institutional risk management.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16.3+-000000.svg?style=flat&logo=next.js&logoColor=white)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg?style=flat&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-FF6F00.svg?style=flat)](https://github.com/langchain-ai/langgraph)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

</div>

---

## 🌟 Executive Overview

AlphaMind AI is an enterprise-grade AI financial intelligence and autonomous paper-trading platform. Built on strict reality-first principles, AlphaMind AI consumes live multi-asset market data (US Equities, Indian NSE Equities, Cryptocurrencies, Energy, and Commodities) with zero synthetic financial values.

Key Architecture Highlights:
- **Interactive Candlestick Terminal**: Full OHLCV rendering, Moving Averages (20/50/200), Bollinger Bands, RSI-14, MACD, and multi-timeframe switching (1D to MAX).
- **Kronos Probabilistic K-Line Forecasting**: Autoregressive foundation candle path predictions with 95% uncertainty envelopes and 3-scenario targets (Bull, Base, Bear).
- **Autonomous Paper Trader**: Closed-loop agent execution with dynamic slippage, spread modeling, commissions, and marked-to-market portfolio accounting.
- **Model Scorecard & Strategy Learning**: Continuous validation of forecasts against realized ground-truth (MAE, RMSE, Directional Accuracy %, Brier score).
- **Dialectical Multi-Agent Research**: Adversarial debates between Bull and Bear researchers moderated by Research Managers with SEC EDGAR citation lineage.

---

## 🏗️ Core Architecture & Topology

```
                                  ┌────────────────────────────────┐
                                  │      Universal Data Layer      │
                                  │  SEC EDGAR • Yahoo • FRED • CC │
                                  └───────────────┬────────────────┘
                                                  │
                                                  ▼
                         ┌──────────────────────────────────────────────────┐
                         │      8 Specialized Financial Research Agents     │
                         │ Technical • Fundamental • Valuation (DCF) • News │
                         │ Sentiment • Macro Regime • Volatility • Earnings │
                         └────────────────────────┬─────────────────────────┘
                                                  │
                                                  ▼
                         ┌──────────────────────────────────────────────────┐
                         │        Adversarial Dialectical Debate            │
                         │   Bull Researcher  ⚔️  Bear Researcher           │
                         │       Refereed by Research Manager               │
                         └────────────────────────┬─────────────────────────┘
                                                  │
                                                  ▼
                         ┌──────────────────────────────────────────────────┐
                         │         Trader & Risk Committee Oversight        │
                         │   Trader Proposal ──► Risk Committee Votes       │
                         │   (Conservative, Moderate, Aggressive debaters)  │
                         └────────────────────────┬─────────────────────────┘
                                                  │
                                                  ▼
                         ┌──────────────────────────────────────────────────┐
                         │          5 Virtual AI Strategy Funds             │
                         │  Deep Value • Momentum • Macro • Parity • Growth │
                         │   Realistic Paper Execution (Slippage/Spread)    │
                         └────────────────────────┬─────────────────────────┘
                                                  │
                                                  ▼
                         ┌──────────────────────────────────────────────────┐
                         │   Brier Score Calibration & Strategy Learning    │
                         └──────────────────────────────────────────────────┘
```

### Strict Agent Isolation & State Graph
- **Zero Direct Agent Calls**: Agents communicate strictly through immutable LangGraph state transitions.
- **Probabilistic Forecasting**: Deterministic single-point price targets are prohibited. Output returns Bull, Base, and Bear scenarios with 95% confidence intervals.
- **SEC Audit Trail**: Every numeric assertion retains verified citations to SEC EDGAR Form 10-K, 10-Q, or 8-K disclosures.

---

## 🤖 11 Specialized Autonomous Agents

| Agent Persona | Role & Capabilities |
| :--- | :--- |
| **Technical Analyst** | RSI-14, MACD signal line crossovers, Bollinger Band squeeze, ATR, EMA 20/50/200, support & resistance levels. |
| **Fundamental Analyst** | Balance sheet health, Piotroski F-Score (0-9), Altman Z-Score solvency, free cash flow conversion rates. |
| **Valuation Analyst** | 3-Scenario DCF intrinsic value (Bull/Base/Bear), WACC discounting, terminal multiples (P/E, EV/EBITDA, PEG). |
| **News Analyst** | Financial headline tone extraction, SEC Form 8-K material disclosure parsing, catalyst timeline tracking. |
| **Sentiment Analyst** | Retail vs institutional sentiment divergence, social crowd psychology, news sentiment velocity. |
| **Macro Analyst** | Yield curve spread (10Y-2Y), Federal funds rate trajectory, CPI inflation, business cycle phase modeling. |
| **Market Regime Analyst**| VIX implied volatility regimes, ADX trend strength, risk-on / risk-off market transition scoring. |
| **Earnings Analyst** | Consensus EPS revisions momentum (up/down revisions ratio), past beat/miss track record, surprise probability. |
| **Bull Researcher** | Builds maximum conviction upside thesis, pricing power justification, and enterprise expansion opportunities. |
| **Bear Researcher** | Stress-tests thesis against margin compression, multiple contraction, regulatory headwinds, and supply risks. |
| **Research Manager** | Referees adversarial debate, resolves factual contradictions, and synthesizes final probabilistic distribution. |

---

## ⚡ Universal Model Gateway

AlphaMind AI features an interchangeable LLM Gateway supporting top frontier models with thinking/effort knobs, retry budgets, fallback routing, and token telemetry:

```python
from packages.agents.models.llm_gateway import get_llm_gateway

gateway = get_llm_gateway()
response = await gateway.generate(
    prompt="Synthesize DCF intrinsic value parameters for NVDA",
    system_prompt="You are an institutional quantitative research manager.",
    temperature=0.2,
    max_tokens=2048,
)
```

- **OpenAI**: `gpt-4o`, `gpt-4o-mini`, `o1`, `o3-mini`
- **Anthropic**: `claude-3-5-sonnet-20241022`, `claude-3-7-sonnet`
- **Google**: `gemini-2.0-flash`, `gemini-1.5-pro`
- **DeepSeek**: `deepseek-chat`, `deepseek-reasoner`
- **Ollama**: Local air-gapped open-source execution (`llama3.3`, `qwen2.5`)

---

## 📊 7 Institutional Optimization Solvers

Located in `packages/portfolio/advanced_solvers.py`:
1. **Risk Parity**: Equalizes marginal risk contributions across high-beta and low-beta assets.
2. **Volatility Targeting**: Dynamically adjusts portfolio leverage to maintain target annualized volatility (e.g., 12%).
3. **Mean-Variance Markowitz**: Maximizes portfolio Sharpe ratio under linear constraints and covariance shrinkage.
4. **Maximum Diversification**: Maximizes the ratio of weighted asset volatilities to total portfolio volatility.
5. **Minimum Variance**: Solves for the global minimum variance frontier allocation.
6. **Equal Weight (1/N)**: Unbiased baseline allocation benchmark.
7. **AI Multi-Factor Score Weighting**: Dynamic allocation proportional to multi-factor opportunity conviction.

---

## 🛡️ Crisis Stress Testing Suite

Located in `packages/risk/crisis_stress_engine.py`:
- **2008 Global Financial Crisis**: Liquidity freeze, credit spread widening, -45% equity shock.
- **2020 COVID-19 Flash Crash**: Sharp volatility spike (VIX > 80), sudden drawdown and recovery.
- **2022 Fed Rate Shock**: Aggressive interest rate hiking cycle and duration repricing.
- **2024 Tech Correction**: Semiconductor multiple contraction and AI capex scrutiny.
- **Crypto Crash & Flash Freeze**: 60% drawdown scenario and exchange liquidity freeze.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python**: 3.11+
- **Node.js**: 18.0+
- **Redis** (Optional for Pub/Sub stream clustering; in-memory fallback enabled by default)

### 2. Backend Installation & Setup
```bash
# Clone the repository
git clone https://github.com/Kushh-Santhosh/AlphaMind-AI.git
cd AlphaMind-AI

# Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI backend server
PYTHONPATH=. uvicorn apps.backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Frontend Installation & Setup
```bash
cd apps/frontend

# Install dependencies
npm install

# Start Next.js development server
npm run dev
```
Open **http://localhost:3000** to explore the application.

---

## 🧪 Testing & Quality Gates

Run full backend unit and integration test suites:
```bash
# Run all 220+ backend unit tests (0 failures)
PYTHONPATH=. .venv/bin/pytest apps/backend/tests/ -v

# Run frontend Vitest test suite
cd apps/frontend
npm test -- --run
```

---

## 📜 Third-Party Notices & Attribution

AlphaMind AI v4 incorporates quantitative and multi-agent architectural concepts from the open-source **TradingAgents** project by Tauric Research, distributed under the Apache License 2.0. Detailed notices and attributions are maintained in [ATTRIBUTIONS.md](ATTRIBUTIONS.md).

---

## ⚖️ Legal & SEC/FINRA Disclaimer

*AlphaMind AI is an algorithmic research, simulation, and educational software platform. All quantitative indicators, adversarial debate outputs, backtest simulations, and opportunity scores are for informational purposes only and do not constitute financial advice, investment recommendations, or an endorsement to buy or sell any security. Past performance in backtested simulations is not indicative of future market results.*
