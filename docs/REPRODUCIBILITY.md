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
