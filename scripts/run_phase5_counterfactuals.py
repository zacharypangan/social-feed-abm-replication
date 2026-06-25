#!/usr/bin/env python3
"""Run Phase 5 paper-aligned case-study counterfactuals."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.config import load_config  # noqa: E402
from social_feed_abm.counterfactual import (  # noqa: E402
    aggregate_by_algorithm,
    paper_table_rows,
    relative_changes_for_case,
)
from social_feed_abm.fakenewsnet import (  # noqa: E402
    parse_fakenewsnet_csv,
    summarize_articles,
)
from social_feed_abm.simulation import SimulationParams, run_simulation, summarize_runs  # noqa: E402


def main() -> int:
    config_path = _config_path()
    config = load_config(config_path)
    output_dir = REPO_ROOT / config["data"]["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    calibration_rows = _load_calibration_rows(
        REPO_ROOT / config["data"]["calibration_output_dir"]
    )
    simulation_config = config["simulation"]
    fidelity_config = config["model_fidelity"]

    all_summary_rows: list[dict[str, object]] = []
    all_relative_rows: list[dict[str, object]] = []
    all_paper_rows: list[dict[str, object]] = []

    for case_index, selected in enumerate(config["selected_cases"]):
        case_output_dir = output_dir / selected["case_name"]
        case_output_dir.mkdir(parents=True, exist_ok=True)
        calibration = _calibration_for_case(calibration_rows, selected["case_name"])
        case_summary_rows: list[dict[str, object]] = []

        for algorithm_index, algorithm in enumerate(simulation_config["feed_algorithms"]):
            runs = []
            for run_index in range(simulation_config["n_sims"]):
                seed = _seed_for(config["seed"], case_index, algorithm_index, run_index)
                params = SimulationParams(
                    n_agents=simulation_config["n_agents"],
                    avg_followees=simulation_config["avg_followees"],
                    avg_viewed_posts=simulation_config["avg_viewed_posts"],
                    timesteps=selected["timesteps"],
                    initial_infected=selected["initial_infected"],
                    p_online=float(calibration["p_online"]),
                    p_reshare=float(calibration["p_reshare"]),
                    p_reject=float(calibration["p_reject"]),
                    seed=seed,
                    belief_acceptance_distance=fidelity_config[
                        "belief_acceptance_distance"
                    ],
                    belief_update_rate=fidelity_config["belief_update_rate"],
                    recent_posts_per_followee=fidelity_config[
                        "recent_posts_per_followee"
                    ],
                    verified_probability=fidelity_config["verified_probability"],
                    popularity_feedback=fidelity_config["popularity_feedback"],
                )
                result = run_simulation(params, algorithm)
                result.update(
                    {
                        "run_index": run_index,
                        "seed": seed,
                        "case_name": selected["case_name"],
                        "story_id": selected["story_id"],
                        "label": selected["expected_label"],
                        "phase": config["project"]["phase"],
                        "calibration_candidate_index": calibration["candidate_index"],
                    }
                )
                runs.append(result)

            aggregate = {
                "case_name": selected["case_name"],
                "story_id": selected["story_id"],
                "label": selected["expected_label"],
                "role": selected["role"],
                "feed_algorithm": algorithm,
                "n_sims": simulation_config["n_sims"],
                "calibration_candidate_index": calibration["candidate_index"],
                "p_online": calibration["p_online"],
                "p_reshare": calibration["p_reshare"],
                "p_reject": calibration["p_reject"],
                **summarize_runs(runs),
            }
            case_summary_rows.append(aggregate)
            _write_json(case_output_dir / f"{algorithm}_runs.json", runs)

        relative_rows = relative_changes_for_case(case_summary_rows)
        paper_rows = paper_table_rows(relative_rows)
        all_summary_rows.extend(case_summary_rows)
        all_relative_rows.extend(relative_rows)
        all_paper_rows.extend(paper_rows)
        _write_json(case_output_dir / "metrics_summary.json", case_summary_rows)
        _write_csv(case_output_dir / "metrics_summary.csv", case_summary_rows)
        _write_json(case_output_dir / "relative_changes.json", relative_rows)
        _write_csv(case_output_dir / "relative_changes.csv", relative_rows)
        _write_json(case_output_dir / "paper_table_rows.json", paper_rows)
        _write_csv(case_output_dir / "paper_table_rows.csv", paper_rows)

    fakenewsnet_summary = _run_fakenewsnet_audit(config, output_dir)
    _write_json(output_dir / "metrics_summary.json", all_summary_rows)
    _write_csv(output_dir / "metrics_summary.csv", all_summary_rows)
    _write_json(output_dir / "relative_changes.json", all_relative_rows)
    _write_csv(output_dir / "relative_changes.csv", all_relative_rows)
    _write_json(output_dir / "paper_table_rows.json", all_paper_rows)
    _write_csv(output_dir / "paper_table_rows.csv", all_paper_rows)
    _write_json(output_dir / "algorithm_summary.json", aggregate_by_algorithm(all_summary_rows))
    _write_json(
        output_dir / "manifest.json",
        {
            "config": str(config_path),
            "phase": config["project"]["phase"],
            "output_dir": str(output_dir),
            "calibration_output_dir": str(
                REPO_ROOT / config["data"]["calibration_output_dir"]
            ),
            "feed_algorithms": simulation_config["feed_algorithms"],
            "n_sims": simulation_config["n_sims"],
            "assumptions": [
                "Phase 5 is paper-aligned and uses the three case studies, not all ACL2017 cascades.",
                "Each case reuses its Phase 4 best chronological calibrated probabilities across all feed objectives.",
                "Relative changes are computed against the chronological feed baseline for the same case.",
                "FakeNewsNet is audited for tweet-ID volume only and is not used as a cascade-validation target.",
                "Phase 5 is a calibrated counterfactual baseline; Phase 6 repairs network and belief-fidelity gaps.",
            ],
            "fakenewsnet_summary_count": len(fakenewsnet_summary),
        },
    )
    print(f"Wrote Phase 5 counterfactual outputs to {output_dir.relative_to(REPO_ROOT)}")
    return 0


def _config_path() -> Path:
    if len(sys.argv) == 3 and sys.argv[1] == "--config":
        return REPO_ROOT / sys.argv[2]
    if len(sys.argv) == 1:
        return REPO_ROOT / "configs/phase5_case_study_counterfactuals.json"
    raise SystemExit(
        "Usage: python3 scripts/run_phase5_counterfactuals.py "
        "[--config configs/phase5_case_study_counterfactuals.json]"
    )


def _seed_for(base_seed: int, case_index: int, algorithm_index: int, run_index: int) -> int:
    return base_seed + (case_index * 1000) + (algorithm_index * 100) + run_index


def _load_calibration_rows(calibration_output_dir: Path) -> list[dict[str, Any]]:
    path = calibration_output_dir / "best_calibration_summary.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Missing Phase 4 calibration summary: {path}. "
            "Run scripts/run_phase4_calibration.py first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _calibration_for_case(
    calibration_rows: list[dict[str, Any]],
    case_name: str,
) -> dict[str, Any]:
    for row in calibration_rows:
        if row["case_name"] == case_name:
            return row
    raise KeyError(f"Missing calibration row for case: {case_name}")


def _run_fakenewsnet_audit(
    config: dict[str, Any],
    output_dir: Path,
) -> list[dict[str, object]]:
    audit_config = config.get("fakenewsnet_audit", {})
    if not audit_config.get("enabled", False):
        return []
    root = REPO_ROOT / config["data"]["fakenewsnet_root"]
    articles = []
    for selected in audit_config["files"]:
        articles.extend(
            parse_fakenewsnet_csv(
                root / selected["path"],
                selected["source"],
                selected["label"],
            )
        )
    summaries = summarize_articles(articles)
    _write_json(output_dir / "fakenewsnet_parameter_audit.json", summaries)
    _write_csv(output_dir / "fakenewsnet_parameter_audit.csv", summaries)
    return summaries


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
