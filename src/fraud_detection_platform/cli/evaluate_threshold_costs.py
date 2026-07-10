"""Command line entry point for cost-sensitive fraud threshold evaluation."""

import argparse
from pathlib import Path

import pandas as pd

from fraud_detection_platform.cli.evaluate_thresholds import DEFAULT_THRESHOLDS
from fraud_detection_platform.evaluation.costs import (
    FraudCostConfig,
    calculate_threshold_costs,
)
from fraud_detection_platform.evaluation.thresholds import evaluate_thresholds


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Evaluate fraud threshold costs using business cost assumptions."
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
        help="Path where the cost-sensitive threshold report CSV should be written.",
    )

    parser.add_argument(
        "--thresholds",
        type=float,
        nargs="+",
        default=DEFAULT_THRESHOLDS,
        help="Threshold values to evaluate.",
    )

    parser.add_argument(
        "--false-positive-cost",
        type=float,
        default=5.0,
        help="Estimated business cost of one false positive.",
    )

    parser.add_argument(
        "--false-negative-cost",
        type=float,
        default=500.0,
        help="Estimated business cost of one missed fraud case.",
    )

    parser.add_argument(
        "--manual-review-cost",
        type=float,
        default=2.0,
        help="Estimated cost of manually reviewing one flagged transaction.",
    )

    return parser


def build_threshold_cost_report(
    scores_path: str | Path,
    output_path: str | Path,
    thresholds: list[float] | None = None,
    cost_config: FraudCostConfig | None = None,
) -> Path:
    """Build and write a cost-sensitive threshold report.

    Args:
        scores_path: Path to score CSV containing is_fraud and fraud_score columns.
        output_path: Path where the cost report should be written.
        thresholds: Optional thresholds to evaluate.
        cost_config: Optional business cost assumptions.

    Returns:
        The resolved output path.

    Raises:
        ValueError: If the input score file is missing required columns.
    """
    resolved_thresholds = thresholds or DEFAULT_THRESHOLDS
    resolved_cost_config = cost_config or FraudCostConfig()

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

    cost_results = calculate_threshold_costs(
        threshold_metrics=threshold_metrics,
        cost_config=resolved_cost_config,
    )

    report_rows = [
        {
            "threshold": result.threshold,
            "false_positive_count": result.false_positive_count,
            "false_negative_count": result.false_negative_count,
            "predicted_positive_count": result.predicted_positive_count,
            "false_positive_cost": result.false_positive_cost,
            "false_negative_cost": result.false_negative_cost,
            "manual_review_cost": result.manual_review_cost,
            "total_cost": result.total_cost,
        }
        for result in cost_results
    ]

    report_data = pd.DataFrame(report_rows)

    resolved_output_path = Path(output_path)
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    report_data.to_csv(resolved_output_path, index=False)

    return resolved_output_path


def main() -> None:
    """Run cost-sensitive threshold evaluation from command line arguments."""
    parser = build_parser()
    args = parser.parse_args()

    cost_config = FraudCostConfig(
        false_positive_cost=args.false_positive_cost,
        false_negative_cost=args.false_negative_cost,
        manual_review_cost=args.manual_review_cost,
    )

    output_path = build_threshold_cost_report(
        scores_path=args.scores_path,
        output_path=args.output_path,
        thresholds=args.thresholds,
        cost_config=cost_config,
    )

    print("Fraud threshold cost evaluation completed")
    print(f"Cost report written to: {output_path}")


if __name__ == "__main__":
    main()
