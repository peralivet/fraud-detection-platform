"""Calibrated PaySim-enriched fraud model utilities."""

from dataclasses import dataclass
from typing import Literal

import pandas as pd
from sklearn.calibration import CalibratedClassifierCV

from fraud_detection_platform.models.paysim_baseline import (
    PaySimBaselineModelConfig,
    build_paysim_baseline_model,
)

CalibrationMethod = Literal["sigmoid", "isotonic"]


@dataclass(frozen=True)
class CalibratedPaySimModelConfig:
    """Configuration for the calibrated PaySim-enriched fraud model."""

    base_model_config: PaySimBaselineModelConfig = PaySimBaselineModelConfig()
    calibration_method: CalibrationMethod = "sigmoid"
    calibration_cv: int = 3


def build_calibrated_paysim_model(
    config: CalibratedPaySimModelConfig | None = None,
) -> CalibratedClassifierCV:
    """Build a calibrated PaySim-enriched fraud detection model.

    The base estimator is the PaySim-enriched Random Forest pipeline.
    The calibration wrapper learns a mapping from raw model scores to better
    calibrated probability estimates.

    Args:
        config: Optional calibrated model configuration.

    Returns:
        A scikit-learn calibrated classifier.
    """
    resolved_config = config or CalibratedPaySimModelConfig()

    base_model = build_paysim_baseline_model(resolved_config.base_model_config)

    return CalibratedClassifierCV(
        estimator=base_model,
        method=resolved_config.calibration_method,
        cv=resolved_config.calibration_cv,
    )


def train_calibrated_paysim_model(
    features: pd.DataFrame,
    target: pd.Series,
    config: CalibratedPaySimModelConfig | None = None,
) -> CalibratedClassifierCV:
    """Train a calibrated PaySim-enriched fraud detection model."""
    model = build_calibrated_paysim_model(config)
    model.fit(features, target)

    return model
