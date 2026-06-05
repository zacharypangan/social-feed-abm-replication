#!/usr/bin/env python3
"""Prepare safe summaries for selected ACL2017 Twitter cases."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.acl2017 import load_case  # noqa: E402
from social_feed_abm.config import load_config  # noqa: E402


def main() -> int:
    config_path = _config_path()
    config = load_config(config_path)
    output_dir = REPO_ROOT / config["data"]["output_dir"] / "observed_cases"
    output_dir.mkdir(parents=True, exist_ok=True)

    dataset_dir = (
        REPO_ROOT / config["data"]["acl2017_root"] / config["data"]["dataset"]
    )
    rows: list[dict[str, object]] = []
    for selected in config["selected_cases"]:
        summary = load_case(dataset_dir, selected["story_id"])
        if summary.label != selected["expected_label"]:
            raise ValueError(
                f"{summary.story_id} expected {selected['expected_label']} "
                f"but found {summary.label}"
            )
        row = {
            **summary.to_dict(),
            "case_name": selected["case_name"],
            "role": selected["role"],
        }
        rows.append(row)
        _write_json(output_dir / f"{selected['case_name']}.json", row)

    _write_json(
        output_dir / "manifest.json",
        {
            "config": str(config_path),
            "dataset_dir": str(dataset_dir),
            "case_count": len(rows),
            "cases": rows,
            "data_policy": "Raw ACL2017 files are local-only and not redistributed.",
        },
    )
    _write_csv(output_dir / "case_summaries.csv", rows)
    print(f"Wrote {len(rows)} case summaries to {output_dir.relative_to(REPO_ROOT)}")
    return 0


def _config_path() -> Path:
    if len(sys.argv) == 3 and sys.argv[1] == "--config":
        return REPO_ROOT / sys.argv[2]
    if len(sys.argv) == 1:
        return REPO_ROOT / "configs/phase1_acl2017_cases.json"
    raise SystemExit(
        "Usage: python3 scripts/prepare_acl2017_cases.py "
        "[--config configs/phase1_acl2017_cases.json]"
    )


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    scalar_rows = [
        {key: value for key, value in row.items() if not isinstance(value, dict)}
        for row in rows
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scalar_rows[0]))
        writer.writeheader()
        writer.writerows(scalar_rows)


if __name__ == "__main__":
    raise SystemExit(main())
