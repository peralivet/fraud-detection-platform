"""PaySim-specific feature engineering utilities.

These features use PaySim balance columns that are not part of the generic
platform transaction schema.
"""

from typing import Final

import pandas as pd

PAYSIM_BALANCE_COLUMNS: Final[list[str]] = [
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
]


def validate_paysim_balance_columns(data: pd.DataFrame) -> None:
    """Validate that PaySim balance feature columns are present."""
    missing_columns = sorted(set(PAYSIM_BALANCE_COLUMNS) - set(data.columns))

    if missing_columns:
        msg = f"PaySim balance feature data is missing required columns: {missing_columns}"
        raise ValueError(msg)


def add_paysim_balance_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add PaySim-specific balance movement features.

    Args:
        data: Raw PaySim-style transaction data.

    Returns:
        DataFrame with additional balance movement features.
    """
    validate_paysim_balance_columns(data)

    transformed = data.copy()

    transformed["origin_balance_delta"] = (
        transformed["oldbalanceOrg"] - transformed["newbalanceOrig"]
    )

    transformed["destination_balance_delta"] = (
        transformed["newbalanceDest"] - transformed["oldbalanceDest"]
    )

    transformed["amount_to_origin_balance_ratio"] = (
        transformed["amount"] / transformed["oldbalanceOrg"].replace(0, pd.NA)
    ).fillna(0.0)

    transformed["amount_to_destination_balance_ratio"] = (
        transformed["amount"] / transformed["oldbalanceDest"].replace(0, pd.NA)
    ).fillna(0.0)

    return transformed
