"""Tests for fraud detection data loading utilities."""

from pathlib import Path

import pandas as pd
import pytest

from fraud_detection_platform.data.loader import (
    load_transaction_data,
    split_features_and_target,
    validate_required_columns,
)


def test_validate_required_columns_accepts_valid_dataset() -> None:
    data = pd.DataFrame(
        {
            "transaction_id": ["txn_001"],
            "customer_id": ["cust_001"],
            "transaction_amount": [125.50],
            "transaction_time": ["2026-01-01 10:00:00"],
            "merchant_category": ["electronics"],
            "payment_channel": ["online"],
            "is_fraud": [0],
        }
    )

    validate_required_columns(data)


def test_validate_required_columns_raises_for_missing_columns() -> None:
    data = pd.DataFrame(
        {
            "transaction_id": ["txn_001"],
            "customer_id": ["cust_001"],
            "transaction_amount": [125.50],
        }
    )

    with pytest.raises(ValueError, match="Dataset is missing required columns"):
        validate_required_columns(data)


def test_split_features_and_target_returns_expected_columns() -> None:
    data = pd.DataFrame(
        {
            "transaction_id": ["txn_001", "txn_002"],
            "customer_id": ["cust_001", "cust_002"],
            "transaction_amount": [125.50, 75.00],
            "transaction_time": ["2026-01-01 10:00:00", "2026-01-01 11:00:00"],
            "merchant_category": ["electronics", "grocery"],
            "payment_channel": ["online", "pos"],
            "is_fraud": [0, 1],
        }
    )

    features, target = split_features_and_target(data)

    assert list(features.columns) == [
        "customer_id",
        "transaction_amount",
        "transaction_time",
        "merchant_category",
        "payment_channel",
    ]
    assert target.tolist() == [0, 1]


def test_load_transaction_data_reads_csv(tmp_path: Path) -> None:
    file_path = tmp_path / "transactions.csv"
    data = pd.DataFrame(
        {
            "transaction_id": ["txn_001"],
            "customer_id": ["cust_001"],
            "transaction_amount": [125.50],
            "transaction_time": ["2026-01-01 10:00:00"],
            "merchant_category": ["electronics"],
            "payment_channel": ["online"],
            "is_fraud": [0],
        }
    )
    data.to_csv(file_path, index=False)

    loaded_data = load_transaction_data(file_path)

    assert loaded_data.shape == (1, 7)
    assert loaded_data.loc[0, "transaction_id"] == "txn_001"


def test_load_transaction_data_raises_for_missing_file() -> None:
    with pytest.raises(FileNotFoundError, match="Transaction data file not found"):
        load_transaction_data("missing-file.csv")
