"""Tests for synthetic fraud transaction sample generation."""

from pathlib import Path

import pytest

from fraud_detection_platform.data.sample_generator import (
    generate_sample_transactions,
    write_sample_transactions,
)


def test_generate_sample_transactions_returns_expected_shape() -> None:
    data = generate_sample_transactions(row_count=10)

    assert data.shape == (10, 7)


def test_generate_sample_transactions_contains_required_columns() -> None:
    data = generate_sample_transactions(row_count=10)

    assert list(data.columns) == [
        "transaction_id",
        "customer_id",
        "transaction_amount",
        "transaction_time",
        "merchant_category",
        "payment_channel",
        "is_fraud",
    ]


def test_generate_sample_transactions_creates_fraud_examples() -> None:
    data = generate_sample_transactions(row_count=10)

    assert data["is_fraud"].sum() > 0
    assert set(data["is_fraud"].unique()) == {0, 1}


def test_generate_sample_transactions_raises_for_invalid_row_count() -> None:
    with pytest.raises(ValueError, match="row_count must be at least 2"):
        generate_sample_transactions(row_count=1)


def test_write_sample_transactions_creates_csv_file(tmp_path: Path) -> None:
    output_path = tmp_path / "transactions.csv"

    written_path = write_sample_transactions(output_path, row_count=10)

    assert written_path == output_path
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8").startswith("transaction_id")
