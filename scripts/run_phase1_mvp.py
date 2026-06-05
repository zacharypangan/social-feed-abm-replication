#!/usr/bin/env python3
"""Run the Phase 1 data-assisted ABM MVP."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.acl2017 import load_case  # noqa: E402
from social_feed_abm.config import load_config  # noqa: E402
from social_feed_abm.simulation import SimulationParams, run_simulation, summarize_runs  # noqa: E402


def main() -> int:
    config_path = _config_path()
    config = load_config(config_path)
    output_dir = REPO_ROOT / config["data"]["output_dir"] / "simulations"
    output_dir.mkdir(parents=True, exist_ok=True)

    dataset_dir = (
        REPO_ROOT / config["data"]["acl2017_root"] / config["data"]["dataset"]
    )
    simulation_config = config["simulation"]
    summaries: list[dict[str, object]] = []

    for case_index, selected in enumerate(config["selected_cases"]):
        case_summary = load_case(dataset_dir, selected["story_id"])
        case_output_dir = output_dir / selected["case_name"]
        case_output_dir.mkdir(parents=True, exist_ok=True)

        for algorithm in simulation_config["feed_algorithms"]:
            runs = []
            for run_index in range(simulation_config["n_sims"]):
                seed = config["seed"] + (case_index * 1000) + (run_index * 100)
                seed += simulation_config["feed_algorithms"].index(algorithm)
                params = SimulationParams(
                    n_agents=simulation_config["n_agents"],
                    avg_followees=simulation_config["avg_followees"],
                    avg_viewed_posts=simulation_config["avg_viewed_posts"],
                    timesteps=selected["timesteps"],
                    initial_infected=selected["initial_infected"],
                    p_online=selected["probabilities"]["p_online"],
                    p_reshare=selected["probabilities"]["p_reshare"],
                    p_reject=selected["probabilities"]["p_reject"],
                    seed=seed,
                )
                result = run_simulation(params, algorithm)
                result.update(
                    {
                        "run_index": run_index,
                        "seed": seed,
                        "case_name": selected["case_name"],
                        "story_id": selected["story_id"],
                        "observed_label": case_summary.label,
                    }
                )
                runs.append(result)

            aggregate = {
                "case_name": selected["case_name"],
                "story_id": selected["story_id"],
                "label": case_summary.label,
                "feed_algorithm": algorithm,
                "n_sims": simulation_config["n_sims"],
                **summarize_runs(runs),
            }
            summaries.append(aggregate)
            _write_json(case_output_dir / f"{algorithm}_runs.json", runs)

    _write_json(
        output_dir / "run_manifest.json",
        {
            "config": str(config_path),
            "dataset_dir": str(dataset_dir),
            "raw_data_policy": "Raw ACL2017 and FakeNewsNet data are local-only.",
            "assumptions": [
                "Phase 1 uses observed cascades for case selection and summaries.",
                "Counterfactual feed runs use a synthetic network and MVP behavior.",
                "Full calibration search and plotted figures are deferred.",
            ],
            "summary_count": len(summaries),
        },
    )
    _write_json(output_dir / "metrics_summary.json", summaries)
    _write_csv(output_dir / "metrics_summary.csv", summaries)
    print(f"Wrote Phase 1 MVP outputs to {output_dir.relative_to(REPO_ROOT)}")
    return 0


def _config_path() -> Path:
    if len(sys.argv) == 3 and sys.argv[1] == "--config":
        return REPO_ROOT / sys.argv[2]
    if len(sys.argv) == 1:
        return REPO_ROOT / "configs/phase1_acl2017_cases.json"
    raise SystemExit(
        "Usage: python3 scripts/run_phase1_mvp.py "
        "[--config configs/phase1_acl2017_cases.json]"
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
