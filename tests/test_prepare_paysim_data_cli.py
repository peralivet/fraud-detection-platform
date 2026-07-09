"""Tests for the PaySim preparation CLI."""

from pathlib import Path

import pytest

from fraud_detection_platform.cli.prepare_paysim_data import build_parser


def test_prepare_paysim_data_cli_requires_input_and_output_paths() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_prepare_paysim_data_cli_accepts_required_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--input-path",
            "data/external/paysim.csv",
            "--output-path",
            "data/raw/paysim_transactions.csv",
        ]
    )

    assert args.input_path == Path("data/external/paysim.csv")
    assert args.output_path == Path("data/raw/paysim_transactions.csv")
    assert args.start_time == "2026-01-01 00:00:00"


def test_prepare_paysim_data_cli_accepts_custom_start_time() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--input-path",
            "data/external/paysim.csv",
            "--output-path",
            "data/raw/paysim_transactions.csv",
            "--start-time",
            "2025-01-01 00:00:00",
        ]
    )

    assert args.start_time == "2025-01-01 00:00:00"
