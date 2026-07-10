"""Tests for the fraud cost scenario comparison CLI."""

from pathlib import Path

import pandas as pd
import pytest

from fraud_detection_platform.cli.evaluate_cost_scenarios import (
    build_cost_scenario_reports,
    build_parser,
)


def test_evaluate_cost_scenarios_cli_requires_paths() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_evaluate_cost_scenarios_cli_accepts_required_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--scores-path",
            "reports/paysim_calibrated_test_scores.csv",
            "--output-path",
            "reports/paysim_cost_scenario_report.csv",
            "--best-output-path",
            "reports/paysim_cost_scenario_best_thresholds.csv",
        ]
    )

    assert args.scores_path == Path("reports/paysim_calibrated_test_scores.csv")
    assert args.output_path == Path("reports/paysim_cost_scenario_report.csv")
    assert args.best_output_path == Path("reports/paysim_cost_scenario_best_thresholds.csv")


def test_evaluate_cost_scenarios_cli_accepts_custom_thresholds() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--scores-path",
            "reports/paysim_calibrated_test_scores.csv",
            "--output-path",
            "reports/paysim_cost_scenario_report.csv",
            "--best-output-path",
            "reports/paysim_cost_scenario_best_thresholds.csv",
            "--thresholds",
            "0.01",
            "0.05",
            "0.10",
        ]
    )

    assert args.thresholds == [0.01, 0.05, 0.10]


def test_build_cost_scenario_reports_writes_expected_files(tmp_path: Path) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "scenario_report.csv"
    best_output_path = tmp_path / "best_thresholds.csv"

    score_data = pd.DataFrame(
        {
            "is_fraud": [0, 0, 1, 1],
            "fraud_score": [0.1, 0.4, 0.6, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    result_output_path, result_best_output_path = build_cost_scenario_reports(
        scores_path=scores_path,
        output_path=output_path,
        best_output_path=best_output_path,
        thresholds=[0.3, 0.8],
    )

    scenario_report = pd.read_csv(output_path)
    best_report = pd.read_csv(best_output_path)

    assert result_output_path == output_path
    assert result_best_output_path == best_output_path
    assert output_path.exists()
    assert best_output_path.exists()
    assert len(scenario_report) == 8
    assert len(best_report) == 4


def test_build_cost_scenario_reports_writes_expected_columns(tmp_path: Path) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "scenario_report.csv"
    best_output_path = tmp_path / "best_thresholds.csv"

    score_data = pd.DataFrame(
        {
            "is_fraud": [0, 0, 1, 1],
            "fraud_score": [0.1, 0.4, 0.6, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    build_cost_scenario_reports(
        scores_path=scores_path,
        output_path=output_path,
        best_output_path=best_output_path,
        thresholds=[0.3, 0.8],
    )

    scenario_report = pd.read_csv(output_path)

    assert list(scenario_report.columns) == [
        "scenario_name",
        "threshold",
        "false_positive_cost_assumption",
        "false_negative_cost_assumption",
        "manual_review_cost_assumption",
        "false_positive_count",
        "false_negative_count",
        "predicted_positive_count",
        "false_positive_cost",
        "false_negative_cost",
        "manual_review_cost",
        "total_cost",
    ]


def test_build_cost_scenario_reports_raises_for_missing_required_columns(
    tmp_path: Path,
) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "scenario_report.csv"
    best_output_path = tmp_path / "best_thresholds.csv"

    score_data = pd.DataFrame(
        {
            "fraud_score": [0.1, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    with pytest.raises(ValueError, match="Score data is missing required columns"):
        build_cost_scenario_reports(
            scores_path=scores_path,
            output_path=output_path,
            best_output_path=best_output_path,
            thresholds=[0.5],
        )
