#!/usr/bin/env python3
"""Run Phase 6 replication-fidelity repair simulations and snapshots."""

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
    paper_table_rows,
    relative_changes_for_case,
    replication_verdict_rows,
)
from social_feed_abm.observed import ObservedCascadeEvent, cascade_snapshot  # noqa: E402
from social_feed_abm.simulation import SimulationParams, run_simulation, summarize_runs  # noqa: E402


def main() -> int:
    config_path = _config_path()
    config = load_config(config_path)
    output_dir = REPO_ROOT / config["data"]["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    all_summary_rows: list[dict[str, object]] = []
    all_relative_rows: list[dict[str, object]] = []
    all_paper_rows: list[dict[str, object]] = []
    all_actual_target_rows: list[dict[str, object]] = []
    network_snapshots: dict[str, object] = {}
    cascade_snapshots: dict[str, object] = {}

    for case_index, selected in enumerate(config["selected_cases"]):
        case_output_dir = output_dir / selected["case_name"]
        case_output_dir.mkdir(parents=True, exist_ok=True)
        case_summary_rows: list[dict[str, object]] = []
        probabilities = selected["paper_probabilities"]

        for algorithm_index, algorithm in enumerate(config["simulation"]["feed_algorithms"]):
            runs = []
            for run_index in range(config["simulation"]["n_sims"]):
                seed = _seed_for(config["seed"], case_index, algorithm_index, run_index)
                params = _simulation_params(config, selected, probabilities, seed)
                params = _with_snapshot_enabled(
                    params,
                    enabled=(algorithm == "chronological" and run_index == 0),
                    fidelity_config=config["model_fidelity"],
                )
                result = run_simulation(params, algorithm)
                if "network_snapshot" in result:
                    network_snapshots[selected["case_name"]] = result["network_snapshot"]
                    _write_json(
                        case_output_dir / "network_snapshot.json",
                        result["network_snapshot"],
                    )
                result.update(
                    {
                        "run_index": run_index,
                        "seed": seed,
                        "case_name": selected["case_name"],
                        "story_id": selected["story_id"],
                        "label": selected["expected_label"],
                        "phase": config["project"]["phase"],
                        "probability_source": "paper_reported",
                    }
                )
                runs.append(result)

            aggregate = {
                "case_name": selected["case_name"],
                "story_id": selected["story_id"],
                "label": selected["expected_label"],
                "role": selected["role"],
                "feed_algorithm": algorithm,
                "n_sims": config["simulation"]["n_sims"],
                "probability_source": "paper_reported",
                "p_online": probabilities["p_online"],
                "p_reshare": probabilities["p_reshare"],
                "p_reject": probabilities["p_reject"],
                **summarize_runs(runs),
            }
            case_summary_rows.append(aggregate)
            _write_json(case_output_dir / f"{algorithm}_runs.json", runs)

        relative_rows = relative_changes_for_case(case_summary_rows)
        paper_rows = paper_table_rows(relative_rows)
        actual_rows = _actual_target_rows(case_summary_rows, relative_rows)
        all_summary_rows.extend(case_summary_rows)
        all_relative_rows.extend(relative_rows)
        all_paper_rows.extend(paper_rows)
        all_actual_target_rows.extend(actual_rows)
        _write_json(case_output_dir / "metrics_summary.json", case_summary_rows)
        _write_csv(case_output_dir / "metrics_summary.csv", case_summary_rows)
        _write_json(case_output_dir / "relative_changes.json", relative_rows)
        _write_csv(case_output_dir / "relative_changes.csv", relative_rows)
        _write_json(case_output_dir / "paper_table_rows.json", paper_rows)
        _write_csv(case_output_dir / "paper_table_rows.csv", paper_rows)
        _write_json(case_output_dir / "actual_target_rows.json", actual_rows)

        observed_events = _load_observed_events(
            REPO_ROOT / config["data"]["observed_output_dir"],
            selected["case_name"],
        )
        snapshot = cascade_snapshot(
            observed_events,
            max_nodes=config["model_fidelity"]["cascade_snapshot_max_nodes"],
        )
        cascade_snapshots[selected["case_name"]] = snapshot
        _write_json(case_output_dir / "cascade_snapshot.json", snapshot)

    verdict_rows = replication_verdict_rows(
        all_actual_target_rows,
        config["paper_targets"],
        match_tolerance=config["verdict"]["match_tolerance"],
        directional_tolerance=config["verdict"]["directional_tolerance"],
    )
    _write_json(output_dir / "metrics_summary.json", all_summary_rows)
    _write_csv(output_dir / "metrics_summary.csv", all_summary_rows)
    _write_json(output_dir / "relative_changes.json", all_relative_rows)
    _write_csv(output_dir / "relative_changes.csv", all_relative_rows)
    _write_json(output_dir / "paper_table_rows.json", all_paper_rows)
    _write_csv(output_dir / "paper_table_rows.csv", all_paper_rows)
    _write_json(output_dir / "actual_target_rows.json", all_actual_target_rows)
    _write_json(output_dir / "replication_verdicts.json", verdict_rows)
    _write_csv(output_dir / "replication_verdicts.csv", verdict_rows)
    _write_json(output_dir / "network_snapshots.json", network_snapshots)
    _write_json(output_dir / "cascade_snapshots.json", cascade_snapshots)
    _write_json(
        output_dir / "manifest.json",
        {
            "config": str(config_path),
            "phase": config["project"]["phase"],
            "output_dir": str(output_dir),
            "simulation": config["simulation"],
            "model_fidelity": config["model_fidelity"],
            "assumptions": [
                "Phase 6 uses paper-reported calibrated probabilities where available.",
                "The synthetic agent network is a Barabasi-Albert directed projection, not an observed follower graph.",
                "The observed cascade visualization uses ACL2017 propagation trees, not follower-network edges.",
                "Paper target table values that have not been transcribed are marked blocked in the verdict matrix.",
                "FakeNewsNet remains parameter context only because local files do not expose verified-user activity.",
            ],
        },
    )
    _update_dashboard_data(
        REPO_ROOT / config["data"]["dashboard_data_path"],
        config,
        all_summary_rows,
        all_relative_rows,
        verdict_rows,
        network_snapshots,
        cascade_snapshots,
    )
    print(f"Wrote Phase 6 fidelity outputs to {output_dir.relative_to(REPO_ROOT)}")
    return 0


def _config_path() -> Path:
    if len(sys.argv) == 3 and sys.argv[1] == "--config":
        return REPO_ROOT / sys.argv[2]
    if len(sys.argv) == 1:
        return REPO_ROOT / "configs/phase6_replication_fidelity_repair.json"
    raise SystemExit(
        "Usage: python3 scripts/run_phase6_replication_fidelity.py "
        "[--config configs/phase6_replication_fidelity_repair.json]"
    )


def _seed_for(base_seed: int, case_index: int, algorithm_index: int, run_index: int) -> int:
    return base_seed + (case_index * 1000) + (algorithm_index * 100) + run_index


def _simulation_params(
    config: dict[str, Any],
    selected: dict[str, Any],
    probabilities: dict[str, float],
    seed: int,
) -> SimulationParams:
    sim = config["simulation"]
    fidelity = config["model_fidelity"]
    return SimulationParams(
        n_agents=sim["n_agents"],
        avg_followees=sim["avg_followees"],
        avg_viewed_posts=sim["avg_viewed_posts"],
        avg_viewed_posts_std=sim["avg_viewed_posts_std"],
        timesteps=selected["timesteps"],
        initial_infected=selected["initial_infected"],
        p_online=probabilities["p_online"],
        p_reshare=probabilities["p_reshare"],
        p_reject=probabilities["p_reject"],
        seed=seed,
        belief_acceptance_distance=fidelity["belief_acceptance_distance"],
        belief_update_rate=fidelity["belief_update_rate"],
        belief_update_mode=fidelity["belief_update_mode"],
        recent_posts_per_followee=fidelity["recent_posts_per_followee"],
        verified_probability=fidelity["verified_probability"],
        verified_influence_multiplier=fidelity["verified_influence_multiplier"],
        popularity_feedback=fidelity["popularity_feedback"],
        network_model=fidelity["network_model"],
        probability_sampling=fidelity["probability_sampling"],
        probability_std_fraction=fidelity["probability_std_fraction"],
        background_posts_per_agent=fidelity["background_posts_per_agent"],
        background_post_probability=fidelity["background_post_probability"],
    )


def _with_snapshot_enabled(
    params: SimulationParams,
    enabled: bool,
    fidelity_config: dict[str, Any],
) -> SimulationParams:
    if not enabled:
        return params
    return SimulationParams(
        **{
            **params.__dict__,
            "include_network_snapshot": True,
            "network_snapshot_max_nodes": fidelity_config["network_snapshot_max_nodes"],
            "network_snapshot_max_edges": fidelity_config["network_snapshot_max_edges"],
        }
    )


def _load_observed_events(
    observed_output_dir: Path,
    case_name: str,
) -> list[ObservedCascadeEvent]:
    path = observed_output_dir / case_name / "events.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    return [
        ObservedCascadeEvent(
            story_id=row["story_id"],
            case_name=row["case_name"],
            label=row["label"],
            source_tweet_id=row["source_tweet_id"],
            parent_user_id=row["parent_user_id"],
            parent_tweet_id=row["parent_tweet_id"],
            user_id=row["user_id"],
            tweet_id=row["tweet_id"],
            delay_minutes=float(row["delay_minutes"]),
            timestep=int(row["timestep"]),
            event_type=row["event_type"],
        )
        for row in rows
    ]


def _actual_target_rows(
    summary_rows: list[dict[str, Any]],
    relative_rows: list[dict[str, Any]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in summary_rows:
        for metric in ("phi_avg_mean", "phi_max_mean", "belief_purity_avg_mean"):
            rows.append(
                {
                    "case_name": row["case_name"],
                    "feed_algorithm": row["feed_algorithm"],
                    "metric": metric,
                    "actual_value": row[metric],
                }
            )
        if row["feed_algorithm"] == "chronological":
            for metric in ("p_online", "p_reshare", "p_reject"):
                rows.append(
                    {
                        "case_name": row["case_name"],
                        "feed_algorithm": row["feed_algorithm"],
                        "metric": metric,
                        "actual_value": row[metric],
                    }
                )
    relative_metric_map = {
        "change_phi_avg": "phi_avg_mean_relative_change",
        "change_phi_max": "phi_max_mean_relative_change",
        "change_belief_purity": "belief_purity_avg_mean_relative_change",
    }
    for row in relative_rows:
        for metric, source_key in relative_metric_map.items():
            rows.append(
                {
                    "case_name": row["case_name"],
                    "feed_algorithm": row["feed_algorithm"],
                    "metric": metric,
                    "actual_value": row[source_key],
                }
            )
    return rows


def _update_dashboard_data(
    dashboard_path: Path,
    config: dict[str, Any],
    summary_rows: list[dict[str, object]],
    relative_rows: list[dict[str, object]],
    verdict_rows: list[dict[str, object]],
    network_snapshots: dict[str, object],
    cascade_snapshots: dict[str, object],
) -> None:
    data = json.loads(dashboard_path.read_text(encoding="utf-8"))
    data["project"]["status"] = "Phase 6 complete; table transcription still needed"
    data["phases"] = [
        {
            **phase,
            "status": "complete" if phase["name"].startswith("Phase 6:") else phase["status"],
            "description": (
                "Added paper-probability repair runs, Barabasi-Albert network snapshots, "
                "observed cascade snapshots, and target-verdict tracking."
                if phase["name"].startswith("Phase 6:")
                else phase["description"]
            ),
            "evidence": (
                "outputs/phase6_replication_fidelity_repair/replication_verdicts.json"
                if phase["name"].startswith("Phase 6:")
                else phase["evidence"]
            ),
        }
        for phase in data["phases"]
    ]
    data["phase6"] = {
        "summary_rows": summary_rows,
        "relative_rows": relative_rows,
        "verdict_rows": verdict_rows,
        "network_snapshots": network_snapshots,
        "cascade_snapshots": cascade_snapshots,
        "model_fidelity": config["model_fidelity"],
        "known_limitations": [
            "Exact paper table targets for Tables 3, 4, and 5 still need transcription.",
            "Observed follower-network edges are unavailable in the local ACL2017 files.",
            "Bayesian update is a paper-aligned approximation pending exact equation-level audit.",
        ],
    }
    for item in data["faithfulness"]:
        if item["name"] == "Social network ABM":
            item["assessment"] = (
                "Phase 6 uses a deterministic Barabasi-Albert directed projection "
                "with diagnostics and dashboard snapshots; it is still synthetic, "
                "not calibrated to observed follower edges."
            )
        if item["name"] == "Agent belief modeling":
            item["assessment"] = (
                "Phase 6 adds Bayesian-style belief updates, background posts, "
                "sampled feed sizes, and verified influence; exact equation-level "
                "paper parity remains an audit item."
            )
    _merge_phase6_cases(data, summary_rows, relative_rows, network_snapshots, cascade_snapshots)
    dashboard_path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _merge_phase6_cases(
    data: dict[str, Any],
    summary_rows: list[dict[str, object]],
    relative_rows: list[dict[str, object]],
    network_snapshots: dict[str, object],
    cascade_snapshots: dict[str, object],
) -> None:
    summary_by_case: dict[str, list[dict[str, object]]] = {}
    for row in summary_rows:
        summary_by_case.setdefault(str(row["case_name"]), []).append(row)
    relative_by_case: dict[str, list[dict[str, object]]] = {}
    for row in relative_rows:
        relative_by_case.setdefault(str(row["case_name"]), []).append(
            {
                "feed_algorithm": row["feed_algorithm"],
                "change_phi_avg": row["phi_avg_mean_relative_change"],
                "change_phi_max": row["phi_max_mean_relative_change"],
                "change_belief_purity": row[
                    "belief_purity_avg_mean_relative_change"
                ],
            }
        )
    for case in data["cases"]:
        case_name = case["case_name"]
        if case_name in summary_by_case:
            case["phase6_simulated_feeds"] = summary_by_case[case_name]
        if case_name in relative_by_case:
            case["phase6_feed_relative_changes"] = relative_by_case[case_name]
        if case_name in network_snapshots:
            case["network_snapshot"] = network_snapshots[case_name]
        if case_name in cascade_snapshots:
            case["cascade_snapshot"] = cascade_snapshots[case_name]


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
