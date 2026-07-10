"""Tests for risk action summary utilities."""

import pandas as pd
import pytest

from fraud_detection_platform.evaluation.action_summary import (
    build_action_summary,
    build_action_summary_frame,
)


def test_build_action_summary_returns_summary_by_recommended_action() -> None:
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

    summaries = build_action_summary(scored_data)

    assert len(summaries) == 3
    assert [summary.recommended_action for summary in summaries] == [
        "approve",
        "manual_review",
        "priority_investigation",
    ]


def test_build_action_summary_calculates_expected_values() -> None:
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

    summaries = build_action_summary(scored_data)
    summary_by_action = {summary.recommended_action: summary for summary in summaries}

    approve_summary = summary_by_action["approve"]
    manual_review_summary = summary_by_action["manual_review"]

    assert approve_summary.transaction_count == 2
    assert approve_summary.percentage_of_total == 0.5
    assert approve_summary.fraud_count == 0
    assert approve_summary.non_fraud_count == 2
    assert approve_summary.fraud_rate == 0.0
    assert approve_summary.average_fraud_score == 0.002
    assert approve_summary.average_transaction_amount == 50.0

    assert manual_review_summary.transaction_count == 2
    assert manual_review_summary.percentage_of_total == 0.5
    assert manual_review_summary.fraud_count == 1
    assert manual_review_summary.non_fraud_count == 1
    assert manual_review_summary.fraud_rate == 0.5
    assert manual_review_summary.average_fraud_score == 0.03
    assert manual_review_summary.average_transaction_amount == 2000.0


def test_build_action_summary_handles_missing_is_fraud_column() -> None:
    scored_data = pd.DataFrame(
        {
            "recommended_action": ["approve", "manual_review"],
            "fraud_score": [0.001, 0.020],
            "transaction_amount": [25.0, 1000.0],
        }
    )

    summaries = build_action_summary(scored_data)

    assert summaries[0].fraud_count == 0
    assert summaries[0].non_fraud_count == 1
    assert summaries[0].fraud_rate == 0.0


def test_build_action_summary_frame_returns_expected_columns() -> None:
    scored_data = pd.DataFrame(
        {
            "recommended_action": ["approve", "manual_review"],
            "fraud_score": [0.001, 0.020],
            "transaction_amount": [25.0, 1000.0],
            "is_fraud": [0, 1],
        }
    )

    summary_frame = build_action_summary_frame(scored_data)

    assert list(summary_frame.columns) == [
        "recommended_action",
        "transaction_count",
        "percentage_of_total",
        "fraud_count",
        "non_fraud_count",
        "fraud_rate",
        "average_fraud_score",
        "average_transaction_amount",
    ]


def test_build_action_summary_raises_for_empty_data() -> None:
    with pytest.raises(ValueError, match="scored_data must not be empty"):
        build_action_summary(pd.DataFrame())


def test_build_action_summary_raises_for_missing_required_columns() -> None:
    scored_data = pd.DataFrame(
        {
            "recommended_action": ["approve"],
            "fraud_score": [0.001],
        }
    )

    with pytest.raises(ValueError, match="Scored data is missing required columns"):
        build_action_summary(scored_data)
