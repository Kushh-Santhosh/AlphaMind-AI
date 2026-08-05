"""
AlphaMind AI - Master Analyst Orchestrator

Central orchestrator coordinating Workflow Runtime, Research Engine, Knowledge Graph,
Financial Intelligence, Forecast Engine, Portfolio Engine, and Continuous Evaluation.
Reuses existing components exclusively with zero duplicate business logic.
"""

from __future__ import annotations

import logging

from packages.agents.execution_engine import WorkflowExecutionEngine
from packages.agents.registry import GraphBuilder
from packages.agents.supervisor import SupervisorOrchestrator
from packages.knowledge_graph.ingestion import GraphIngestionEngine
from packages.memory.hierarchical_memory import HierarchicalMemoryManager
from packages.portfolio.analytics import PortfolioAnalyticsEngine
from packages.portfolio.risk_engine import QuantitativeRiskEngine
from packages.prediction.ensemble_engine import EnsembleEngine
from packages.prediction.model_registry import ModelRegistry
from packages.prediction.scenario_engine import ScenarioEngine
from packages.research.company_engine import CompanyResearchEngine
from packages.research.contradiction_engine import ContradictionEngine
from packages.research.factor_extractor import FactorExtractionEngine
from packages.research.financial_statement_engine import FinancialStatementEngine
from packages.research.macro_engine import MacroeconomicEngine
from packages.research.news_engine import NewsEngine

logger = logging.getLogger(__name__)


class MasterAnalystOrchestrator:
    """
    Master Orchestrator connecting all completed platform engines into a unified AI Analyst framework.
    """

    def __init__(self) -> None:
        self.graph_builder = GraphBuilder("MasterAnalystGraph")
        self.supervisor = SupervisorOrchestrator()
        self.execution_engine = WorkflowExecutionEngine(self.graph_builder)

        # Engine Registries & Instances
        self.company_engine = CompanyResearchEngine()
        self.financial_engine = FinancialStatementEngine()
        self.news_engine = NewsEngine()
        self.macro_engine = MacroeconomicEngine()
        self.factor_extractor = FactorExtractionEngine()
        self.contradiction_engine = ContradictionEngine()

        self.graph_ingest = GraphIngestionEngine()
        self.model_registry = ModelRegistry()
        self.ensemble_engine = EnsembleEngine(self.model_registry)
        self.scenario_engine = ScenarioEngine()

        self.risk_engine = QuantitativeRiskEngine()
        self.portfolio_analytics = PortfolioAnalyticsEngine()
        self.memory_manager = HierarchicalMemoryManager()

        logger.info("Initialized MasterAnalystOrchestrator connecting all 11 platform subsystems.")
