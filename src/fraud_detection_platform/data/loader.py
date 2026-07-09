"""Data loading and validation utilities for fraud detection datasets."""

from pathlib import Path

import pandas as pd

from fraud_detection_platform.data.schema import (
    FEATURE_COLUMNS,
    INFERENCE_REQUIRED_COLUMNS,
    REQUIRED_COLUMNS,
    TARGET_COLUMN,
)


def load_transaction_data(file_path: str | Path) -> pd.DataFrame:
    """Load labeled transaction data from a CSV file.

    This loader is used for training and evaluation, where the target label
    column is required.
    """
    resolved_path = Path(file_path)

    if not resolved_path.exists():
        msg = f"Transaction data file not found: {resolved_path}"
        raise FileNotFoundError(msg)

    data = pd.read_csv(resolved_path)
    validate_required_columns(data)

    return data


def load_inference_transaction_data(file_path: str | Path) -> pd.DataFrame:
    """Load transaction data for inference.

    This loader supports production-style scoring data where the target label
    may not be available yet.
    """
    resolved_path = Path(file_path)

    if not resolved_path.exists():
        msg = f"Transaction data file not found: {resolved_path}"
        raise FileNotFoundError(msg)

    data = pd.read_csv(resolved_path)
    validate_inference_required_columns(data)

    return data


def validate_required_columns(data: pd.DataFrame) -> None:
    """Validate that labeled training data contains all required columns."""
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(data.columns))

    if missing_columns:
        msg = f"Dataset is missing required columns: {missing_columns}"
        raise ValueError(msg)


def validate_inference_required_columns(data: pd.DataFrame) -> None:
    """Validate that inference data contains all required transaction columns."""
    missing_columns = sorted(set(INFERENCE_REQUIRED_COLUMNS) - set(data.columns))

    if missing_columns:
        msg = f"Inference dataset is missing required columns: {missing_columns}"
        raise ValueError(msg)


def split_features_and_target(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Split labeled transaction data into model features and target."""
    validate_required_columns(data)

    features = data[FEATURE_COLUMNS].copy()
    target = data[TARGET_COLUMN].copy()

    return features, target


def select_features(data: pd.DataFrame) -> pd.DataFrame:
    """Select model features from transformed transaction data."""
    missing_columns = sorted(set(FEATURE_COLUMNS) - set(data.columns))

    if missing_columns:
        msg = f"Feature table is missing required columns: {missing_columns}"
        raise ValueError(msg)

    return data[FEATURE_COLUMNS].copy()
