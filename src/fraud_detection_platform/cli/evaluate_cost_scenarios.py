"""Command line entry point for fraud cost scenario comparison."""

import argparse
from pathlib import Path

import pandas as pd

from fraud_detection_platform.cli.evaluate_thresholds import DEFAULT_THRESHOLDS
from fraud_detection_platform.evaluation.cost_scenarios import (
    DEFAULT_COST_SCENARIOS,
    ScenarioThresholdCostResult,
    calculate_cost_scenario_results,
    find_best_threshold_by_scenario,
)
from fraud_detection_platform.evaluation.thresholds import evaluate_thresholds


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Compare fraud threshold costs across business cost scenarios."
    )

    parser.add_argument(
        "--scores-path",
        type=Path,
        required=True,
        help="Path to a CSV containing is_fraud and fraud_score columns.",
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        required=True,
        help="Path where the full scenario cost report CSV should be written.",
    )

    parser.add_argument(
        "--best-output-path",
        type=Path,
        required=True,
        help="Path where the best threshold per scenario CSV should be written.",
    )

    parser.add_argument(
        "--thresholds",
        type=float,
        nargs="+",
        default=DEFAULT_THRESHOLDS,
        help="Threshold values to evaluate.",
    )

    return parser


def build_cost_scenario_reports(
    scores_path: str | Path,
    output_path: str | Path,
    best_output_path: str | Path,
    thresholds: list[float] | None = None,
) -> tuple[Path, Path]:
    """Build full and best-threshold cost scenario reports.

    Args:
        scores_path: Path to score CSV containing is_fraud and fraud_score columns.
        output_path: Path where the full scenario report should be written.
        best_output_path: Path where the best-threshold summary should be written.
        thresholds: Optional thresholds to evaluate.

    Returns:
        Tuple of full report path and best-threshold report path.

    Raises:
        ValueError: If the input score file is missing required columns.
    """
    resolved_thresholds = thresholds or DEFAULT_THRESHOLDS

    score_data = pd.read_csv(scores_path)

    required_columns = {"is_fraud", "fraud_score"}
    missing_columns = sorted(required_columns - set(score_data.columns))

    if missing_columns:
        msg = f"Score data is missing required columns: {missing_columns}"
        raise ValueError(msg)

    threshold_metrics = evaluate_thresholds(
        y_true=score_data["is_fraud"].astype(int).tolist(),
        fraud_scores=score_data["fraud_score"].astype(float).tolist(),
        thresholds=resolved_thresholds,
    )

    scenario_results = calculate_cost_scenario_results(
        threshold_metrics=threshold_metrics,
        scenarios=DEFAULT_COST_SCENARIOS,
    )

    best_results = find_best_threshold_by_scenario(scenario_results)

    resolved_output_path = Path(output_path)
    resolved_best_output_path = Path(best_output_path)

    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_best_output_path.parent.mkdir(parents=True, exist_ok=True)

    _scenario_results_to_frame(scenario_results).to_csv(
        resolved_output_path,
        index=False,
    )
    _scenario_results_to_frame(best_results).to_csv(
        resolved_best_output_path,
        index=False,
    )

    return resolved_output_path, resolved_best_output_path


def _scenario_results_to_frame(
    scenario_results: list[ScenarioThresholdCostResult],
) -> pd.DataFrame:
    """Convert scenario results to a report DataFrame."""
    report_rows = [
        {
            "scenario_name": result.scenario_name,
            "threshold": result.threshold,
            "false_positive_cost_assumption": result.false_positive_cost_assumption,
            "false_negative_cost_assumption": result.false_negative_cost_assumption,
            "manual_review_cost_assumption": result.manual_review_cost_assumption,
            "false_positive_count": result.false_positive_count,
            "false_negative_count": result.false_negative_count,
            "predicted_positive_count": result.predicted_positive_count,
            "false_positive_cost": result.false_positive_cost,
            "false_negative_cost": result.false_negative_cost,
            "manual_review_cost": result.manual_review_cost,
            "total_cost": result.total_cost,
        }
        for result in scenario_results
    ]

    return pd.DataFrame(report_rows)


def main() -> None:
    """Run cost scenario comparison from command line arguments."""
    parser = build_parser()
    args = parser.parse_args()

    output_path, best_output_path = build_cost_scenario_reports(
        scores_path=args.scores_path,
        output_path=args.output_path,
        best_output_path=args.best_output_path,
        thresholds=args.thresholds,
    )

    print("Fraud cost scenario comparison completed")
    print(f"Full scenario report written to: {output_path}")
    print(f"Best-threshold report written to: {best_output_path}")


if __name__ == "__main__":
    main()
