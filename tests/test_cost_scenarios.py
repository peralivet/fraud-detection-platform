"""Tests for fraud cost scenario comparison utilities."""

import pytest

from fraud_detection_platform.evaluation.cost_scenarios import (
    DEFAULT_COST_SCENARIOS,
    FraudCostScenario,
    calculate_cost_scenario_results,
    find_best_threshold_by_scenario,
)
from fraud_detection_platform.evaluation.costs import FraudCostConfig
from fraud_detection_platform.evaluation.thresholds import evaluate_thresholds


def test_default_cost_scenarios_are_defined() -> None:
    assert len(DEFAULT_COST_SCENARIOS) == 4
    assert [scenario.name for scenario in DEFAULT_COST_SCENARIOS] == [
        "balanced_operations",
        "high_fraud_loss",
        "high_customer_friction",
        "high_review_cost",
    ]


def test_calculate_cost_scenario_results_returns_result_for_each_scenario_and_threshold() -> None:
    threshold_metrics = evaluate_thresholds(
        y_true=[0, 0, 1, 1],
        fraud_scores=[0.1, 0.4, 0.6, 0.9],
        thresholds=[0.3, 0.8],
    )

    scenarios = [
        FraudCostScenario(
            name="balanced",
            cost_config=FraudCostConfig(
                false_positive_cost=5.0,
                false_negative_cost=500.0,
                manual_review_cost=2.0,
            ),
        ),
        FraudCostScenario(
            name="high_fraud_loss",
            cost_config=FraudCostConfig(
                false_positive_cost=5.0,
                false_negative_cost=1000.0,
                manual_review_cost=2.0,
            ),
        ),
    ]

    results = calculate_cost_scenario_results(
        threshold_metrics=threshold_metrics,
        scenarios=scenarios,
    )

    assert len(results) == 4
    assert [result.scenario_name for result in results] == [
        "balanced",
        "balanced",
        "high_fraud_loss",
        "high_fraud_loss",
    ]
    assert [result.threshold for result in results] == [0.3, 0.8, 0.3, 0.8]


def test_calculate_cost_scenario_results_includes_cost_assumptions() -> None:
    threshold_metrics = evaluate_thresholds(
        y_true=[0, 0, 1, 1],
        fraud_scores=[0.1, 0.4, 0.6, 0.9],
        thresholds=[0.3],
    )

    scenarios = [
        FraudCostScenario(
            name="custom",
            cost_config=FraudCostConfig(
                false_positive_cost=10.0,
                false_negative_cost=1000.0,
                manual_review_cost=3.0,
            ),
        )
    ]

    results = calculate_cost_scenario_results(
        threshold_metrics=threshold_metrics,
        scenarios=scenarios,
    )

    result = results[0]

    assert result.scenario_name == "custom"
    assert result.threshold == 0.3
    assert result.false_positive_cost_assumption == 10.0
    assert result.false_negative_cost_assumption == 1000.0
    assert result.manual_review_cost_assumption == 3.0


def test_find_best_threshold_by_scenario_returns_lowest_cost_threshold_per_scenario() -> None:
    threshold_metrics = evaluate_thresholds(
        y_true=[0, 0, 1, 1],
        fraud_scores=[0.1, 0.4, 0.6, 0.9],
        thresholds=[0.3, 0.8],
    )

    scenarios = [
        FraudCostScenario(
            name="low_false_negative_cost",
            cost_config=FraudCostConfig(
                false_positive_cost=5.0,
                false_negative_cost=1.0,
                manual_review_cost=2.0,
            ),
        ),
        FraudCostScenario(
            name="high_false_negative_cost",
            cost_config=FraudCostConfig(
                false_positive_cost=5.0,
                false_negative_cost=1000.0,
                manual_review_cost=2.0,
            ),
        ),
    ]

    scenario_results = calculate_cost_scenario_results(
        threshold_metrics=threshold_metrics,
        scenarios=scenarios,
    )

    best_results = find_best_threshold_by_scenario(scenario_results)

    assert len(best_results) == 2

    best_by_name = {result.scenario_name: result for result in best_results}

    assert best_by_name["low_false_negative_cost"].threshold == 0.8
    assert best_by_name["high_false_negative_cost"].threshold == 0.3


def test_calculate_cost_scenario_results_raises_for_empty_threshold_metrics() -> None:
    with pytest.raises(ValueError, match="threshold_metrics must not be empty"):
        calculate_cost_scenario_results(threshold_metrics=[])


def test_calculate_cost_scenario_results_raises_for_empty_scenarios() -> None:
    threshold_metrics = evaluate_thresholds(
        y_true=[0, 1],
        fraud_scores=[0.1, 0.9],
        thresholds=[0.5],
    )

    with pytest.raises(ValueError, match="scenarios must not be empty"):
        calculate_cost_scenario_results(
            threshold_metrics=threshold_metrics,
            scenarios=[],
        )


def test_find_best_threshold_by_scenario_raises_for_empty_results() -> None:
    with pytest.raises(ValueError, match="scenario_results must not be empty"):
        find_best_threshold_by_scenario([])
