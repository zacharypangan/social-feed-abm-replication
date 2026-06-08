"""Safe summaries for local FakeNewsNet metadata CSVs."""

from __future__ import annotations

import csv
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class FakeNewsNetArticle:
    """One local FakeNewsNet metadata row."""

    source: str
    label: str
    article_id: str
    tweet_count: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def parse_fakenewsnet_csv(path: Path, source: str, label: str) -> list[FakeNewsNetArticle]:
    """Parse one FakeNewsNet metadata CSV without exposing tweet IDs."""

    csv.field_size_limit(sys.maxsize)
    articles: list[FakeNewsNetArticle] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            tweet_ids = [
                value for value in row.get("tweet_ids", "").split("\t") if value.strip()
            ]
            articles.append(
                FakeNewsNetArticle(
                    source=source,
                    label=label,
                    article_id=row["id"],
                    tweet_count=len(tweet_ids),
                )
            )
    return articles


def summarize_articles(articles: list[FakeNewsNetArticle]) -> list[dict[str, object]]:
    """Summarize article and tweet-ID counts by source and label."""

    groups = sorted({(article.source, article.label) for article in articles})
    summaries: list[dict[str, object]] = []
    for source, label in groups:
        group = [
            article for article in articles
            if article.source == source and article.label == label
        ]
        tweet_counts = [article.tweet_count for article in group]
        summaries.append(
            {
                "source": source,
                "label": label,
                "article_count": len(group),
                "tweet_id_count": sum(tweet_counts),
                "min_tweet_ids_per_article": min(tweet_counts) if tweet_counts else 0,
                "max_tweet_ids_per_article": max(tweet_counts) if tweet_counts else 0,
                "avg_tweet_ids_per_article": (
                    sum(tweet_counts) / len(tweet_counts) if tweet_counts else 0.0
                ),
            }
        )
    return summaries
