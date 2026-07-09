"""Tests for the fraud detection training pipeline."""

from pathlib import Path

import pandas as pd
import pytest

from fraud_detection_platform.models.persistence import load_model
from fraud_detection_platform.pipelines.training import (
    TrainingPipelineConfig,
    run_training_pipeline,
)


@pytest.fixture
def sample_training_data_path(tmp_path: Path) -> Path:
    """Create a small synthetic training dataset for pipeline tests."""
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
    data.to_csv(data_path, index=False)

    return data_path


def test_run_training_pipeline_returns_metrics_and_row_counts(
    sample_training_data_path: Path,
) -> None:
    config = TrainingPipelineConfig(test_size=0.25, random_state=42)

    result = run_training_pipeline(sample_training_data_path, config)

    assert result.train_rows == 15
    assert result.test_rows == 5
    assert 0.0 <= result.metrics.precision <= 1.0
    assert 0.0 <= result.metrics.recall <= 1.0
    assert 0.0 <= result.metrics.f1 <= 1.0
    assert 0.0 <= result.metrics.roc_auc <= 1.0
    assert 0.0 <= result.metrics.pr_auc <= 1.0


def test_run_training_pipeline_saves_model_when_output_path_is_provided(
    sample_training_data_path: Path,
    tmp_path: Path,
) -> None:
    model_output_path = tmp_path / "baseline_model.joblib"

    result = run_training_pipeline(
        sample_training_data_path,
        TrainingPipelineConfig(model_output_path=model_output_path),
    )

    loaded_model = load_model(model_output_path)

    assert result.train_rows == 15
    assert result.test_rows == 5
    assert model_output_path.exists()
    assert loaded_model is not None
