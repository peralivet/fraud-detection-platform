"""Tests for PaySim-specific feature engineering utilities."""

import pandas as pd
import pytest

from fraud_detection_platform.features.paysim_features import (
    add_paysim_balance_features,
    validate_paysim_balance_columns,
)


def test_validate_paysim_balance_columns_accepts_required_columns() -> None:
    data = pd.DataFrame(
        {
            "amount": [500.0],
            "oldbalanceOrg": [1000.0],
            "newbalanceOrig": [500.0],
            "oldbalanceDest": [200.0],
            "newbalanceDest": [700.0],
        }
    )

    validate_paysim_balance_columns(data)


def test_validate_paysim_balance_columns_raises_for_missing_columns() -> None:
    data = pd.DataFrame(
        {
            "amount": [500.0],
            "oldbalanceOrg": [1000.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="PaySim balance feature data is missing required columns",
    ):
        validate_paysim_balance_columns(data)


def test_add_paysim_balance_features_adds_expected_columns() -> None:
    data = pd.DataFrame(
        {
            "amount": [500.0],
            "oldbalanceOrg": [1000.0],
            "newbalanceOrig": [500.0],
            "oldbalanceDest": [200.0],
            "newbalanceDest": [700.0],
        }
    )

    transformed = add_paysim_balance_features(data)

    assert "origin_balance_delta" in transformed.columns
    assert "destination_balance_delta" in transformed.columns
    assert "amount_to_origin_balance_ratio" in transformed.columns
    assert "amount_to_destination_balance_ratio" in transformed.columns


def test_add_paysim_balance_features_calculates_values_correctly() -> None:
    data = pd.DataFrame(
        {
            "amount": [500.0],
            "oldbalanceOrg": [1000.0],
            "newbalanceOrig": [500.0],
            "oldbalanceDest": [200.0],
            "newbalanceDest": [700.0],
        }
    )

    transformed = add_paysim_balance_features(data)
    row = transformed.iloc[0]

    assert row["origin_balance_delta"] == 500.0
    assert row["destination_balance_delta"] == 500.0
    assert row["amount_to_origin_balance_ratio"] == 0.5
    assert row["amount_to_destination_balance_ratio"] == 2.5


def test_add_paysim_balance_features_handles_zero_balances() -> None:
    data = pd.DataFrame(
        {
            "amount": [500.0],
            "oldbalanceOrg": [0.0],
            "newbalanceOrig": [0.0],
            "oldbalanceDest": [0.0],
            "newbalanceDest": [500.0],
        }
    )

    transformed = add_paysim_balance_features(data)
    row = transformed.iloc[0]

    assert row["amount_to_origin_balance_ratio"] == 0.0
    assert row["amount_to_destination_balance_ratio"] == 0.0
