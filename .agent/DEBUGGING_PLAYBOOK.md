# Debugging Playbook

Use this for failures in scripts, experiments, APIs, dashboards, notebooks, or tests.

## First Pass

1. Capture the exact command, input, and error.
2. Identify the smallest reproducible case.
3. Inspect relevant files only.
4. Check recent changes in `git status` and `git diff` if useful.
5. Form one likely hypothesis before patching.

## Common Checks

- Config path, environment variables, and working directory.
- Data existence, schema, encoding, and row counts.
- Dependency versions, only if versioning is already documented.
- Random seeds and nondeterministic steps.
- API request/response shapes.
- Frontend console/network errors.
- Notebook state that differs from script state.

## Patch Rules

- Patch the root cause, not only the symptom.
- Keep the fix narrow.
- Add regression coverage when the failure is likely to recur.
- Record any assumption that affects interpretation of results.

## Validation Template

```text
Failure:
Cause:
Fix:
Validation command:
Remaining risk:
```
