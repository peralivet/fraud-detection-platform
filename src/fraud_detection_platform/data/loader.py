"""Data loading and validation utilities for fraud detection datasets."""

from pathlib import Path

import pandas as pd

from fraud_detection_platform.data.schema import FEATURE_COLUMNS, REQUIRED_COLUMNS, TARGET_COLUMN


def load_transaction_data(file_path: str | Path) -> pd.DataFrame:
    """Load transaction data from a CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        Loaded transaction dataset.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the dataset is missing required columns.
    """
    resolved_path = Path(file_path)

    if not resolved_path.exists():
        msg = f"Transaction data file not found: {resolved_path}"
        raise FileNotFoundError(msg)

    data = pd.read_csv(resolved_path)
    validate_required_columns(data)

    return data


def validate_required_columns(data: pd.DataFrame) -> None:
    """Validate that the dataset contains all required columns.

    Args:
        data: Transaction dataset.

    Raises:
        ValueError: If required columns are missing.
    """
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(data.columns))

    if missing_columns:
        msg = f"Dataset is missing required columns: {missing_columns}"
        raise ValueError(msg)


def split_features_and_target(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Split transaction data into model features and target.

    Args:
        data: Transaction dataset containing feature columns and target column.

    Returns:
        A tuple containing the feature matrix and target vector.

    Raises:
        ValueError: If required columns are missing.
    """
    validate_required_columns(data)

    features = data[FEATURE_COLUMNS].copy()
    target = data[TARGET_COLUMN].copy()

    return features, target
