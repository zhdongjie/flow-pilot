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


def format_reply(step: dict[str, Any] | None, state: dict[str, Any] | None) -> str:
    if step is None:
        return "未找到可执行步骤。"

    current_page = "未知"
    if state:
        page = state.get("current_page")
        if isinstance(page, str) and page.strip():
            current_page = page

    action_text = _build_action_text(step)

    lines = [
        f"当前页面：{current_page}",
        "",
        "建议下一步：",
        action_text,
        "",
        "原因：",
        "这是流程的下一步。",
    ]

    return "\n".join(lines)
