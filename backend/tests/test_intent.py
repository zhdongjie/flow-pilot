import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.agent.intent import detect_intent


class IntentTests(unittest.TestCase):
    def test_detect_open_account(self) -> None:
        self.assertEqual(detect_intent("我要开户"), "open_account")

    def test_detect_unknown(self) -> None:
        self.assertEqual(detect_intent("你好"), "unknown")


if __name__ == "__main__":
    unittest.main()
