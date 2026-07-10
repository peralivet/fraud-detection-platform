"""Tests for the fraud score distribution analysis CLI."""

from pathlib import Path

import pandas as pd
import pytest

from fraud_detection_platform.cli.analyze_score_distribution import (
    build_parser,
    build_score_distribution_report,
)


def test_analyze_score_distribution_cli_requires_scores_path_and_output_path() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_analyze_score_distribution_cli_accepts_required_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--scores-path",
            "reports/paysim_enriched_test_scores.csv",
            "--output-path",
            "reports/paysim_score_distribution_report.csv",
        ]
    )

    assert args.scores_path == Path("reports/paysim_enriched_test_scores.csv")
    assert args.output_path == Path("reports/paysim_score_distribution_report.csv")


def test_build_score_distribution_report_writes_expected_columns(tmp_path: Path) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "score_distribution_report.csv"

    score_data = pd.DataFrame(
        {
            "is_fraud": [0, 0, 1, 1],
            "fraud_score": [0.1, 0.4, 0.6, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    result_path = build_score_distribution_report(
        scores_path=scores_path,
        output_path=output_path,
    )

    report_data = pd.read_csv(output_path)

    assert result_path == output_path
    assert output_path.exists()
    assert list(report_data.columns) == [
        "label",
        "count",
        "min_score",
        "p01",
        "p05",
        "p10",
        "p25",
        "median",
        "p75",
        "p90",
        "p95",
        "p99",
        "max_score",
        "mean_score",
    ]
    assert len(report_data) == 2


def test_build_score_distribution_report_calculates_expected_values(
    tmp_path: Path,
) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "score_distribution_report.csv"

    score_data = pd.DataFrame(
        {
            "is_fraud": [0, 0, 0, 1, 1, 1],
            "fraud_score": [0.1, 0.2, 0.3, 0.7, 0.8, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    build_score_distribution_report(
        scores_path=scores_path,
        output_path=output_path,
    )

    report_data = pd.read_csv(output_path)

    non_fraud_row = report_data.loc[report_data["label"] == 0].iloc[0]
    fraud_row = report_data.loc[report_data["label"] == 1].iloc[0]

    assert non_fraud_row["count"] == 3
    assert non_fraud_row["min_score"] == 0.1
    assert non_fraud_row["median"] == 0.2
    assert non_fraud_row["max_score"] == 0.3

    assert fraud_row["count"] == 3
    assert fraud_row["min_score"] == 0.7
    assert fraud_row["median"] == 0.8
    assert fraud_row["max_score"] == 0.9


def test_build_score_distribution_report_raises_for_missing_required_columns(
    tmp_path: Path,
) -> None:
    scores_path = tmp_path / "scores.csv"
    output_path = tmp_path / "score_distribution_report.csv"

    score_data = pd.DataFrame(
        {
            "fraud_score": [0.1, 0.9],
        }
    )
    score_data.to_csv(scores_path, index=False)

    with pytest.raises(ValueError, match="Score data is missing required columns"):
        build_score_distribution_report(
            scores_path=scores_path,
            output_path=output_path,
        )
