"""Tests for the fraud threshold evaluation CLI."""

from pathlib import Path

import pandas as pd
import pytest

from fraud_detection_platform.cli.evaluate_thresholds import (
    DEFAULT_THRESHOLDS,
    build_parser,
    build_threshold_report,
)


def test_evaluate_thresholds_cli_requires_scores_path_and_output_path() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_evaluate_thresholds_cli_accepts_required_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--scores-path",
            "reports/paysim_enriched_test_scores.csv",
            "--output-path",
            "reports/paysim_threshold_report.csv",
        ]
    )

    assert args.scores_path == Path("reports/paysim_enriched_test_scores.csv")
    assert args.output_path == Path("reports/paysim_threshold_report.csv")
    assert args.thresholds == DEFAULT_THRESHOLDS


def test_evaluate_thresholds_cli_accepts_custom_thresholds() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--scores-path",
            "reports/paysim_enriched_test_scores.csv",
            "--output-path",
            "reports/paysim_threshold_report.csv",
            "--thresholds",
            "0.25",
            "0.5",
            "0.75",
        ]
    )

    assert args.thresholds == [0.25, 0.5, 0.75]


def test_build_threshold_report_writes_expected_columns(tmp_path: Path) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "threshold_report.csv"

    score_data = pd.DataFrame(
        {
            "is_fraud": [0, 0, 1, 1],
            "fraud_score": [0.1, 0.4, 0.6, 0.9],
            "fraud_prediction": [0, 0, 1, 1],
        }
    )
    score_data.to_csv(scores_path, index=False)

    result_path = build_threshold_report(
        scores_path=scores_path,
        output_path=output_path,
        thresholds=[0.3, 0.5, 0.8],
    )

    report_data = pd.read_csv(output_path)

    assert result_path == output_path
    assert output_path.exists()
    assert list(report_data.columns) == [
        "threshold",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "pr_auc",
        "true_negatives",
        "false_positives",
        "false_negatives",
        "true_positives",
    ]
    assert len(report_data) == 3


def test_build_threshold_report_calculates_expected_values(tmp_path: Path) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "threshold_report.csv"

    score_data = pd.DataFrame(
        {
            "is_fraud": [0, 0, 1, 1],
            "fraud_score": [0.1, 0.4, 0.6, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    build_threshold_report(
        scores_path=scores_path,
        output_path=output_path,
        thresholds=[0.5],
    )

    report_data = pd.read_csv(output_path)
    row = report_data.iloc[0]

    assert row["threshold"] == 0.5
    assert row["precision"] == 1.0
    assert row["recall"] == 1.0
    assert row["f1"] == 1.0
    assert row["true_negatives"] == 2
    assert row["false_positives"] == 0
    assert row["false_negatives"] == 0
    assert row["true_positives"] == 2


def test_build_threshold_report_raises_for_missing_required_columns(tmp_path: Path) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "threshold_report.csv"

    score_data = pd.DataFrame(
        {
            "fraud_score": [0.1, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    with pytest.raises(ValueError, match="Score data is missing required columns"):
        build_threshold_report(
            scores_path=scores_path,
            output_path=output_path,
            thresholds=[0.5],
        )
