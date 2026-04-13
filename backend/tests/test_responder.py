import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.agent.responder import format_reply


class ResponderTests(unittest.TestCase):
    def test_format_reply_contains_action(self) -> None:
        task = {
            "steps": [
                {"step": 1, "page": "/home", "action": "进入客户管理"},
                {"step": 2, "page": "/customer", "action": "点击开户按钮"},
            ]
        }
        step = {"step": 2, "page": "/customer", "action": "点击开户按钮"}
        reply = format_reply(task, step, {"current_page": "/customer"})
        self.assertIn("点击开户按钮", reply)


if __name__ == "__main__":
    unittest.main()
