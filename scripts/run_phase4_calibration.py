#!/usr/bin/env python3
"""Run Phase 4 chronological calibration and validation.

This command compares chronological Phase 3-style simulations against the
observed Phase 2 `Phi` targets. It performs a small deterministic grid search
around the paper-reported calibrated probabilities and reports RMSE/NRMSE.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from social_feed_abm.calibration import (  # noqa: E402
    best_candidate,
    calibration_scores,
    mean_series,
    probability_grid,
)
from social_feed_abm.config import load_config  # noqa: E402
from social_feed_abm.simulation import SimulationParams, run_simulation  # noqa: E402


def main() -> int:
    config_path = _config_path()
    config = load_config(config_path)
    output_dir = REPO_ROOT / config["data"]["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    simulation_config = config["simulation"]
    fidelity_config = config["model_fidelity"]
    calibration_config = config["calibration"]
    all_candidate_rows: list[dict[str, object]] = []
    best_rows: list[dict[str, object]] = []

    for case_index, selected in enumerate(config["selected_cases"]):
        case_output_dir = output_dir / selected["case_name"]
        case_output_dir.mkdir(parents=True, exist_ok=True)

        observed_phi = _load_observed_phi(
            REPO_ROOT / config["data"]["observed_output_dir"],
            selected["case_name"],
        )
        if len(observed_phi) != selected["timesteps"]:
            raise ValueError(
                f"{selected['case_name']} expected {selected['timesteps']} observed "
                f"timesteps but found {len(observed_phi)}"
            )

        candidates = probability_grid(
            selected["probabilities"],
            calibration_config["candidate_multipliers"],
        )
        case_candidate_rows: list[dict[str, object]] = []
        case_run_records: list[dict[str, object]] = []

        for candidate_index, probabilities in enumerate(candidates):
            run_series: list[list[float]] = []
            run_records: list[dict[str, object]] = []
            for run_index in range(simulation_config["n_sims"]):
                seed = _seed_for(config["seed"], case_index, candidate_index, run_index)
                params = SimulationParams(
                    n_agents=simulation_config["n_agents"],
                    avg_followees=simulation_config["avg_followees"],
                    avg_viewed_posts=simulation_config["avg_viewed_posts"],
                    timesteps=selected["timesteps"],
                    initial_infected=selected["initial_infected"],
                    p_online=probabilities["p_online"],
                    p_reshare=probabilities["p_reshare"],
                    p_reject=probabilities["p_reject"],
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
                result = run_simulation(params, simulation_config["feed_algorithm"])
                run_series.append([float(value) for value in result["phi_by_timestep"]])
                run_records.append(
                    {
                        "candidate_index": candidate_index,
                        "run_index": run_index,
                        "seed": seed,
                        "phi_avg": result["phi_avg"],
                        "phi_max": result["phi_max"],
                        "belief_purity_avg": result["belief_purity_avg"],
                        "total_story_tweets": result["total_story_tweets"],
                    }
                )

            predicted_phi = mean_series(run_series)
            scores = calibration_scores(observed_phi, predicted_phi)
            row = {
                "case_name": selected["case_name"],
                "story_id": selected["story_id"],
                "label": selected["expected_label"],
                "role": selected["role"],
                "feed_algorithm": simulation_config["feed_algorithm"],
                "candidate_index": candidate_index,
                "n_sims": simulation_config["n_sims"],
                "p_online": probabilities["p_online"],
                "p_reshare": probabilities["p_reshare"],
                "p_reject": probabilities["p_reject"],
                "rmse": scores["rmse"],
                "nrmse": scores["nrmse"],
                "observed_phi_avg": sum(observed_phi) / len(observed_phi),
                "predicted_phi_avg": sum(predicted_phi) / len(predicted_phi),
                "observed_phi_max": max(observed_phi),
                "predicted_phi_max": max(predicted_phi),
            }
            case_candidate_rows.append(row)
            case_run_records.extend(run_records)
            _write_json(
                case_output_dir / f"candidate_{candidate_index:03d}_phi.json",
                _series_rows(observed_phi, predicted_phi),
            )

        best = best_candidate(case_candidate_rows)
        best_rows.append(best)
        all_candidate_rows.extend(case_candidate_rows)
        _write_json(case_output_dir / "candidate_scores.json", case_candidate_rows)
        _write_csv(case_output_dir / "candidate_scores.csv", case_candidate_rows)
        _write_json(case_output_dir / "run_records.json", case_run_records)
        _write_json(case_output_dir / "best_candidate.json", best)

    _write_json(output_dir / "candidate_scores.json", all_candidate_rows)
    _write_csv(output_dir / "candidate_scores.csv", all_candidate_rows)
    _write_json(output_dir / "best_calibration_summary.json", best_rows)
    _write_csv(output_dir / "best_calibration_summary.csv", best_rows)
    _write_json(
        output_dir / "manifest.json",
        {
            "config": str(config_path),
            "phase": config["project"]["phase"],
            "output_dir": str(output_dir),
            "observed_output_dir": str(
                REPO_ROOT / config["data"]["observed_output_dir"]
            ),
            "feed_algorithm": simulation_config["feed_algorithm"],
            "search_strategy": calibration_config["search_strategy"],
            "selection_metric": calibration_config["selection_metric"],
            "tie_breaker": calibration_config["tie_breaker"],
            "candidate_count_per_case": len(
                probability_grid(
                    config["selected_cases"][0]["probabilities"],
                    calibration_config["candidate_multipliers"],
                )
            ),
            "assumptions": [
                "Phase 4 uses Phase 2 observed Phi targets as validation curves.",
                "Only the chronological feed is calibrated in this pass.",
                "The search is a small deterministic multiplier grid around paper-reported probabilities.",
                "The synthetic network is still not calibrated to real follower data.",
                "Best candidates are selected by NRMSE with RMSE as a tie breaker.",
            ],
        },
    )
    print(
        f"Wrote Phase 4 calibration outputs for {len(best_rows)} cases to "
        f"{output_dir.relative_to(REPO_ROOT)}"
    )
    return 0


def _config_path() -> Path:
    if len(sys.argv) == 3 and sys.argv[1] == "--config":
        return REPO_ROOT / sys.argv[2]
    if len(sys.argv) == 1:
        return REPO_ROOT / "configs/phase4_calibration_validation.json"
    raise SystemExit(
        "Usage: python3 scripts/run_phase4_calibration.py "
        "[--config configs/phase4_calibration_validation.json]"
    )


def _seed_for(base_seed: int, case_index: int, candidate_index: int, run_index: int) -> int:
    return base_seed + (case_index * 10000) + (candidate_index * 100) + run_index


def _load_observed_phi(observed_output_dir: Path, case_name: str) -> list[float]:
    path = observed_output_dir / case_name / "phi_by_timestep.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Missing observed Phi target: {path}. Run "
            "scripts/prepare_observed_cascades.py first."
        )
    rows = json.loads(path.read_text(encoding="utf-8"))
    return [float(row["phi"]) for row in rows]


def _series_rows(
    observed_phi: list[float],
    predicted_phi: list[float],
) -> list[dict[str, object]]:
    return [
        {
            "timestep": timestep,
            "observed_phi": observed,
            "predicted_phi": predicted,
            "residual": predicted - observed,
        }
        for timestep, (observed, predicted) in enumerate(
            zip(observed_phi, predicted_phi)
        )
    ]


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
