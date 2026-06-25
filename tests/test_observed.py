from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
FIXTURE_DIR = REPO_ROOT / "tests/fixtures/acl2017_twitter15"

from social_feed_abm.acl2017 import parse_tree_line  # noqa: E402
from social_feed_abm.observed import (  # noqa: E402
    ObservedCascadeEvent,
    cascade_snapshot,
    classify_event,
    delay_to_timestep,
    phi_series,
    reconstruct_case_events,
)


class ObservedCascadeTests(unittest.TestCase):
    def test_delay_to_timestep_uses_hourly_bins(self) -> None:
        self.assertEqual(delay_to_timestep(0.0, 60), 0)
        self.assertEqual(delay_to_timestep(59.99, 60), 0)
        self.assertEqual(delay_to_timestep(60.0, 60), 1)
        self.assertEqual(delay_to_timestep(121.0, 60), 2)

    def test_classify_event_identifies_source_edge(self) -> None:
        edge = parse_tree_line(
            "['ROOT', 'ROOT', '0.0']->['1', '505369323922522113', '0.0']"
        )

        self.assertEqual(classify_event(edge), "source")

    def test_classify_event_identifies_propagation_edge(self) -> None:
        edge = parse_tree_line(
            "['1', '505369323922522113', '0.0']->['2', '505369400000000000', '61.0']"
        )

        self.assertEqual(classify_event(edge), "propagation")

    def test_reconstruct_case_events_uses_fixture_tree(self) -> None:
        summary, events = reconstruct_case_events(
            dataset_dir=FIXTURE_DIR,
            case_name="false_tupac_hiding",
            story_id="505369323922522113",
            time_bin_minutes=60,
        )

        self.assertEqual(summary.label, "false")
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].event_type, "source")
        self.assertEqual(events[1].event_type, "propagation")

    def test_phi_series_excludes_source_and_pads_horizon(self) -> None:
        _, events = reconstruct_case_events(
            dataset_dir=FIXTURE_DIR,
            case_name="false_tupac_hiding",
            story_id="505369323922522113",
            time_bin_minutes=60,
        )

        series = phi_series(
            events=events,
            horizon_timesteps=3,
            denominator_n_agents=1000,
            count_source_events=False,
        )

        self.assertEqual(len(series), 3)
        self.assertEqual(series[0]["event_count"], 1)
        self.assertEqual(series[0]["phi"], 0.001)
        self.assertEqual(series[1]["event_count"], 0)
        self.assertEqual(series[2]["event_count"], 0)

    def test_phi_series_can_count_source_events_when_requested(self) -> None:
        _, events = reconstruct_case_events(
            dataset_dir=FIXTURE_DIR,
            case_name="false_tupac_hiding",
            story_id="505369323922522113",
            time_bin_minutes=60,
        )

        series = phi_series(
            events=events,
            horizon_timesteps=1,
            denominator_n_agents=1000,
            count_source_events=True,
        )

        self.assertEqual(series[0]["event_count"], 2)
        self.assertEqual(series[0]["phi"], 0.002)

    def test_cascade_snapshot_preserves_source_and_sanitizes_ids(self) -> None:
        events = [
            ObservedCascadeEvent(
                story_id="story",
                case_name="case",
                label="false",
                source_tweet_id="story",
                parent_user_id="ROOT",
                parent_tweet_id="ROOT",
                user_id="raw_user_1",
                tweet_id="raw_tweet_source",
                delay_minutes=0.0,
                timestep=0,
                event_type="source",
            ),
            ObservedCascadeEvent(
                story_id="story",
                case_name="case",
                label="false",
                source_tweet_id="story",
                parent_user_id="raw_user_1",
                parent_tweet_id="raw_tweet_source",
                user_id="raw_user_2",
                tweet_id="raw_tweet_child",
                delay_minutes=65.0,
                timestep=1,
                event_type="propagation",
            ),
        ]

        snapshot = cascade_snapshot(events)

        self.assertEqual(snapshot["nodes"][0]["event_type"], "source")
        self.assertEqual(snapshot["nodes"][0]["id"], "cascade_0000")
        self.assertEqual(snapshot["edges"][0]["source"], "cascade_0000")
        self.assertEqual(snapshot["edges"][0]["target"], "cascade_0001")
        self.assertNotIn("raw_tweet_source", json.dumps(snapshot))
