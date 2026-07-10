"""Calibrated risk-band decision policy for fraud scores."""

from dataclasses import dataclass
from typing import Literal

CalibratedFraudAction = Literal[
    "approve",
    "manual_review",
    "high_risk_review",
    "priority_investigation",
]


@dataclass(frozen=True)
class CalibratedRiskDecisionPolicy:
    """Threshold-based policy for calibrated fraud scores.

    This policy is intended for calibrated rare-event fraud probabilities.

    Default bands:

        fraud_score < 0.010:
            approve

        0.010 <= fraud_score < 0.075:
            manual_review

        0.075 <= fraud_score < 0.100:
            high_risk_review

        fraud_score >= 0.100:
            priority_investigation
    """

    review_threshold: float = 0.010
    high_risk_threshold: float = 0.075
    priority_threshold: float = 0.100

    def __post_init__(self) -> None:
        """Validate calibrated decision thresholds."""
        if not 0.0 <= self.review_threshold <= 1.0:
            msg = "review_threshold must be between 0.0 and 1.0"
            raise ValueError(msg)

        if not 0.0 <= self.high_risk_threshold <= 1.0:
            msg = "high_risk_threshold must be between 0.0 and 1.0"
            raise ValueError(msg)

        if not 0.0 <= self.priority_threshold <= 1.0:
            msg = "priority_threshold must be between 0.0 and 1.0"
            raise ValueError(msg)

        if self.review_threshold >= self.high_risk_threshold:
            msg = "review_threshold must be less than high_risk_threshold"
            raise ValueError(msg)

        if self.high_risk_threshold >= self.priority_threshold:
            msg = "high_risk_threshold must be less than priority_threshold"
            raise ValueError(msg)


def recommend_calibrated_action(
    fraud_score: float,
    policy: CalibratedRiskDecisionPolicy | None = None,
) -> CalibratedFraudAction:
    """Recommend a fraud action from a calibrated fraud score.

    Args:
        fraud_score: Calibrated fraud probability-like score.
        policy: Optional calibrated risk decision policy.

    Returns:
        Recommended calibrated fraud action.

    Raises:
        ValueError: If fraud_score is outside the [0, 1] range.
    """
    if not 0.0 <= fraud_score <= 1.0:
        msg = "fraud_score must be between 0.0 and 1.0"
        raise ValueError(msg)

    resolved_policy = policy or CalibratedRiskDecisionPolicy()

    if fraud_score >= resolved_policy.priority_threshold:
        return "priority_investigation"

    if fraud_score >= resolved_policy.high_risk_threshold:
        return "high_risk_review"

    if fraud_score >= resolved_policy.review_threshold:
        return "manual_review"

    return "approve"
