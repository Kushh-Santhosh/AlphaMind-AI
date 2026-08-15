# Third-Party Notices & Open Source Attributions

AlphaMind AI incorporates architectural patterns, algorithmic formulations, and engineering principles inspired by leading open-source financial and quantitative machine learning repositories. We gratefully acknowledge these foundational contributions.

---

## 1. TauricResearch/TradingAgents
- **Source**: [https://github.com/TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
- **License**: Apache License 2.0
- **Influence on AlphaMind AI**:
  - Multi-agent dialectical role architecture: Bull Researcher, Bear Researcher, Fundamentals Analyst, Technical Analyst, Risk Committee, and Research Manager.
  - State-driven LangGraph coordination graph and structured debate synthesis.
  - Native implementation within `packages/agents/` and `packages/debate/`.

---

## 2. Kronos Financial K-Line Foundation Model
- **Concept & Paper**: Autoregressive K-line trajectory modeling and candlestick foundation representations.
- **Influence on AlphaMind AI**:
  - Probabilistic future OHLCV trajectory generation (Open, High, Low, Close, Volume) over multi-step horizons (Short: 5, Medium: 15, Long: 30 days).
  - 90% and 95% uncertainty envelope modeling and scenario paths (Bull, Base, Bear).
  - Model evaluation scorecard comparing predicted vs ground-truth realizations (MAE, RMSE, MAPE, Directional Accuracy %, Brier Score).
  - Native implementation within `packages/prediction/kronos_forecast_engine.py` and `packages/evaluation/model_scorecard_engine.py`.

---

## 3. Microsoft Qlib (Quantitative Investment Platform)
- **Source**: [https://github.com/microsoft/qlib](https://github.com/microsoft/qlib)
- **License**: MIT License
- **Influence on AlphaMind AI**:
  - Real-time quantitative factor computation: Momentum (ROC, RSI, MACD, Distance to 52-week High), Valuation (P/E, EV/EBITDA, FCF Yield), Quality (ROE, ROIC, Net Margin), and Realized Volatility.
  - Factor-based opportunity ranking and scoring engine.
  - Walk-forward validation methodology (70% In-Sample / 30% Out-of-Sample).
  - Native implementation within `packages/research/opportunity_scanner.py` and `packages/research/factor_engine.py`.

---

## 4. AI4Finance-Foundation / FinRL
- **Source**: [https://github.com/AI4Finance-Foundation/FinRL](https://github.com/AI4Finance-Foundation/FinRL)
- **License**: MIT License
- **Influence on AlphaMind AI**:
  - Strategy performance tracking and regime classification (Bull Expansion, Bear Contraction, High Volatility).
  - Outcome-driven strategy memory recording win rates, profit factors, Sharpe ratios, and drawdowns.
  - Native implementation within `packages/memory/strategy_learning_memory.py`.

---

## 5. NautilusTrader
- **Source**: [https://github.com/nautechsystems/nautilus_trader](https://github.com/nautechsystems/nautilus_trader)
- **License**: LGPL v3.0 / MIT
- **Influence on AlphaMind AI**:
  - Realistic virtual execution matching engine: Market, Limit, and Stop orders.
  - Bid/ask spread modeling, dynamic slippage calculation, fixed commissions, and order lifecycle states (`PENDING`, `SUBMITTED`, `FILLED`, `CANCELLED`, `REJECTED`).
  - Strict `[PAPER MODE]` simulation guarantees.
  - Native implementation within `packages/portfolio/paper_exchange.py` and `packages/agents/agents/autonomous_paper_trader.py`.

---

## 6. yfinance
- **Source**: [https://github.com/ranaroussi/yfinance](https://github.com/ranaroussi/yfinance)
- **License**: Apache License 2.0
- **Influence on AlphaMind AI**:
  - Async threadpool wrapped market data ingestion across US Equities, Indian Equities (NSE `.NS`), Global ETFs, Crypto, Energy (`CL=F`, `BZ=F`), and Commodities (`GC=F`, `SI=F`).
  - Direct calculation of technical indicators and corporate metadata.
  - Native implementation within `packages/market/provider_registry.py`.
