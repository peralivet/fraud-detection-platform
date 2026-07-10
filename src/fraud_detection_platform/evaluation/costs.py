"""Cost-sensitive evaluation utilities for fraud detection thresholds."""

from dataclasses import dataclass

from fraud_detection_platform.evaluation.thresholds import ThresholdMetrics


@dataclass(frozen=True)
class FraudCostConfig:
    """Business cost assumptions for fraud threshold evaluation."""

    false_positive_cost: float = 5.0
    false_negative_cost: float = 500.0
    manual_review_cost: float = 2.0

    def __post_init__(self) -> None:
        """Validate cost assumptions."""
        if self.false_positive_cost < 0:
            msg = "false_positive_cost must be non-negative"
            raise ValueError(msg)

        if self.false_negative_cost < 0:
            msg = "false_negative_cost must be non-negative"
            raise ValueError(msg)

        if self.manual_review_cost < 0:
            msg = "manual_review_cost must be non-negative"
            raise ValueError(msg)


@dataclass(frozen=True)
class ThresholdCostResult:
    """Cost-sensitive result for one fraud threshold."""

    threshold: float
    false_positive_count: int
    false_negative_count: int
    predicted_positive_count: int
    false_positive_cost: float
    false_negative_cost: float
    manual_review_cost: float
    total_cost: float


def calculate_threshold_cost(
    threshold_metrics: ThresholdMetrics,
    cost_config: FraudCostConfig | None = None,
) -> ThresholdCostResult:
    """Calculate business cost for one threshold result.

    Args:
        threshold_metrics: Threshold-specific classification metrics.
        cost_config: Business cost assumptions.

    Returns:
        Cost-sensitive threshold result.
    """
    resolved_config = cost_config or FraudCostConfig()
    metrics = threshold_metrics.metrics

    predicted_positive_count = metrics.false_positives + metrics.true_positives

    false_positive_cost = metrics.false_positives * resolved_config.false_positive_cost
    false_negative_cost = metrics.false_negatives * resolved_config.false_negative_cost
    manual_review_cost = predicted_positive_count * resolved_config.manual_review_cost

    total_cost = false_positive_cost + false_negative_cost + manual_review_cost

    return ThresholdCostResult(
        threshold=threshold_metrics.threshold,
        false_positive_count=metrics.false_positives,
        false_negative_count=metrics.false_negatives,
        predicted_positive_count=predicted_positive_count,
        false_positive_cost=false_positive_cost,
        false_negative_cost=false_negative_cost,
        manual_review_cost=manual_review_cost,
        total_cost=total_cost,
    )


def calculate_threshold_costs(
    threshold_metrics: list[ThresholdMetrics],
    cost_config: FraudCostConfig | None = None,
) -> list[ThresholdCostResult]:
    """Calculate business costs for multiple threshold results."""
    if not threshold_metrics:
        msg = "threshold_metrics must not be empty"
        raise ValueError(msg)

    resolved_config = cost_config or FraudCostConfig()

    return [
        calculate_threshold_cost(
            threshold_metrics=result,
            cost_config=resolved_config,
        )
        for result in threshold_metrics
    ]
