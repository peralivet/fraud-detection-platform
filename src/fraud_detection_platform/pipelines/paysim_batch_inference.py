"""PaySim-enriched batch inference pipeline for calibrated fraud models."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from fraud_detection_platform.data.paysim import transform_paysim_to_platform_schema
from fraud_detection_platform.data.schema import TARGET_COLUMN, TRANSACTION_ID_COLUMN
from fraud_detection_platform.features.paysim_features import add_paysim_balance_features
from fraud_detection_platform.features.transformers import build_basic_feature_table
from fraud_detection_platform.models.paysim_baseline import select_paysim_enriched_features
from fraud_detection_platform.models.persistence import load_model
from fraud_detection_platform.risk.calibrated_decision_policy import (
    CalibratedRiskDecisionPolicy,
    recommend_calibrated_action,
)


@dataclass(frozen=True)
class PaySimBatchInferenceConfig:
    """Configuration for PaySim calibrated batch inference."""

    prediction_threshold: float = 0.010
    risk_policy: CalibratedRiskDecisionPolicy = CalibratedRiskDecisionPolicy()
    include_labels: bool = True


@dataclass(frozen=True)
class PaySimBatchInferenceResult:
    """Result returned by PaySim calibrated batch inference."""

    output_path: Path
    scored_rows: int


def run_paysim_batch_inference_pipeline(
    raw_paysim_data_path: str | Path,
    model_path: str | Path,
    output_path: str | Path,
    config: PaySimBatchInferenceConfig | None = None,
) -> PaySimBatchInferenceResult:
    """Run calibrated PaySim batch inference.

    Args:
        raw_paysim_data_path: Path to raw PaySim-style CSV data.
        model_path: Path to a saved calibrated PaySim model.
        output_path: Path where scored output should be written.
        config: Optional inference configuration.

    Returns:
        Batch inference result containing output path and scored row count.
    """
    resolved_config = config or PaySimBatchInferenceConfig()

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
    model = load_model(model_path)

    fraud_scores = model.predict_proba(features)[:, 1]
    fraud_predictions = (fraud_scores >= resolved_config.prediction_threshold).astype(int)

    scored_data = platform_data.copy()
    scored_data["fraud_score"] = fraud_scores
    scored_data["fraud_prediction"] = fraud_predictions
    scored_data["recommended_action"] = [
        recommend_calibrated_action(
            fraud_score=float(score),
            policy=resolved_config.risk_policy,
        )
        for score in fraud_scores
    ]

    selected_columns = [
        TRANSACTION_ID_COLUMN,
        "customer_id",
        "transaction_time",
        "transaction_amount",
        "merchant_category",
        "payment_channel",
        "fraud_score",
        "fraud_prediction",
        "recommended_action",
    ]

    if resolved_config.include_labels and TARGET_COLUMN in scored_data.columns:
        selected_columns.append(TARGET_COLUMN)

    resolved_output_path = Path(output_path)
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    scored_data[selected_columns].to_csv(resolved_output_path, index=False)

    return PaySimBatchInferenceResult(
        output_path=resolved_output_path,
        scored_rows=len(scored_data),
    )
