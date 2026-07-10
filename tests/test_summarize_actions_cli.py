"""Tests for the fraud risk action summary CLI."""

from pathlib import Path

import pandas as pd
import pytest

from fraud_detection_platform.cli.summarize_actions import (
    build_action_summary_report,
    build_parser,
)


def test_summarize_actions_cli_requires_scored_path_and_output_path() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_summarize_actions_cli_accepts_required_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--scored-path",
            "reports/paysim_calibrated_scored_transactions.csv",
            "--output-path",
            "reports/paysim_action_summary.csv",
        ]
    )

    assert args.scored_path == Path("reports/paysim_calibrated_scored_transactions.csv")
    assert args.output_path == Path("reports/paysim_action_summary.csv")


def test_build_action_summary_report_writes_expected_file(tmp_path: Path) -> None:
    scored_path = tmp_path / "scored_transactions.csv"
    output_path = tmp_path / "action_summary.csv"

    scored_data = pd.DataFrame(
        {
            "recommended_action": [
                "approve",
                "approve",
                "manual_review",
                "priority_investigation",
            ],
            "fraud_score": [0.001, 0.002, 0.020, 0.120],
            "transaction_amount": [25.0, 50.0, 1000.0, 5000.0],
            "is_fraud": [0, 0, 1, 1],
        }
    )
    scored_data.to_csv(scored_path, index=False)

    result_path = build_action_summary_report(
        scored_path=scored_path,
        output_path=output_path,
    )

    summary_data = pd.read_csv(output_path)

    assert result_path == output_path
    assert output_path.exists()
    assert len(summary_data) == 3


def test_build_action_summary_report_writes_expected_columns(tmp_path: Path) -> None:
    scored_path = tmp_path / "scored_transactions.csv"
    output_path = tmp_path / "action_summary.csv"

    scored_data = pd.DataFrame(
        {
            "recommended_action": ["approve", "manual_review"],
            "fraud_score": [0.001, 0.020],
            "transaction_amount": [25.0, 1000.0],
            "is_fraud": [0, 1],
        }
    )
    scored_data.to_csv(scored_path, index=False)

    build_action_summary_report(
        scored_path=scored_path,
        output_path=output_path,
    )

    summary_data = pd.read_csv(output_path)

    assert list(summary_data.columns) == [
        "recommended_action",
        "transaction_count",
        "percentage_of_total",
        "fraud_count",
        "non_fraud_count",
        "fraud_rate",
        "average_fraud_score",
        "average_transaction_amount",
    ]


def test_build_action_summary_report_calculates_expected_values(tmp_path: Path) -> None:
    scored_path = tmp_path / "scored_transactions.csv"
    output_path = tmp_path / "action_summary.csv"

    scored_data = pd.DataFrame(
        {
            "recommended_action": [
                "approve",
                "approve",
                "manual_review",
                "manual_review",
            ],
            "fraud_score": [0.001, 0.003, 0.020, 0.040],
            "transaction_amount": [25.0, 75.0, 1000.0, 3000.0],
            "is_fraud": [0, 0, 0, 1],
        }
    )
    scored_data.to_csv(scored_path, index=False)

    build_action_summary_report(
        scored_path=scored_path,
        output_path=output_path,
    )

    summary_data = pd.read_csv(output_path)
    approve_row = summary_data.loc[summary_data["recommended_action"] == "approve"].iloc[0]
    manual_review_row = summary_data.loc[
        summary_data["recommended_action"] == "manual_review"
    ].iloc[0]

    assert approve_row["transaction_count"] == 2
    assert approve_row["percentage_of_total"] == 0.5
    assert approve_row["fraud_count"] == 0
    assert approve_row["non_fraud_count"] == 2
    assert approve_row["fraud_rate"] == 0.0
    assert approve_row["average_fraud_score"] == 0.002
    assert approve_row["average_transaction_amount"] == 50.0

    assert manual_review_row["transaction_count"] == 2
    assert manual_review_row["percentage_of_total"] == 0.5
    assert manual_review_row["fraud_count"] == 1
    assert manual_review_row["non_fraud_count"] == 1
    assert manual_review_row["fraud_rate"] == 0.5
    assert manual_review_row["average_fraud_score"] == 0.03
    assert manual_review_row["average_transaction_amount"] == 2000.0
