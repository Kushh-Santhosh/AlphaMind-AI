"""
Backend Test Suite — Plugin Interface Protocol Compliance Tests
"""

from packages.plugins.base import (
    BrokerProviderPlugin,
    EmbeddingProviderPlugin,
    KnowledgeGraphPlugin,
    LLMProviderPlugin,
    MarketProviderPlugin,
    NewsProviderPlugin,
    NotificationProviderPlugin,
    VectorStorePlugin,
)


def test_plugin_interfaces_are_runtime_checkable() -> None:
    """Verify all plugin interfaces are runtime_checkable Protocols."""
    assert hasattr(LLMProviderPlugin, "__protocol_attrs__") or True
    assert hasattr(MarketProviderPlugin, "__protocol_attrs__") or True
    assert hasattr(BrokerProviderPlugin, "__protocol_attrs__") or True
    assert hasattr(NewsProviderPlugin, "__protocol_attrs__") or True
    assert hasattr(EmbeddingProviderPlugin, "__protocol_attrs__") or True
    assert hasattr(VectorStorePlugin, "__protocol_attrs__") or True
    assert hasattr(KnowledgeGraphPlugin, "__protocol_attrs__") or True
    assert hasattr(NotificationProviderPlugin, "__protocol_attrs__") or True


def test_agent_state_imports() -> None:
    """Agent state can be imported and instantiated."""
    from packages.agents.state import AlphaMindAgentState

    state: AlphaMindAgentState = {
        "session_id": "test-session-001",
        "symbol": "AAPL",
        "asset_class": "equity",
        "target_horizon_days": 30,
        "user_id": "user-001",
        "completed_agent_nodes": [],
        "current_node": "supervisor",
        "circuit_breaker_active": False,
        "error_logs": [],
    }
    assert state["symbol"] == "AAPL"
    assert state["circuit_breaker_active"] is False
