"""Tests for the PaySim calibrated batch inference CLI."""

from pathlib import Path

import pytest

from fraud_detection_platform.cli.paysim_batch_inference import build_parser


def test_paysim_batch_inference_cli_requires_required_paths() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_paysim_batch_inference_cli_accepts_required_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--raw-paysim-data-path",
            "data/external/PS_20174392719_1491204439457_log.csv",
            "--model-path",
            "models/paysim_calibrated_fraud_model.joblib",
            "--output-path",
            "reports/paysim_calibrated_scored_transactions.csv",
        ]
    )

    assert args.raw_paysim_data_path == Path("data/external/PS_20174392719_1491204439457_log.csv")
    assert args.model_path == Path("models/paysim_calibrated_fraud_model.joblib")
    assert args.output_path == Path("reports/paysim_calibrated_scored_transactions.csv")
    assert args.threshold == 0.010
    assert args.review_threshold == 0.010
    assert args.high_risk_threshold == 0.075
    assert args.priority_threshold == 0.100


def test_paysim_batch_inference_cli_accepts_custom_thresholds() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--raw-paysim-data-path",
            "data/external/PS_20174392719_1491204439457_log.csv",
            "--model-path",
            "models/paysim_calibrated_fraud_model.joblib",
            "--output-path",
            "reports/paysim_calibrated_scored_transactions.csv",
            "--threshold",
            "0.02",
            "--review-threshold",
            "0.02",
            "--high-risk-threshold",
            "0.08",
            "--priority-threshold",
            "0.15",
        ]
    )

    assert args.threshold == 0.02
    assert args.review_threshold == 0.02
    assert args.high_risk_threshold == 0.08
    assert args.priority_threshold == 0.15


def test_paysim_batch_inference_cli_accepts_production_mode() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--raw-paysim-data-path",
            "data/external/PS_20174392719_1491204439457_log.csv",
            "--model-path",
            "models/paysim_calibrated_fraud_model.joblib",
            "--output-path",
            "reports/paysim_calibrated_scored_transactions_production.csv",
            "--production-mode",
        ]
    )

    assert args.production_mode is True
