"""
AlphaMind AI - Prediction Model Registry

Central registry managing model registration, dynamic instantiation, and provider interchangeability.
"""

from __future__ import annotations

import logging

from packages.prediction.models import (
    ARIMAModel,
    BaseForecastModel,
    BayesianModel,
    CatBoostModel,
    LSTMModel,
    ProphetModel,
    RandomForestModel,
    TFTModel,
    TransformerModel,
    XGBoostModel,
)

logger = logging.getLogger(__name__)


class ModelRegistry:
    """Registry managing interchangeable predictive model instances."""

    def __init__(self) -> None:
        self._models: dict[str, BaseForecastModel] = {}
        self._register_default_models()

    def _register_default_models(self) -> None:
        defaults = [
            ARIMAModel(),
            ProphetModel(),
            LSTMModel(),
            TransformerModel(),
            TFTModel(),
            XGBoostModel(),
            CatBoostModel(),
            RandomForestModel(),
            BayesianModel(),
        ]
        for m in defaults:
            self.register_model(m)

    def register_model(self, model: BaseForecastModel) -> None:
        self._models[model.model_id] = model
        logger.info("Registered forecast model '%s' (%s).", model.model_id, model.model_name)

    def get_model(self, model_id: str) -> BaseForecastModel | None:
        return self._models.get(model_id)

    def list_models(self) -> list[dict[str, str]]:
        return [{"model_id": m.model_id, "model_name": m.model_name} for m in self._models.values()]
