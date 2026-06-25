# Task Log

Use this file for durable continuity across coding-agent sessions. Keep entries short.

## Active Context

- Current objective: realign Phase 6 dashboard tracking with paper curation
  intervention targets and clearer synthetic-network provenance visualization.
- Current branch/status: initial template customization; many template files are
  newly added or unstaged.
- Important open question: dependency management and final package layout are
  not decided yet.
- Latest validation command: `python3 scripts/check_repo.py`, `python3 -m
  unittest discover`, `python3 scripts/prepare_observed_cascades.py --config
  configs/phase2_observed_cascades.json`, `python3
  scripts/run_phase6_replication_fidelity.py --config
  configs/phase6_replication_fidelity_repair.json`, `npm run check` in
  `outputs/replication-dashboard`, and browser render verification passed.

## Decisions

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-06-05 | Use `Social Feed ABM Replication` as the project identity. | Matches the repository name and public GitHub framing. |
| 2026-06-05 | Start with a synthetic ABM replication before original cascade validation. | Avoids blocking on restricted data access and creates a reproducible MVP. |
| 2026-06-05 | Do not commit restricted raw Twitter-derived cascade data. | Protects data rights, privacy, and reproducibility expectations. |
| 2026-06-05 | Expected stack is Python ABM with NetworkX, NumPy/Pandas, SciPy or scikit-learn later, and Matplotlib/Seaborn. | Aligns with the replication plan while deferring dependency installation. |
| 2026-06-05 | Treat the paper's five related-work questions as replication design criteria. | They define required model capabilities, while the repo RQs remain outcome-oriented. |
| 2026-06-05 | Phase 1 uses ACL2017 Twitter15 cases and minimal dependencies. | The local dataset contains the paper's named cases, and the current environment lacks pandas, NetworkX, PyYAML, and matplotlib. |
| 2026-06-05 | Phase 2 reconstructs observed cascades with hourly bins and source events excluded from `Phi`. | Creates validation targets while preserving source events for lineage. |
| 2026-06-08 | Phase 3 keeps the network synthetic but records richer simulated mechanism traces. | This improves paper-facing model fidelity before adding calibration search or dependencies. |
| 2026-06-08 | Phase 4 uses a small deterministic grid around paper probabilities. | Keeps chronological calibration executable without adding SciPy/sklearn yet. |
| 2026-06-08 | Phase 5 remains case-study based rather than full-dataset based. | The paper calibrates/validates case-study ABMs; full-dataset average propagation is future robustness work. |
| 2026-06-08 | Phase 6 separates synthetic agent-network snapshots from observed cascade snapshots. | ACL2017 propagation trees are not follower-network edges and should not be visualized as the ABM social network. |
| 2026-06-08 | Keep unknown paper table targets blocked rather than guessed. | Target-verdict tracking should be auditable and avoid fabricated replication precision. |
| 2026-06-08 | Track curation interventions as actual-vs-paper paired effects. | The paper's central claim is about intervention effects of feed objectives relative to chronological curation. |

## Recent Tasks

| Date | Task | Files touched | Validation | Notes |
| --- | --- | --- | --- | --- |
| 2026-06-05 | Added missing template continuity files. | `.agent/`, `.env.example`, `.gitignore` | `python3 scripts/check_repo.py` passed. | User copied these from the template repository. |
| 2026-06-05 | Planned preliminary documentation curation. | AGENTS and `.agent` docs | Planning only. | No code implementation requested for preliminaries. |
| 2026-06-05 | Rewrote public project overview and added data documentation. | `README.md`, `data/README.md` | `python3 scripts/check_repo.py` passed. | Documentation-only; no ABM code or dependencies added. |
| 2026-06-05 | Added paper-derived replication design criteria to docs. | `README.md`, `.agent/PROJECT_BRIEF.md`, `.agent/RESEARCH_PROJECT_GUIDE.md`, `.agent/TASK_LOG.md` | `python3 scripts/check_repo.py` passed. | Contextualizes the original paper's five questions for replication. |
| 2026-06-05 | Implemented Phase 1 data-assisted MVP scaffold. | `src/social_feed_abm/`, scripts, `configs/phase1_acl2017_cases.json`, tests, docs | `python3 scripts/check_repo.py`; `python3 -m unittest discover`; Phase 1 prep and run scripts passed. | Uses ACL2017 summaries and synthetic counterfactual feed runs; no new dependencies. |
| 2026-06-05 | Implemented Phase 2 observed cascade reconstruction. | `src/social_feed_abm/observed.py`, `scripts/prepare_observed_cascades.py`, `configs/phase2_observed_cascades.json`, tests, docs | `python3 scripts/check_repo.py`; `python3 -m unittest discover`; Phase 2 observed-cascade script passed. | Produces event tables, padded `Phi` series, combined summary, and manifest. |
| 2026-06-08 | Implemented Phase 3 model-fidelity upgrade. | `src/social_feed_abm/simulation.py`, `src/social_feed_abm/feed_algorithms.py`, `scripts/run_phase3_model_fidelity.py`, `configs/phase3_model_fidelity.json`, tests, docs, dashboard data | `python3 scripts/check_repo.py`; `python3 -m unittest discover`; Phase 3 model-fidelity script passed. | Adds event/state traces, scalar belief updates, source-post lineage, and popularity feedback. |
| 2026-06-08 | Implemented Phase 4 chronological calibration/validation. | `src/social_feed_abm/calibration.py`, `scripts/run_phase4_calibration.py`, `configs/phase4_calibration_validation.json`, tests, docs, dashboard data | `python3 scripts/check_repo.py`; `python3 -m unittest discover`; Phase 4 calibration script passed. | Writes candidate scores and best RMSE/NRMSE fits for the three selected cases. |
| 2026-06-08 | Implemented Phase 5 case-study counterfactuals and result visualizations. | `src/social_feed_abm/counterfactual.py`, `src/social_feed_abm/fakenewsnet.py`, `scripts/run_phase5_counterfactuals.py`, `configs/phase5_case_study_counterfactuals.json`, tests, docs, dashboard files | `python3 scripts/check_repo.py`; `python3 -m unittest discover`; Phase 5 script passed. | Produces paper-style relative-change rows, FakeNewsNet parameter audit, and dashboard charts. |
| 2026-06-08 | Implemented Phase 6 replication-fidelity repair and provenance visuals. | `src/social_feed_abm/simulation.py`, `src/social_feed_abm/observed.py`, `src/social_feed_abm/counterfactual.py`, `scripts/run_phase6_replication_fidelity.py`, `configs/phase6_replication_fidelity_repair.json`, tests, docs, dashboard files | `python3 scripts/check_repo.py`; `python3 -m unittest discover`; Phase 2 prep; Phase 6 script; dashboard data check; browser render verification passed. | Adds BA network repair, Bayesian-style belief updates, sampled `Nposts`, background posts, verified influence, target verdicts, and network/cascade SVG data. |
| 2026-06-08 | Added curation intervention and hub-network dashboard views. | `configs/phase6_replication_fidelity_repair.json`, `outputs/replication-dashboard/` | Phase 6 script; `python3 scripts/check_repo.py`; `python3 -m unittest discover`; `npm run check`; browser render verification passed. | Exact Table 4, 5, and B.2 targets now drive paired actual-vs-paper intervention bars; network view emphasizes hubs, rings, and degree distribution. |
| 2026-06-25 | Added concepts tab to the replication dashboard. | `outputs/replication-dashboard/` | `npm run check`; `node --check assets/app.js`; browser tab-switch smoke test; 390px overflow check passed. | Explains SNA, information diffusion, ABM, feed curation, belief purity, calibration, and how the paper's questions map to the replication workflow. |
| 2026-06-25 | Added animated concept-card visualizations. | `outputs/replication-dashboard/` | `npm run check`; `node --check assets/app.js`; `python3 scripts/check_repo.py`; browser animation smoke test; 390px overflow check passed. | Each core concept card now has a dependency-free animated SVG teaching aid with reduced-motion fallbacks. |
| 2026-06-25 | Added research proposal dashboard tab. | `outputs/replication-dashboard/` | `npm run check`; `node --check assets/app.js`; `python3 scripts/check_repo.py`; browser tab smoke test; 390px overflow check passed. | New tab explains the exposure-aware semantic network simulation proposal with framework layers, RQs, work packages, prototype scope, and contribution map. |
| 2026-06-25 | Deployed replication dashboard to Vercel production. | `outputs/replication-dashboard/README.md`, `outputs/replication-dashboard/.gitignore` | `npm run check`; Vercel production deploy; live `curl` returned 200. | Production alias: `https://replication-dashboard.vercel.app`; Vercel project: `replication-dashboard`. |

## Follow-Ups

- Decide dependency management before adding packages.
- Generate paper-style static figures/tables from Phase 6 outputs.
- Repair the simulation mechanism so popularity and belief curation reproduce
  the paper's intervention directions and approximate magnitudes.
- Add full-dataset robustness phase after the faithful case-study path is accepted.
