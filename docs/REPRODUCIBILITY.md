# Reproducibility

Use this guide to make research results repeatable without over-engineering.

## Configs

- Put run-changing parameters in `configs/` or an experiment manifest.
- Prefer explicit config files over hidden constants.
- Save the config used for important runs.
- Record config path in experiment notes and output folders.

## Seeds

- Set seeds for random steps when supported.
- Record the seed in logs or run records.
- Document nondeterministic components that cannot be fully controlled.
- Do not imply exact reproducibility when external services or models can change.

## Data Lineage

Record how each output dataset or result was produced:

- Source dataset and version/snapshot.
- Raw input path.
- Processing script.
- Config and parameters.
- Command used.
- Output path.
- Row counts before and after processing.
- Filters, exclusions, joins, and label transformations.

## Observed Cascade Records

For Phase 2 observed cascade reconstruction, record:

- Config path, especially `time_bin_minutes`, selected cases, and `Phi`
  denominator.
- Raw ACL2017 dataset path and dataset split.
- Whether `ROOT -> source` events are counted in `Phi`.
- Event table output path.
- `Phi` time-series output path.
- Horizon/padding rule for each case.
- Any approximation relative to the original paper, especially use of
  `n_agents=1000` as the observed `Phi` denominator.

## Phase 3 Simulation Records

For Phase 3 model-fidelity runs, record:

- Config path and full `model_fidelity` block.
- Selected case ID, label, and simulated horizon.
- Feed objective.
- Seed and run index.
- Synthetic network summary, including average followees/followers and max
  followers.
- Per-timestep `Phi`, belief purity, event counts, and state counts.
- Whether popularity feedback was enabled.
- Assumption that ACL2017 cascades select cases but do not calibrate the
  synthetic network yet.

## Phase 4 Calibration Records

For Phase 4 chronological calibration runs, record:

- Config path and candidate multiplier grid.
- Observed Phase 2 `Phi` target path for each case.
- Feed objective, currently chronological only.
- Candidate probabilities for `p_online`, `p_reshare`, and `p_reject`.
- Seed and number of simulations per candidate.
- Averaged simulated `Phi` series.
- RMSE and NRMSE for each candidate.
- Best-candidate selection rule.
- Assumption that this is a lightweight executable grid, not a final
  calibration search.

## Phase 5 Counterfactual Records

For Phase 5 case-study counterfactual runs, record:

- Config path and Phase 4 calibration output path.
- Case ID, calibrated probabilities, feed objective, seed, and run index.
- Number of simulations per feed condition.
- Per-feed `Phi_avg`, `Phi_max`, belief purity, and event summaries.
- Paper-style relative changes against chronological baseline.
- FakeNewsNet audit summaries as parameter context only.
- Assumption that full-dataset average propagation analysis is a later
  robustness phase, not the faithful paper replication target.

## Phase 6 Fidelity Repair Records

For Phase 6 replication-fidelity repair runs, record:

- Config path and paper-probability source for each case.
- Synthetic network model, target average followees, seed, and network summary.
- Whether probability sampling, sampled `Nposts`, Bayesian-style belief update,
  background posts, verified influence, and popularity feedback were enabled.
- Per-feed `Phi_avg`, `Phi_max`, belief purity, event summaries, and relative
  changes against chronological baseline.
- Target-verdict rows, including `blocked` rows where exact paper target values
  have not yet been transcribed.
- Sanitized synthetic network snapshot path and observed cascade snapshot path.
- Assumption that the observed ACL2017 propagation tree is not the underlying
  follower network.

## Outputs

- Write generated artifacts under `outputs/`.
- Use run IDs or dated folders for experiments.
- Save metrics, result tables, logs, and figures in predictable locations.
- Avoid overwriting important results unless intentional.
- Do not commit large outputs unless there is a clear reason.

## Environment Files

- Use `.env.example` to document required environment variables.
- Keep real `.env` files local and ignored.
- Document runtime versions and package managers.
- Add lockfiles only when the project actually uses dependency management.
- Ask before installing or upgrading dependencies.

## Minimum Run Record

```text
Command:
Config:
Seed:
Data input:
Code version:
Output folder:
Metrics:
Notes:
```
