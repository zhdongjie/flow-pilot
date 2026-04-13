from __future__ import annotations

from typing import Any


def _build_action_text(step: dict[str, Any]) -> str:
    action = step.get("action")
    if isinstance(action, str) and action.strip():
        return action

    form = step.get("form")
    if isinstance(form, list) and form:
        fields: list[str] = []
        for item in form:
            if not isinstance(item, dict):
                continue
            field = item.get("field")
            desc = item.get("desc")
            if isinstance(field, str) and isinstance(desc, str):
                fields.append(f"{desc}（{field}）")
            elif isinstance(desc, str):
                fields.append(desc)
            elif isinstance(field, str):
                fields.append(field)
        if fields:
            return "填写表单：" + "，".join(fields)

    return "执行下一步操作"


def _format_step_line(step: dict[str, Any]) -> str:
    action_text = _build_action_text(step)
    page = step.get("page")
    if isinstance(page, str) and page.strip():
        return f"{action_text}（{page}）"
    return action_text


def format_reply(
    task: dict[str, Any],
    step: dict[str, Any] | None,
    state: dict[str, Any] | None,
) -> str:
    steps = task.get("steps") or []
    if not steps or step is None:
        return "未找到可执行步骤。"

    current_page = "未知"
    if state:
        page = state.get("current_page")
        if isinstance(page, str) and page.strip():
            current_page = page

    action_text = _build_action_text(step)

    step_lines: list[str] = []
    for item in steps:
        if not isinstance(item, dict):
            continue
        step_no = item.get("step")
        if isinstance(step_no, int):
            step_lines.append(f"{step_no}. {_format_step_line(item)}")
        else:
            step_lines.append(f"- {_format_step_line(item)}")

    lines = [
        f"当前页面：{current_page}",
        "",
        "完整流程：",
        *step_lines,
        "",
        "建议下一步：",
        action_text,
        "",
        "原因：",
        "这是流程的下一步。",
    ]

    return "\n".join(lines)
