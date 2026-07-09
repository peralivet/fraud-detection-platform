"""Schema definitions for fraud detection transaction data."""

from typing import Final

TARGET_COLUMN: Final[str] = "is_fraud"

TRANSACTION_ID_COLUMN: Final[str] = "transaction_id"

BASE_TRANSACTION_COLUMNS: Final[list[str]] = [
    "transaction_id",
    "customer_id",
    "transaction_amount",
    "transaction_time",
    "merchant_category",
    "payment_channel",
]

REQUIRED_COLUMNS: Final[list[str]] = [
    *BASE_TRANSACTION_COLUMNS,
    TARGET_COLUMN,
]

INFERENCE_REQUIRED_COLUMNS: Final[list[str]] = BASE_TRANSACTION_COLUMNS

FEATURE_COLUMNS: Final[list[str]] = [
    "customer_id",
    "transaction_amount",
    "transaction_hour",
    "transaction_day_of_week",
    "transaction_amount_log",
    "merchant_category",
    "payment_channel",
]
