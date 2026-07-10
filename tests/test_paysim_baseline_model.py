"""Tests for the PaySim-enriched baseline fraud model."""

import pandas as pd
from sklearn.pipeline import Pipeline

from fraud_detection_platform.models.paysim_baseline import (
    PaySimBaselineModelConfig,
    build_paysim_baseline_model,
    select_paysim_enriched_features,
    train_paysim_baseline_model,
)


def test_select_paysim_enriched_features_returns_expected_columns() -> None:
    data = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "transaction_amount": [100.0, 5000.0],
            "transaction_hour": [1, 2],
            "transaction_day_of_week": [0, 0],
            "transaction_amount_log": [4.61, 8.52],
            "merchant_category": ["transfer", "cash_out"],
            "payment_channel": ["transfer", "cash_out"],
            "origin_balance_delta": [100.0, 5000.0],
            "destination_balance_delta": [100.0, 5000.0],
            "amount_to_origin_balance_ratio": [0.1, 1.0],
            "amount_to_destination_balance_ratio": [0.2, 0.0],
            "extra_column": ["ignored", "ignored"],
        }
    )

    features = select_paysim_enriched_features(data)

    assert list(features.columns) == [
        "customer_id",
        "transaction_amount",
        "transaction_hour",
        "transaction_day_of_week",
        "transaction_amount_log",
        "merchant_category",
        "payment_channel",
        "origin_balance_delta",
        "destination_balance_delta",
        "amount_to_origin_balance_ratio",
        "amount_to_destination_balance_ratio",
    ]


def test_select_paysim_enriched_features_raises_for_missing_columns() -> None:
    data = pd.DataFrame(
        {
            "customer_id": ["C001"],
            "transaction_amount": [100.0],
        }
    )

    try:
        select_paysim_enriched_features(data)
    except ValueError as error:
        assert "PaySim enriched feature table is missing required columns" in str(error)
    else:
        raise AssertionError("Expected ValueError for missing PaySim enriched features")


def test_build_paysim_baseline_model_returns_pipeline() -> None:
    model = build_paysim_baseline_model()

    assert isinstance(model, Pipeline)


def test_build_paysim_baseline_model_uses_custom_config() -> None:
    config = PaySimBaselineModelConfig(
        random_state=123,
        n_estimators=10,
        max_depth=3,
    )

    model = build_paysim_baseline_model(config)

    classifier = model.named_steps["classifier"]

    assert classifier.random_state == 123
    assert classifier.n_estimators == 10
    assert classifier.max_depth == 3


def test_train_paysim_baseline_model_fits_and_predicts() -> None:
    features = pd.DataFrame(
        {
            "customer_id": [f"C{index % 4:03d}" for index in range(20)],
            "transaction_amount": [
                25.0,
                30.0,
                35.0,
                40.0,
                45.0,
                50.0,
                55.0,
                60.0,
                65.0,
                70.0,
                2500.0,
                2600.0,
                2700.0,
                2800.0,
                2900.0,
                3000.0,
                3100.0,
                3200.0,
                3300.0,
                3400.0,
            ],
            "transaction_hour": [index % 24 for index in range(20)],
            "transaction_day_of_week": [index % 7 for index in range(20)],
            "transaction_amount_log": [
                3.26,
                3.43,
                3.58,
                3.71,
                3.83,
                3.93,
                4.03,
                4.11,
                4.19,
                4.26,
                7.82,
                7.86,
                7.90,
                7.94,
                7.97,
                8.01,
                8.04,
                8.07,
                8.10,
                8.13,
            ],
            "merchant_category": [
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "transfer",
                "transfer",
                "cash_out",
                "cash_out",
                "transfer",
                "cash_out",
                "transfer",
                "cash_out",
                "transfer",
                "cash_out",
            ],
            "payment_channel": [
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "payment",
                "transfer",
                "transfer",
                "cash_out",
                "cash_out",
                "transfer",
                "cash_out",
                "transfer",
                "cash_out",
                "transfer",
                "cash_out",
            ],
            "origin_balance_delta": [
                25.0,
                30.0,
                35.0,
                40.0,
                45.0,
                50.0,
                55.0,
                60.0,
                65.0,
                70.0,
                2500.0,
                2600.0,
                2700.0,
                2800.0,
                2900.0,
                3000.0,
                3100.0,
                3200.0,
                3300.0,
                3400.0,
            ],
            "destination_balance_delta": [
                25.0,
                30.0,
                35.0,
                40.0,
                45.0,
                50.0,
                55.0,
                60.0,
                65.0,
                70.0,
                2500.0,
                2600.0,
                2700.0,
                2800.0,
                2900.0,
                3000.0,
                3100.0,
                3200.0,
                3300.0,
                3400.0,
            ],
            "amount_to_origin_balance_ratio": [
                0.1,
                0.1,
                0.1,
                0.1,
                0.1,
                0.1,
                0.1,
                0.1,
                0.1,
                0.1,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
            ],
            "amount_to_destination_balance_ratio": [
                0.2,
                0.2,
                0.2,
                0.2,
                0.2,
                0.2,
                0.2,
                0.2,
                0.2,
                0.2,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
            ],
        }
    )
    target = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    model = train_paysim_baseline_model(features, target)

    predictions = model.predict(features)
    scores = model.predict_proba(features)[:, 1]

    assert len(predictions) == len(features)
    assert len(scores) == len(features)
    assert set(predictions).issubset({0, 1})
