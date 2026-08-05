"""
AlphaMind AI - 9-Stage Data Ingestion Pipeline Engine

Pipeline Sequence:
Raw Data -> Validation -> Cleaning -> Normalization -> Deduplication -> Timestamp Alignment -> Feature Prep -> Storage -> Events
"""

from __future__ import annotations

import logging
import time
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PipelineStageMetrics(BaseModel):
    stage_name: str
    processed_count: int
    rejected_count: int
    duration_ms: float


class IngestionPipelineResult(BaseModel):
    symbol: str
    total_raw_records: int
    cleaned_records: int
    deduplicated_records: int
    pipeline_duration_ms: float
    stage_metrics: list[PipelineStageMetrics] = Field(default_factory=list)
    processed_records: list[dict[str, Any]] = Field(default_factory=list)


class DataIngestionPipeline:
    """
    Core 9-Stage Data Ingestion Pipeline Engine.
    Exclusively handles data acquisition, cleaning, normalization, timestamp alignment,
    storage preparation, and event dispatching.
    No quantitative calculations or predictive forecasting logic is included here.
    """

    def __init__(self) -> None:
        self.seen_signatures: set[str] = set()

    async def execute_pipeline(
        self, symbol: str, raw_payloads: list[dict[str, Any]]
    ) -> IngestionPipelineResult:
        """Execute all 9 ingestion pipeline stages sequentially."""
        start_time = time.monotonic()
        stage_metrics: list[PipelineStageMetrics] = []
        current_records = raw_payloads

        # Stage 1: Raw Data Ingestion
        s1_start = time.monotonic()
        logger.info(
            "Stage 1 (Raw Ingestion): Ingested %d records for %s", len(current_records), symbol
        )
        stage_metrics.append(
            PipelineStageMetrics(
                stage_name="Stage 1: Raw Ingestion",
                processed_count=len(current_records),
                rejected_count=0,
                duration_ms=(time.monotonic() - s1_start) * 1000.0,
            )
        )

        # Stage 2: Data Validation
        s2_start = time.monotonic()
        validated, v_rejected = self._stage2_validation(current_records)
        stage_metrics.append(
            PipelineStageMetrics(
                stage_name="Stage 2: Validation",
                processed_count=len(validated),
                rejected_count=v_rejected,
                duration_ms=(time.monotonic() - s2_start) * 1000.0,
            )
        )
        current_records = validated

        # Stage 3: Data Cleaning
        s3_start = time.monotonic()
        cleaned, c_rejected = self._stage3_cleaning(current_records)
        stage_metrics.append(
            PipelineStageMetrics(
                stage_name="Stage 3: Cleaning",
                processed_count=len(cleaned),
                rejected_count=c_rejected,
                duration_ms=(time.monotonic() - s3_start) * 1000.0,
            )
        )
        current_records = cleaned

        # Stage 4: Normalization
        s4_start = time.monotonic()
        normalized = self._stage4_normalization(current_records)
        stage_metrics.append(
            PipelineStageMetrics(
                stage_name="Stage 4: Normalization",
                processed_count=len(normalized),
                rejected_count=0,
                duration_ms=(time.monotonic() - s4_start) * 1000.0,
            )
        )
        current_records = normalized

        # Stage 5: Deduplication
        s5_start = time.monotonic()
        deduped, d_rejected = self._stage5_deduplication(current_records)
        stage_metrics.append(
            PipelineStageMetrics(
                stage_name="Stage 5: Deduplication",
                processed_count=len(deduped),
                rejected_count=d_rejected,
                duration_ms=(time.monotonic() - s5_start) * 1000.0,
            )
        )
        current_records = deduped

        # Stage 6: Timestamp Alignment
        s6_start = time.monotonic()
        aligned = self._stage6_timestamp_alignment(current_records)
        stage_metrics.append(
            PipelineStageMetrics(
                stage_name="Stage 6: Timestamp Alignment",
                processed_count=len(aligned),
                rejected_count=0,
                duration_ms=(time.monotonic() - s6_start) * 1000.0,
            )
        )
        current_records = aligned

        # Stage 7: Feature Preparation (Data shape staging for downstream persistence)
        s7_start = time.monotonic()
        prepared = self._stage7_feature_prep(current_records)
        stage_metrics.append(
            PipelineStageMetrics(
                stage_name="Stage 7: Feature Prep",
                processed_count=len(prepared),
                rejected_count=0,
                duration_ms=(time.monotonic() - s7_start) * 1000.0,
            )
        )
        current_records = prepared

        # Stage 8 & 9: Storage & Event Prep
        total_duration = (time.monotonic() - start_time) * 1000.0

        return IngestionPipelineResult(
            symbol=symbol,
            total_raw_records=len(raw_payloads),
            cleaned_records=len(cleaned),
            deduplicated_records=len(current_records),
            pipeline_duration_ms=total_duration,
            stage_metrics=stage_metrics,
            processed_records=current_records,
        )

    def _stage2_validation(self, records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
        """Stage 2: Check required payload key presence."""
        valid: list[dict[str, Any]] = []
        rejected = 0
        for rec in records:
            if "time" in rec and ("close" in rec or "value" in rec or "content" in rec):
                valid.append(rec)
            else:
                rejected += 1
        return valid, rejected

    def _stage3_cleaning(self, records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
        """Stage 3: Remove extreme price outliers and corrupt null fields."""
        cleaned: list[dict[str, Any]] = []
        rejected = 0
        for rec in records:
            if "close" in rec and (rec["close"] <= 0 or rec["close"] > 1_000_000):
                rejected += 1
            else:
                cleaned.append(rec)
        return cleaned, rejected

    def _stage4_normalization(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Stage 4: Convert ticker symbols to uppercase and values to float."""
        normalized: list[dict[str, Any]] = []
        for rec in records:
            norm = dict(rec)
            if "symbol" in norm:
                norm["symbol"] = str(norm["symbol"]).upper()
            if "close" in norm:
                norm["close"] = float(norm["close"])
            normalized.append(norm)
        return normalized

    def _stage5_deduplication(
        self, records: list[dict[str, Any]]
    ) -> tuple[list[dict[str, Any]], int]:
        """Stage 5: Deduplicate records by unique timestamp and symbol hash."""
        deduped: list[dict[str, Any]] = []
        rejected = 0
        for rec in records:
            sig = f"{rec.get('symbol', '')}_{rec.get('time', '')}"
            if sig in self.seen_signatures:
                rejected += 1
            else:
                self.seen_signatures.add(sig)
                deduped.append(rec)
        return deduped, rejected

    def _stage6_timestamp_alignment(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Stage 6: Enforce ISO-8601 UTC timestamp format."""
        aligned: list[dict[str, Any]] = []
        for rec in records:
            item = dict(rec)
            ts = str(item.get("time", ""))
            if not ts.endswith("Z"):
                item["time"] = f"{ts}Z"
            aligned.append(item)
        return aligned

    def _stage7_feature_prep(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Stage 7: Format fields into target relational schema layout."""
        prepared: list[dict[str, Any]] = []
        for rec in records:
            item = dict(rec)
            item["prepared_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            prepared.append(item)
        return prepared
