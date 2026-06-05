"""Feed ranking functions for the Phase 1 ABM."""

from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class FeedPost:
    """Candidate post available to an agent's feed."""

    author_id: int
    timestamp: int
    belief_value: float
    retweet_count: int
    follower_count: int


def rank_feed(
    algorithm: str,
    posts: Sequence[FeedPost],
    agent_belief: float,
    rng: random.Random,
) -> list[FeedPost]:
    """Rank candidate posts for one curation objective."""

    if algorithm == "chronological":
        return sorted(posts, key=lambda post: post.timestamp, reverse=True)
    if algorithm == "belief":
        return sorted(posts, key=lambda post: abs(post.belief_value - agent_belief))
    if algorithm == "popularity":
        return sorted(
            posts,
            key=lambda post: (post.retweet_count + post.follower_count, post.timestamp),
            reverse=True,
        )
    if algorithm == "random":
        shuffled = list(posts)
        rng.shuffle(shuffled)
        return shuffled
    raise ValueError(f"Unknown feed algorithm: {algorithm}")
