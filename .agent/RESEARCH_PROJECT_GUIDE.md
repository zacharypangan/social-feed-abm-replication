# Research Project Guide

Use this guide to keep research code understandable, reusable, and paper/report-ready.

## Replication Target

This repository is an independent replication and extension workspace for
Gausen, Luk, and Guo's agent-based model of algorithmic newsfeed curation on
social media. The core replication compares four feed objectives:
chronological, belief-based, popularity-based, and random curation.

The first implementation target is a synthetic ABM that reproduces the study's
qualitative behavior before attempting full original-data calibration.

## Replication Design Criteria

The original paper's literature-review questions should be treated as
capability checks for this replication:

1. Misinformation modeling: model false and non-false story diffusion in a way
   comparable to the original study.
2. Social network ABM: represent a Twitter-like social media network with agents
   and follower/followee structure.
3. Empirical calibration and validation: support real social media cascade data
   for calibration and validation when legally obtainable.
4. Agent belief modeling: include agent beliefs and belief-updating behavior
   sufficient to compute belief purity.
5. Newsfeed curation modeling: implement chronological, belief-based,
   popularity-based, and random feed objectives.

These are not replacements for the repository's empirical research questions;
they define what the model must contain before results should be interpreted as
a faithful replication.

## Model Summary

- Agents represent Twitter-like users on a Barabasi-Albert social network.
- Baseline agent states are `susceptible`, `believe`, `deny`, and `cured`.
- Agents may go online, post, view a curated feed, reshare, update belief, or
  reject a previous belief according to configured probabilities.
- Candidate feed items come from neighboring/followed users; the feed objective
  determines which posts are viewed.
- Faithful replication should be kept separate from later extensions such as
  semantic belief vectors, empirical networks, LLM agents, or diversity-aware
  recommender objectives.

## Core Metrics

- Information spread `Phi`: proportion of story-related tweets per timestep.
- Average and maximum `Phi` across runs and timesteps.
- Belief purity: similarity between an agent's belief and the beliefs/content
  represented in the viewed feed.
- RMSE and NRMSE for chronological-baseline validation against observed cascade
  data when available.

## Observed Cascade Reconstruction

Phase 2 reconstructs observed validation targets from ACL2017 propagation trees.
Each tree edge becomes an event row. The `ROOT -> source` edge is preserved as a
`source` event for lineage but excluded from observed `Phi` by default.

- Default time bin: hourly, using `floor(delay_minutes / 60)`.
- Default `Phi` denominator: `n_agents=1000`, matching the paper's baseline ABM
  population as an approximation.
- False cases are padded to 80 timesteps; the non-rumor case is padded to 40
  timesteps.
- Generated observed outputs live under `outputs/phase2_observed_cascades/` and
  should remain ignored by Git.

## Phase 3 Model-Fidelity Upgrade

Phase 3 keeps the dependency-light synthetic network but makes the simulated
mechanism more faithful and inspectable:

- Agents retain scalar beliefs and explicit states: `susceptible`, `believe`,
  `deny`, and `cured`.
- Viewed feeds can update beliefs toward the viewed-post belief mean.
- Susceptible agents can move to `believe` or `deny` based on configured belief
  acceptance distance.
- Reshares preserve source-post lineage and can increment source retweet counts
  for popularity-feedback ranking.
- Each run records per-timestep event counts, state counts, `Phi`, belief
  purity, and network summary metadata.

Phase 3 is still not calibrated against real follower networks or cascade
curves. Treat it as the model-fidelity baseline that Phase 4 will fit and
validate against Phase 2 observed targets.

## Phase 4 Chronological Calibration

Phase 4 calibrates the chronological-feed baseline against Phase 2 observed
`Phi` targets:

- Inputs: Phase 2 per-case `phi_by_timestep.json` files.
- Model: Phase 3-style synthetic ABM with the chronological feed objective.
- Search: small deterministic multiplier grid around the paper-reported
  `p_online`, `p_reshare`, and `p_reject` probabilities.
- Repetitions: currently 3 simulations per candidate for a lightweight
  executable baseline.
- Metrics: RMSE and NRMSE between observed `Phi` and averaged simulated `Phi`.
- Selection: lowest NRMSE, with RMSE as the tie breaker.

This phase establishes an executable validation workflow. It should not be
treated as final paper replication quality until the search space, simulation
count, and model assumptions are reviewed.

## Phase 5 Case-Study Counterfactuals

Phase 5 is aligned with the paper's case-study design:

- Inputs: Phase 4 best chronological calibration records for the Tupac,
  Justin Bieber, and Helric Fredou cases.
- Feed objectives: chronological, popularity-based, belief-based, and random.
- Repetitions: 5 simulations per feed condition, matching the original paper's
  reported simulation count.
- Metrics: `Phi_avg`, `Phi_max`, belief purity, and paper-style relative
  changes against the chronological baseline.
- FakeNewsNet: used only as a parameter-context audit from local tweet-ID
  metadata, not as a propagation-cascade validation target.

Full ACL2017/FakeNewsNet generalization is a later robustness phase, because
the paper states that additional case studies do not enrich case-dependent
calibration/validation and suggests average propagation patterns as future
work.

## Phase 6 Replication-Fidelity Repair

Phase 6 repairs known fidelity gaps before paper-style claims:

- Synthetic agent networks use a deterministic Barabasi-Albert directed
  projection with follower/followee diagnostics and public-safe snapshots.
- Viewed post counts can be sampled around the paper mean of 40 with std 20.
- Paper-reported calibrated probabilities are used directly for final
  case-study runs, while Phase 4 grid results remain diagnostic baselines.
- Belief updates use a Bayesian-style posterior approximation instead of only a
  linear mean shift.
- Background non-story posts and verified-user influence are explicit
  configurable mechanisms.
- Observed ACL2017 cascade snapshots are visualized separately from the
  synthetic social network.
- Paper target values that are not yet transcribed are represented as blocked
  verdicts rather than guessed numeric targets.

## Baseline Parameters To Preserve

- Agents: 1,000.
- Average followers/followees: 100.
- Average viewed posts: 40.
- Simulations in original paper: 5 per condition.
- False story: initial infected proportion 0.7; timesteps 80.
- Non-false story: initial infected proportion 0.5; timesteps 40.
- Calibrated false-story probabilities: `p_reshare=0.03669678`,
  `p_reject=0.01459229`, `p_online=0.10714111`.
- Calibrated non-false-story probabilities: `p_reshare=0.0770166`,
  `p_reject=0.06335449`, `p_online=0.06335449`.
- Additional Helric Fredou false-story probabilities used in Phase 6:
  `p_reshare=0.02094727`, `p_reject=0.00696533`,
  `p_online=0.10001950`.

Record any deviation from these values in configs, experiment notes, and result
summaries.

## Replication Risks

- Dataset access: the original calibration uses historical Twitter cascades from
  the Ma et al. rumor dataset. Raw restricted data should not be redistributed.
- Calibration ambiguity: the paper reports calibrated values but not every
  implementation detail, so assumptions must be explicit.
- Chronological baseline: the validation logic depends on pre-2016 Twitter
  chronological-feed behavior.
- Low simulation count: the original uses 5 simulations, which supports
  comparability but may be weak for robustness; later sensitivity runs should
  use more repetitions.
- Belief representation: scalar belief is useful for replication but limited;
  semantic or multidimensional belief representations belong in extension work.

## Code Structure

- `src/`: stable reusable logic, shared utilities, package code, API modules, UI modules.
- `scripts/`: runnable commands for data prep, experiments, evaluation, and exports.
- `notebooks/`: exploratory analysis, quick inspection, and figures in progress.
- `configs/`: parameters, paths, model settings, and experiment variants.
- `experiments/`: experiment plans, run manifests, notes, and comparisons.
- `docs/`: methods notes, setup guides, assumptions, and report/paper support.
- `outputs/`: generated results, plots, tables, logs, and exports.

## Prototype vs Stable Code

- Start rough ideas in `notebooks/` or clearly named prototype scripts.
- Move repeated or trusted logic into `src/`.
- Keep runnable workflows in `scripts/` so they can be repeated outside notebooks.
- Avoid making notebooks the only source of important transformations or results.
- Mark exploratory code with TODOs or notes before it becomes a dependency.

## Assumptions

- Document assumptions near the code, config, or experiment record they affect.
- Include assumptions about data filters, labels, models, prompts, metrics, and exclusions.
- Prefer explicit defaults in configs over hidden constants.
- Record known limitations before interpreting results.

## Reproducibility

- Use configs for parameters that change between runs.
- Record command, config path, data version/path, seed, code version, and output folder.
- Keep raw data immutable and generate processed data through scripts.
- Write results to predictable folders under `outputs/`.
- Validate scripts with small samples or smoke runs when full runs are expensive.

## Paper / Report Readiness

- Keep figure/table generation scripted when results may be cited.
- Save result tables with clear metric names and run identifiers.
- Keep notes that map outputs back to methods, configs, and data.
- Document evaluation choices and failure cases.
- Prefer readable methods code over clever abstractions.

## Method Note Template

```text
Method:
Question:
Assumptions:
Inputs:
Config:
Command:
Outputs:
Metrics:
Limitations:
```
