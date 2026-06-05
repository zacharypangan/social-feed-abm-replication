"""Parsers and summaries for the ACL 2017 Twitter rumor dataset."""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class TreeNode:
    """One node tuple from an ACL2017 propagation tree."""

    user_id: str
    tweet_id: str
    delay_minutes: float


@dataclass(frozen=True)
class PropagationEdge:
    """One parent-child propagation edge."""

    parent: TreeNode
    child: TreeNode


@dataclass(frozen=True)
class CaseSummary:
    """Safe summary of one source-tweet propagation case."""

    dataset: str
    story_id: str
    label: str
    source_text: str
    edge_count: int
    node_count: int
    non_root_node_count: int
    max_delay_minutes: float
    median_delay_minutes: float
    label_counts_in_dataset: dict[str, int]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def parse_label_file(path: Path) -> dict[str, str]:
    """Parse lines shaped as ``label:source_tweet_id``."""

    labels: dict[str, str] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"{path}:{line_no} is not shaped as label:tweet_id")
        label, story_id = line.split(":", 1)
        labels[story_id.strip()] = label.strip()
    return labels


def parse_source_tweets(path: Path) -> dict[str, str]:
    """Parse source tweet content keyed by source tweet ID."""

    sources: dict[str, str] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        if "\t" not in line:
            raise ValueError(f"{path}:{line_no} is not shaped as tweet_id<TAB>text")
        story_id, text = line.split("\t", 1)
        sources[story_id.strip()] = text.strip()
    return sources


def parse_tree_line(line: str) -> PropagationEdge:
    """Parse one ACL2017 propagation edge line."""

    if "->" not in line:
        raise ValueError(f"Tree line is missing edge separator: {line!r}")
    parent_raw, child_raw = line.split("->", 1)
    return PropagationEdge(parent=_parse_node(parent_raw), child=_parse_node(child_raw))


def parse_tree_file(path: Path) -> list[PropagationEdge]:
    """Parse all propagation edges for one source tweet."""

    edges: list[PropagationEdge] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            edges.append(parse_tree_line(line))
        except ValueError as exc:
            raise ValueError(f"{path}:{line_no}: {exc}") from exc
    return edges


def load_case(dataset_dir: Path, story_id: str) -> CaseSummary:
    """Load and summarize one ACL2017 source-tweet case."""

    labels = parse_label_file(dataset_dir / "label.txt")
    sources = parse_source_tweets(dataset_dir / "source_tweets.txt")
    tree_path = dataset_dir / "tree" / f"{story_id}.txt"
    if story_id not in labels:
        raise KeyError(f"Story ID {story_id} not found in {dataset_dir / 'label.txt'}")
    if story_id not in sources:
        raise KeyError(f"Story ID {story_id} not found in source_tweets.txt")
    if not tree_path.exists():
        raise FileNotFoundError(tree_path)

    edges = parse_tree_file(tree_path)
    nodes = {edge.parent for edge in edges} | {edge.child for edge in edges}
    non_root_nodes = [node for node in nodes if node.user_id != "ROOT"]
    delays = sorted(node.delay_minutes for node in non_root_nodes)

    return CaseSummary(
        dataset=dataset_dir.name,
        story_id=story_id,
        label=labels[story_id],
        source_text=sources[story_id],
        edge_count=len(edges),
        node_count=len(nodes),
        non_root_node_count=len(non_root_nodes),
        max_delay_minutes=max(delays) if delays else 0.0,
        median_delay_minutes=_median(delays),
        label_counts_in_dataset=dict(Counter(labels.values())),
    )


def _parse_node(value: str) -> TreeNode:
    raw = ast.literal_eval(value.strip())
    if not isinstance(raw, (list, tuple)) or len(raw) != 3:
        raise ValueError(f"Node is not a 3-item tuple/list: {value!r}")
    user_id, tweet_id, delay = raw
    return TreeNode(str(user_id), str(tweet_id), float(delay))


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    midpoint = len(values) // 2
    if len(values) % 2:
        return values[midpoint]
    return (values[midpoint - 1] + values[midpoint]) / 2
