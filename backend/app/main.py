from __future__ import annotations

from typing import Any

from fastapi import FastAPI

try:
    from app.agent.engine import get_next_step, load_task
    from app.agent.intent import detect_intent
    from app.agent.responder import format_reply
except ImportError:  # pragma: no cover - supports direct CLI execution
    from agent.engine import get_next_step, load_task
    from agent.intent import detect_intent
    from agent.responder import format_reply


app = FastAPI()


def run_cli() -> None:
    print("FlowPilot CLI Demo")
    message = input("输入：").strip()
    if not message:
        print("未输入内容。")
        return

    page = input("当前页面(可选)：").strip()
    state: dict[str, Any] = {"current_page": page} if page else {}

    intent = detect_intent(message)
    if intent == "unknown":
        print("未识别意图。")
        return

    task = load_task(intent)
    step = get_next_step(task, state)
    reply = format_reply(step, state)

    print("\n" + reply)


if __name__ == "__main__":
    run_cli()
