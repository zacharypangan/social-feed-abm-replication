from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
FIXTURE_DIR = REPO_ROOT / "tests/fixtures/acl2017_twitter15"

from social_feed_abm.acl2017 import load_case, parse_label_file, parse_tree_line  # noqa: E402


class ACL2017Tests(unittest.TestCase):
    def test_parse_label_file_finds_selected_cases(self) -> None:
        labels = parse_label_file(FIXTURE_DIR / "label.txt")

        self.assertEqual(labels["505369323922522113"], "false")
        self.assertEqual(labels["692812029611089920"], "non-rumor")
        self.assertEqual(labels["553960736964476928"], "false")

    def test_parse_tree_line_handles_root_edge(self) -> None:
        edge = parse_tree_line(
            "['ROOT', 'ROOT', '0.0']->['15754281', '724703995147751424', '0.0']"
        )

        self.assertEqual(edge.parent.user_id, "ROOT")
        self.assertEqual(edge.child.user_id, "15754281")
        self.assertEqual(edge.child.delay_minutes, 0.0)

    def test_load_case_summarizes_tupac_case(self) -> None:
        summary = load_case(FIXTURE_DIR, "505369323922522113")

        self.assertEqual(summary.label, "false")
        self.assertIn("tupac was hiding", summary.source_text.lower())
        self.assertEqual(summary.edge_count, 2)
        self.assertGreater(summary.non_root_node_count, 0)
