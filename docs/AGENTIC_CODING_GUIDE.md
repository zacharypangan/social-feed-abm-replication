# Agentic Coding Guide

Use this template to keep Codex sessions focused, low-token, and reproducible.

## How To Use Codex With This Template

Start each new project by asking Codex to read:

- `AGENTS.md`
- `.agent/PROJECT_BRIEF.md`
- `.agent/TASK_LOG.md`

Then give one focused task with scope, constraints, validation, and expected
return format. Use `.agent/PROMPT_TEMPLATES.md` when possible.

## Save Tokens

- Point Codex to specific files or folders.
- Ask for summaries instead of full file dumps.
- Put stable facts in `.agent/PROJECT_BRIEF.md`.
- Put recent decisions in `.agent/TASK_LOG.md`.
- Avoid pasting long logs; paste the command, key error, and expected behavior.
- Ask Codex to inspect before editing.

## Write Small Prompts

Use this shape:

```text
Task:
{task}

Scope:
{files}

Constraints:
Minimal diff. No new dependencies. Preserve architecture.

Validation:
Run {command} if available.

Return:
Summary, files changed, validation, risks/not verified, next step.
```

## Update TASK_LOG When

- A task changes project direction.
- A command, workflow, or validation result becomes important later.
- A bug cause or workaround should be remembered.
- An experiment result or limitation should be traceable.
- Work pauses with unfinished follow-ups.

Keep entries short.

## Update PROJECT_BRIEF When

- The project goal changes.
- The tech stack changes.
- Install, test, run, or validation commands change.
- Data/privacy constraints change.
- Current priorities change.
- A stable architectural decision is made.

## Good Codex Requests

- "Inspect these files and summarize the current workflow before editing."
- "Patch only `{files}` and validate with `{command}`."
- "Do not add dependencies; suggest one only if needed."
- "Update `.agent/TASK_LOG.md` with the final decision."
- "Review this diff for reproducibility and validation gaps."
