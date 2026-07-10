"""Tests for PaySim calibrated batch inference pipeline."""

from pathlib import Path

import numpy as np
import pandas as pd

from fraud_detection_platform.models.persistence import save_model
from fraud_detection_platform.pipelines.paysim_batch_inference import (
    PaySimBatchInferenceConfig,
    run_paysim_batch_inference_pipeline,
)
from fraud_detection_platform.risk.calibrated_decision_policy import (
    CalibratedRiskDecisionPolicy,
)


class FakeCalibratedPaySimModel:
    """Simple fake model for testing calibrated PaySim inference."""

    def predict_proba(self, features: pd.DataFrame) -> np.ndarray:
        """Return deterministic fraud probabilities."""

        scores = [0.005, 0.020, 0.080, 0.120]

        return np.array([[1.0 - score, score] for score in scores[: len(features)]])


def test_run_paysim_batch_inference_pipeline_writes_scored_output(
    tmp_path: Path,
) -> None:
    raw_paysim_data = pd.DataFrame(
        {
            "step": [1, 2, 3, 4],
            "type": ["PAYMENT", "TRANSFER", "CASH_OUT", "TRANSFER"],
            "amount": [25.0, 2500.0, 3000.0, 4000.0],
            "nameOrig": ["C001", "C002", "C003", "C004"],
            "oldbalanceOrg": [1000.0, 2500.0, 3000.0, 4000.0],
            "newbalanceOrig": [975.0, 0.0, 0.0, 0.0],
            "nameDest": ["D001", "D002", "D003", "D004"],
            "oldbalanceDest": [500.0, 0.0, 0.0, 0.0],
            "newbalanceDest": [525.0, 2500.0, 3000.0, 4000.0],
            "isFraud": [0, 1, 1, 1],
        }
    )

    raw_paysim_path = tmp_path / "raw_paysim.csv"
    model_path = tmp_path / "fake_model.joblib"
    output_path = tmp_path / "scored_paysim.csv"

    raw_paysim_data.to_csv(raw_paysim_path, index=False)
    save_model(FakeCalibratedPaySimModel(), model_path)

    result = run_paysim_batch_inference_pipeline(
        raw_paysim_data_path=raw_paysim_path,
        model_path=model_path,
        output_path=output_path,
        config=PaySimBatchInferenceConfig(
            prediction_threshold=0.010,
            risk_policy=CalibratedRiskDecisionPolicy(
                review_threshold=0.010,
                high_risk_threshold=0.075,
                priority_threshold=0.100,
            ),
        ),
    )

    scored_data = pd.read_csv(output_path)

    assert result.output_path == output_path
    assert result.scored_rows == 4
    assert output_path.exists()
    assert list(scored_data.columns) == [
        "transaction_id",
        "customer_id",
        "transaction_time",
        "transaction_amount",
        "merchant_category",
        "payment_channel",
        "fraud_score",
        "fraud_prediction",
        "recommended_action",
        "is_fraud",
    ]
    assert scored_data["fraud_score"].tolist() == [0.005, 0.020, 0.080, 0.120]
    assert scored_data["fraud_prediction"].tolist() == [0, 1, 1, 1]
    assert scored_data["recommended_action"].tolist() == [
        "approve",
        "manual_review",
        "high_risk_review",
        "priority_investigation",
    ]


def test_run_paysim_batch_inference_pipeline_supports_custom_policy(
    tmp_path: Path,
) -> None:
    raw_paysim_data = pd.DataFrame(
        {
            "step": [1, 2],
            "type": ["PAYMENT", "TRANSFER"],
            "amount": [25.0, 2500.0],
            "nameOrig": ["C001", "C002"],
            "oldbalanceOrg": [1000.0, 2500.0],
            "newbalanceOrig": [975.0, 0.0],
            "nameDest": ["D001", "D002"],
            "oldbalanceDest": [500.0, 0.0],
            "newbalanceDest": [525.0, 2500.0],
            "isFraud": [0, 1],
        }
    )

    raw_paysim_path = tmp_path / "raw_paysim.csv"
    model_path = tmp_path / "fake_model.joblib"
    output_path = tmp_path / "scored_paysim.csv"

    raw_paysim_data.to_csv(raw_paysim_path, index=False)
    save_model(FakeCalibratedPaySimModel(), model_path)

    run_paysim_batch_inference_pipeline(
        raw_paysim_data_path=raw_paysim_path,
        model_path=model_path,
        output_path=output_path,
        config=PaySimBatchInferenceConfig(
            prediction_threshold=0.050,
            risk_policy=CalibratedRiskDecisionPolicy(
                review_threshold=0.015,
                high_risk_threshold=0.050,
                priority_threshold=0.100,
            ),
        ),
    )

    scored_data = pd.read_csv(output_path)

    assert scored_data["fraud_prediction"].tolist() == [0, 0]
    assert scored_data["recommended_action"].tolist() == [
        "approve",
        "manual_review",
    ]


def test_run_paysim_batch_inference_pipeline_can_omit_labels_for_production_scoring(
    tmp_path: Path,
) -> None:
    raw_paysim_data = pd.DataFrame(
        {
            "step": [1, 2],
            "type": ["PAYMENT", "TRANSFER"],
            "amount": [25.0, 2500.0],
            "nameOrig": ["C001", "C002"],
            "oldbalanceOrg": [1000.0, 2500.0],
            "newbalanceOrig": [975.0, 0.0],
            "nameDest": ["D001", "D002"],
            "oldbalanceDest": [500.0, 0.0],
            "newbalanceDest": [525.0, 2500.0],
            "isFraud": [0, 1],
        }
    )

    raw_paysim_path = tmp_path / "raw_paysim.csv"
    model_path = tmp_path / "fake_model.joblib"
    output_path = tmp_path / "production_scored_paysim.csv"

    raw_paysim_data.to_csv(raw_paysim_path, index=False)
    save_model(FakeCalibratedPaySimModel(), model_path)

    run_paysim_batch_inference_pipeline(
        raw_paysim_data_path=raw_paysim_path,
        model_path=model_path,
        output_path=output_path,
        config=PaySimBatchInferenceConfig(
            prediction_threshold=0.010,
            include_labels=False,
        ),
    )

    scored_data = pd.read_csv(output_path)

    assert list(scored_data.columns) == [
        "transaction_id",
        "customer_id",
        "transaction_time",
        "transaction_amount",
        "merchant_category",
        "payment_channel",
        "fraud_score",
        "fraud_prediction",
        "recommended_action",
    ]
    assert "is_fraud" not in scored_data.columns
