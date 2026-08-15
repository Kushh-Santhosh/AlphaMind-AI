# AlphaMind AI — Paper Trading & Virtual Execution Engine

AlphaMind AI incorporates an institutional-grade virtual paper trading engine inspired by event-driven architectures (NautilusTrader, Qlib) and quantitative risk management frameworks.

---

## 1. Virtual Execution Matching Engine (`PaperExchange`)

- **Order Types**:
  - `MARKET`: Immediate fill at live provider quote adjusted for slippage and spread.
  - `LIMIT`: Queue order; fills when market price crosses or touches limit threshold.
  - `STOP`: Triggers market fill when market price breaches stop trigger.
- **Microstructure Modeling**:
  - Dynamic slippage based on asset volatility and order size (default baseline 2.0 bps).
  - Bid/Ask half-spread simulation (0.5 bps to 5.0 bps depending on asset class).
  - Fixed commission ($1.00 per trade) and SEC transaction fee simulation.
- **Order Lifecycle States**:
  - `PENDING` → `SUBMITTED` → `PARTIALLY_FILLED` → `FILLED` / `CANCELLED` / `REJECTED` / `EXPIRED`.

---

## 2. Multi-Asset Portfolio Simulator (`PortfolioSimulator`)

- **Marked-to-Market Accounting**:
  - Tracks total portfolio equity, cash balances, buying power, maintenance margin, unrealized P&L, realized P&L, and daily P&L.
- **Multi-Asset Positions Support**:
  - US Equities (AAPL, NVDA, MSFT, TSLA)
  - Indian Equities NSE (RELIANCE.NS, TCS.NS, INFY.NS)
  - Cryptocurrencies (BTC-USD, ETH-USD, SOL-USD)
  - Energy & Commodities (WTI Crude `CL=F`, Gold `GC=F`, Natural Gas `NG=F`)
  - Global ETFs (SPY, QQQ, SMH, GLD, TLT)

---

## 3. Autonomous Paper Trader Daemon (`AutonomousPaperTrader`)

Autonomous closed-loop trading daemon:
1. **Screening**: Screens multi-asset universe via `OpportunityScannerEngine`.
2. **Foundation Forecasting**: Generates probabilistic K-line trajectory via `KronosForecastEngine`.
3. **Pre-Trade Risk**: Evaluates `PreTradeRiskEngine` limits (max 10% cash allocation per position, margin compliance, drawdown guardrails).
4. **Execution**: Submits simulated order to `PaperExchange`.
5. **Learning Reflection**: Logs execution context, entry rationale, and expected alpha to `StrategyLearningMemory`.
6. **Safety Badge**: Labeled with explicit `[PAPER MODE]` indicator.
