"""Score distribution analysis utilities for fraud detection models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreDistributionSummary:
    """Summary statistics for fraud scores within one label group."""

    label: int
    count: int
    min_score: float
    p01: float
    p05: float
    p10: float
    p25: float
    median: float
    p75: float
    p90: float
    p95: float
    p99: float
    max_score: float
    mean_score: float


def _quantile(sorted_scores: list[float], percentile: float) -> float:
    """Calculate a percentile using linear interpolation."""
    if not sorted_scores:
        msg = "sorted_scores must not be empty"
        raise ValueError(msg)

    if not 0.0 <= percentile <= 1.0:
        msg = "percentile must be between 0.0 and 1.0"
        raise ValueError(msg)

    if len(sorted_scores) == 1:
        return sorted_scores[0]

    position = percentile * (len(sorted_scores) - 1)
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(sorted_scores) - 1)
    weight = position - lower_index

    lower_value = sorted_scores[lower_index]
    upper_value = sorted_scores[upper_index]

    return lower_value + (upper_value - lower_value) * weight


def summarize_score_distribution(
    y_true: list[int],
    fraud_scores: list[float],
) -> list[ScoreDistributionSummary]:
    """Summarize fraud score distribution by true label.

    Args:
        y_true: True binary labels, where 1 means fraud and 0 means non-fraud.
        fraud_scores: Fraud probability-like scores from the model.

    Returns:
        Score distribution summaries grouped by label.

    Raises:
        ValueError: If inputs are empty or have different lengths.
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

    summaries: list[ScoreDistributionSummary] = []

    for label in sorted(set(y_true)):
        label_scores = [
            float(score)
            for actual_label, score in zip(y_true, fraud_scores, strict=True)
            if actual_label == label
        ]

        sorted_scores = sorted(label_scores)

        summaries.append(
            ScoreDistributionSummary(
                label=label,
                count=len(sorted_scores),
                min_score=min(sorted_scores),
                p01=_quantile(sorted_scores, 0.01),
                p05=_quantile(sorted_scores, 0.05),
                p10=_quantile(sorted_scores, 0.10),
                p25=_quantile(sorted_scores, 0.25),
                median=_quantile(sorted_scores, 0.50),
                p75=_quantile(sorted_scores, 0.75),
                p90=_quantile(sorted_scores, 0.90),
                p95=_quantile(sorted_scores, 0.95),
                p99=_quantile(sorted_scores, 0.99),
                max_score=max(sorted_scores),
                mean_score=sum(sorted_scores) / len(sorted_scores),
            )
        )

    return summaries
