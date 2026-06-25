from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.feed_algorithms import FeedPost  # noqa: E402
from social_feed_abm.simulation import (  # noqa: E402
    SimulationParams,
    _bayesian_posterior,
    _make_agents,
    _sample_probability,
    _sample_viewed_post_count,
    network_snapshot,
    run_simulation,
    summarize_runs,
)


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

    def test_barabasi_albert_network_is_deterministic_and_consistent(self) -> None:
        import random

        params = SimulationParams(
            n_agents=80,
            avg_followees=12,
            avg_viewed_posts=4,
            timesteps=2,
            initial_infected=0.2,
            p_online=0.5,
            p_reshare=0.2,
            p_reject=0.1,
            seed=11,
        )

        first = _make_agents(params, random.Random(params.seed))
        second = _make_agents(params, random.Random(params.seed))
        first_edges = {
            (agent.agent_id, followee_id)
            for agent in first
            for followee_id in agent.followees
        }
        second_edges = {
            (agent.agent_id, followee_id)
            for agent in second
            for followee_id in agent.followees
        }

        self.assertEqual(first_edges, second_edges)
        self.assertFalse(any(source == target for source, target in first_edges))
        for source, target in first_edges:
            self.assertIn(source, first[target].followers)
        avg_followees = sum(len(agent.followees) for agent in first) / len(first)
        self.assertGreater(avg_followees, 8)
        self.assertGreater(
            max(len(agent.followers) for agent in first),
            avg_followees,
        )

    def test_network_snapshot_caps_and_sanitizes(self) -> None:
        import random

        params = SimulationParams(
            n_agents=40,
            avg_followees=8,
            avg_viewed_posts=4,
            timesteps=2,
            initial_infected=0.2,
            p_online=0.5,
            p_reshare=0.2,
            p_reject=0.1,
            seed=17,
        )
        agents = _make_agents(params, random.Random(params.seed))

        snapshot = network_snapshot(agents, max_nodes=10, max_edges=12)

        self.assertEqual(snapshot["sample"]["node_count"], 10)
        self.assertLessEqual(snapshot["sample"]["edge_count"], 12)
        self.assertTrue(snapshot["nodes"][0]["id"].startswith("agent_"))

    def test_sampled_nposts_can_be_fixed_or_stochastic(self) -> None:
        import random

        fixed = SimulationParams(
            n_agents=10,
            avg_followees=3,
            avg_viewed_posts=4,
            timesteps=1,
            initial_infected=0.2,
            p_online=0.5,
            p_reshare=0.2,
            p_reject=0.1,
            seed=1,
        )
        sampled = SimulationParams(**{**fixed.__dict__, "avg_viewed_posts_std": 2})

        self.assertEqual(_sample_viewed_post_count(fixed, random.Random(1)), 4)
        self.assertGreaterEqual(_sample_viewed_post_count(sampled, random.Random(1)), 1)

    def test_probability_sampling_can_be_disabled(self) -> None:
        import random

        params = SimulationParams(
            n_agents=10,
            avg_followees=3,
            avg_viewed_posts=4,
            timesteps=1,
            initial_infected=0.2,
            p_online=0.5,
            p_reshare=0.2,
            p_reject=0.1,
            seed=1,
            probability_sampling=False,
            probability_std_fraction=0.5,
        )

        self.assertEqual(_sample_probability(0.25, params, random.Random(1)), 0.25)

    def test_bayesian_update_moves_toward_evidence(self) -> None:
        self.assertGreater(_bayesian_posterior(0.4, 0.8), 0.4)
        self.assertLess(_bayesian_posterior(0.6, 0.2), 0.6)


if __name__ == "__main__":
    unittest.main()
