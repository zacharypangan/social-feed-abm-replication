# Project Setup Checklist

Use this after duplicating the template.

## Repository Identity

- [ ] Rename the repository.
- [ ] Update `README.md` with project name and purpose.
- [ ] Fill `.agent/PROJECT_BRIEF.md`.
- [ ] Create the first `.agent/TASK_LOG.md` entry.

## Tech Stack

- [ ] Choose language/runtime versions.
- [ ] Choose package manager/environment tool.
- [ ] Define install command.
- [ ] Define test command.
- [ ] Define lint/format/typecheck commands if used.
- [ ] Document app/API/dashboard run commands if used.

## Structure

- [ ] Decide what belongs in `src/`.
- [ ] Decide what belongs in `scripts/`.
- [ ] Decide what belongs in `notebooks/`.
- [ ] Decide where configs live.
- [ ] Decide where outputs should be written.

## Data

- [ ] Document data sources.
- [ ] Record licenses and usage constraints.
- [ ] Mark sensitive/private data.
- [ ] Define raw, interim, processed, and output paths if needed.
- [ ] Document schemas.
- [ ] Add processing commands.

## Reproducibility

- [ ] Use configs for variable parameters.
- [ ] Record seeds where relevant.
- [ ] Record command lines for repeatable workflows.
- [ ] Record data lineage.
- [ ] Record output folders.
- [ ] Document environment files.

## Agentic Coding

- [ ] Read `AGENTS.md`.
- [ ] Keep stable context in `.agent/PROJECT_BRIEF.md`.
- [ ] Keep recent context in `.agent/TASK_LOG.md`.
- [ ] Use `.agent/PROMPT_TEMPLATES.md` for short focused prompts.
- [ ] Ask before adding dependencies or destructive changes.
