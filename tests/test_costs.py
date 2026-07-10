"""Tests for cost-sensitive fraud threshold evaluation utilities."""

import pytest

from fraud_detection_platform.evaluation.costs import (
    FraudCostConfig,
    calculate_threshold_cost,
    calculate_threshold_costs,
)
from fraud_detection_platform.evaluation.thresholds import evaluate_thresholds


def test_fraud_cost_config_rejects_negative_false_positive_cost() -> None:
    with pytest.raises(ValueError, match="false_positive_cost must be non-negative"):
        FraudCostConfig(false_positive_cost=-1.0)


def test_fraud_cost_config_rejects_negative_false_negative_cost() -> None:
    with pytest.raises(ValueError, match="false_negative_cost must be non-negative"):
        FraudCostConfig(false_negative_cost=-1.0)


def test_fraud_cost_config_rejects_negative_manual_review_cost() -> None:
    with pytest.raises(ValueError, match="manual_review_cost must be non-negative"):
        FraudCostConfig(manual_review_cost=-1.0)


def test_calculate_threshold_cost_returns_expected_costs() -> None:
    threshold_metrics = evaluate_thresholds(
        y_true=[0, 0, 1, 1],
        fraud_scores=[0.1, 0.4, 0.6, 0.9],
        thresholds=[0.3],
    )[0]

    cost_result = calculate_threshold_cost(
        threshold_metrics=threshold_metrics,
        cost_config=FraudCostConfig(
            false_positive_cost=5.0,
            false_negative_cost=500.0,
            manual_review_cost=2.0,
        ),
    )

    assert cost_result.threshold == 0.3
    assert cost_result.false_positive_count == 1
    assert cost_result.false_negative_count == 0
    assert cost_result.predicted_positive_count == 3
    assert cost_result.false_positive_cost == 5.0
    assert cost_result.false_negative_cost == 0.0
    assert cost_result.manual_review_cost == 6.0
    assert cost_result.total_cost == 11.0


def test_calculate_threshold_cost_includes_false_negative_cost() -> None:
    threshold_metrics = evaluate_thresholds(
        y_true=[0, 0, 1, 1],
        fraud_scores=[0.1, 0.4, 0.6, 0.9],
        thresholds=[0.8],
    )[0]

    cost_result = calculate_threshold_cost(
        threshold_metrics=threshold_metrics,
        cost_config=FraudCostConfig(
            false_positive_cost=5.0,
            false_negative_cost=500.0,
            manual_review_cost=2.0,
        ),
    )

    assert cost_result.false_positive_count == 0
    assert cost_result.false_negative_count == 1
    assert cost_result.predicted_positive_count == 1
    assert cost_result.false_positive_cost == 0.0
    assert cost_result.false_negative_cost == 500.0
    assert cost_result.manual_review_cost == 2.0
    assert cost_result.total_cost == 502.0


def test_calculate_threshold_costs_returns_costs_for_each_threshold() -> None:
    threshold_metrics = evaluate_thresholds(
        y_true=[0, 0, 1, 1],
        fraud_scores=[0.1, 0.4, 0.6, 0.9],
        thresholds=[0.3, 0.5, 0.8],
    )

    cost_results = calculate_threshold_costs(
        threshold_metrics=threshold_metrics,
        cost_config=FraudCostConfig(),
    )

    assert len(cost_results) == 3
    assert [result.threshold for result in cost_results] == [0.3, 0.5, 0.8]


def test_calculate_threshold_costs_raises_for_empty_results() -> None:
    with pytest.raises(ValueError, match="threshold_metrics must not be empty"):
        calculate_threshold_costs([])
