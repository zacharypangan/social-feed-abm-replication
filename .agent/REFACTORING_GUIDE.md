# Refactoring Guide

Refactor only when it reduces real complexity or supports the requested task.

## Before Refactoring

- Confirm the user asked for refactoring or the change requires it.
- Identify the behavior that must remain unchanged.
- Find existing tests or create a small safety check.
- Keep unrelated style churn out of the diff.

## Good Refactors

- Extract repeated experiment setup.
- Move reusable notebook logic into `src/`.
- Split large scripts into readable functions.
- Clarify config loading or data paths.
- Add typed boundaries for APIs or data records where useful.

## Avoid

- New abstractions without repeated use.
- Renaming for taste alone.
- Framework migrations.
- Dependency additions.
- Reformatting unrelated files.

## Validation

- Run tests before and after when possible.
- Compare representative outputs when refactoring experiments.
- Document any behavior change explicitly.
