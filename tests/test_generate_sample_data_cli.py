"""Tests for the synthetic sample data generation CLI."""

from pathlib import Path

from fraud_detection_platform.cli.generate_sample_data import build_parser


def test_generate_sample_data_cli_parser_uses_defaults() -> None:
    parser = build_parser()

    args = parser.parse_args([])

    assert args.output_path == Path("data/raw/sample_transactions.csv")
    assert args.row_count == 100


def test_generate_sample_data_cli_parser_accepts_optional_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--output-path",
            "data/raw/demo_transactions.csv",
            "--row-count",
            "250",
        ]
    )

    assert args.output_path == Path("data/raw/demo_transactions.csv")
    assert args.row_count == 250
