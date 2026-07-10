"""Tests for the PaySim-enriched training CLI."""

from pathlib import Path

import pytest

from fraud_detection_platform.cli.train_paysim_enriched import build_parser


def test_train_paysim_enriched_cli_requires_raw_paysim_data_path() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_train_paysim_enriched_cli_accepts_required_argument() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--raw-paysim-data-path",
            "data/external/PS_20174392719_1491204439457_log.csv",
        ]
    )

    assert args.raw_paysim_data_path == Path("data/external/PS_20174392719_1491204439457_log.csv")
    assert args.test_size == 0.25
    assert args.threshold == 0.5
    assert args.random_state == 42
    assert args.model_output_path is None
    assert args.scores_output_path is None


def test_train_paysim_enriched_cli_accepts_optional_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--raw-paysim-data-path",
            "data/external/PS_20174392719_1491204439457_log.csv",
            "--test-size",
            "0.3",
            "--threshold",
            "0.7",
            "--random-state",
            "123",
            "--model-output-path",
            "models/paysim_enriched_fraud_model.joblib",
            "--scores-output-path",
            "reports/paysim_enriched_test_scores.csv",
        ]
    )

    assert args.raw_paysim_data_path == Path("data/external/PS_20174392719_1491204439457_log.csv")
    assert args.test_size == 0.3
    assert args.threshold == 0.7
    assert args.random_state == 123
    assert args.model_output_path == Path("models/paysim_enriched_fraud_model.joblib")
    assert args.scores_output_path == Path("reports/paysim_enriched_test_scores.csv")
