import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.agent.engine import get_next_step, load_task


class EngineTests(unittest.TestCase):
    def test_next_step_matches_page(self) -> None:
        task = load_task("open_account")
        step = get_next_step(task, {"current_page": "/customer"})
        self.assertIsNotNone(step)
        self.assertEqual(step.get("step"), 2)

    def test_next_step_fallback_first(self) -> None:
        task = load_task("open_account")
        step = get_next_step(task, {})
        self.assertIsNotNone(step)
        self.assertEqual(step.get("step"), 1)


if __name__ == "__main__":
    unittest.main()
