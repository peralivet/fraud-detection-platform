"""Baseline model utilities for fraud detection."""

from dataclasses import dataclass

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


@dataclass(frozen=True)
class BaselineModelConfig:
    """Configuration for the baseline fraud model."""

    random_state: int = 42
    n_estimators: int = 100
    max_depth: int | None = 5


def build_baseline_model(config: BaselineModelConfig | None = None) -> Pipeline:
    """Build a baseline fraud detection model pipeline.

    Args:
        config: Optional baseline model configuration.

    Returns:
        A scikit-learn pipeline with preprocessing and a Random Forest classifier.
    """
    resolved_config = config or BaselineModelConfig()

    numeric_features = [
        "transaction_amount",
        "transaction_hour",
        "transaction_day_of_week",
        "transaction_amount_log",
    ]

    categorical_features = [
        "customer_id",
        "merchant_category",
        "payment_channel",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("numeric", "passthrough", numeric_features),
        ]
    )

    classifier = RandomForestClassifier(
        n_estimators=resolved_config.n_estimators,
        max_depth=resolved_config.max_depth,
        random_state=resolved_config.random_state,
        class_weight="balanced",
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def train_baseline_model(
    features: pd.DataFrame,
    target: pd.Series,
    config: BaselineModelConfig | None = None,
) -> Pipeline:
    """Train the baseline fraud detection model.

    Args:
        features: Model-ready feature table.
        target: Fraud target values.
        config: Optional baseline model configuration.

    Returns:
        Trained scikit-learn pipeline.
    """
    model = build_baseline_model(config)
    model.fit(features, target)

    return model
