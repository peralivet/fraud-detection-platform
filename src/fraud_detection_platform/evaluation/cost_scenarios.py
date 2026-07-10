"""Cost scenario comparison utilities for fraud threshold evaluation."""

from dataclasses import dataclass

from fraud_detection_platform.evaluation.costs import (
    FraudCostConfig,
    ThresholdCostResult,
    calculate_threshold_costs,
)
from fraud_detection_platform.evaluation.thresholds import ThresholdMetrics


@dataclass(frozen=True)
class FraudCostScenario:
    """Named fraud cost scenario for sensitivity analysis."""

    name: str
    cost_config: FraudCostConfig


@dataclass(frozen=True)
class ScenarioThresholdCostResult:
    """Threshold cost result under one named business scenario."""

    scenario_name: str
    threshold: float
    false_positive_cost_assumption: float
    false_negative_cost_assumption: float
    manual_review_cost_assumption: float
    false_positive_count: int
    false_negative_count: int
    predicted_positive_count: int
    false_positive_cost: float
    false_negative_cost: float
    manual_review_cost: float
    total_cost: float


DEFAULT_COST_SCENARIOS: tuple[FraudCostScenario, ...] = (
    FraudCostScenario(
        name="balanced_operations",
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
    FraudCostScenario(
        name="high_customer_friction",
        cost_config=FraudCostConfig(
            false_positive_cost=25.0,
            false_negative_cost=500.0,
            manual_review_cost=2.0,
        ),
    ),
    FraudCostScenario(
        name="high_review_cost",
        cost_config=FraudCostConfig(
            false_positive_cost=5.0,
            false_negative_cost=500.0,
            manual_review_cost=10.0,
        ),
    ),
)


def calculate_cost_scenario_results(
    threshold_metrics: list[ThresholdMetrics],
    scenarios: list[FraudCostScenario] | tuple[FraudCostScenario, ...] = DEFAULT_COST_SCENARIOS,
) -> list[ScenarioThresholdCostResult]:
    """Calculate threshold costs across multiple business cost scenarios.

    Args:
        threshold_metrics: Threshold-specific classification metrics.
        scenarios: Named business cost scenarios.

    Returns:
        Scenario-threshold cost results.

    Raises:
        ValueError: If threshold metrics or scenarios are empty.
    """
    if not threshold_metrics:
        msg = "threshold_metrics must not be empty"
        raise ValueError(msg)

    if not scenarios:
        msg = "scenarios must not be empty"
        raise ValueError(msg)

    scenario_results: list[ScenarioThresholdCostResult] = []

    for scenario in scenarios:
        cost_results = calculate_threshold_costs(
            threshold_metrics=threshold_metrics,
            cost_config=scenario.cost_config,
        )

        scenario_results.extend(
            _build_scenario_result(
                scenario=scenario,
                threshold_cost_result=cost_result,
            )
            for cost_result in cost_results
        )

    return scenario_results


def find_best_threshold_by_scenario(
    scenario_results: list[ScenarioThresholdCostResult],
) -> list[ScenarioThresholdCostResult]:
    """Find the lowest-cost threshold for each scenario."""
    if not scenario_results:
        msg = "scenario_results must not be empty"
        raise ValueError(msg)

    best_results: list[ScenarioThresholdCostResult] = []

    scenario_names = sorted({result.scenario_name for result in scenario_results})

    for scenario_name in scenario_names:
        matching_results = [
            result for result in scenario_results if result.scenario_name == scenario_name
        ]

        best_results.append(
            min(
                matching_results,
                key=lambda result: result.total_cost,
            )
        )

    return best_results


def _build_scenario_result(
    scenario: FraudCostScenario,
    threshold_cost_result: ThresholdCostResult,
) -> ScenarioThresholdCostResult:
    """Build a scenario-specific threshold cost result."""
    return ScenarioThresholdCostResult(
        scenario_name=scenario.name,
        threshold=threshold_cost_result.threshold,
        false_positive_cost_assumption=scenario.cost_config.false_positive_cost,
        false_negative_cost_assumption=scenario.cost_config.false_negative_cost,
        manual_review_cost_assumption=scenario.cost_config.manual_review_cost,
        false_positive_count=threshold_cost_result.false_positive_count,
        false_negative_count=threshold_cost_result.false_negative_count,
        predicted_positive_count=threshold_cost_result.predicted_positive_count,
        false_positive_cost=threshold_cost_result.false_positive_cost,
        false_negative_cost=threshold_cost_result.false_negative_cost,
        manual_review_cost=threshold_cost_result.manual_review_cost,
        total_cost=threshold_cost_result.total_cost,
    )
