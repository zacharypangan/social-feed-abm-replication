# Getting Started

Use this checklist after duplicating the template for a real project.

## 1. Rename And Describe The Project

- Update `README.md` with the project name.
- Replace template language with the project goal.
- Add the primary research question or product question.

## 2. Fill The Project Brief

Update `.agent/PROJECT_BRIEF.md`:

- Project name.
- Research area.
- Primary goal.
- Current stage.
- Known commands.
- Important constraints.
- Current priorities.

## 3. Define The Tech Stack

Record what this project will actually use:

- Python, TypeScript, or both.
- Notebook workflow, scripts, API, frontend, dashboard, or experiment runner.
- Package manager and environment tool.
- Test runner, linter, formatter, and typechecker if used.

Do not add tools just because the template supports them.

## 4. Define Commands

Document real commands before relying on them:

- Install: TODO
- Test: TODO
- Lint/typecheck: TODO
- Run scripts: TODO
- Run experiments: TODO
- Run app/API/dashboard: TODO

Put these in `README.md` and `.agent/PROJECT_BRIEF.md`.

## 5. Add Data Sources

Document each dataset before processing it:

- Source and license.
- Access instructions.
- Privacy/sensitivity notes.
- Raw path.
- Expected schema.
- Processing command.

Use `.agent/DATA_WORKFLOW.md` as the checklist.

## 6. Create The First Task Log

Update `.agent/TASK_LOG.md` with:

- Current objective.
- Initial decisions.
- First task.
- Validation available or missing.
- Open questions.

## 7. Start Small

- Add dependencies only when needed.
- Keep the first feature or experiment narrow.
- Validate with a smoke test before building larger workflows.
