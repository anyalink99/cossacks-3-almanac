import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "parser"))
try:
    from parse_units import parse_bool
finally:
    sys.path.pop(0)


class UnitScriptParser(unittest.TestCase):
    def test_building_capture_constant_is_true(self):
        self.assertIs(parse_bool("bCapture"), True)
        self.assertIs(parse_bool("True"), True)
        self.assertIs(parse_bool("False"), False)
        self.assertIsNone(parse_bool("default"))


if __name__ == "__main__":
    unittest.main()
