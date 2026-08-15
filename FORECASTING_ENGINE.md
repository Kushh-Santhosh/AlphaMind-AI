# AlphaMind AI — Probabilistic Forecasting & Kronos Engine

AlphaMind AI employs a probabilistic time-series forecasting architecture inspired by foundational autoregressive K-line modeling (Kronos) and ensemble methods.

---

## 1. Kronos Probabilistic K-Line Engine (`packages/prediction/kronos_forecast_engine.py`)

- **Autoregressive K-Line Generation**:
  - Generates future candle sequences (Open, High, Low, Close, Volume) over:
    - **Short Horizon**: 5 candles forward
    - **Medium Horizon**: 15 candles forward
    - **Long Horizon**: 30 candles forward
- **Uncertainty Envelope Modeling**:
  - Computes 90% and 95% confidence intervals from realized historical log-return drift and annualized volatility.
  - Generates 3-scenario target distributions: **Bull** (95% upper bound), **Base** (median drift path), and **Bear** (95% lower bound).
- **Compliance & Anti-Deterministic Rules**:
  - Explicit `MODEL FORECAST ONLY` badge.
  - Zero single-point guaranteed price targets.

---

## 2. Model Evaluation Scorecard Engine (`packages/evaluation/model_scorecard_engine.py`)

Continuously tracks predicted vs ground-truth realized outcomes:
- **MAE (Mean Absolute Error)**: Measures average absolute dollar error.
- **RMSE (Root Mean Squared Error)**: Penalizes large outlier forecast errors.
- **MAPE (Mean Absolute Percentage Error)**: Percentage error normalized by asset price.
- **Directional Accuracy (%)**: Fraction of candles correctly predicting return sign.
- **Hit Rate (%)**: Percentage of realized prices settling inside the 95% uncertainty cone.
- **Brier Score Calibration**: Probabilistic calibration verification.
- **Benchmark Comparison**: Benchmarks Kronos Foundation Model vs Technical Baseline (EMA/RSI) vs Naive Persistence (Random Walk).
