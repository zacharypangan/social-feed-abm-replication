from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.fakenewsnet import (  # noqa: E402
    parse_fakenewsnet_csv,
    summarize_articles,
)


class FakeNewsNetTests(unittest.TestCase):
    def test_parse_fakenewsnet_csv_counts_tab_separated_tweet_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.csv"
            path.write_text(
                "id,news_url,title,tweet_ids\n"
                "story-1,https://example.test,Title,1\t2\t3\n"
                "story-2,https://example.test,Title,\n",
                encoding="utf-8",
            )

            rows = parse_fakenewsnet_csv(path, source="politifact", label="fake")

        self.assertEqual(rows[0].tweet_count, 3)
        self.assertEqual(rows[1].tweet_count, 0)
        self.assertEqual(rows[0].source, "politifact")

    def test_summarize_articles_groups_by_source_and_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.csv"
            path.write_text(
                "id,news_url,title,tweet_ids\n"
                "story-1,https://example.test,Title,1\t2\n"
                "story-2,https://example.test,Title,3\n",
                encoding="utf-8",
            )
            articles = parse_fakenewsnet_csv(path, source="gossipcop", label="real")

        summary = summarize_articles(articles)

        self.assertEqual(summary[0]["article_count"], 2)
        self.assertEqual(summary[0]["tweet_id_count"], 3)
        self.assertEqual(summary[0]["avg_tweet_ids_per_article"], 1.5)


if __name__ == "__main__":
    unittest.main()
