"""Command line entry point for fraud threshold evaluation."""

import argparse
from pathlib import Path

import pandas as pd

from fraud_detection_platform.evaluation.thresholds import evaluate_thresholds

DEFAULT_THRESHOLDS: list[float] = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Evaluate fraud classification metrics across score thresholds."
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
        help="Path where the threshold report CSV should be written.",
    )

    parser.add_argument(
        "--thresholds",
        type=float,
        nargs="+",
        default=DEFAULT_THRESHOLDS,
        help="Threshold values to evaluate.",
    )

    return parser


def build_threshold_report(
    scores_path: str | Path,
    output_path: str | Path,
    thresholds: list[float] | None = None,
) -> Path:
    """Build and write a threshold comparison report.

    Args:
        scores_path: Path to score CSV containing is_fraud and fraud_score columns.
        output_path: Path where the threshold report should be written.
        thresholds: Optional list of thresholds to evaluate.

    Returns:
        The resolved output path.

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

    threshold_results = evaluate_thresholds(
        y_true=score_data["is_fraud"].astype(int).tolist(),
        fraud_scores=score_data["fraud_score"].astype(float).tolist(),
        thresholds=resolved_thresholds,
    )

    report_rows = [
        {
            "threshold": result.threshold,
            "precision": result.metrics.precision,
            "recall": result.metrics.recall,
            "f1": result.metrics.f1,
            "roc_auc": result.metrics.roc_auc,
            "pr_auc": result.metrics.pr_auc,
            "true_negatives": result.metrics.true_negatives,
            "false_positives": result.metrics.false_positives,
            "false_negatives": result.metrics.false_negatives,
            "true_positives": result.metrics.true_positives,
        }
        for result in threshold_results
    ]

    report_data = pd.DataFrame(report_rows)

    resolved_output_path = Path(output_path)
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    report_data.to_csv(resolved_output_path, index=False)

    return resolved_output_path


def main() -> None:
    """Run threshold evaluation from command line arguments."""
    parser = build_parser()
    args = parser.parse_args()

    output_path = build_threshold_report(
        scores_path=args.scores_path,
        output_path=args.output_path,
        thresholds=args.thresholds,
    )

    print("Fraud threshold evaluation completed")
    print(f"Threshold report written to: {output_path}")


if __name__ == "__main__":
    main()
