"""Tests for PaySim dataset ingestion utilities."""

from pathlib import Path

import pandas as pd
import pytest

from fraud_detection_platform.data.paysim import (
    PAYSIM_REQUIRED_COLUMNS,
    load_paysim_dataset,
    transform_paysim_to_platform_schema,
    validate_paysim_columns,
)


def test_validate_paysim_columns_accepts_required_columns() -> None:
    data = pd.DataFrame(
        {
            "step": [1],
            "type": ["TRANSFER"],
            "amount": [1000.0],
            "nameOrig": ["C123"],
            "nameDest": ["C456"],
            "isFraud": [1],
        }
    )

    validate_paysim_columns(data)


def test_validate_paysim_columns_raises_for_missing_columns() -> None:
    data = pd.DataFrame(
        {
            "step": [1],
            "type": ["TRANSFER"],
            "amount": [1000.0],
            "nameOrig": ["C123"],
        }
    )

    with pytest.raises(ValueError, match="PaySim dataset is missing required columns"):
        validate_paysim_columns(data)


def test_transform_paysim_to_platform_schema_returns_expected_columns() -> None:
    data = pd.DataFrame(
        {
            "step": [1, 2],
            "type": ["TRANSFER", "CASH_OUT"],
            "amount": [1000.0, 2500.0],
            "nameOrig": ["C123", "C789"],
            "nameDest": ["C456", "C000"],
            "isFraud": [1, 0],
        }
    )

    transformed = transform_paysim_to_platform_schema(data)

    assert list(transformed.columns) == [
        "transaction_id",
        "customer_id",
        "transaction_amount",
        "transaction_time",
        "merchant_category",
        "payment_channel",
        "is_fraud",
    ]
    assert transformed.shape == (2, len(PAYSIM_REQUIRED_COLUMNS) + 1)


def test_transform_paysim_to_platform_schema_maps_values_correctly() -> None:
    data = pd.DataFrame(
        {
            "step": [1],
            "type": ["TRANSFER"],
            "amount": [1000.0],
            "nameOrig": ["C123"],
            "nameDest": ["C456"],
            "isFraud": [1],
        }
    )

    transformed = transform_paysim_to_platform_schema(
        data,
        start_time="2026-01-01 00:00:00",
    )

    row = transformed.iloc[0]

    assert row["transaction_id"] == "paysim_txn_0000000"
    assert row["customer_id"] == "C123"
    assert row["transaction_amount"] == 1000.0
    assert row["transaction_time"] == "2026-01-01 01:00:00"
    assert row["merchant_category"] == "transfer"
    assert row["payment_channel"] == "transfer"
    assert row["is_fraud"] == 1


def test_load_paysim_dataset_reads_and_transforms_csv(tmp_path: Path) -> None:
    raw_path = tmp_path / "paysim.csv"

    raw_data = pd.DataFrame(
        {
            "step": [3],
            "type": ["CASH_OUT"],
            "amount": [500.0],
            "nameOrig": ["C999"],
            "nameDest": ["C111"],
            "isFraud": [0],
        }
    )
    raw_data.to_csv(raw_path, index=False)

    transformed = load_paysim_dataset(raw_path)

    assert transformed.shape == (1, 7)
    assert transformed.iloc[0]["transaction_id"] == "paysim_txn_0000000"
    assert transformed.iloc[0]["transaction_time"] == "2026-01-01 03:00:00"
    assert transformed.iloc[0]["is_fraud"] == 0
