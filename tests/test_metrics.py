"""Tests for fraud detection evaluation metrics."""

from fraud_detection_platform.evaluation.metrics import calculate_classification_metrics


def test_calculate_classification_metrics_returns_expected_values() -> None:
    y_true = [0, 0, 1, 1]
    y_pred = [0, 1, 1, 1]
    y_score = [0.05, 0.65, 0.80, 0.95]

    metrics = calculate_classification_metrics(y_true, y_pred, y_score)

    assert round(metrics.precision, 4) == 0.6667
    assert round(metrics.recall, 4) == 1.0000
    assert round(metrics.f1, 4) == 0.8000
    assert round(metrics.roc_auc, 4) == 1.0000
    assert round(metrics.pr_auc, 4) == 1.0000

    assert metrics.true_negatives == 1
    assert metrics.false_positives == 1
    assert metrics.false_negatives == 0
    assert metrics.true_positives == 2


def test_calculate_classification_metrics_handles_no_positive_predictions() -> None:
    y_true = [0, 0, 1, 1]
    y_pred = [0, 0, 0, 0]
    y_score = [0.05, 0.10, 0.20, 0.30]

    metrics = calculate_classification_metrics(y_true, y_pred, y_score)

    assert metrics.precision == 0.0
    assert metrics.recall == 0.0
    assert metrics.f1 == 0.0

    assert metrics.true_negatives == 2
    assert metrics.false_positives == 0
    assert metrics.false_negatives == 2
    assert metrics.true_positives == 0
