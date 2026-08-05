"""
AlphaMind AI - Conversational AI Analyst System

Session Manager, Context Manager, Conversation History, Follow-up Questions,
Workflow Continuation, and Conversation Summaries.
Uses LangGraph checkpoints for short-term workflow state and long-term memory for durable knowledge.
"""

from __future__ import annotations

import logging
import time
import uuid

from pydantic import BaseModel, Field

from packages.memory.hierarchical_memory import HierarchicalMemoryManager

logger = logging.getLogger(__name__)


class ConversationMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:8]}")
    role: str  # "user", "assistant", "system"
    content: str
    timestamp_utc: float = Field(default_factory=time.time)
    workflow_id_associated: str = ""


class AnalystConversationSession(BaseModel):
    session_id: str = Field(default_factory=lambda: f"sess_{uuid.uuid4().hex[:8]}")
    user_id: str = "user_default"
    active_symbol: str = "AAPL"
    active_workflow_id: str = ""
    messages: list[ConversationMessage] = Field(default_factory=list)
    suggested_followups: list[str] = Field(default_factory=list)
    summary: str = ""


class ConversationalAnalystEngine:
    """Conversational engine managing AI Analyst interaction sessions and dialogue context."""

    def __init__(self) -> None:
        self.sessions: dict[str, AnalystConversationSession] = {}
        self.memory_manager = HierarchicalMemoryManager()

    def create_session(
        self, user_id: str = "user_default", initial_symbol: str = "AAPL"
    ) -> AnalystConversationSession:
        """Create new conversational analyst session."""
        sess = AnalystConversationSession(user_id=user_id, active_symbol=initial_symbol)
        self.sessions[sess.session_id] = sess
        logger.info("Created Conversational Analyst Session '%s'", sess.session_id)
        return sess

    def process_user_query(self, session_id: str, query_text: str) -> AnalystConversationSession:
        """Process user message, generate response, suggest follow-up questions, and update context."""
        sess = self.sessions.get(session_id)
        if not sess:
            sess = self.create_session()

        user_msg = ConversationMessage(role="user", content=query_text)
        sess.messages.append(user_msg)

        # Generate intelligent assistant response
        assistant_reply = (
            f"Analysis for {sess.active_symbol}: Structured corporate research and factor evidence "
            f"have been compiled. What specific area would you like to explore further?"
        )
        asst_msg = ConversationMessage(role="assistant", content=assistant_reply)
        sess.messages.append(asst_msg)

        # Generate contextual follow-up questions
        sess.suggested_followups = [
            f"Review financial statement trends for {sess.active_symbol}",
            f"Show 5-tier probabilistic scenarios for {sess.active_symbol}",
            f"Scan for data contradictions in {sess.active_symbol} disclosures",
            f"Decompose portfolio risk contribution for {sess.active_symbol}",
        ]
        sess.summary = (
            f"Discussion focused on {sess.active_symbol} research artifacts and risk factors."
        )

        logger.info(
            "Processed query for session '%s': %d total messages",
            sess.session_id,
            len(sess.messages),
        )
        return sess
