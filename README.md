# Social Feed ABM Replication

Independent replication and extension workspace for an agent-based model of
algorithmic newsfeed curation on social media.

This project aims to reproduce the core findings of Gausen, Luk, and Guo's
study on how feed-ranking objectives affect information spread, misinformation
diffusion, and belief purity in a Twitter-like social network. The first target
is a synthetic, reproducible Python ABM. Full calibration and validation against
historical cascade data will be added only after the baseline model and data
workflow are documented.

## Original Study

This repository is an independent replication and is not the original authors'
code.

Reference:

Gausen, A., Luk, W., and Guo, C. (2022). "Using Agent-Based Modelling to
Evaluate the Impact of Algorithmic Curation on Social Media." Journal of Data
and Information Quality, 15(1), Article 2.
https://doi.org/10.1145/3546915

## Research Questions

The original paper uses five related-work questions to identify the model gap it
addresses. In this replication, those become design criteria for deciding
whether the implementation is faithful enough:

1. Does the replication model false and non-false story diffusion in a way
   comparable to the original study's misinformation setup?
2. Does the replication represent a Twitter-like social media network with
   agents and follower/followee structure?
3. Can the replication use real social media cascade data for calibration and
   validation when those data are legally obtainable?
4. Does the replication model agent beliefs and belief updating well enough to
   compute belief purity?
5. Does the replication implement newsfeed curation algorithms, especially the
   chronological, belief-based, popularity-based, and random objectives?

The empirical replication questions for this repository are:

1. Can a Python ABM reproduce the qualitative effects reported for
   chronological, belief-based, popularity-based, and random feed curation?
2. How do those curation objectives affect information spread and belief purity?
3. Can a chronological-feed baseline be calibrated and validated against
   available cascade data using RMSE and NRMSE?
4. Which assumptions remain stable under sensitivity checks and future
   NLP/SNA/recommender-system extensions?

## Model Scope

The replication baseline will model:

- A Twitter-like social network with a Barabasi-Albert topology.
- Agents with story states: `susceptible`, `believe`, `deny`, and `cured`.
- Four feed objectives: chronological, belief-based, popularity-based, and
  random.
- Information spread measured as the proportion of story-related tweets per
  timestep, `Phi`.
- Belief purity as a proxy for feed homogeneity and potential echo chamber
  formation.
- Chronological-baseline validation with RMSE and NRMSE when suitable cascade
  data is available.

Extensions such as semantic belief vectors, empirical networks, diversity-aware
ranking, and LLM-agent behavior are planned only after the faithful synthetic
replication path is working.

## Current Status

This repository has Phase 1, Phase 2, and Phase 3 replication scaffolds. Phase
1 includes local-only ACL2017 case preprocessing and a dependency-light
synthetic ABM runner. Phase 2 reconstructs observed cascade event tables and
`Phi` time series from the ACL2017 propagation trees for the paper-relevant
Twitter15 cases. Phase 3 upgrades the simulated mechanism with explicit
per-timestep event traces, state counts, scalar belief updates, source-post
lineage, and popularity feedback. The project does not yet include calibration
search, plotted figures, or validated replication results.

Current validation command:

```bash
python3 scripts/check_repo.py
python3 -m unittest discover
python3 scripts/prepare_acl2017_cases.py --config configs/phase1_acl2017_cases.json
python3 scripts/run_phase1_mvp.py --config configs/phase1_acl2017_cases.json
python3 scripts/prepare_observed_cascades.py --config configs/phase2_observed_cascades.json
python3 scripts/run_phase3_model_fidelity.py --config configs/phase3_model_fidelity.json
```

## Planned Workflow

1. Curate project docs, data policy, and reproducibility conventions.
2. Implement a synthetic ABM smoke workflow.
3. Reconstruct observed cascade event tables and `Phi` time series.
4. Upgrade the ABM toward paper-faithful agent, feed, belief, and popularity
   mechanics.
5. Fit and validate the chronological baseline with RMSE/NRMSE.
6. Reproduce the four feed curation comparisons.
7. Run sensitivity checks and extensions.

## Data

Raw Twitter-derived cascade data is not redistributed in this repository. Data
work will start with synthetic fixtures and schema documentation. If historical
cascade data such as the Ma et al. Twitter rumor dataset is used, it must remain
local unless redistribution rights are explicit and documented.

See `data/README.md` for the project data policy, planned data layout, expected
schemas, and lineage requirements.

## Repository Structure

```text
.
├── AGENTS.md
├── README.md
├── .agent/
├── configs/
├── data/
├── docs/
├── experiments/
├── notebooks/
├── outputs/
├── scripts/
├── src/
└── tests/
```

Key folders:

- `.agent/`: durable project context, workflow notes, and task log for coding
  agents.
- `configs/`: future simulation, calibration, and sensitivity parameters.
- `data/`: local data documentation and non-restricted fixtures.
- `experiments/`: experiment plans, run notes, and comparisons.
- `outputs/`: generated logs, metrics, plots, and tables.
- `scripts/`: reproducible command-line entry points.
- `src/`: reusable implementation code after the setup phase.
- `tests/`: automated tests for reusable logic and workflows.

## Reproducibility Expectations

Important runs should record:

- Command.
- Config path and saved config contents.
- Seed.
- Data input and version.
- Code version.
- Output folder.
- Metrics.
- Assumptions and deviations from the original study.

Do not add dependencies or upload raw restricted data without explicit approval.

## License And Citation

Licensing and software citation metadata are not finalized yet. When this
repository is used in research, cite both this software repository and the
original Gausen, Luk, and Guo study.
