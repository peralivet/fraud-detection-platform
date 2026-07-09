"""Tests for fraud detection baseline model utilities."""

import pandas as pd
from sklearn.pipeline import Pipeline

from fraud_detection_platform.models.baseline import (
    BaselineModelConfig,
    build_baseline_model,
    train_baseline_model,
)


def test_build_baseline_model_returns_pipeline() -> None:
    model = build_baseline_model()

    assert isinstance(model, Pipeline)
    assert "preprocessor" in model.named_steps
    assert "classifier" in model.named_steps


def test_build_baseline_model_uses_custom_config() -> None:
    config = BaselineModelConfig(
        random_state=7,
        n_estimators=10,
        max_depth=3,
    )

    model = build_baseline_model(config)
    classifier = model.named_steps["classifier"]

    assert classifier.random_state == 7
    assert classifier.n_estimators == 10
    assert classifier.max_depth == 3


def test_train_baseline_model_fits_pipeline() -> None:
    features = pd.DataFrame(
        {
            "customer_id": ["cust_001", "cust_002", "cust_003", "cust_004"],
            "transaction_amount": [25.0, 2500.0, 35.0, 3000.0],
            "transaction_hour": [10, 2, 11, 3],
            "transaction_day_of_week": [1, 5, 2, 6],
            "transaction_amount_log": [3.2581, 7.8244, 3.5835, 8.0067],
            "merchant_category": ["grocery", "electronics", "grocery", "travel"],
            "payment_channel": ["pos", "online", "pos", "online"],
        }
    )
    target = pd.Series([0, 1, 0, 1])

    config = BaselineModelConfig(n_estimators=5, max_depth=2, random_state=42)
    model = train_baseline_model(features, target, config)

    predictions = model.predict(features)
    probabilities = model.predict_proba(features)

    assert len(predictions) == 4
    assert probabilities.shape == (4, 2)
