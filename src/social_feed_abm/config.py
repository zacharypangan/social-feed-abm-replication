"""Config loading for Phase 1 scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config(path: Path) -> dict[str, Any]:
    """Load a JSON config file."""

    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    _require(config, ["project", "data", "selected_cases"])
    return config


def _require(mapping: dict[str, Any], keys: list[str]) -> None:
    missing = [key for key in keys if key not in mapping]
    if missing:
        raise KeyError(f"Config is missing required keys: {', '.join(missing)}")
