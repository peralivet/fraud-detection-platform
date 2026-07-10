"""Tests for the calibrated PaySim-enriched fraud model."""

import pandas as pd
from sklearn.calibration import CalibratedClassifierCV

from fraud_detection_platform.models.calibrated_paysim import (
    CalibratedPaySimModelConfig,
    build_calibrated_paysim_model,
    train_calibrated_paysim_model,
)
from fraud_detection_platform.models.paysim_baseline import PaySimBaselineModelConfig


def _build_training_features() -> pd.DataFrame:
    """Build a small PaySim-enriched feature table for model tests."""
    return pd.DataFrame(
        {
            "customer_id": [f"C{index % 4:03d}" for index in range(40)],
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
                75.0,
                80.0,
                85.0,
                90.0,
                95.0,
                100.0,
                105.0,
                110.0,
                115.0,
                120.0,
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
                3500.0,
                3600.0,
                3700.0,
                3800.0,
                3900.0,
                4000.0,
                4100.0,
                4200.0,
                4300.0,
                4400.0,
            ],
            "transaction_hour": [index % 24 for index in range(40)],
            "transaction_day_of_week": [index % 7 for index in range(40)],
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
                4.33,
                4.39,
                4.45,
                4.51,
                4.56,
                4.62,
                4.66,
                4.71,
                4.75,
                4.80,
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
                8.16,
                8.19,
                8.22,
                8.24,
                8.27,
                8.29,
                8.32,
                8.34,
                8.37,
                8.39,
            ],
            "merchant_category": [
                *(["payment"] * 20),
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
                "transfer",
                "cash_out",
                "transfer",
                "cash_out",
                "transfer",
                "cash_out",
                "transfer",
                "cash_out",
                "transfer",
                "cash_out",
            ],
            "payment_channel": [
                *(["payment"] * 20),
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
                "transfer",
                "cash_out",
                "transfer",
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
                75.0,
                80.0,
                85.0,
                90.0,
                95.0,
                100.0,
                105.0,
                110.0,
                115.0,
                120.0,
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
                3500.0,
                3600.0,
                3700.0,
                3800.0,
                3900.0,
                4000.0,
                4100.0,
                4200.0,
                4300.0,
                4400.0,
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
                75.0,
                80.0,
                85.0,
                90.0,
                95.0,
                100.0,
                105.0,
                110.0,
                115.0,
                120.0,
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
                3500.0,
                3600.0,
                3700.0,
                3800.0,
                3900.0,
                4000.0,
                4100.0,
                4200.0,
                4300.0,
                4400.0,
            ],
            "amount_to_origin_balance_ratio": [
                *(0.1 for _ in range(20)),
                *(1.0 for _ in range(20)),
            ],
            "amount_to_destination_balance_ratio": [
                *(0.2 for _ in range(20)),
                *(0.0 for _ in range(20)),
            ],
        }
    )


def test_build_calibrated_paysim_model_returns_calibrated_classifier() -> None:
    model = build_calibrated_paysim_model()

    assert isinstance(model, CalibratedClassifierCV)


def test_build_calibrated_paysim_model_uses_custom_config() -> None:
    config = CalibratedPaySimModelConfig(
        base_model_config=PaySimBaselineModelConfig(
            random_state=123,
            n_estimators=10,
            max_depth=3,
        ),
        calibration_method="sigmoid",
        calibration_cv=2,
    )

    model = build_calibrated_paysim_model(config)

    assert model.method == "sigmoid"
    assert model.cv == 2


def test_train_calibrated_paysim_model_fits_and_predicts() -> None:
    features = _build_training_features()
    target = pd.Series(
        [
            *(0 for _ in range(20)),
            *(1 for _ in range(20)),
        ]
    )

    config = CalibratedPaySimModelConfig(
        base_model_config=PaySimBaselineModelConfig(
            n_estimators=10,
            max_depth=3,
        ),
        calibration_cv=2,
    )

    model = train_calibrated_paysim_model(
        features=features,
        target=target,
        config=config,
    )

    predictions = model.predict(features)
    scores = model.predict_proba(features)[:, 1]

    assert len(predictions) == len(features)
    assert len(scores) == len(features)
    assert set(predictions).issubset({0, 1})
    assert all(0.0 <= score <= 1.0 for score in scores)
