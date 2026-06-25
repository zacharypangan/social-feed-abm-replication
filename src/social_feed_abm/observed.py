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


def cascade_snapshot(
    events: list[ObservedCascadeEvent],
    max_nodes: int = 250,
) -> dict[str, object]:
    """Build a sanitized connected snapshot of an observed propagation cascade."""

    if max_nodes <= 0:
        raise ValueError("max_nodes must be positive")
    if not events:
        return {
            "type": "observed_acl2017_cascade",
            "case_name": "",
            "story_id": "",
            "nodes": [],
            "edges": [],
            "summary": {
                "observed_event_count": 0,
                "sample_node_count": 0,
                "sample_edge_count": 0,
                "max_depth": 0,
                "max_timestep": 0,
            },
        }

    ordered = sorted(
        events,
        key=lambda event: (
            0 if event.event_type == "source" else 1,
            event.timestep,
            event.delay_minutes,
            event.tweet_id,
        ),
    )
    public_ids: dict[str, str] = {}
    selected: dict[str, ObservedCascadeEvent] = {}
    depths: dict[str, int] = {}

    def public_id(tweet_id: str) -> str:
        if tweet_id not in public_ids:
            public_ids[tweet_id] = f"cascade_{len(public_ids):04d}"
        return public_ids[tweet_id]

    for event in ordered:
        if event.event_type == "source":
            selected[event.tweet_id] = event
            depths[event.tweet_id] = 0
            public_id(event.tweet_id)
            break

    if not selected:
        first = ordered[0]
        selected[first.tweet_id] = first
        depths[first.tweet_id] = 0
        public_id(first.tweet_id)

    for event in ordered:
        if len(selected) >= max_nodes:
            break
        if event.tweet_id in selected:
            continue
        if event.parent_tweet_id not in selected:
            continue
        selected[event.tweet_id] = event
        depths[event.tweet_id] = depths[event.parent_tweet_id] + 1
        public_id(event.tweet_id)

    child_counts: Counter[str] = Counter()
    edges: list[dict[str, object]] = []
    for event in selected.values():
        if event.parent_tweet_id in selected:
            edges.append(
                {
                    "source": public_id(event.parent_tweet_id),
                    "target": public_id(event.tweet_id),
                    "timestep": event.timestep,
                }
            )
            child_counts[event.parent_tweet_id] += 1

    nodes = [
        {
            "id": public_id(event.tweet_id),
            "event_type": event.event_type,
            "timestep": event.timestep,
            "depth": depths.get(event.tweet_id, 0),
            "child_count": child_counts[event.tweet_id],
        }
        for event in selected.values()
    ]

    return {
        "type": "observed_acl2017_cascade",
        "case_name": ordered[0].case_name,
        "story_id": ordered[0].story_id,
        "nodes": nodes,
        "edges": edges[: max(0, max_nodes - 1)],
        "summary": {
            "observed_event_count": len(events),
            "sample_node_count": len(nodes),
            "sample_edge_count": min(len(edges), max(0, max_nodes - 1)),
            "max_depth": max((node["depth"] for node in nodes), default=0),
            "max_timestep": max((event.timestep for event in events), default=0),
        },
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
