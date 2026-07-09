"""Command line entry point for preparing PaySim fraud data."""

import argparse
from pathlib import Path

from fraud_detection_platform.data.paysim import load_paysim_dataset


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Transform a raw PaySim CSV into the platform transaction schema."
    )

    parser.add_argument(
        "--input-path",
        type=Path,
        required=True,
        help="Path to the raw PaySim CSV file.",
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        required=True,
        help="Path where the transformed platform CSV should be written.",
    )

    parser.add_argument(
        "--start-time",
        type=str,
        default="2026-01-01 00:00:00",
        help="Base timestamp used to convert PaySim step values into transaction times.",
    )

    return parser


def main() -> None:
    """Prepare PaySim data from command line arguments."""
    parser = build_parser()
    args = parser.parse_args()

    transformed_data = load_paysim_dataset(
        file_path=args.input_path,
        start_time=args.start_time,
    )

    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    transformed_data.to_csv(args.output_path, index=False)

    print("PaySim data preparation completed")
    print(f"Input path: {args.input_path}")
    print(f"Output path: {args.output_path}")
    print(f"Rows written: {len(transformed_data)}")


if __name__ == "__main__":
    main()
