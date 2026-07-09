"""PaySim dataset ingestion utilities.

This module transforms PaySim-style transaction data into the internal
fraud detection platform schema.
"""

from pathlib import Path
from typing import Final

import pandas as pd

from fraud_detection_platform.data.schema import REQUIRED_COLUMNS

PAYSIM_REQUIRED_COLUMNS: Final[list[str]] = [
    "step",
    "type",
    "amount",
    "nameOrig",
    "nameDest",
    "isFraud",
]


def validate_paysim_columns(data: pd.DataFrame) -> None:
    """Validate that a PaySim-style dataset contains required columns."""
    missing_columns = sorted(set(PAYSIM_REQUIRED_COLUMNS) - set(data.columns))

    if missing_columns:
        msg = f"PaySim dataset is missing required columns: {missing_columns}"
        raise ValueError(msg)


def transform_paysim_to_platform_schema(
    data: pd.DataFrame,
    start_time: str = "2026-01-01 00:00:00",
) -> pd.DataFrame:
    """Transform PaySim-style data into the platform transaction schema.

    Args:
        data: Raw PaySim-style transaction data.
        start_time: Timestamp used as the starting point for converting
            PaySim simulation steps into transaction timestamps.

    Returns:
        Transaction data matching the platform's labeled training schema.
    """
    validate_paysim_columns(data)

    transformed = pd.DataFrame()
    transformed["transaction_id"] = [f"paysim_txn_{index:07d}" for index in range(len(data))]
    transformed["customer_id"] = data["nameOrig"].astype(str)
    transformed["transaction_amount"] = data["amount"].astype(float)

    base_time = pd.Timestamp(start_time)
    transformed["transaction_time"] = [
        (base_time + pd.Timedelta(int(step), unit="h")).strftime("%Y-%m-%d %H:%M:%S")
        for step in data["step"]
    ]

    transformed["merchant_category"] = data["type"].astype(str).str.lower()
    transformed["payment_channel"] = data["type"].astype(str).str.lower()
    transformed["is_fraud"] = data["isFraud"].astype(int)

    return transformed[REQUIRED_COLUMNS]


def load_paysim_dataset(
    file_path: str | Path,
    start_time: str = "2026-01-01 00:00:00",
) -> pd.DataFrame:
    """Load a raw PaySim CSV and transform it into the platform schema."""
    raw_data = pd.read_csv(file_path)

    return transform_paysim_to_platform_schema(raw_data, start_time=start_time)
