"""PaySim-enriched training pipeline for fraud detection."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from fraud_detection_platform.data.paysim import transform_paysim_to_platform_schema
from fraud_detection_platform.evaluation.metrics import (
    ClassificationMetrics,
    calculate_classification_metrics,
)
from fraud_detection_platform.features.paysim_features import add_paysim_balance_features
from fraud_detection_platform.features.transformers import build_basic_feature_table
from fraud_detection_platform.models.paysim_baseline import (
    PaySimBaselineModelConfig,
    select_paysim_enriched_features,
    train_paysim_baseline_model,
)
from fraud_detection_platform.models.persistence import save_model


@dataclass(frozen=True)
class PaySimTrainingPipelineConfig:
    """Configuration for the PaySim-enriched training pipeline."""

    test_size: float = 0.25
    random_state: int = 42
    prediction_threshold: float = 0.5
    model_config: PaySimBaselineModelConfig = PaySimBaselineModelConfig()
    model_output_path: Path | None = None


@dataclass(frozen=True)
class PaySimTrainingPipelineResult:
    """Result returned by the PaySim-enriched training pipeline."""

    metrics: ClassificationMetrics
    train_rows: int
    test_rows: int


def run_paysim_training_pipeline(
    raw_paysim_data_path: str | Path,
    config: PaySimTrainingPipelineConfig | None = None,
) -> PaySimTrainingPipelineResult:
    """Run the PaySim-enriched fraud detection training pipeline."""
    resolved_config = config or PaySimTrainingPipelineConfig()

    raw_paysim_data = pd.read_csv(raw_paysim_data_path)

    paysim_balance_data = add_paysim_balance_features(raw_paysim_data)
    platform_data = transform_paysim_to_platform_schema(paysim_balance_data)
    feature_data = build_basic_feature_table(platform_data)

    enriched_feature_data = pd.concat(
        [
            feature_data,
            paysim_balance_data[
                [
                    "origin_balance_delta",
                    "destination_balance_delta",
                    "amount_to_origin_balance_ratio",
                    "amount_to_destination_balance_ratio",
                ]
            ],
        ],
        axis=1,
    )

    features = select_paysim_enriched_features(enriched_feature_data)
    target = enriched_feature_data["is_fraud"].copy()

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=resolved_config.test_size,
        random_state=resolved_config.random_state,
        stratify=target,
    )

    model = train_paysim_baseline_model(
        features=x_train,
        target=y_train,
        config=resolved_config.model_config,
    )

    fraud_scores = model.predict_proba(x_test)[:, 1]
    fraud_predictions = (fraud_scores >= resolved_config.prediction_threshold).astype(int)

    metrics = calculate_classification_metrics(
        y_true=y_test.tolist(),
        y_pred=fraud_predictions.tolist(),
        y_score=fraud_scores.tolist(),
    )

    if resolved_config.model_output_path is not None:
        save_model(model, resolved_config.model_output_path)

    return PaySimTrainingPipelineResult(
        metrics=metrics,
        train_rows=len(x_train),
        test_rows=len(x_test),
    )
