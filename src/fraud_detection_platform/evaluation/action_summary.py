"""Risk action summary utilities for scored fraud transactions."""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class RiskActionSummary:
    """Summary statistics for one recommended action group."""

    recommended_action: str
    transaction_count: int
    percentage_of_total: float
    fraud_count: int
    non_fraud_count: int
    fraud_rate: float
    average_fraud_score: float
    average_transaction_amount: float


REQUIRED_ACTION_SUMMARY_COLUMNS: set[str] = {
    "recommended_action",
    "fraud_score",
    "transaction_amount",
}


def build_action_summary(scored_data: pd.DataFrame) -> list[RiskActionSummary]:
    """Build a risk action summary from scored fraud transactions.

    Args:
        scored_data: DataFrame containing scored transactions.

    Returns:
        Summary statistics grouped by recommended action.

    Raises:
        ValueError: If required columns are missing or scored data is empty.
    """
    if scored_data.empty:
        msg = "scored_data must not be empty"
        raise ValueError(msg)

    missing_columns = sorted(REQUIRED_ACTION_SUMMARY_COLUMNS - set(scored_data.columns))

    if missing_columns:
        msg = f"Scored data is missing required columns: {missing_columns}"
        raise ValueError(msg)

    total_rows = len(scored_data)
    summaries: list[RiskActionSummary] = []

    for recommended_action, group in scored_data.groupby("recommended_action"):
        fraud_count = int(group["is_fraud"].sum()) if "is_fraud" in group.columns else 0
        non_fraud_count = len(group) - fraud_count

        summaries.append(
            RiskActionSummary(
                recommended_action=str(recommended_action),
                transaction_count=len(group),
                percentage_of_total=len(group) / total_rows,
                fraud_count=fraud_count,
                non_fraud_count=non_fraud_count,
                fraud_rate=fraud_count / len(group),
                average_fraud_score=float(group["fraud_score"].mean()),
                average_transaction_amount=float(group["transaction_amount"].mean()),
            )
        )

    return sorted(
        summaries,
        key=lambda summary: summary.transaction_count,
        reverse=True,
    )


def build_action_summary_frame(scored_data: pd.DataFrame) -> pd.DataFrame:
    """Build a risk action summary as a DataFrame."""
    summaries = build_action_summary(scored_data)

    return pd.DataFrame(
        [
            {
                "recommended_action": summary.recommended_action,
                "transaction_count": summary.transaction_count,
                "percentage_of_total": summary.percentage_of_total,
                "fraud_count": summary.fraud_count,
                "non_fraud_count": summary.non_fraud_count,
                "fraud_rate": summary.fraud_rate,
                "average_fraud_score": summary.average_fraud_score,
                "average_transaction_amount": summary.average_transaction_amount,
            }
            for summary in summaries
        ]
    )
