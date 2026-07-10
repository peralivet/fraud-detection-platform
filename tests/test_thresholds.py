"""Tests for fraud threshold analysis utilities."""

import pytest

from fraud_detection_platform.evaluation.thresholds import evaluate_thresholds


def test_evaluate_thresholds_returns_metrics_for_each_threshold() -> None:
    y_true = [0, 0, 1, 1]
    fraud_scores = [0.1, 0.4, 0.6, 0.9]
    thresholds = [0.3, 0.5, 0.8]

    results = evaluate_thresholds(
        y_true=y_true,
        fraud_scores=fraud_scores,
        thresholds=thresholds,
    )

    assert len(results) == 3
    assert [result.threshold for result in results] == thresholds


def test_evaluate_thresholds_calculates_expected_confusion_matrix_values() -> None:
    y_true = [0, 0, 1, 1]
    fraud_scores = [0.1, 0.4, 0.6, 0.9]

    results = evaluate_thresholds(
        y_true=y_true,
        fraud_scores=fraud_scores,
        thresholds=[0.5],
    )

    metrics = results[0].metrics

    assert metrics.true_negatives == 2
    assert metrics.false_positives == 0
    assert metrics.false_negatives == 0
    assert metrics.true_positives == 2
    assert metrics.precision == 1.0
    assert metrics.recall == 1.0
    assert metrics.f1 == 1.0


def test_evaluate_thresholds_shows_tradeoff_at_lower_threshold() -> None:
    y_true = [0, 0, 1, 1]
    fraud_scores = [0.1, 0.4, 0.6, 0.9]

    results = evaluate_thresholds(
        y_true=y_true,
        fraud_scores=fraud_scores,
        thresholds=[0.3],
    )

    metrics = results[0].metrics

    assert metrics.true_negatives == 1
    assert metrics.false_positives == 1
    assert metrics.false_negatives == 0
    assert metrics.true_positives == 2
    assert metrics.recall == 1.0


def test_evaluate_thresholds_shows_tradeoff_at_higher_threshold() -> None:
    y_true = [0, 0, 1, 1]
    fraud_scores = [0.1, 0.4, 0.6, 0.9]

    results = evaluate_thresholds(
        y_true=y_true,
        fraud_scores=fraud_scores,
        thresholds=[0.8],
    )

    metrics = results[0].metrics

    assert metrics.true_negatives == 2
    assert metrics.false_positives == 0
    assert metrics.false_negatives == 1
    assert metrics.true_positives == 1
    assert metrics.precision == 1.0
    assert metrics.recall == 0.5


def test_evaluate_thresholds_raises_for_empty_y_true() -> None:
    with pytest.raises(ValueError, match="y_true must not be empty"):
        evaluate_thresholds(
            y_true=[],
            fraud_scores=[0.1],
            thresholds=[0.5],
        )


def test_evaluate_thresholds_raises_for_empty_fraud_scores() -> None:
    with pytest.raises(ValueError, match="fraud_scores must not be empty"):
        evaluate_thresholds(
            y_true=[0],
            fraud_scores=[],
            thresholds=[0.5],
        )


def test_evaluate_thresholds_raises_for_mismatched_lengths() -> None:
    with pytest.raises(ValueError, match="y_true and fraud_scores must have the same length"):
        evaluate_thresholds(
            y_true=[0, 1],
            fraud_scores=[0.1],
            thresholds=[0.5],
        )


def test_evaluate_thresholds_raises_for_empty_thresholds() -> None:
    with pytest.raises(ValueError, match="thresholds must not be empty"):
        evaluate_thresholds(
            y_true=[0, 1],
            fraud_scores=[0.1, 0.9],
            thresholds=[],
        )


def test_evaluate_thresholds_raises_for_invalid_threshold() -> None:
    with pytest.raises(ValueError, match="threshold values must be between 0.0 and 1.0"):
        evaluate_thresholds(
            y_true=[0, 1],
            fraud_scores=[0.1, 0.9],
            thresholds=[1.5],
        )
