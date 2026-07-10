"""Tests for the cost-sensitive fraud threshold evaluation CLI."""

from pathlib import Path

import pandas as pd
import pytest

from fraud_detection_platform.cli.evaluate_threshold_costs import (
    build_parser,
    build_threshold_cost_report,
)
from fraud_detection_platform.cli.evaluate_thresholds import DEFAULT_THRESHOLDS
from fraud_detection_platform.evaluation.costs import FraudCostConfig


def test_evaluate_threshold_costs_cli_requires_scores_path_and_output_path() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_evaluate_threshold_costs_cli_accepts_required_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--scores-path",
            "reports/paysim_calibrated_test_scores.csv",
            "--output-path",
            "reports/paysim_calibrated_cost_report.csv",
        ]
    )

    assert args.scores_path == Path("reports/paysim_calibrated_test_scores.csv")
    assert args.output_path == Path("reports/paysim_calibrated_cost_report.csv")
    assert args.thresholds == DEFAULT_THRESHOLDS
    assert args.false_positive_cost == 5.0
    assert args.false_negative_cost == 500.0
    assert args.manual_review_cost == 2.0


def test_evaluate_threshold_costs_cli_accepts_custom_cost_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--scores-path",
            "reports/paysim_calibrated_test_scores.csv",
            "--output-path",
            "reports/paysim_calibrated_cost_report.csv",
            "--thresholds",
            "0.01",
            "0.05",
            "0.10",
            "--false-positive-cost",
            "10",
            "--false-negative-cost",
            "1000",
            "--manual-review-cost",
            "3",
        ]
    )

    assert args.thresholds == [0.01, 0.05, 0.10]
    assert args.false_positive_cost == 10.0
    assert args.false_negative_cost == 1000.0
    assert args.manual_review_cost == 3.0


def test_build_threshold_cost_report_writes_expected_columns(tmp_path: Path) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "cost_report.csv"

    score_data = pd.DataFrame(
        {
            "is_fraud": [0, 0, 1, 1],
            "fraud_score": [0.1, 0.4, 0.6, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    result_path = build_threshold_cost_report(
        scores_path=scores_path,
        output_path=output_path,
        thresholds=[0.3, 0.5, 0.8],
        cost_config=FraudCostConfig(
            false_positive_cost=5.0,
            false_negative_cost=500.0,
            manual_review_cost=2.0,
        ),
    )

    report_data = pd.read_csv(output_path)

    assert result_path == output_path
    assert output_path.exists()
    assert list(report_data.columns) == [
        "threshold",
        "false_positive_count",
        "false_negative_count",
        "predicted_positive_count",
        "false_positive_cost",
        "false_negative_cost",
        "manual_review_cost",
        "total_cost",
    ]
    assert len(report_data) == 3


def test_build_threshold_cost_report_calculates_expected_values(tmp_path: Path) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "cost_report.csv"

    score_data = pd.DataFrame(
        {
            "is_fraud": [0, 0, 1, 1],
            "fraud_score": [0.1, 0.4, 0.6, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    build_threshold_cost_report(
        scores_path=scores_path,
        output_path=output_path,
        thresholds=[0.3],
        cost_config=FraudCostConfig(
            false_positive_cost=5.0,
            false_negative_cost=500.0,
            manual_review_cost=2.0,
        ),
    )

    report_data = pd.read_csv(output_path)
    row = report_data.iloc[0]

    assert row["threshold"] == 0.3
    assert row["false_positive_count"] == 1
    assert row["false_negative_count"] == 0
    assert row["predicted_positive_count"] == 3
    assert row["false_positive_cost"] == 5.0
    assert row["false_negative_cost"] == 0.0
    assert row["manual_review_cost"] == 6.0
    assert row["total_cost"] == 11.0


def test_build_threshold_cost_report_raises_for_missing_required_columns(
    tmp_path: Path,
) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "cost_report.csv"

    score_data = pd.DataFrame(
        {
            "fraud_score": [0.1, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    with pytest.raises(ValueError, match="Score data is missing required columns"):
        build_threshold_cost_report(
            scores_path=scores_path,
            output_path=output_path,
            thresholds=[0.5],
        )
