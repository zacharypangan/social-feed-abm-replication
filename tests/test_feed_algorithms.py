from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.feed_algorithms import FeedPost, rank_feed  # noqa: E402


POSTS = [
    FeedPost(author_id=1, timestamp=1, belief_value=0.2, retweet_count=2, follower_count=5),
    FeedPost(author_id=2, timestamp=3, belief_value=0.8, retweet_count=1, follower_count=1),
    FeedPost(author_id=3, timestamp=2, belief_value=0.55, retweet_count=5, follower_count=5),
]


class FeedAlgorithmTests(unittest.TestCase):
    def test_chronological_feed_sorts_by_timestamp_descending(self) -> None:
        ranked = rank_feed("chronological", POSTS, agent_belief=0.5, rng=random.Random(1))

        self.assertEqual([post.author_id for post in ranked], [2, 3, 1])

    def test_belief_feed_sorts_by_nearest_belief(self) -> None:
        ranked = rank_feed("belief", POSTS, agent_belief=0.5, rng=random.Random(1))

        self.assertEqual([post.author_id for post in ranked], [3, 1, 2])

    def test_popularity_feed_sorts_by_engagement_proxy(self) -> None:
        ranked = rank_feed("popularity", POSTS, agent_belief=0.5, rng=random.Random(1))

        self.assertEqual([post.author_id for post in ranked], [3, 1, 2])

    def test_random_feed_is_deterministic_for_seed(self) -> None:
        ranked = rank_feed("random", POSTS, agent_belief=0.5, rng=random.Random(1))

        self.assertEqual([post.author_id for post in ranked], [2, 3, 1])
