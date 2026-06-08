"""Counterfactual feed-comparison helpers."""

from __future__ import annotations

from statistics import mean
from typing import Any


COMPARISON_METRICS = (
    "phi_avg_mean",
    "phi_max_mean",
    "belief_purity_avg_mean",
)


def relative_change(value: float, baseline: float) -> float:
    """Return paper-style relative change from a chronological baseline."""

    if baseline == 0:
        return 0.0
    return (value - baseline) / baseline


def relative_changes_for_case(
    summary_rows: list[dict[str, Any]],
    baseline_algorithm: str = "chronological",
) -> list[dict[str, object]]:
    """Compute per-feed metric changes relative to the baseline algorithm."""

    baseline = _find_algorithm(summary_rows, baseline_algorithm)
    changes: list[dict[str, object]] = []
    for row in summary_rows:
        change_row: dict[str, object] = {
            "case_name": row["case_name"],
            "story_id": row["story_id"],
            "label": row["label"],
            "feed_algorithm": row["feed_algorithm"],
            "baseline_algorithm": baseline_algorithm,
        }
        for metric in COMPARISON_METRICS:
            change_row[f"{metric}_relative_change"] = relative_change(
                float(row[metric]),
                float(baseline[metric]),
            )
        changes.append(change_row)
    return changes


def paper_table_rows(relative_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Map internal relative-change fields to paper-style table columns."""

    return [
        {
            "case_name": row["case_name"],
            "label": row["label"],
            "feed_algorithm": row["feed_algorithm"],
            "change_phi_avg": row["phi_avg_mean_relative_change"],
            "change_phi_max": row["phi_max_mean_relative_change"],
            "change_belief_purity": row[
                "belief_purity_avg_mean_relative_change"
            ],
        }
        for row in relative_rows
    ]


def aggregate_by_algorithm(rows: list[dict[str, Any]]) -> list[dict[str, object]]:
    """Aggregate feed summaries across cases for dashboard-level tracking."""

    algorithms = sorted({str(row["feed_algorithm"]) for row in rows})
    aggregates: list[dict[str, object]] = []
    for algorithm in algorithms:
        algorithm_rows = [row for row in rows if row["feed_algorithm"] == algorithm]
        aggregate = {"feed_algorithm": algorithm, "case_count": len(algorithm_rows)}
        for metric in COMPARISON_METRICS:
            aggregate[metric] = mean(float(row[metric]) for row in algorithm_rows)
        aggregates.append(aggregate)
    return aggregates


def _find_algorithm(
    rows: list[dict[str, Any]],
    algorithm: str,
) -> dict[str, Any]:
    for row in rows:
        if row["feed_algorithm"] == algorithm:
            return row
    raise ValueError(f"Missing baseline feed algorithm: {algorithm}")
