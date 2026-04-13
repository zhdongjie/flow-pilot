from __future__ import annotations

from typing import Any


def get_current_page(state: dict[str, Any] | None) -> str | None:
    if not state:
        return None

    page = state.get("current_page")
    if isinstance(page, str) and page.strip():
        return page

    return None
