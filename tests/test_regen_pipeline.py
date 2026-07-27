"""Regression tests for the repository regeneration graph."""
from __future__ import annotations

import unittest

from scripts import regen


class RegenerationOrder(unittest.TestCase):
    def test_full_build_refreshes_derived_inputs_before_reports(self):
        order = regen.ALIASES["all"]
        self.assertLess(order.index("data"), order.index("derived"))
        self.assertLess(order.index("derived"), order.index("reports-map"))
        self.assertEqual(order[-1], "manifests")

    def test_sanity_rebuild_and_check_are_sequential(self):
        self.assertIn("sanity", regen.SEQUENTIAL_TARGETS)
        self.assertEqual(
            regen.TARGETS["sanity"],
            [
                ["parser/build_data.py"],
                ["scripts/check_data_sanity.py"],
            ],
        )


if __name__ == "__main__":
    unittest.main()
