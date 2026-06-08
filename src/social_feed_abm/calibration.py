"""Calibration helpers for chronological-feed validation."""

from __future__ import annotations

from itertools import product
from statistics import mean
from typing import Any

from social_feed_abm.metrics import nrmse, rmse


PROBABILITY_KEYS = ("p_online", "p_reshare", "p_reject")


def probability_grid(
    base_probabilities: dict[str, float],
    multipliers: dict[str, list[float]],
) -> list[dict[str, float]]:
    """Generate bounded probability candidates around paper values."""

    missing = [key for key in PROBABILITY_KEYS if key not in base_probabilities]
    if missing:
        raise KeyError(f"Missing base probabilities: {', '.join(missing)}")

    multiplier_lists = [
        multipliers.get(key, [1.0])
        for key in PROBABILITY_KEYS
    ]
    candidates: list[dict[str, float]] = []
    seen: set[tuple[float, float, float]] = set()

    for values in product(*multiplier_lists):
        candidate = {
            key: _clip_probability(base_probabilities[key] * multiplier)
            for key, multiplier in zip(PROBABILITY_KEYS, values)
        }
        signature = tuple(round(candidate[key], 12) for key in PROBABILITY_KEYS)
        if signature not in seen:
            seen.add(signature)
            candidates.append(candidate)
    return candidates


def mean_series(series_list: list[list[float]]) -> list[float]:
    """Average equal-length series elementwise."""

    if not series_list:
        return []
    expected_length = len(series_list[0])
    for series in series_list:
        if len(series) != expected_length:
            raise ValueError("all series must have equal length")
    return [
        mean(series[timestep] for series in series_list)
        for timestep in range(expected_length)
    ]


def calibration_scores(
    observed_phi: list[float],
    predicted_phi: list[float],
) -> dict[str, float]:
    """Compute Phase 4 fit metrics."""

    return {
        "rmse": rmse(observed_phi, predicted_phi),
        "nrmse": nrmse(observed_phi, predicted_phi),
    }


def best_candidate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Select the lowest-NRMSE candidate, breaking ties by RMSE."""

    if not rows:
        raise ValueError("at least one candidate row is required")
    return min(rows, key=lambda row: (float(row["nrmse"]), float(row["rmse"])))


def _clip_probability(value: float) -> float:
    return min(1.0, max(0.0, value))
