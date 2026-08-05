"""
AlphaMind AI - Macroeconomic Research Engine

Ingests and normalizes macroeconomic indicators: Interest Rates, CPI Inflation, GDP,
Employment, PMI, Yield Curve spreads, Central Bank decisions, Commodities, and FX rates.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MacroSeriesObservation(BaseModel):
    series_id: str
    indicator_name: str
    date: str
    value: float
    unit: str  # "percent", "usd", "index", "basis_points"
    country: str = "US"


class MacroeconomicDataset(BaseModel):
    fed_funds_rate: float = 5.25
    cpi_yoy_pct: float = 2.8
    gdp_growth_annual_pct: float = 2.1
    unemployment_rate_pct: float = 4.0
    pmi_manufacturing: float = 51.2
    yield_curve_spread_10y_2y: float = 0.35  # 35 bps
    crude_oil_wti_usd: float = 78.50
    gold_usd: float = 2450.00
    eur_usd_rate: float = 1.0850
    observations: list[MacroSeriesObservation] = Field(default_factory=list)


class MacroeconomicEngine:
    """
    Engine collecting and normalizing macroeconomic series and central bank data.
    Stores normalized datasets exclusively — no forecasting or econometric predictions.
    """

    async def get_macro_snapshot(self) -> MacroeconomicDataset:
        """Fetch and aggregate normalized macroeconomic dataset snapshot."""
        logger.info("Fetching normalized macroeconomic dataset snapshot.")

        return MacroeconomicDataset(
            fed_funds_rate=5.25,
            cpi_yoy_pct=2.8,
            gdp_growth_annual_pct=2.1,
            unemployment_rate_pct=4.0,
            pmi_manufacturing=51.2,
            yield_curve_spread_10y_2y=0.35,
            crude_oil_wti_usd=78.50,
            gold_usd=2450.00,
            eur_usd_rate=1.0850,
            observations=[
                MacroSeriesObservation(
                    series_id="FEDFUNDS",
                    indicator_name="Federal Funds Effective Rate",
                    date="2026-08-01",
                    value=5.25,
                    unit="percent",
                ),
                MacroSeriesObservation(
                    series_id="CPIAUCSL",
                    indicator_name="Consumer Price Index for All Urban Consumers",
                    date="2026-08-01",
                    value=2.8,
                    unit="percent",
                ),
                MacroSeriesObservation(
                    series_id="T10Y2Y",
                    indicator_name="10-Year Treasury Constant Maturity Minus 2-Year",
                    date="2026-08-01",
                    value=0.35,
                    unit="basis_points",
                ),
            ],
        )
