"""Training pipeline for the fraud detection platform."""

from dataclasses import dataclass
from pathlib import Path

from sklearn.model_selection import train_test_split

from fraud_detection_platform.data.loader import load_transaction_data, split_features_and_target
from fraud_detection_platform.evaluation.metrics import (
    ClassificationMetrics,
    calculate_classification_metrics,
)
from fraud_detection_platform.features.transformers import build_basic_feature_table
from fraud_detection_platform.models.baseline import BaselineModelConfig, train_baseline_model


@dataclass(frozen=True)
class TrainingPipelineConfig:
    """Configuration for the fraud detection training pipeline."""

    test_size: float = 0.25
    random_state: int = 42
    prediction_threshold: float = 0.5
    model_config: BaselineModelConfig = BaselineModelConfig()


@dataclass(frozen=True)
class TrainingPipelineResult:
    """Result returned by the fraud detection training pipeline."""

    metrics: ClassificationMetrics
    train_rows: int
    test_rows: int


def run_training_pipeline(
    data_path: str | Path,
    config: TrainingPipelineConfig | None = None,
) -> TrainingPipelineResult:
    """Run the end-to-end fraud detection training pipeline.

    Args:
        data_path: Path to the transaction CSV dataset.
        config: Optional training pipeline configuration.

    Returns:
        Training pipeline result containing metrics and row counts.
    """
    resolved_config = config or TrainingPipelineConfig()

    raw_data = load_transaction_data(data_path)
    feature_data = build_basic_feature_table(raw_data)
    features, target = split_features_and_target(feature_data)

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=resolved_config.test_size,
        random_state=resolved_config.random_state,
        stratify=target,
    )

    model = train_baseline_model(x_train, y_train, resolved_config.model_config)

    fraud_scores = model.predict_proba(x_test)[:, 1]
    fraud_predictions = (fraud_scores >= resolved_config.prediction_threshold).astype(int)

    metrics = calculate_classification_metrics(
        y_true=y_test.tolist(),
        y_pred=fraud_predictions.tolist(),
        y_score=fraud_scores.tolist(),
    )

    return TrainingPipelineResult(
        metrics=metrics,
        train_rows=len(x_train),
        test_rows=len(x_test),
    )
