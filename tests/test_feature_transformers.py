"""Tests for fraud detection feature engineering utilities."""

import pandas as pd
import pytest

from fraud_detection_platform.features.transformers import (
    add_amount_features,
    add_transaction_time_features,
    build_basic_feature_table,
)


def test_add_transaction_time_features_creates_expected_columns() -> None:
    data = pd.DataFrame(
        {
            "transaction_time": ["2026-01-01 10:30:00", "2026-01-03 23:15:00"],
        }
    )

    transformed = add_transaction_time_features(data)

    assert "transaction_hour" in transformed.columns
    assert "transaction_day_of_week" in transformed.columns
    assert transformed["transaction_hour"].tolist() == [10, 23]
    assert transformed["transaction_day_of_week"].tolist() == [3, 5]


def test_add_transaction_time_features_raises_for_missing_column() -> None:
    data = pd.DataFrame({"transaction_amount": [100.0]})

    with pytest.raises(ValueError, match="Dataset is missing required column: transaction_time"):
        add_transaction_time_features(data)


def test_add_amount_features_creates_log_amount_column() -> None:
    data = pd.DataFrame({"transaction_amount": [0.0, 99.0]})

    transformed = add_amount_features(data)

    assert "transaction_amount_log" in transformed.columns
    assert transformed["transaction_amount_log"].round(4).tolist() == [0.0, 4.6052]


def test_add_amount_features_raises_for_missing_column() -> None:
    data = pd.DataFrame({"transaction_time": ["2026-01-01 10:30:00"]})

    with pytest.raises(ValueError, match="Dataset is missing required column: transaction_amount"):
        add_amount_features(data)


def test_build_basic_feature_table_adds_time_and_amount_features() -> None:
    data = pd.DataFrame(
        {
            "transaction_time": ["2026-01-01 10:30:00"],
            "transaction_amount": [99.0],
        }
    )

    transformed = build_basic_feature_table(data)

    assert "transaction_hour" in transformed.columns
    assert "transaction_day_of_week" in transformed.columns
    assert "transaction_amount_log" in transformed.columns
