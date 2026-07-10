"""Command line entry point for PaySim calibrated batch inference."""

import argparse
from pathlib import Path

from fraud_detection_platform.pipelines.paysim_batch_inference import (
    PaySimBatchInferenceConfig,
    run_paysim_batch_inference_pipeline,
)
from fraud_detection_platform.risk.calibrated_decision_policy import (
    CalibratedRiskDecisionPolicy,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Run calibrated PaySim batch inference with risk-band actions."
    )

    parser.add_argument(
        "--raw-paysim-data-path",
        type=Path,
        required=True,
        help="Path to the raw PaySim CSV dataset.",
    )

    parser.add_argument(
        "--model-path",
        type=Path,
        required=True,
        help="Path to the saved calibrated PaySim model.",
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        required=True,
        help="Path where scored transactions should be written.",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.010,
        help="Fraud score threshold used to create binary fraud predictions.",
    )

    parser.add_argument(
        "--review-threshold",
        type=float,
        default=0.010,
        help="Minimum calibrated fraud score for manual review.",
    )

    parser.add_argument(
        "--high-risk-threshold",
        type=float,
        default=0.075,
        help="Minimum calibrated fraud score for high-risk review.",
    )

    parser.add_argument(
        "--priority-threshold",
        type=float,
        default=0.100,
        help="Minimum calibrated fraud score for priority investigation.",
    )

    parser.add_argument(
        "--production-mode",
        action="store_true",
        help="Omit ground-truth labels from the scored output.",
    )

    return parser


def main() -> None:
    """Run calibrated PaySim batch inference from command line arguments."""
    parser = build_parser()
    args = parser.parse_args()

    risk_policy = CalibratedRiskDecisionPolicy(
        review_threshold=args.review_threshold,
        high_risk_threshold=args.high_risk_threshold,
        priority_threshold=args.priority_threshold,
    )

    config = PaySimBatchInferenceConfig(
        prediction_threshold=args.threshold,
        risk_policy=risk_policy,
        include_labels=not args.production_mode,
    )

    result = run_paysim_batch_inference_pipeline(
        raw_paysim_data_path=args.raw_paysim_data_path,
        model_path=args.model_path,
        output_path=args.output_path,
        config=config,
    )

    print("PaySim calibrated batch inference completed")
    print(f"Scored rows: {result.scored_rows}")
    print(f"Predictions written to: {result.output_path}")

    if args.production_mode:
        print("Production mode: labels omitted from output")


if __name__ == "__main__":
    main()
