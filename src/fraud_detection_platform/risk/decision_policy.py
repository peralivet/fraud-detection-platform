"""Risk decision policy for fraud detection outputs."""

from dataclasses import dataclass
from typing import Literal

FraudAction = Literal["approve", "manual_review", "block"]


@dataclass(frozen=True)
class RiskDecisionPolicy:
    """Threshold-based policy for converting fraud scores into business actions.

    The model produces a probability-like fraud score.
    This policy converts that score into an operational recommendation.

    Example:
        0.20 -> approve
        0.65 -> manual_review
        0.90 -> block
    """

    review_threshold: float = 0.5
    block_threshold: float = 0.8

    def __post_init__(self) -> None:
        """Validate policy thresholds."""
        if not 0.0 <= self.review_threshold <= 1.0:
            msg = "review_threshold must be between 0.0 and 1.0"
            raise ValueError(msg)

        if not 0.0 <= self.block_threshold <= 1.0:
            msg = "block_threshold must be between 0.0 and 1.0"
            raise ValueError(msg)

        if self.review_threshold >= self.block_threshold:
            msg = "review_threshold must be less than block_threshold"
            raise ValueError(msg)


def recommend_action(
    fraud_score: float,
    policy: RiskDecisionPolicy | None = None,
) -> FraudAction:
    """Recommend a business action from a fraud score.

    Args:
        fraud_score: Probability-like score between 0.0 and 1.0.
        policy: Optional risk decision policy.

    Returns:
        Recommended fraud action.

    Raises:
        ValueError: If fraud_score is outside the valid range.
    """
    if not 0.0 <= fraud_score <= 1.0:
        msg = "fraud_score must be between 0.0 and 1.0"
        raise ValueError(msg)

    resolved_policy = policy or RiskDecisionPolicy()

    if fraud_score >= resolved_policy.block_threshold:
        return "block"

    if fraud_score >= resolved_policy.review_threshold:
        return "manual_review"

    return "approve"
