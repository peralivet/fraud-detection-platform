"""Tests for the fraud batch inference CLI."""

from pathlib import Path

import pytest

from fraud_detection_platform.cli.batch_inference import build_parser


def test_batch_inference_cli_parser_requires_required_arguments() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_batch_inference_cli_parser_accepts_required_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--data-path",
            "data/raw/sample_transactions.csv",
            "--model-path",
            "models/baseline_fraud_model.joblib",
            "--output-path",
            "data/processed/fraud_predictions.csv",
        ]
    )

    assert args.data_path == Path("data/raw/sample_transactions.csv")
    assert args.model_path == Path("models/baseline_fraud_model.joblib")
    assert args.output_path == Path("data/processed/fraud_predictions.csv")
    assert args.threshold == 0.5


def test_batch_inference_cli_parser_accepts_threshold() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--data-path",
            "data/raw/sample_transactions.csv",
            "--model-path",
            "models/baseline_fraud_model.joblib",
            "--output-path",
            "data/processed/fraud_predictions.csv",
            "--threshold",
            "0.7",
        ]
    )

    assert args.threshold == 0.7
