"""Tests for score distribution analysis utilities."""

import pytest

from fraud_detection_platform.evaluation.score_distribution import (
    summarize_score_distribution,
)


def test_summarize_score_distribution_returns_summary_for_each_label() -> None:
    y_true = [0, 0, 0, 1, 1, 1]
    fraud_scores = [0.1, 0.2, 0.3, 0.7, 0.8, 0.9]

    summaries = summarize_score_distribution(
        y_true=y_true,
        fraud_scores=fraud_scores,
    )

    assert len(summaries) == 2
    assert [summary.label for summary in summaries] == [0, 1]
    assert [summary.count for summary in summaries] == [3, 3]


def test_summarize_score_distribution_calculates_expected_values() -> None:
    y_true = [0, 0, 0, 0]
    fraud_scores = [0.1, 0.2, 0.3, 0.4]

    summaries = summarize_score_distribution(
        y_true=y_true,
        fraud_scores=fraud_scores,
    )

    summary = summaries[0]

    assert summary.label == 0
    assert summary.count == 4
    assert summary.min_score == 0.1
    assert summary.p25 == 0.17500000000000002
    assert summary.median == 0.25
    assert summary.p75 == 0.325
    assert summary.max_score == 0.4
    assert summary.mean_score == 0.25


def test_summarize_score_distribution_handles_single_value_label() -> None:
    y_true = [0, 1]
    fraud_scores = [0.2, 0.8]

    summaries = summarize_score_distribution(
        y_true=y_true,
        fraud_scores=fraud_scores,
    )

    non_fraud_summary = summaries[0]
    fraud_summary = summaries[1]

    assert non_fraud_summary.min_score == 0.2
    assert non_fraud_summary.median == 0.2
    assert non_fraud_summary.max_score == 0.2
    assert fraud_summary.min_score == 0.8
    assert fraud_summary.median == 0.8
    assert fraud_summary.max_score == 0.8


def test_summarize_score_distribution_raises_for_empty_y_true() -> None:
    with pytest.raises(ValueError, match="y_true must not be empty"):
        summarize_score_distribution(
            y_true=[],
            fraud_scores=[0.1],
        )


def test_summarize_score_distribution_raises_for_empty_fraud_scores() -> None:
    with pytest.raises(ValueError, match="fraud_scores must not be empty"):
        summarize_score_distribution(
            y_true=[0],
            fraud_scores=[],
        )


def test_summarize_score_distribution_raises_for_mismatched_lengths() -> None:
    with pytest.raises(ValueError, match="y_true and fraud_scores must have the same length"):
        summarize_score_distribution(
            y_true=[0, 1],
            fraud_scores=[0.1],
        )
