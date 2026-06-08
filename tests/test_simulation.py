from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.feed_algorithms import FeedPost  # noqa: E402
from social_feed_abm.simulation import SimulationParams, run_simulation, summarize_runs  # noqa: E402


class SimulationTests(unittest.TestCase):
    def test_run_simulation_includes_phase3_trace_fields(self) -> None:
        params = SimulationParams(
            n_agents=30,
            avg_followees=5,
            avg_viewed_posts=4,
            timesteps=6,
            initial_infected=0.2,
            p_online=0.8,
            p_reshare=0.3,
            p_reject=0.1,
            seed=7,
            verified_probability=0.1,
        )

        result = run_simulation(params, "chronological")

        self.assertEqual(result["timesteps"], 6)
        self.assertEqual(len(result["event_counts_by_timestep"]), 6)
        self.assertEqual(len(result["state_counts_by_timestep"]), 6)
        self.assertIn("network_summary", result)
        self.assertIn("online", result["event_counts_by_timestep"][0])
        self.assertIn("believe", result["state_counts_by_timestep"][0])
        self.assertEqual(result["network_summary"]["n_agents"], 30.0)

    def test_summarize_runs_includes_phase3_event_means(self) -> None:
        runs = [
            {
                "phi_avg": 0.1,
                "phi_max": 0.2,
                "belief_purity_avg": 0.3,
                "total_story_tweets": 4,
                "event_counts_by_timestep": [
                    {"online": 2, "reshare": 1, "believe": 1, "deny": 0},
                    {"online": 3, "reshare": 2, "believe": 0, "deny": 1},
                ],
            },
            {
                "phi_avg": 0.2,
                "phi_max": 0.4,
                "belief_purity_avg": 0.5,
                "total_story_tweets": 6,
                "event_counts_by_timestep": [
                    {"online": 4, "reshare": 3, "believe": 2, "deny": 1}
                ],
            },
        ]

        summary = summarize_runs(runs)

        self.assertEqual(summary["total_story_tweets_mean"], 5.0)
        self.assertEqual(summary["online_events_mean"], 4.5)
        self.assertEqual(summary["reshare_events_mean"], 3.0)
        self.assertEqual(summary["believe_events_mean"], 1.5)
        self.assertEqual(summary["deny_events_mean"], 1.0)

    def test_feed_posts_support_popularity_feedback(self) -> None:
        post = FeedPost(
            author_id=1,
            timestamp=0,
            belief_value=0.4,
            retweet_count=2,
            follower_count=10,
            story_id="example",
            source_author_id=1,
        )

        post.retweet_count += 1

        self.assertEqual(post.retweet_count, 3)
        self.assertEqual(post.story_id, "example")


if __name__ == "__main__":
    unittest.main()
