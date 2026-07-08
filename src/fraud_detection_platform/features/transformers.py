"""Feature engineering utilities for fraud detection."""

import pandas as pd


def add_transaction_time_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add time-based features from the transaction_time column.

    Args:
        data: Transaction dataset containing a transaction_time column.

    Returns:
        Dataset with transaction_hour and transaction_day_of_week columns added.

    Raises:
        ValueError: If transaction_time column is missing.
    """
    if "transaction_time" not in data.columns:
        msg = "Dataset is missing required column: transaction_time"
        raise ValueError(msg)

    transformed = data.copy()
    transaction_time = pd.to_datetime(transformed["transaction_time"], errors="coerce")

    transformed["transaction_hour"] = transaction_time.dt.hour
    transformed["transaction_day_of_week"] = transaction_time.dt.dayofweek

    return transformed


def add_amount_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add amount-based fraud detection features.

    Args:
        data: Transaction dataset containing a transaction_amount column.

    Returns:
        Dataset with amount-derived features added.

    Raises:
        ValueError: If transaction_amount column is missing.
    """
    if "transaction_amount" not in data.columns:
        msg = "Dataset is missing required column: transaction_amount"
        raise ValueError(msg)

    transformed = data.copy()
    amount = transformed["transaction_amount"].clip(lower=0).add(1)
    transformed["transaction_amount_log"] = amount.apply("log")

    return transformed


def build_basic_feature_table(data: pd.DataFrame) -> pd.DataFrame:
    """Build a basic feature table for fraud detection modeling.

    Args:
        data: Raw transaction dataset.

    Returns:
        Dataset with basic engineered features.
    """
    transformed = add_transaction_time_features(data)
    transformed = add_amount_features(transformed)

    return transformed
