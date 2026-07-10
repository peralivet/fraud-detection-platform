"""Tests for the PaySim-enriched training pipeline."""

from pathlib import Path

import pandas as pd

from fraud_detection_platform.models.persistence import load_model
from fraud_detection_platform.pipelines.paysim_training import (
    PaySimTrainingPipelineConfig,
    run_paysim_training_pipeline,
)


def test_run_paysim_training_pipeline_returns_metrics_row_counts_and_scores_file(
    tmp_path: Path,
) -> None:
    raw_paysim_data = pd.DataFrame(
        {
            "step": [index + 1 for index in range(20)],
            "type": [
                "PAYMENT",
                "PAYMENT",
                "PAYMENT",
                "PAYMENT",
                "PAYMENT",
                "CASH_IN",
                "CASH_IN",
                "CASH_IN",
                "CASH_IN",
                "CASH_IN",
                "TRANSFER",
                "TRANSFER",
                "TRANSFER",
                "TRANSFER",
                "TRANSFER",
                "CASH_OUT",
                "CASH_OUT",
                "CASH_OUT",
                "CASH_OUT",
                "CASH_OUT",
            ],
            "amount": [
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
            "nameOrig": [f"C{index % 5:03d}" for index in range(20)],
            "oldbalanceOrg": [
                1000.0,
                1000.0,
                1000.0,
                1000.0,
                1000.0,
                1000.0,
                1000.0,
                1000.0,
                1000.0,
                1000.0,
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
            "newbalanceOrig": [
                975.0,
                970.0,
                965.0,
                960.0,
                955.0,
                1050.0,
                1055.0,
                1060.0,
                1065.0,
                1070.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
            "nameDest": [f"D{index % 5:03d}" for index in range(20)],
            "oldbalanceDest": [
                500.0,
                500.0,
                500.0,
                500.0,
                500.0,
                500.0,
                500.0,
                500.0,
                500.0,
                500.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
            "newbalanceDest": [
                525.0,
                530.0,
                535.0,
                540.0,
                545.0,
                450.0,
                445.0,
                440.0,
                435.0,
                430.0,
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
            "isFraud": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
            ],
        }
    )

    raw_paysim_path = tmp_path / "raw_paysim.csv"
    model_output_path = tmp_path / "paysim_model.joblib"
    scores_output_path = tmp_path / "paysim_scores.csv"

    raw_paysim_data.to_csv(raw_paysim_path, index=False)

    result = run_paysim_training_pipeline(
        raw_paysim_data_path=raw_paysim_path,
        config=PaySimTrainingPipelineConfig(
            model_output_path=model_output_path,
            scores_output_path=scores_output_path,
        ),
    )

    loaded_model = load_model(model_output_path)
    score_data = pd.read_csv(scores_output_path)

    assert result.train_rows == 15
    assert result.test_rows == 5
    assert model_output_path.exists()
    assert scores_output_path.exists()
    assert result.scores_output_path == scores_output_path
    assert loaded_model is not None
    assert list(score_data.columns) == ["is_fraud", "fraud_score", "fraud_prediction"]
    assert len(score_data) == result.test_rows
    assert 0.0 <= result.metrics.precision <= 1.0
    assert 0.0 <= result.metrics.recall <= 1.0
    assert 0.0 <= result.metrics.f1 <= 1.0
    assert 0.0 <= result.metrics.roc_auc <= 1.0
    assert 0.0 <= result.metrics.pr_auc <= 1.0


def test_run_paysim_training_pipeline_supports_calibrated_model(
    tmp_path: Path,
) -> None:
    raw_paysim_data = pd.DataFrame(
        {
            "step": [index + 1 for index in range(40)],
            "type": [
                *(["PAYMENT"] * 20),
                *(["TRANSFER"] * 10),
                *(["CASH_OUT"] * 10),
            ],
            "amount": [
                *[float(25 + index * 5) for index in range(20)],
                *[float(2500 + index * 100) for index in range(20)],
            ],
            "nameOrig": [f"C{index % 5:03d}" for index in range(40)],
            "oldbalanceOrg": [
                *(1000.0 for _ in range(20)),
                *[float(2500 + index * 100) for index in range(20)],
            ],
            "newbalanceOrig": [
                *[float(975 - index * 5) for index in range(20)],
                *(0.0 for _ in range(20)),
            ],
            "nameDest": [f"D{index % 5:03d}" for index in range(40)],
            "oldbalanceDest": [
                *(500.0 for _ in range(20)),
                *(0.0 for _ in range(20)),
            ],
            "newbalanceDest": [
                *[float(525 + index * 5) for index in range(20)],
                *[float(2500 + index * 100) for index in range(20)],
            ],
            "isFraud": [
                *(0 for _ in range(20)),
                *(1 for _ in range(20)),
            ],
        }
    )

    raw_paysim_path = tmp_path / "raw_paysim.csv"
    model_output_path = tmp_path / "paysim_calibrated_model.joblib"
    scores_output_path = tmp_path / "paysim_calibrated_scores.csv"

    raw_paysim_data.to_csv(raw_paysim_path, index=False)

    result = run_paysim_training_pipeline(
        raw_paysim_data_path=raw_paysim_path,
        config=PaySimTrainingPipelineConfig(
            model_type="calibrated",
            model_output_path=model_output_path,
            scores_output_path=scores_output_path,
        ),
    )

    score_data = pd.read_csv(scores_output_path)

    assert result.train_rows == 30
    assert result.test_rows == 10
    assert model_output_path.exists()
    assert scores_output_path.exists()
    assert result.scores_output_path == scores_output_path
    assert list(score_data.columns) == ["is_fraud", "fraud_score", "fraud_prediction"]
    assert len(score_data) == result.test_rows
    assert 0.0 <= result.metrics.precision <= 1.0
    assert 0.0 <= result.metrics.recall <= 1.0
    assert 0.0 <= result.metrics.f1 <= 1.0
    assert 0.0 <= result.metrics.roc_auc <= 1.0
    assert 0.0 <= result.metrics.pr_auc <= 1.0
