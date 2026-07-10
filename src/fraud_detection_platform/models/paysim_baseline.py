"""PaySim-enriched baseline model utilities.

This model uses the generic fraud platform features plus PaySim-specific
financial behavior features.
"""

from dataclasses import dataclass

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

PAYSIM_ENRICHED_FEATURE_COLUMNS: list[str] = [
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


@dataclass(frozen=True)
class PaySimBaselineModelConfig:
    """Configuration for the PaySim-enriched fraud model."""

    random_state: int = 42
    n_estimators: int = 100
    max_depth: int | None = 5


def select_paysim_enriched_features(data: pd.DataFrame) -> pd.DataFrame:
    """Select PaySim-enriched model features."""
    missing_columns = sorted(set(PAYSIM_ENRICHED_FEATURE_COLUMNS) - set(data.columns))

    if missing_columns:
        msg = f"PaySim enriched feature table is missing required columns: {missing_columns}"
        raise ValueError(msg)

    return data[PAYSIM_ENRICHED_FEATURE_COLUMNS].copy()


def build_paysim_baseline_model(
    config: PaySimBaselineModelConfig | None = None,
) -> Pipeline:
    """Build a PaySim-enriched baseline fraud detection model pipeline."""
    resolved_config = config or PaySimBaselineModelConfig()

    numeric_features = [
        "transaction_amount",
        "transaction_hour",
        "transaction_day_of_week",
        "transaction_amount_log",
        "origin_balance_delta",
        "destination_balance_delta",
        "amount_to_origin_balance_ratio",
        "amount_to_destination_balance_ratio",
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


def train_paysim_baseline_model(
    features: pd.DataFrame,
    target: pd.Series,
    config: PaySimBaselineModelConfig | None = None,
) -> Pipeline:
    """Train the PaySim-enriched baseline fraud detection model."""
    model = build_paysim_baseline_model(config)
    model.fit(features, target)

    return model
