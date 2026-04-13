from __future__ import annotations


def detect_intent(text: str) -> str:
    if not text:
        return "unknown"

    if "开卡" in text or "开户" in text:
        return "open_account"

    return "unknown"
