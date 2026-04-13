from __future__ import annotations

from typing import Any


REQUIRED_TASK_KEYS = {"id", "name"}


def validate_task(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("task data must be a dict")

    task = data.get("task")
    steps = data.get("steps")

    if not isinstance(task, dict):
        raise ValueError("task section is missing")
    if not REQUIRED_TASK_KEYS.issubset(task.keys()):
        raise ValueError("task.id and task.name are required")

    if not isinstance(steps, list):
        raise ValueError("steps must be a list")

    for step in steps:
        if not isinstance(step, dict):
            raise ValueError("each step must be a dict")
        if "step" not in step:
            raise ValueError("each step must include 'step'")

    return data
