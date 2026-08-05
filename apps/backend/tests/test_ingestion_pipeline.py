"""
Data Foundation Test Suite — 9-Stage Data Ingestion Pipeline Tests
"""

import pytest

from packages.market.ingestion_pipeline import DataIngestionPipeline


@pytest.mark.asyncio
async def test_9_stage_ingestion_pipeline_execution() -> None:
    """Execute 9-stage ingestion pipeline with raw test records."""
    pipeline = DataIngestionPipeline()
    raw_records = [
        {"time": "2026-08-01T00:00:00", "symbol": "aapl", "close": 154.5},
        {"time": "2026-08-01T00:00:00", "symbol": "aapl", "close": 154.5},  # Duplicate
        {"time": "2026-08-02T00:00:00", "symbol": "aapl", "close": -10.0},  # Invalid price outlier
        {"time": "2026-08-03T00:00:00", "symbol": "aapl", "close": 158.2},
    ]

    result = await pipeline.execute_pipeline("AAPL", raw_records)

    assert result.symbol == "AAPL"
    assert result.total_raw_records == 4
    # Outlier (-10.0) removed, duplicate removed -> 2 processed records remaining
    assert result.deduplicated_records == 2
    assert len(result.stage_metrics) == 7
    assert result.processed_records[0]["symbol"] == "AAPL"
    assert result.processed_records[0]["time"].endswith("Z")
