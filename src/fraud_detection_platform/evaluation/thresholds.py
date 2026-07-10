"""Threshold analysis utilities for fraud detection models."""

from dataclasses import dataclass

from fraud_detection_platform.evaluation.metrics import (
    ClassificationMetrics,
    calculate_classification_metrics,
)


@dataclass(frozen=True)
class ThresholdMetrics:
    """Classification metrics calculated at a specific fraud threshold."""

    threshold: float
    metrics: ClassificationMetrics


def evaluate_thresholds(
    y_true: list[int],
    fraud_scores: list[float],
    thresholds: list[float],
) -> list[ThresholdMetrics]:
    """Evaluate fraud classification metrics across multiple thresholds.

    Args:
        y_true: True binary labels, where 1 means fraud and 0 means non-fraud.
        fraud_scores: Fraud probability-like scores from the model.
        thresholds: Threshold values used to convert fraud scores into predictions.

    Returns:
        A list of threshold-specific metric results.

    Raises:
        ValueError: If inputs are empty, mismatched, or contain invalid thresholds.
    """
    if not y_true:
        msg = "y_true must not be empty"
        raise ValueError(msg)

    if not fraud_scores:
        msg = "fraud_scores must not be empty"
        raise ValueError(msg)

    if len(y_true) != len(fraud_scores):
        msg = "y_true and fraud_scores must have the same length"
        raise ValueError(msg)

    if not thresholds:
        msg = "thresholds must not be empty"
        raise ValueError(msg)

    results: list[ThresholdMetrics] = []

    for threshold in thresholds:
        if not 0.0 <= threshold <= 1.0:
            msg = "threshold values must be between 0.0 and 1.0"
            raise ValueError(msg)

        predictions = [1 if score >= threshold else 0 for score in fraud_scores]

        metrics = calculate_classification_metrics(
            y_true=y_true,
            y_pred=predictions,
            y_score=fraud_scores,
        )

        results.append(
            ThresholdMetrics(
                threshold=threshold,
                metrics=metrics,
            )
        )

    return results
