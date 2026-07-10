"""Command line entry point for PaySim-enriched fraud model training."""

import argparse
from pathlib import Path

from fraud_detection_platform.pipelines.paysim_training import (
    PaySimTrainingPipelineConfig,
    run_paysim_training_pipeline,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Run the PaySim-enriched fraud detection training pipeline."
    )

    parser.add_argument(
        "--raw-paysim-data-path",
        type=Path,
        required=True,
        help="Path to the raw PaySim CSV dataset.",
    )

    parser.add_argument(
        "--test-size",
        type=float,
        default=0.25,
        help="Fraction of rows to use for the test split.",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Fraud probability threshold used to create class predictions.",
    )

    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed used for reproducible splitting and modeling.",
    )

    parser.add_argument(
        "--model-output-path",
        type=Path,
        default=None,
        help="Optional path where the trained model artifact should be saved.",
    )

    return parser


def main() -> None:
    """Run the PaySim-enriched training pipeline from command line arguments."""
    parser = build_parser()
    args = parser.parse_args()

    config = PaySimTrainingPipelineConfig(
        test_size=args.test_size,
        random_state=args.random_state,
        prediction_threshold=args.threshold,
        model_output_path=args.model_output_path,
    )

    result = run_paysim_training_pipeline(
        raw_paysim_data_path=args.raw_paysim_data_path,
        config=config,
    )

    print("PaySim-enriched fraud training completed")
    print(f"Train rows: {result.train_rows}")
    print(f"Test rows: {result.test_rows}")
    print(f"Precision: {result.metrics.precision:.4f}")
    print(f"Recall: {result.metrics.recall:.4f}")
    print(f"F1: {result.metrics.f1:.4f}")
    print(f"ROC-AUC: {result.metrics.roc_auc:.4f}")
    print(f"PR-AUC: {result.metrics.pr_auc:.4f}")
    print(f"True negatives: {result.metrics.true_negatives}")
    print(f"False positives: {result.metrics.false_positives}")
    print(f"False negatives: {result.metrics.false_negatives}")
    print(f"True positives: {result.metrics.true_positives}")


if __name__ == "__main__":
    main()
