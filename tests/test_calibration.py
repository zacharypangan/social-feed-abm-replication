from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.calibration import (  # noqa: E402
    best_candidate,
    calibration_scores,
    mean_series,
    probability_grid,
)


class CalibrationTests(unittest.TestCase):
    def test_probability_grid_applies_multipliers_and_clips(self) -> None:
        candidates = probability_grid(
            {"p_online": 0.8, "p_reshare": 0.2, "p_reject": 0.1},
            {
                "p_online": [1.0, 2.0],
                "p_reshare": [0.5],
                "p_reject": [1.0],
            },
        )

        self.assertEqual(len(candidates), 2)
        self.assertEqual(candidates[0]["p_online"], 0.8)
        self.assertEqual(candidates[1]["p_online"], 1.0)
        self.assertEqual(candidates[0]["p_reshare"], 0.1)

    def test_mean_series_averages_elementwise(self) -> None:
        averaged = mean_series([[0.0, 1.0, 2.0], [2.0, 3.0, 4.0]])

        self.assertEqual(averaged, [1.0, 2.0, 3.0])

    def test_mean_series_rejects_mismatched_lengths(self) -> None:
        with self.assertRaises(ValueError):
            mean_series([[0.0], [0.0, 1.0]])

    def test_calibration_scores_use_rmse_and_nrmse(self) -> None:
        scores = calibration_scores([0.0, 1.0, 2.0], [0.0, 1.0, 4.0])

        self.assertEqual(round(scores["rmse"], 6), 1.154701)
        self.assertEqual(round(scores["nrmse"], 6), 0.57735)

    def test_best_candidate_prefers_nrmse_then_rmse(self) -> None:
        selected = best_candidate(
            [
                {"candidate_index": 0, "nrmse": 0.4, "rmse": 0.2},
                {"candidate_index": 1, "nrmse": 0.3, "rmse": 0.5},
                {"candidate_index": 2, "nrmse": 0.3, "rmse": 0.1},
            ]
        )

        self.assertEqual(selected["candidate_index"], 2)


if __name__ == "__main__":
    unittest.main()
