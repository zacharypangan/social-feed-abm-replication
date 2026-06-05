"""Check that the research template repository has its expected structure."""

from __future__ import annotations

from pathlib import Path


REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    ".env.example",
    ".agent/PROJECT_BRIEF.md",
    ".agent/TASK_LOG.md",
    "configs/phase1_acl2017_cases.json",
    "configs",
    "data",
    "data/README.md",
    "docs/GETTING_STARTED.md",
    "docs/PROJECT_SETUP_CHECKLIST.md",
    "docs/REPRODUCIBILITY.md",
    "docs/AGENTIC_CODING_GUIDE.md",
    "experiments",
    "notebooks",
    "outputs",
    "scripts/check_repo.py",
    "scripts/new_experiment.py",
    "src/__init__.py",
    "tests/test_template_placeholder.py",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_PATHS if not (repo_root / path).exists()]

    if missing:
        print("Missing required template paths:")
        for path in missing:
            print(f"- {path}")
        return 1

    print("Template structure check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
