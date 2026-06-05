"""Metrics for the Social Feed ABM replication."""

from __future__ import annotations

from collections.abc import Sequence
from math import sqrt


def phi(story_tweet_count: int, n_agents: int) -> float:
    """Proportion of story-related tweets per timestep."""

    if n_agents <= 0:
        raise ValueError("n_agents must be positive")
    return story_tweet_count / n_agents


def belief_purity(agent_belief: float, feed_beliefs: Sequence[float]) -> float:
    """Compute 1 minus average belief distance for one viewed feed."""

    if not feed_beliefs:
        return 0.0
    avg_distance = sum(abs(agent_belief - belief) for belief in feed_beliefs) / len(
        feed_beliefs
    )
    return max(0.0, min(1.0, 1.0 - avg_distance))


def rmse(observed: Sequence[float], predicted: Sequence[float]) -> float:
    """Root mean squared error."""

    _validate_equal_length(observed, predicted)
    if not observed:
        return 0.0
    mse = sum((left - right) ** 2 for left, right in zip(observed, predicted)) / len(
        observed
    )
    return sqrt(mse)


def nrmse(observed: Sequence[float], predicted: Sequence[float]) -> float:
    """Normalized RMSE using observed range."""

    if not observed:
        return 0.0
    spread = max(observed) - min(observed)
    if spread == 0:
        return 0.0
    return rmse(observed, predicted) / spread


def _validate_equal_length(observed: Sequence[float], predicted: Sequence[float]) -> None:
    if len(observed) != len(predicted):
        raise ValueError("observed and predicted sequences must have equal length")
