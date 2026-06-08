# Project Brief

Use this file to give future Codex sessions high-signal project context.

## Project Identity

- Project name: Social Feed ABM Replication
- Research area: agent-based modeling, social media simulation, social network
  analysis, misinformation diffusion, and recommender/newsfeed curation.
- Primary goal: independently reproduce and extend the core simulation logic of
  Gausen, Luk, and Guo's study on algorithmic newsfeed curation, measuring how
  chronological, belief-based, popularity-based, and random feed objectives
  affect information spread, belief purity, and validation fit.
- Current stage: Phase 3 model-fidelity upgrade with simulated event/state
  traces, scalar belief updates, source-post lineage, and popularity feedback.
- Main stakeholders/users: the project owner, future research collaborators,
  reviewers of a public GitHub replication package, and readers of a future
  paper or technical report.

## Core Questions

- Paper-derived replication design criteria:
  - Does the replication model false and non-false story diffusion in a way
    comparable to the original study's misinformation setup?
  - Does the replication represent a Twitter-like social media network with
    agents and follower/followee structure?
  - Can the replication use real social media cascade data for calibration and
    validation when those data are legally obtainable?
  - Does the replication model agent beliefs and belief updating well enough to
    compute belief purity?
  - Does the replication implement newsfeed curation algorithms, especially the
    chronological, belief-based, popularity-based, and random objectives?
- Can a Python ABM reproduce the qualitative effects reported by the original
  study for four social-feed curation objectives?
- Can the chronological baseline be calibrated and validated against available
  cascade data using information spread, RMSE, and NRMSE?
- How do feed curation objectives change information spread, belief purity, and
  the possible formation of echo chambers?
- A useful result is a reproducible experiment package that can generate
  comparable tables, plots, and run records for synthetic and, if available,
  original-data replication cases.
- Assumptions to test include Barabasi-Albert network structure, scalar belief
  representation, initial infected proportion, average viewed posts, number of
  simulations, calibrated probability values, and the chronological-feed
  baseline assumption.

## System Shape

- Source code location: `src/`
- Scripts location: `scripts/`
- Configs location: `configs/`
- Tests location: `tests/`
- Data location: `data/`
- Outputs location: `outputs/`
- Notebooks location: `notebooks/`
- Experiment notes location: `experiments/`

## Known Commands

- Setup: no project-specific install command yet; do not add dependencies
  without approval.
- Test: `python3 scripts/check_repo.py` for template structure.
- Lint/typecheck: not defined yet.
- Run experiment: `python3 scripts/prepare_acl2017_cases.py --config
  configs/phase1_acl2017_cases.json`, then `python3 scripts/run_phase1_mvp.py
  --config configs/phase1_acl2017_cases.json`, then `python3
  scripts/prepare_observed_cascades.py --config
  configs/phase2_observed_cascades.json`, then `python3
  scripts/run_phase3_model_fidelity.py --config
  configs/phase3_model_fidelity.json`.
- Run backend/dashboard/frontend: not applicable in the current preliminary
  phase.

## Important Constraints

- Dependencies to avoid: avoid adding any dependency until the first
  implementation task justifies it and the user approves. Expected future stack
  is Python with NetworkX, NumPy/Pandas, SciPy or scikit-learn for calibration,
  and Matplotlib/Seaborn for plots.
- Data/privacy constraints: use synthetic data first. Do not commit restricted
  raw Twitter-derived cascade data. If using the Ma et al. Twitter rumor dataset,
  document access, license/usage constraints, acquisition date, schema, and
  preprocessing lineage.
- Performance constraints: start with the paper baseline of 1,000 agents and
  small simulation counts; scale only after the smoke workflow is reproducible.
- Reproducibility requirements: record seeds, configs, calibrated
  probabilities, command lines, data paths, code version, output folder, metrics,
  and assumptions for every important run.

## Current Priorities

- Compare Phase 3 chronological traces against Phase 2 observed `Phi` outputs
  before implementing calibration.
- Replace template placeholder tests once Phase 1 coverage is stable.
- Decide dependency management before adding plotting, pandas, NetworkX, or
  calibration search.
- Keep implementation aligned with the five paper-derived replication design
  criteria.
