"""Tests for the fraud detection training CLI."""

from pathlib import Path

from fraud_detection_platform.cli.train import build_parser


def test_training_cli_parser_accepts_required_data_path() -> None:
    parser = build_parser()

    args = parser.parse_args(["--data-path", "data/raw/transactions.csv"])

    assert args.data_path == Path("data/raw/transactions.csv")
    assert args.test_size == 0.25
    assert args.threshold == 0.5
    assert args.random_state == 42


def test_training_cli_parser_accepts_optional_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--data-path",
            "data/raw/transactions.csv",
            "--test-size",
            "0.2",
            "--threshold",
            "0.7",
            "--random-state",
            "7",
        ]
    )

    assert args.data_path == Path("data/raw/transactions.csv")
    assert args.test_size == 0.2
    assert args.threshold == 0.7
    assert args.random_state == 7
