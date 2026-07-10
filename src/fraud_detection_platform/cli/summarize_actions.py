"""Command line entry point for summarizing fraud risk actions."""

import argparse
from pathlib import Path

import pandas as pd

from fraud_detection_platform.evaluation.action_summary import (
    build_action_summary_frame,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Summarize scored fraud transactions by recommended action."
    )

    parser.add_argument(
        "--scored-path",
        type=Path,
        required=True,
        help="Path to a scored transactions CSV.",
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        required=True,
        help="Path where the action summary CSV should be written.",
    )

    return parser


def build_action_summary_report(
    scored_path: str | Path,
    output_path: str | Path,
) -> Path:
    """Build and write a risk action summary report.

    Args:
        scored_path: Path to scored transactions CSV.
        output_path: Path where the action summary report should be written.

    Returns:
        The resolved output path.
    """
    scored_data = pd.read_csv(scored_path)
    summary_data = build_action_summary_frame(scored_data)

    resolved_output_path = Path(output_path)
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_data.to_csv(resolved_output_path, index=False)

    return resolved_output_path


def main() -> None:
    """Run risk action summary generation from command line arguments."""
    parser = build_parser()
    args = parser.parse_args()

    output_path = build_action_summary_report(
        scored_path=args.scored_path,
        output_path=args.output_path,
    )

    print("Fraud risk action summary completed")
    print(f"Action summary written to: {output_path}")


if __name__ == "__main__":
    main()
