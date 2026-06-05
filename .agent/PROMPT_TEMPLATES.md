# Prompt Templates

Copy-paste prompts for Codex sessions. Replace placeholders like `{task}`, `{files}`, and `{command}`.

## 1. Repository Exploration

```text
Task:
Explore this repository and explain how it is organized.

Scope:
Focus on {files or areas}. Read `AGENTS.md` and relevant `.agent/` files first.

Constraints:
Inspect before summarizing. Do not edit files. Avoid dumping long file contents.

Validation:
No code validation needed.

Return:
Summarize architecture, key files, available commands, risks, and recommended next steps.
```

## 2. New Research Prototype Feature

```text
Task:
Implement {feature}.

Scope:
Touch only {files or folders}. Put reusable logic in `src/` and runnable entry points in `scripts/` when appropriate.

Constraints:
Keep the diff minimal. Do not add dependencies without asking. Preserve existing architecture.

Validation:
Run {command} if available, otherwise state what could not be validated.

Return:
Summary, files changed, validation, risks/not verified, next step.
```

## 3. Bug Fix

```text
Task:
Fix {bug}.

Scope:
Start with {files, command, or error output}.

Constraints:
Find the root cause before patching. Make the smallest safe fix. Avoid unrelated refactors.

Validation:
Re-run {command} or the smallest reproduction.

Return:
Cause, fix summary, files changed, validation, remaining risk.
```

## 4. Refactor

```text
Task:
Refactor {code or workflow}.

Scope:
Limit changes to {files or modules}.

Constraints:
Preserve behavior. Avoid new dependencies. Avoid unrelated formatting churn.

Validation:
Run {command} and compare expected behavior before/after if possible.

Return:
What changed, why it is behavior-preserving, files changed, validation, risks.
```

## 5. Add Tests

```text
Task:
Add tests for {behavior}.

Scope:
Use existing test patterns in {files or tests folder}.

Constraints:
Keep tests deterministic. Use small fixtures. Do not require private data or network access.

Validation:
Run {test command}.

Return:
Test coverage added, files changed, validation, remaining gaps.
```

## 6. Create Data Processing Script

```text
Task:
Create a data processing script for {task}.

Scope:
Inputs: {input paths}. Outputs: {output paths}. Config: {config path if any}.

Constraints:
Do not overwrite raw data. Make inputs/outputs traceable. Keep logic readable.

Validation:
Run {command} on a small sample or dry run.

Return:
Script behavior, files changed, validation, assumptions, next step.
```

## 7. Create Experiment Script

```text
Task:
Create a reproducible experiment script for {experiment}.

Scope:
Use {data}, {config}, and write outputs to {output path}.

Constraints:
Record assumptions, config, command, seed, and output location. Keep reusable logic in `src/`.

Validation:
Run {command} or a small smoke test.

Return:
Experiment flow, files changed, validation, reproducibility notes, risks.
```

## 8. Add Evaluation Metrics

```text
Task:
Add evaluation metrics for {task or model}.

Scope:
Implement metrics in {files}. Inputs are {inputs}; expected outputs are {outputs}.

Constraints:
Make formulas explicit. Add tests for edge cases. Avoid changing unrelated evaluation logic.

Validation:
Run {command}.

Return:
Metrics added, assumptions, files changed, validation, limitations.
```

## 9. Create FastAPI Endpoint

```text
Task:
Create a FastAPI endpoint for {endpoint purpose}.

Scope:
Route: {method path}. Request: {schema}. Response: {schema}. Files: {files}.

Constraints:
Follow existing API patterns. Validate inputs. Do not add dependencies without asking.

Validation:
Run {command} and a smoke request if available.

Return:
Endpoint behavior, files changed, validation, risks/not verified.
```

## 10. Create React UI Component

```text
Task:
Create a React UI component for {component purpose}.

Scope:
Files: {files}. Props/state: {props or state}. Data source: {data source}.

Constraints:
Follow existing design patterns. Handle loading, empty, and error states. Keep TypeScript types clear.

Validation:
Run {command} and verify UI behavior if a dev server is available.

Return:
Component behavior, files changed, validation, UI risks/not verified.
```

## 11. Review Code

```text
Task:
Review the current changes for bugs and research-quality risks.

Scope:
Review {files or diff}.

Constraints:
Prioritize correctness, reproducibility, data safety, validation gaps, and maintainability.

Validation:
Do not patch unless asked. Mention any checks you ran or did not run.

Return:
Findings first by severity with file/line references, then questions, then brief summary.
```

## 12. Summarize Project State

```text
Task:
Summarize the current project state.

Scope:
Read `AGENTS.md`, `.agent/PROJECT_BRIEF.md`, `.agent/TASK_LOG.md`, and {files if relevant}.

Constraints:
Do not edit files. Keep it concise. Summarize instead of dumping content.

Validation:
No code validation needed.

Return:
Project purpose, architecture, commands, recent work, open risks, recommended next step.
```

## 13. Prepare Handoff Notes

```text
Task:
Prepare handoff notes for {work or milestone}.

Scope:
Use {files}, recent changes, and `.agent/TASK_LOG.md` if present.

Constraints:
Be concise and actionable. Include assumptions and unfinished work.

Validation:
Mention validation already run: {command or none}.

Return:
Context, changes made, how to run/validate, known risks, next tasks.
```

## 14. Optimize Token Usage In A Codex Session

```text
Task:
Optimize this Codex session for token-efficient work on {task}.

Scope:
Use only relevant files: {files}. Prefer summaries over full dumps.

Constraints:
Read `AGENTS.md` and only the necessary `.agent/` files. Keep updates and final answer concise.

Validation:
Use {command} only if needed for the task.

Return:
Brief plan, files inspected, minimal next action, and what context should be saved to `.agent/TASK_LOG.md`.
```
