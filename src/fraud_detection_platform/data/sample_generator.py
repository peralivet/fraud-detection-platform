"""Synthetic sample data generation for the fraud detection platform."""

from pathlib import Path

import pandas as pd


def generate_sample_transactions(row_count: int = 100) -> pd.DataFrame:
    """Generate a synthetic transaction dataset for local development.

    Args:
        row_count: Number of transaction rows to generate.

    Returns:
        Synthetic transaction dataset with the required fraud schema.

    Raises:
        ValueError: If row_count is less than 2.
    """
    if row_count < 2:
        msg = "row_count must be at least 2"
        raise ValueError(msg)

    rows: list[dict[str, object]] = []

    for index in range(row_count):
        is_fraud = int(index % 5 == 0)
        transaction_amount = 2500.0 + index if is_fraud else 25.0 + index

        rows.append(
            {
                "transaction_id": f"txn_{index:06d}",
                "customer_id": f"cust_{index % 20:03d}",
                "transaction_amount": transaction_amount,
                "transaction_time": f"2026-01-{(index % 28) + 1:02d} {(index % 24):02d}:00:00",
                "merchant_category": "electronics" if is_fraud else "grocery",
                "payment_channel": "online" if is_fraud else "pos",
                "is_fraud": is_fraud,
            }
        )

    return pd.DataFrame(rows)


def write_sample_transactions(output_path: str | Path, row_count: int = 100) -> Path:
    """Write synthetic transaction data to a CSV file.

    Args:
        output_path: Destination CSV path.
        row_count: Number of rows to generate.

    Returns:
        Path to the written CSV file.
    """
    resolved_output_path = Path(output_path)
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)

    data = generate_sample_transactions(row_count=row_count)
    data.to_csv(resolved_output_path, index=False)

    return resolved_output_path
