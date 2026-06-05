# Testing Guide

Use tests to protect reusable logic, experiment integrity, and user-facing workflows.

## What To Test

- Data parsing and transformation logic.
- Metrics, scoring, and evaluation code.
- Prompt formatting and response parsing.
- API request/response contracts.
- Frontend state transitions and critical UI flows.
- Regression cases for fixed bugs.

## Test Style

- Keep tests deterministic.
- Use small fixtures.
- Avoid depending on private data or external services.
- Prefer explicit expected values over broad snapshots.
- Name tests by behavior.

## Validation Commands

Document project-specific commands here:

- Unit tests: TODO
- Integration tests: TODO
- Typecheck: TODO
- Lint/format check: TODO
- Smoke test: TODO

## When Tests Are Missing

- Run the smallest relevant manual check.
- State what was not validated.
- Suggest the next test to add.
