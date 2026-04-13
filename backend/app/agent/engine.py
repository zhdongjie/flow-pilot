from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

try:
    from app.schemas.task_schema import validate_task
except ImportError:  # pragma: no cover - supports direct CLI execution
    from schemas.task_schema import validate_task


TASK_DIR = Path(__file__).resolve().parent.parent / "kb" / "tasks"


def load_task(task_id: str) -> dict[str, Any]:
    path = TASK_DIR / f"{task_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"task not found: {task_id}")

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    return validate_task(data)


def get_next_step(task: dict[str, Any], state: dict[str, Any] | None) -> dict[str, Any] | None:
    steps = task.get("steps") or []
    if not steps:
        return None

    current_page = None
    if state:
        current_page = state.get("current_page")

    if current_page:
        for step in steps:
            if step.get("page") == current_page:
                return step

    return steps[0]
