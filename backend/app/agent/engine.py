from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from app.schemas.task_schema import validate_task


TASK_DIR = Path(__file__).resolve().parent.parent / "kb" / "tasks"


def load_task(task_id: str) -> dict[str, Any]:
    path = TASK_DIR / f"{task_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"task not found: {task_id}")

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    return validate_task(data)


def _state_matches(step_state: Any, state: dict[str, Any] | None) -> bool:
    if not isinstance(step_state, dict):
        return True
    if not state:
        return True
    for key, expected in step_state.items():
        if key not in state:
            continue
        if state.get(key) != expected:
            return False
    return True


def get_next_step(
    task: dict[str, Any],
    state: dict[str, Any] | None,
    current_step: int | None = None,
) -> dict[str, Any] | None:
    steps = task.get("steps") or []
    if not steps:
        return None

    if current_step is not None:
        for idx, step in enumerate(steps):
            step_no = step.get("step")
            if step_no == current_step:
                for next_step in steps[idx + 1 :]:
                    if _state_matches(next_step.get("state"), state):
                        return next_step
                return None

    current_page = None
    if state:
        current_page = state.get("current_page")

    if current_page:
        for step in steps:
            if step.get("page") == current_page and _state_matches(
                step.get("state"), state
            ):
                return step

    for step in steps:
        if _state_matches(step.get("state"), state):
            return step

    return steps[0]
