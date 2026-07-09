"""Command line entry point for generating synthetic fraud transaction data."""

import argparse
from pathlib import Path

from fraud_detection_platform.data.sample_generator import write_sample_transactions


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Generate a synthetic fraud transaction dataset.")

    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("data/raw/sample_transactions.csv"),
        help="Destination path for the generated CSV file.",
    )

    parser.add_argument(
        "--row-count",
        type=int,
        default=100,
        help="Number of transaction rows to generate.",
    )

    return parser


def main() -> None:
    """Generate synthetic fraud transaction data from command line arguments."""
    parser = build_parser()
    args = parser.parse_args()

    output_path = write_sample_transactions(
        output_path=args.output_path,
        row_count=args.row_count,
    )

    print(f"Sample transaction data written to: {output_path}")


if __name__ == "__main__":
    main()
