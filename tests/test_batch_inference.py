"""Tests for the fraud batch inference pipeline."""

from pathlib import Path

import pandas as pd

from fraud_detection_platform.data.loader import split_features_and_target
from fraud_detection_platform.features.transformers import build_basic_feature_table
from fraud_detection_platform.models.baseline import train_baseline_model
from fraud_detection_platform.models.persistence import save_model
from fraud_detection_platform.pipelines.batch_inference import run_batch_inference_pipeline


def test_run_batch_inference_pipeline_writes_predictions(tmp_path: Path) -> None:
    data = pd.DataFrame(
        {
            "transaction_id": [f"txn_{index:03d}" for index in range(20)],
            "customer_id": [f"cust_{index % 5:03d}" for index in range(20)],
            "transaction_amount": [
                25.0,
                30.0,
                35.0,
                40.0,
                45.0,
                50.0,
                55.0,
                60.0,
                65.0,
                70.0,
                2500.0,
                2600.0,
                2700.0,
                2800.0,
                2900.0,
                3000.0,
                3100.0,
                3200.0,
                3300.0,
                3400.0,
            ],
            "transaction_time": [
                f"2026-01-{(index % 20) + 1:02d} {(index % 24):02d}:00:00" for index in range(20)
            ],
            "merchant_category": [
                "grocery",
                "grocery",
                "grocery",
                "grocery",
                "grocery",
                "grocery",
                "grocery",
                "grocery",
                "grocery",
                "grocery",
                "electronics",
                "electronics",
                "electronics",
                "electronics",
                "electronics",
                "electronics",
                "electronics",
                "electronics",
                "electronics",
                "electronics",
            ],
            "payment_channel": [
                "pos",
                "pos",
                "pos",
                "pos",
                "pos",
                "pos",
                "pos",
                "pos",
                "pos",
                "pos",
                "online",
                "online",
                "online",
                "online",
                "online",
                "online",
                "online",
                "online",
                "online",
                "online",
            ],
            "is_fraud": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        }
    )

    data_path = tmp_path / "transactions.csv"
    model_path = tmp_path / "model.joblib"
    output_path = tmp_path / "predictions.csv"

    data.to_csv(data_path, index=False)

    feature_data = build_basic_feature_table(data)
    features, target = split_features_and_target(feature_data)
    model = train_baseline_model(features, target)
    save_model(model, model_path)

    result = run_batch_inference_pipeline(
        data_path=data_path,
        model_path=model_path,
        output_path=output_path,
    )

    predictions = pd.read_csv(output_path)

    assert result.output_path == output_path
    assert result.scored_rows == 20
    assert output_path.exists()
    assert list(predictions.columns) == [
        "transaction_id",
        "fraud_score",
        "fraud_prediction",
        "recommended_action",
        "is_fraud",
    ]
    assert len(predictions) == 20
    assert predictions["fraud_score"].between(0.0, 1.0).all()
    assert set(predictions["fraud_prediction"].unique()).issubset({0, 1})
    assert set(predictions["recommended_action"].unique()).issubset(
        {"approve", "manual_review", "block"}
    )
