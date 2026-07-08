"""Schema definitions for fraud detection transaction data."""

from typing import Final

TARGET_COLUMN: Final[str] = "is_fraud"

TRANSACTION_ID_COLUMN: Final[str] = "transaction_id"

REQUIRED_COLUMNS: Final[list[str]] = [
    "transaction_id",
    "customer_id",
    "transaction_amount",
    "transaction_time",
    "merchant_category",
    "payment_channel",
    "is_fraud",
]

FEATURE_COLUMNS: Final[list[str]] = [
    "customer_id",
    "transaction_amount",
    "transaction_time",
    "merchant_category",
    "payment_channel",
]
