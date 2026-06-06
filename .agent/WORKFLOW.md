# Workflow

Use this as the default operating loop for coding-agent work.

## Standard Loop

1. Understand the task and restate assumptions if needed.
2. Inspect only relevant files.
3. Make a brief plan for non-trivial work.
4. Patch minimally.
5. Validate with the smallest relevant command.
6. Summarize changes, validation, risks, and next step.

## Project Stages

1. Preliminary docs: curate agent instructions, project brief, workflow, research
   guide, data rules, and task log.
2. Synthetic MVP replication: implement a minimal Python ABM using synthetic
   network/cascade behavior before relying on restricted external data.
3. Observed cascade reconstruction: convert local ACL2017 propagation trees into
   event tables and observed `Phi` time series.
4. Original parameter replication: encode the fixed parameters and calibrated
   probabilities reported in the paper.
5. Calibration and validation: fit the chronological-feed baseline to available
   cascade data and report RMSE/NRMSE.
6. Counterfactual feed comparison: run chronological, belief-based,
   popularity-based, and random feed objectives under comparable settings.
7. Sensitivity and extension experiments: test robustness, then add NLP, SNA, or
   recommender-system extensions only after the replication baseline is stable.

## Before Editing

- Check `AGENTS.md`.
- Check `.agent/PROJECT_BRIEF.md` for project context.
- Check `.agent/TASK_LOG.md` for recent decisions.
- Inspect the files directly related to the task.
- Identify the repo's existing patterns before adding new ones.
- For research-method changes, check `.agent/RESEARCH_PROJECT_GUIDE.md` and
  `.agent/EXPERIMENT_TRACKING.md`.
- For data changes, check `.agent/DATA_WORKFLOW.md` and confirm raw data will not
  be modified or redistributed.

## During Editing

- Prefer small diffs over broad refactors.
- Preserve public interfaces unless the task requires changing them.
- Keep names explicit and research-readable.
- Add comments only for non-obvious assumptions or complex logic.
- Avoid new dependencies unless the user approves them.
- Keep faithful replication logic separate from robustness checks and
  extensions.
- Prefer explicit config values for simulation parameters, seeds, calibration
  values, and output paths.

## After Editing

- Run documented validation commands if available.
- If validation is unavailable, state that clearly.
- Update docs or task logs when durable knowledge changed.
- Keep the final answer concise.

## Minimum Run Record

Use this record shape for meaningful experiments once implementation begins:

```text
Command:
Config:
Seed:
Data input:
Code version:
Output folder:
Metrics:
Assumptions/deviations:
Notes:
```
