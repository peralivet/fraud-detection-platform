"""Command line entry point for fraud score distribution analysis."""

import argparse
from pathlib import Path

import pandas as pd

from fraud_detection_platform.evaluation.score_distribution import (
    summarize_score_distribution,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Analyze fraud score distribution by true label.")

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
        help="Path where the score distribution report CSV should be written.",
    )

    return parser


def build_score_distribution_report(
    scores_path: str | Path,
    output_path: str | Path,
) -> Path:
    """Build and write a score distribution report.

    Args:
        scores_path: Path to score CSV containing is_fraud and fraud_score columns.
        output_path: Path where the score distribution report should be written.

    Returns:
        The resolved output path.

    Raises:
        ValueError: If the input score file is missing required columns.
    """
    score_data = pd.read_csv(scores_path)

    required_columns = {"is_fraud", "fraud_score"}
    missing_columns = sorted(required_columns - set(score_data.columns))

    if missing_columns:
        msg = f"Score data is missing required columns: {missing_columns}"
        raise ValueError(msg)

    summaries = summarize_score_distribution(
        y_true=score_data["is_fraud"].astype(int).tolist(),
        fraud_scores=score_data["fraud_score"].astype(float).tolist(),
    )

    report_rows = [
        {
            "label": summary.label,
            "count": summary.count,
            "min_score": summary.min_score,
            "p01": summary.p01,
            "p05": summary.p05,
            "p10": summary.p10,
            "p25": summary.p25,
            "median": summary.median,
            "p75": summary.p75,
            "p90": summary.p90,
            "p95": summary.p95,
            "p99": summary.p99,
            "max_score": summary.max_score,
            "mean_score": summary.mean_score,
        }
        for summary in summaries
    ]

    report_data = pd.DataFrame(report_rows)

    resolved_output_path = Path(output_path)
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    report_data.to_csv(resolved_output_path, index=False)

    return resolved_output_path


def main() -> None:
    """Run score distribution analysis from command line arguments."""
    parser = build_parser()
    args = parser.parse_args()

    output_path = build_score_distribution_report(
        scores_path=args.scores_path,
        output_path=args.output_path,
    )

    print("Fraud score distribution analysis completed")
    print(f"Score distribution report written to: {output_path}")


if __name__ == "__main__":
    main()
