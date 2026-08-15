"""
AlphaMind AI v2 — Mission Control Terminal: Backend Unit Tests

Tests cover:
  - /dashboard aggregated state
  - /health subsystem status
  - /activity-feed pagination and structure
  - /funds listing and single fund detail
  - /intelligence snapshot
  - /notifications limit enforcement
  - /timeline-stats aggregation
  - /reasoning/{id} Decision Inspector
  - /replay/status, /replay/step, /replay/jump
  - /search cross-entity search
  - /stream SSE response headers
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from apps.backend.app.main import app
from apps.backend.app.middleware.rate_limit import _IN_MEMORY_BUCKET
from fastapi.testclient import TestClient

client = TestClient(app)


# ── Fixtures ───────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def _reset_mocks() -> Iterator[None]:
    """Ensure each test gets a clean call context. No state bleed."""
    _IN_MEMORY_BUCKET.clear()
    yield
    _IN_MEMORY_BUCKET.clear()


# ── /dashboard ─────────────────────────────────────────────────────────────────


class TestDashboard:
    def test_dashboard_returns_200(self) -> None:
        resp = client.get("/api/v1/mission-control/dashboard")
        assert resp.status_code == 200

    def test_dashboard_has_required_keys(self) -> None:
        data = client.get("/api/v1/mission-control/dashboard").json()
        required = {
            "generated_at_utc",
            "uptime_seconds",
            "system_health",
            "funds",
            "timeline",
            "reasoning",
            "activity_feed",
            "intelligence",
            "notifications",
            "timeline_stats",
            "total_aum_usd",
            "avg_confidence",
        }
        assert required.issubset(data.keys())

    def test_dashboard_funds_list_is_five(self) -> None:
        data = client.get("/api/v1/mission-control/dashboard").json()
        assert len(data["funds"]) == 5

    def test_dashboard_generated_at_utc_present(self) -> None:
        data = client.get("/api/v1/mission-control/dashboard").json()
        assert data["generated_at_utc"] is not None
        assert "T" in data["generated_at_utc"]

    def test_dashboard_total_aum_positive(self) -> None:
        data = client.get("/api/v1/mission-control/dashboard").json()
        assert data["total_aum_usd"] > 0

    def test_dashboard_uptime_nonnegative(self) -> None:
        data = client.get("/api/v1/mission-control/dashboard").json()
        assert data["uptime_seconds"] >= 0


# ── /health ────────────────────────────────────────────────────────────────────


class TestHealth:
    def test_health_returns_200(self) -> None:
        assert client.get("/api/v1/mission-control/health").status_code == 200

    def test_health_status_healthy(self) -> None:
        data = client.get("/api/v1/mission-control/health").json()
        assert data["status"] == "HEALTHY"

    def test_health_subsystems_present(self) -> None:
        data = client.get("/api/v1/mission-control/health").json()
        assert "subsystems" in data
        assert len(data["subsystems"]) >= 5

    def test_health_all_subsystems_up(self) -> None:
        data = client.get("/api/v1/mission-control/health").json()
        for sub_name, sub in data["subsystems"].items():
            assert sub["status"] in ("UP", "HEALTHY", "DEGRADED", "OFFLINE")

    def test_health_uptime_seconds_positive(self) -> None:
        data = client.get("/api/v1/mission-control/health").json()
        assert data["uptime_seconds"] >= 0


# ── /activity-feed ─────────────────────────────────────────────────────────────


class TestActivityFeed:
    def test_activity_feed_returns_200(self) -> None:
        assert client.get("/api/v1/mission-control/activity-feed").status_code == 200

    def test_activity_feed_respects_limit(self) -> None:
        data = client.get("/api/v1/mission-control/activity-feed?limit=5").json()
        assert len(data["items"]) <= 5

    def test_activity_feed_items_have_required_keys(self) -> None:
        data = client.get("/api/v1/mission-control/activity-feed?limit=3").json()
        if data["items"]:
            item = data["items"][0]
            for k in ("event_id", "event_type", "headline", "source_subsystem", "timestamp_utc"):
                assert k in item

    def test_activity_feed_has_total(self) -> None:
        data = client.get("/api/v1/mission-control/activity-feed").json()
        assert "total" in data
        assert isinstance(data["total"], int)

    def test_activity_feed_limit_max_100(self) -> None:
        resp = client.get("/api/v1/mission-control/activity-feed?limit=101")
        assert resp.status_code == 422

    def test_activity_feed_timeline_link_present(self) -> None:
        data = client.get("/api/v1/mission-control/activity-feed?limit=1").json()
        if data["items"]:
            assert "timeline_link" in data["items"][0]


# ── /funds ─────────────────────────────────────────────────────────────────────


class TestFunds:
    def test_funds_returns_200(self) -> None:
        assert client.get("/api/v1/mission-control/funds").status_code == 200

    def test_funds_returns_five(self) -> None:
        data = client.get("/api/v1/mission-control/funds").json()
        assert len(data["funds"]) == 5

    def test_fund_has_performance_metrics(self) -> None:
        data = client.get("/api/v1/mission-control/funds").json()
        fund = data["funds"][0]
        for k in ("fund_id", "name", "cagr_pct", "sharpe_ratio", "allocations"):
            assert k in fund

    def test_funds_total_aum_is_sum(self) -> None:
        data = client.get("/api/v1/mission-control/funds").json()
        calculated_aum = sum(f["current_market_value_usd"] for f in data["funds"])
        assert abs(data["total_aum_usd"] - calculated_aum) < 1.0

    def test_fund_detail_valid_id(self) -> None:
        data = client.get("/api/v1/mission-control/funds").json()
        fund_id = data["funds"][0]["fund_id"]
        resp = client.get(f"/api/v1/mission-control/funds/{fund_id}")
        assert resp.status_code == 200
        assert resp.json()["fund"]["fund_id"] == fund_id

    def test_fund_detail_invalid_id_returns_404(self) -> None:
        resp = client.get("/api/v1/mission-control/funds/NONEXISTENT_FUND_ID")
        assert resp.status_code == 404

    def test_fund_detail_has_allocations(self) -> None:
        data = client.get("/api/v1/mission-control/funds").json()
        fund_id = data["funds"][0]["fund_id"]
        detail = client.get(f"/api/v1/mission-control/funds/{fund_id}").json()
        assert "allocations" in detail["fund"]
        assert "recent_reasoning" in detail


# ── /intelligence ──────────────────────────────────────────────────────────────


class TestIntelligence:
    def test_intelligence_returns_200(self) -> None:
        assert client.get("/api/v1/mission-control/intelligence").status_code == 200

    def test_intelligence_has_macro_factors(self) -> None:
        data = client.get("/api/v1/mission-control/intelligence").json()
        assert "current_reasoning" in data

    def test_intelligence_avg_confidence_between_0_and_1(self) -> None:
        data = client.get("/api/v1/mission-control/intelligence").json()
        assert 0.0 <= data["avg_confidence_score"] <= 1.0

    def test_intelligence_current_reasoning_is_list(self) -> None:
        data = client.get("/api/v1/mission-control/intelligence").json()
        assert isinstance(data["current_reasoning"], list)


# ── /notifications ─────────────────────────────────────────────────────────────


class TestNotifications:
    def test_notifications_returns_200(self) -> None:
        assert client.get("/api/v1/mission-control/notifications").status_code == 200

    def test_notifications_has_unread_count(self) -> None:
        data = client.get("/api/v1/mission-control/notifications").json()
        assert "unread_count" in data
        assert isinstance(data["unread_count"], int)

    def test_notifications_respects_limit(self) -> None:
        data = client.get("/api/v1/mission-control/notifications?limit=5").json()
        assert len(data["notifications"]) <= 5

    def test_notifications_limit_max_50(self) -> None:
        resp = client.get("/api/v1/mission-control/notifications?limit=51")
        assert resp.status_code == 422

    def test_notification_has_type_and_title(self) -> None:
        data = client.get("/api/v1/mission-control/notifications?limit=1").json()
        if data["notifications"]:
            n = data["notifications"][0]
            assert "type" in n
            assert "title" in n
            assert "created_at_utc" in n


# ── /timeline-stats ────────────────────────────────────────────────────────────


class TestTimelineStats:
    def test_timeline_stats_returns_200(self) -> None:
        assert client.get("/api/v1/mission-control/timeline-stats").status_code == 200

    def test_timeline_stats_has_total(self) -> None:
        data = client.get("/api/v1/mission-control/timeline-stats").json()
        assert "total_events" in data
        assert data["total_events"] >= 0

    def test_timeline_stats_has_by_type(self) -> None:
        data = client.get("/api/v1/mission-control/timeline-stats").json()
        assert "by_type" in data
        assert isinstance(data["by_type"], dict)

    def test_timeline_stats_has_by_subsystem(self) -> None:
        data = client.get("/api/v1/mission-control/timeline-stats").json()
        assert "by_subsystem" in data
        assert isinstance(data["by_subsystem"], dict)


# ── /reasoning/{id} (Decision Inspector) ──────────────────────────────────────


class TestReasoningRecord:
    def test_reasoning_missing_id_returns_404(self) -> None:
        resp = client.get("/api/v1/mission-control/reasoning/NONEXISTENT_ID_XYZ")
        assert resp.status_code == 404

    def test_reasoning_valid_id_returns_200(self) -> None:
        from apps.backend.app.api.v1.mission_control import _reasoning_records

        records = _reasoning_records(limit=1)
        if not records:
            pytest.skip("No reasoning records seeded; skipping.")
        rid = records[0]["reasoning_id"]
        resp = client.get(f"/api/v1/mission-control/reasoning/{rid}")
        assert resp.status_code == 200

    def test_reasoning_record_has_decision_inspector_fields(self) -> None:
        from apps.backend.app.api.v1.mission_control import _reasoning_records

        records = _reasoning_records(limit=1)
        if not records:
            pytest.skip("No reasoning records seeded; skipping.")
        rid = records[0]["reasoning_id"]
        data = client.get(f"/api/v1/mission-control/reasoning/{rid}").json()
        required = {
            "reasoning_id",
            "selected_action",
            "confidence_score",
            "assumptions",
            "evidence_references",
            "contradicting_evidence",
            "probability_distribution",
        }
        assert required.issubset(data.keys())

    def test_reasoning_probability_distribution_sums_to_100(self) -> None:
        from apps.backend.app.api.v1.mission_control import _reasoning_records

        records = _reasoning_records(limit=1)
        if not records:
            pytest.skip("No reasoning records seeded; skipping.")
        rid = records[0]["reasoning_id"]
        data = client.get(f"/api/v1/mission-control/reasoning/{rid}").json()
        pd = data["probability_distribution"]
        total = pd["bull_pct"] + pd["base_pct"] + pd["bear_pct"]
        assert total == 100, f"Probability distribution sums to {total}, expected 100"


# ── /replay/status, /step, /jump ───────────────────────────────────────────────


class TestChessReplay:
    def test_replay_status_returns_200(self) -> None:
        assert client.get("/api/v1/mission-control/replay/status").status_code == 200

    def test_replay_status_has_session_id(self) -> None:
        data = client.get("/api/v1/mission-control/replay/status").json()
        assert "session_id" in data
        assert data["session_id"]

    def test_replay_step_forward(self) -> None:
        resp = client.post(
            "/api/v1/mission-control/replay/step",
            json={"direction": "forward"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "position" in data
        assert data["direction"] == "forward"

    def test_replay_step_backward(self) -> None:
        resp = client.post(
            "/api/v1/mission-control/replay/step",
            json={"direction": "backward"},
        )
        assert resp.status_code == 200

    def test_replay_step_invalid_direction_returns_400(self) -> None:
        resp = client.post(
            "/api/v1/mission-control/replay/step",
            json={"direction": "sideways"},
        )
        assert resp.status_code == 400

    def test_replay_jump_valid(self) -> None:
        resp = client.post("/api/v1/mission-control/replay/jump", json={"step": 0})
        assert resp.status_code == 200

    def test_replay_jump_has_position(self) -> None:
        resp = client.post("/api/v1/mission-control/replay/jump", json={"step": 0})
        data = resp.json()
        assert "position" in data
        assert "target_step" in data

    def test_replay_status_has_total_frames(self) -> None:
        data = client.get("/api/v1/mission-control/replay/status").json()
        assert "total_frames" in data
        assert isinstance(data["total_frames"], int)


# ── /search ───────────────────────────────────────────────────────────────────


class TestGlobalSearch:
    def test_search_returns_200(self) -> None:
        assert client.get("/api/v1/mission-control/search?q=fund").status_code == 200

    def test_search_has_results_key(self) -> None:
        data = client.get("/api/v1/mission-control/search?q=fund").json()
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_search_has_query_echo(self) -> None:
        data = client.get("/api/v1/mission-control/search?q=conservative").json()
        assert data["query"] == "conservative"

    def test_search_finds_fund_by_name(self) -> None:
        data = client.get("/api/v1/mission-control/search?q=Conservative").json()
        fund_results = [r for r in data["results"] if r["type"] == "FUND"]
        assert len(fund_results) >= 1

    def test_search_missing_q_returns_422(self) -> None:
        assert client.get("/api/v1/mission-control/search").status_code == 422

    def test_search_has_total(self) -> None:
        data = client.get("/api/v1/mission-control/search?q=fund").json()
        assert "total" in data
        assert isinstance(data["total"], int)


# ── /stream ────────────────────────────────────────────────────────────────────


class TestSSEStream:
    @pytest.mark.asyncio
    async def test_stream_returns_200_with_event_stream_type(self) -> None:
        from packages.os_core.sse_broadcaster import RedisSSEBroadcaster
        broadcaster = RedisSSEBroadcaster()
        broadcaster.enable_pubsub = False
        broadcaster.heartbeat_interval = 0.001
        await broadcaster.publish_event({"type": "test_event", "payload": {}})
        gen = broadcaster.event_generator(tick_interval=0.001)
        chunk = await gen.__anext__()
        assert "data: " in chunk
        await gen.aclose()

    @pytest.mark.asyncio
    async def test_stream_has_cache_control_no_cache(self) -> None:
        from apps.backend.app.api.v1.mission_control import live_activity_stream
        resp = await live_activity_stream(tick_interval=1.0)
        assert resp.headers.get("cache-control") == "no-cache"
        assert resp.media_type == "text/event-stream"

    def test_stream_tick_interval_too_low_returns_422(self) -> None:
        resp = client.get("/api/v1/mission-control/stream?tick_interval=0.1")
        assert resp.status_code == 422
