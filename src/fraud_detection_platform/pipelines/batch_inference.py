"""Batch inference pipeline for fraud detection."""

from dataclasses import dataclass
from pathlib import Path

from fraud_detection_platform.data.loader import load_transaction_data, split_features_and_target
from fraud_detection_platform.data.schema import TARGET_COLUMN, TRANSACTION_ID_COLUMN
from fraud_detection_platform.features.transformers import build_basic_feature_table
from fraud_detection_platform.models.persistence import load_model


@dataclass(frozen=True)
class BatchInferenceConfig:
    """Configuration for the fraud batch inference pipeline."""

    prediction_threshold: float = 0.5


@dataclass(frozen=True)
class BatchInferenceResult:
    """Result returned by the fraud batch inference pipeline."""

    output_path: Path
    scored_rows: int


def run_batch_inference_pipeline(
    data_path: str | Path,
    model_path: str | Path,
    output_path: str | Path,
    config: BatchInferenceConfig | None = None,
) -> BatchInferenceResult:
    """Run batch inference on transaction data using a saved fraud model."""
    resolved_config = config or BatchInferenceConfig()

    raw_data = load_transaction_data(data_path)
    feature_data = build_basic_feature_table(raw_data)
    features, _ = split_features_and_target(feature_data)

    model = load_model(model_path)

    fraud_scores = model.predict_proba(features)[:, 1]
    fraud_predictions = (fraud_scores >= resolved_config.prediction_threshold).astype(int)

    scored_data = raw_data.copy()
    scored_data["fraud_score"] = fraud_scores
    scored_data["fraud_prediction"] = fraud_predictions

    selected_columns = [
        TRANSACTION_ID_COLUMN,
        "fraud_score",
        "fraud_prediction",
        TARGET_COLUMN,
    ]

    resolved_output_path = Path(output_path)
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    scored_data[selected_columns].to_csv(resolved_output_path, index=False)

    return BatchInferenceResult(
        output_path=resolved_output_path,
        scored_rows=len(scored_data),
    )
