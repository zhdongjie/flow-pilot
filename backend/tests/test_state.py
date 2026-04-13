import sys
from pathlib import Path
import unittest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.agent.state import get_current_page


class StateTests(unittest.TestCase):
    def test_get_current_page(self) -> None:
        self.assertEqual(get_current_page({"current_page": "/home"}), "/home")

    def test_get_current_page_blank(self) -> None:
        self.assertIsNone(get_current_page({"current_page": ""}))

    def test_get_current_page_missing(self) -> None:
        self.assertIsNone(get_current_page(None))


if __name__ == "__main__":
    unittest.main()
