#!/usr/bin/env python3
"""Prepare observed cascade event tables and Phi series for ACL2017 cases."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.config import load_config  # noqa: E402
from social_feed_abm.observed import (  # noqa: E402
    phi_series,
    reconstruct_case_events,
    summarize_observed_case,
)


def main() -> int:
    config_path = _config_path()
    config = load_config(config_path)
    observed_config = config["observed_cascade"]
    output_dir = REPO_ROOT / config["data"]["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    dataset_dir = (
        REPO_ROOT / config["data"]["acl2017_root"] / config["data"]["dataset"]
    )

    combined_summary_rows: list[dict[str, object]] = []
    manifest_cases: list[dict[str, object]] = []

    for selected in config["selected_cases"]:
        case_output_dir = output_dir / selected["case_name"]
        case_output_dir.mkdir(parents=True, exist_ok=True)

        summary, events = reconstruct_case_events(
            dataset_dir=dataset_dir,
            case_name=selected["case_name"],
            story_id=selected["story_id"],
            time_bin_minutes=observed_config["time_bin_minutes"],
        )
        if summary.label != selected["expected_label"]:
            raise ValueError(
                f"{summary.story_id} expected {selected['expected_label']} "
                f"but found {summary.label}"
            )

        series = phi_series(
            events=events,
            horizon_timesteps=selected["timesteps"],
            denominator_n_agents=observed_config["phi_denominator_n_agents"],
            count_source_events=observed_config["source_events_count_for_phi"],
        )
        case_summary = {
            **summarize_observed_case(
                summary=summary,
                events=events,
                series=series,
                count_source_events=observed_config["source_events_count_for_phi"],
            ),
            "case_name": selected["case_name"],
            "role": selected["role"],
            "time_bin_minutes": observed_config["time_bin_minutes"],
            "phi_denominator_n_agents": observed_config["phi_denominator_n_agents"],
            "source_events_count_for_phi": observed_config[
                "source_events_count_for_phi"
            ],
        }

        event_rows = [event.to_dict() for event in events]
        _write_json(case_output_dir / "events.json", event_rows)
        _write_csv(case_output_dir / "events.csv", event_rows)
        _write_json(case_output_dir / "phi_by_timestep.json", series)
        _write_csv(case_output_dir / "phi_by_timestep.csv", series)
        _write_json(case_output_dir / "summary.json", case_summary)

        combined_summary_rows.append(case_summary)
        manifest_cases.append(
            {
                "case_name": selected["case_name"],
                "story_id": selected["story_id"],
                "label": summary.label,
                "event_count": len(events),
                "phi_output": str(
                    (case_output_dir / "phi_by_timestep.csv").relative_to(REPO_ROOT)
                ),
            }
        )

    _write_csv(output_dir / "observed_phi_summary.csv", combined_summary_rows)
    _write_json(output_dir / "observed_phi_summary.json", combined_summary_rows)
    _write_json(
        output_dir / "manifest.json",
        {
            "config": str(config_path),
            "dataset_dir": str(dataset_dir),
            "output_dir": str(output_dir),
            "time_bin_minutes": observed_config["time_bin_minutes"],
            "phi_denominator_n_agents": observed_config["phi_denominator_n_agents"],
            "source_events_count_for_phi": observed_config[
                "source_events_count_for_phi"
            ],
            "assumptions": [
                "ACL2017 delay_minutes are used as observed cascade time.",
                "Delays are binned into hourly timesteps by default.",
                "ROOT -> source events are preserved in event tables.",
                "Source events are excluded from observed Phi counts by default.",
                "Phi denominator uses the paper baseline n_agents=1000 as a Phase 2 approximation.",
            ],
            "raw_data_policy": "Raw ACL2017 and FakeNewsNet files are local-only and not redistributed.",
            "cases": manifest_cases,
        },
    )
    print(
        f"Wrote observed cascades for {len(combined_summary_rows)} cases to "
        f"{output_dir.relative_to(REPO_ROOT)}"
    )
    return 0


def _config_path() -> Path:
    if len(sys.argv) == 3 and sys.argv[1] == "--config":
        return REPO_ROOT / sys.argv[2]
    if len(sys.argv) == 1:
        return REPO_ROOT / "configs/phase2_observed_cascades.json"
    raise SystemExit(
        "Usage: python3 scripts/prepare_observed_cascades.py "
        "[--config configs/phase2_observed_cascades.json]"
    )


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
