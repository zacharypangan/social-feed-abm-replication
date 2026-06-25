"""Feed ranking functions for the Social Feed ABM replication."""

from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Optional


@dataclass
class FeedPost:
    """Candidate post available to an agent's feed."""

    author_id: int
    timestamp: int
    belief_value: float
    retweet_count: int
    follower_count: int
    story_id: str = "story"
    source_author_id: Optional[int] = None
    is_story: bool = True
    verified_author: bool = False


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
            key=lambda post: (
                post.retweet_count,
                post.follower_count,
                post.timestamp,
            ),
            reverse=True,
        )
    if algorithm == "random":
        shuffled = list(posts)
        rng.shuffle(shuffled)
        return shuffled
    raise ValueError(f"Unknown feed algorithm: {algorithm}")
