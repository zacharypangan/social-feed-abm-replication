from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.metrics import belief_purity, nrmse, phi, rmse  # noqa: E402


class MetricTests(unittest.TestCase):
    def test_phi_scales_story_tweets_by_agents(self) -> None:
        self.assertEqual(phi(25, 1000), 0.025)

    def test_belief_purity_is_one_minus_average_distance(self) -> None:
        self.assertEqual(belief_purity(0.5, [0.4, 0.6]), 0.9)

    def test_rmse_and_nrmse(self) -> None:
        observed = [0.0, 1.0, 2.0]
        predicted = [0.0, 1.0, 4.0]

        self.assertEqual(round(rmse(observed, predicted), 6), 1.154701)
        self.assertEqual(round(nrmse(observed, predicted), 6), 0.57735)
