from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.counterfactual import (  # noqa: E402
    paper_table_rows,
    relative_change,
    relative_changes_for_case,
    replication_verdict_rows,
)


class CounterfactualTests(unittest.TestCase):
    def test_relative_change_uses_chronological_baseline(self) -> None:
        self.assertEqual(relative_change(15.0, 10.0), 0.5)

    def test_relative_change_handles_zero_baseline(self) -> None:
        self.assertEqual(relative_change(1.0, 0.0), 0.0)

    def test_relative_changes_for_case(self) -> None:
        rows = [
            {
                "case_name": "case",
                "story_id": "1",
                "label": "false",
                "feed_algorithm": "chronological",
                "phi_avg_mean": 2.0,
                "phi_max_mean": 4.0,
                "belief_purity_avg_mean": 0.5,
            },
            {
                "case_name": "case",
                "story_id": "1",
                "label": "false",
                "feed_algorithm": "popularity",
                "phi_avg_mean": 3.0,
                "phi_max_mean": 2.0,
                "belief_purity_avg_mean": 0.25,
            },
        ]

        changes = relative_changes_for_case(rows)
        popularity = changes[1]

        self.assertEqual(popularity["phi_avg_mean_relative_change"], 0.5)
        self.assertEqual(popularity["phi_max_mean_relative_change"], -0.5)
        self.assertEqual(popularity["belief_purity_avg_mean_relative_change"], -0.5)

    def test_paper_table_rows_maps_metrics(self) -> None:
        rows = paper_table_rows(
            [
                {
                    "case_name": "case",
                    "label": "false",
                    "feed_algorithm": "random",
                    "phi_avg_mean_relative_change": -0.1,
                    "phi_max_mean_relative_change": -0.2,
                    "belief_purity_avg_mean_relative_change": 0.3,
                }
            ]
        )

        self.assertEqual(rows[0]["change_phi_avg"], -0.1)
        self.assertEqual(rows[0]["change_phi_max"], -0.2)
        self.assertEqual(rows[0]["change_belief_purity"], 0.3)

    def test_replication_verdict_rows_handles_matches_and_blocked_targets(self) -> None:
        rows = replication_verdict_rows(
            [
                {
                    "case_name": "case",
                    "feed_algorithm": "chronological",
                    "metric": "p_online",
                    "actual_value": 0.101,
                }
            ],
            [
                {
                    "case_name": "case",
                    "feed_algorithm": "chronological",
                    "metric": "p_online",
                    "paper_table": "B.1",
                    "target_value": 0.1,
                },
                {
                    "case_name": "case",
                    "feed_algorithm": "popularity",
                    "metric": "change_phi_avg",
                    "paper_table": "3",
                    "target_value": None,
                },
            ],
        )

        self.assertEqual(rows[0]["verdict"], "matched")
        self.assertEqual(rows[1]["verdict"], "blocked")


if __name__ == "__main__":
    unittest.main()
