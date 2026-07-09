"""Tests for the fraud detection training pipeline."""

from pathlib import Path

import pandas as pd

from fraud_detection_platform.pipelines.training import (
    TrainingPipelineConfig,
    run_training_pipeline,
)


def test_run_training_pipeline_returns_metrics_and_row_counts(tmp_path: Path) -> None:
    data_path = tmp_path / "transactions.csv"

    data = pd.DataFrame(
        {
            "transaction_id": [f"txn_{index:03d}" for index in range(20)],
            "customer_id": [f"cust_{index % 5}" for index in range(20)],
            "transaction_amount": [
                25.0,
                30.0,
                22.0,
                28.0,
                35.0,
                40.0,
                26.0,
                33.0,
                27.0,
                31.0,
                2500.0,
                3000.0,
                2750.0,
                3200.0,
                2600.0,
                3100.0,
                2900.0,
                3300.0,
                2800.0,
                3400.0,
            ],
            "transaction_time": [
                "2026-01-01 10:00:00",
                "2026-01-01 11:00:00",
                "2026-01-01 12:00:00",
                "2026-01-01 13:00:00",
                "2026-01-01 14:00:00",
                "2026-01-01 15:00:00",
                "2026-01-01 16:00:00",
                "2026-01-01 17:00:00",
                "2026-01-01 18:00:00",
                "2026-01-01 19:00:00",
                "2026-01-02 01:00:00",
                "2026-01-02 02:00:00",
                "2026-01-02 03:00:00",
                "2026-01-02 04:00:00",
                "2026-01-02 05:00:00",
                "2026-01-02 06:00:00",
                "2026-01-02 07:00:00",
                "2026-01-02 08:00:00",
                "2026-01-02 09:00:00",
                "2026-01-02 10:00:00",
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
                "travel",
                "travel",
                "travel",
                "crypto",
                "crypto",
                "crypto",
                "crypto",
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
    data.to_csv(data_path, index=False)

    config = TrainingPipelineConfig(test_size=0.25, random_state=42)
    result = run_training_pipeline(data_path, config)

    assert result.train_rows == 15
    assert result.test_rows == 5
    assert 0.0 <= result.metrics.precision <= 1.0
    assert 0.0 <= result.metrics.recall <= 1.0
    assert 0.0 <= result.metrics.f1 <= 1.0
    assert 0.0 <= result.metrics.roc_auc <= 1.0
    assert 0.0 <= result.metrics.pr_auc <= 1.0
