# Code Review Checklist

Use this for reviews before committing or merging.

## Correctness

- Does the change solve the stated task?
- Are edge cases handled explicitly?
- Are assumptions visible in code, config, or docs?
- Are errors handled at the right level?

## Research Quality

- Are inputs, configs, seeds, and outputs traceable?
- Can the result be reproduced by another session?
- Are metrics and evaluation logic clear?
- Are notebooks backed by scripts where repeatability matters?

## Maintainability

- Is the diff minimal and focused?
- Does it follow existing project patterns?
- Are names clear to a future researcher?
- Is reusable logic in `src/` rather than hidden in notebooks?

## Frontend / Backend

- React/TypeScript: Are states, loading, errors, and types handled?
- FastAPI/API: Are request/response shapes explicit and validated?
- Dashboards: Are charts and filters tied to traceable data sources?

## Validation

- Were tests, lint, typecheck, smoke tests, or experiment dry runs executed?
- If not, is the gap stated clearly?
- Are new risks documented?
