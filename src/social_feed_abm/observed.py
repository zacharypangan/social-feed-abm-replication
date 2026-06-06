"""Observed cascade reconstruction from ACL2017 propagation trees."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from social_feed_abm.acl2017 import (
    CaseSummary,
    PropagationEdge,
    load_case,
    parse_tree_file,
)
from social_feed_abm.metrics import phi


@dataclass(frozen=True)
class ObservedCascadeEvent:
    """One reconstructed observed cascade event."""

    story_id: str
    case_name: str
    label: str
    source_tweet_id: str
    parent_user_id: str
    parent_tweet_id: str
    user_id: str
    tweet_id: str
    delay_minutes: float
    timestep: int
    event_type: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def delay_to_timestep(delay_minutes: float, time_bin_minutes: int) -> int:
    """Convert minute delay to a zero-based timestep."""

    if time_bin_minutes <= 0:
        raise ValueError("time_bin_minutes must be positive")
    if delay_minutes < 0:
        raise ValueError("delay_minutes must be non-negative")
    return int(delay_minutes // time_bin_minutes)


def classify_event(edge: PropagationEdge) -> str:
    """Classify a tree edge as source or propagation."""

    if edge.parent.user_id == "ROOT" and edge.parent.tweet_id == "ROOT":
        return "source"
    return "propagation"


def reconstruct_case_events(
    dataset_dir: Path,
    case_name: str,
    story_id: str,
    time_bin_minutes: int,
) -> tuple[CaseSummary, list[ObservedCascadeEvent]]:
    """Reconstruct observed event rows for one ACL2017 case."""

    summary = load_case(dataset_dir, story_id)
    edges = parse_tree_file(dataset_dir / "tree" / f"{story_id}.txt")
    events = [
        _edge_to_event(edge, summary, case_name, time_bin_minutes) for edge in edges
    ]
    events.sort(key=lambda event: (event.timestep, event.delay_minutes, event.tweet_id))
    return summary, events


def phi_series(
    events: list[ObservedCascadeEvent],
    horizon_timesteps: int,
    denominator_n_agents: int,
    count_source_events: bool = False,
) -> list[dict[str, object]]:
    """Build a padded observed Phi time series from reconstructed events."""

    if horizon_timesteps <= 0:
        raise ValueError("horizon_timesteps must be positive")
    counts: Counter[int] = Counter()
    for event in events:
        if event.event_type == "source" and not count_source_events:
            continue
        if event.timestep < horizon_timesteps:
            counts[event.timestep] += 1

    return [
        {
            "timestep": timestep,
            "event_count": counts[timestep],
            "phi": phi(counts[timestep], denominator_n_agents),
        }
        for timestep in range(horizon_timesteps)
    ]


def summarize_observed_case(
    summary: CaseSummary,
    events: list[ObservedCascadeEvent],
    series: list[dict[str, object]],
    count_source_events: bool,
) -> dict[str, object]:
    """Create a compact summary for manifests and combined outputs."""

    counted_events = [
        event
        for event in events
        if count_source_events or event.event_type != "source"
    ]
    return {
        "dataset": summary.dataset,
        "story_id": summary.story_id,
        "label": summary.label,
        "source_text": summary.source_text,
        "event_count": len(events),
        "counted_event_count": len(counted_events),
        "source_event_count": sum(1 for event in events if event.event_type == "source"),
        "propagation_event_count": sum(
            1 for event in events if event.event_type == "propagation"
        ),
        "horizon_timesteps": len(series),
        "observed_phi_avg": sum(float(row["phi"]) for row in series) / len(series),
        "observed_phi_max": max(float(row["phi"]) for row in series),
    }


def _edge_to_event(
    edge: PropagationEdge,
    summary: CaseSummary,
    case_name: str,
    time_bin_minutes: int,
) -> ObservedCascadeEvent:
    return ObservedCascadeEvent(
        story_id=summary.story_id,
        case_name=case_name,
        label=summary.label,
        source_tweet_id=summary.story_id,
        parent_user_id=edge.parent.user_id,
        parent_tweet_id=edge.parent.tweet_id,
        user_id=edge.child.user_id,
        tweet_id=edge.child.tweet_id,
        delay_minutes=edge.child.delay_minutes,
        timestep=delay_to_timestep(edge.child.delay_minutes, time_bin_minutes),
        event_type=classify_event(edge),
    )
