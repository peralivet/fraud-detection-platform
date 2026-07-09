"""Tests for the fraud training CLI."""

from pathlib import Path

import pytest

from fraud_detection_platform.cli.train import build_parser


def test_training_cli_parser_requires_data_path() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_training_cli_parser_accepts_required_data_path() -> None:
    parser = build_parser()

    args = parser.parse_args(["--data-path", "data/raw/sample_transactions.csv"])

    assert args.data_path == Path("data/raw/sample_transactions.csv")
    assert args.test_size == 0.25
    assert args.threshold == 0.5
    assert args.random_state == 42
    assert args.model_output_path is None


def test_training_cli_parser_accepts_optional_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--data-path",
            "data/raw/sample_transactions.csv",
            "--test-size",
            "0.3",
            "--threshold",
            "0.7",
            "--random-state",
            "123",
            "--model-output-path",
            "models/baseline_fraud_model.joblib",
        ]
    )

    assert args.data_path == Path("data/raw/sample_transactions.csv")
    assert args.test_size == 0.3
    assert args.threshold == 0.7
    assert args.random_state == 123
    assert args.model_output_path == Path("models/baseline_fraud_model.joblib")
