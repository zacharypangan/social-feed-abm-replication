"""Create a lightweight timestamped experiment folder."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    cleaned = []
    for char in value.lower().strip():
        if char.isalnum():
            cleaned.append(char)
        elif char in {" ", "-", "_"}:
            cleaned.append("-")
    slug = "".join(cleaned).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "experiment"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Short experiment name")
    parser.add_argument(
        "--base-dir",
        choices=("experiments", "outputs"),
        default="experiments",
        help="Where to create the timestamped folder",
    )
    parser.add_argument(
        "--config",
        default="configs/phase1_acl2017_cases.json",
        help="Config file to copy into the experiment folder",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    experiment_dir = repo_root / args.base_dir / f"{timestamp}-{slugify(args.name)}"
    experiment_dir.mkdir(parents=True, exist_ok=False)

    config_path = repo_root / args.config
    if config_path.exists():
        shutil.copy2(config_path, experiment_dir / "config.yaml")
    else:
        (experiment_dir / "config.yaml").write_text(
            "# TODO: add experiment config\n",
            encoding="utf-8",
        )

    (experiment_dir / "README.md").write_text(
        "\n".join(
            [
                f"# {args.name}",
                "",
                f"- Created: {timestamp}",
                f"- Source config: {args.config}",
                "- Command: TODO",
                "- Notes: TODO",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(experiment_dir.relative_to(repo_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
