"""
Unit and Integration Tests for HARD-05 Scalable Redis Pub/Sub SSE Event Broadcaster
"""

import pytest

from packages.os_core.sse_broadcaster import RedisSSEBroadcaster


@pytest.mark.asyncio
async def test_sse_broadcaster_event_publish_fallback():
    """Verify event publishing fallback when Redis Pub/Sub is in offline fallback mode."""
    broadcaster = RedisSSEBroadcaster()
    broadcaster.enable_pubsub = False

    payload = {"type": "test_event", "data": "AAPL market tick"}
    published = await broadcaster.publish_event(payload)

    assert isinstance(published, bool)
    assert not broadcaster._local_event_queue.empty()


@pytest.mark.asyncio
async def test_sse_generator_heartbeat_and_cleanup():
    """Verify SSE generator yields heartbeats and cleans up active client count on exit."""
    broadcaster = RedisSSEBroadcaster()
    broadcaster.enable_pubsub = False
    broadcaster.heartbeat_interval = 0  # Immediate heartbeat trigger

    gen = broadcaster.event_generator(tick_interval=0.01)

    # Fetch first chunk (should be heartbeat or queued message)
    chunk = await gen.__anext__()
    assert "data: " in chunk
    assert "heartbeat" in chunk or "active_clients" in chunk

    # Close generator
    await gen.aclose()
    assert broadcaster.active_clients_count == 0


@pytest.mark.asyncio
async def test_max_sse_clients_capacity_limit():
    """Verify max client connection limit enforcement."""
    broadcaster = RedisSSEBroadcaster()
    broadcaster.max_clients = 0  # Trigger capacity limit immediately

    gen = broadcaster.event_generator(tick_interval=0.01)
    chunk = await gen.__anext__()
    assert "Max SSE client capacity reached" in chunk
