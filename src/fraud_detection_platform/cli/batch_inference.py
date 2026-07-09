"""Command line entry point for fraud batch inference."""

import argparse
from pathlib import Path

from fraud_detection_platform.pipelines.batch_inference import (
    BatchInferenceConfig,
    run_batch_inference_pipeline,
)
from fraud_detection_platform.risk.decision_policy import RiskDecisionPolicy


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Run fraud batch inference using a saved model artifact."
    )

    parser.add_argument(
        "--data-path",
        type=Path,
        required=True,
        help="Path to the transaction CSV dataset.",
    )

    parser.add_argument(
        "--model-path",
        type=Path,
        required=True,
        help="Path to the saved model artifact.",
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        required=True,
        help="Path where prediction results should be written.",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Fraud probability threshold used to create class predictions.",
    )
    parser.add_argument(
        "--review-threshold",
        type=float,
        default=0.5,
        help="Fraud score threshold where transactions should be sent to manual review.",
    )

    parser.add_argument(
        "--block-threshold",
        type=float,
        default=0.8,
        help="Fraud score threshold where transactions should be blocked.",
    )

    return parser


def main() -> None:
    """Run batch inference from command line arguments."""
    parser = build_parser()
    args = parser.parse_args()

    risk_policy = RiskDecisionPolicy(
        review_threshold=args.review_threshold,
        block_threshold=args.block_threshold,
    )
    config = BatchInferenceConfig(
        prediction_threshold=args.threshold,
        risk_policy=risk_policy,
    )

    result = run_batch_inference_pipeline(
        data_path=args.data_path,
        model_path=args.model_path,
        output_path=args.output_path,
        config=config,
    )

    print("Fraud batch inference completed")
    print(f"Scored rows: {result.scored_rows}")
    print(f"Predictions written to: {result.output_path}")


if __name__ == "__main__":
    main()
