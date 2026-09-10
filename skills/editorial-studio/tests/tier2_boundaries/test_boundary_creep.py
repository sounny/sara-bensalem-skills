"""
tests/tier2_boundaries/test_boundary_creep.py
Feature 1 (Tier 2): Boundary and edge conditions for gutter creep calculus
Authoritative Source: ORIGINAL_REQUEST.md §R3, spec_miner_skills/report.md §3, §Edge Cases #5-#6
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.tier1_features.test_gutter_creep import calculate_creep

class TestBoundaryCreep(unittest.TestCase):
    """
    Tests edge and boundary conditions for binding creep:
    - Single page (N=1)
    - Small booklet (N=4)
    - Extreme page counts (N=500)
    - Zero paper caliper (c=0.0mm)
    - Heavy board caliper (c=0.35mm)
    - Invalid page index bounds
    """

    def test_01_single_page_boundary(self):
        """Verify single page document (N=1) calculates zero creep displacement."""
        res = calculate_creep(page=1, total_pages=1, binding_type="SMYTH_SEWN", signature_size=16)
        self.assertEqual(res["delta_creep_mm"], 0.0)
        self.assertEqual(res["inner_margin_mm"], 20.0)
        self.assertEqual(res["outer_margin_mm"], 18.0)

    def test_02_small_booklet_four_pages(self):
        """Verify 4-page folded leaflet (N=4) has bounded, non-negative creep."""
        res_p1 = calculate_creep(page=1, total_pages=4, binding_type="SADDLE_STITCHED", paper_caliper_mm=0.15)
        res_p2 = calculate_creep(page=2, total_pages=4, binding_type="SADDLE_STITCHED", paper_caliper_mm=0.15)
        self.assertGreaterEqual(res_p1["delta_creep_mm"], 0.0)
        self.assertGreaterEqual(res_p2["delta_creep_mm"], 0.0)
        self.assertLess(res_p2["delta_creep_mm"], 1.0)

    def test_03_extreme_page_count_500_pages(self):
        """Verify extreme 500-page monograph retains safe outer margins (>5mm)."""
        res = calculate_creep(
            page=250,
            total_pages=500,
            binding_type="SMYTH_SEWN",
            signature_size=32,
            paper_caliper_mm=0.12,
            base_inner_mm=22.0,
            base_outer_mm=18.0
        )
        self.assertLess(res["delta_creep_mm"], 2.0)
        self.assertGreater(res["outer_margin_mm"], 15.0)

    def test_04_zero_caliper_boundary(self):
        """Verify paper caliper c=0.0 produces zero creep displacement across all pages."""
        for p in [1, 16, 64, 128]:
            res = calculate_creep(page=p, total_pages=128, binding_type="PERFECT_BOUND", paper_caliper_mm=0.0, gutter_draw_mm=7.0)
            self.assertEqual(res["delta_creep_mm"], 0.0)
            self.assertEqual(res["inner_margin_mm"], 27.0)
            self.assertEqual(res["outer_margin_mm"], 18.0)

    def test_05_heavy_board_caliper_stress(self):
        """Verify heavy card stock (c=0.35mm) does not cause negative outer margins."""
        res = calculate_creep(
            page=16,
            total_pages=32,
            binding_type="SADDLE_STITCHED",
            paper_caliper_mm=0.35,
            base_inner_mm=25.0,
            base_outer_mm=20.0
        )
        self.assertGreater(res["outer_margin_mm"], 5.0, "Outer margin must never breach 5mm safety zone")

    def test_06_invalid_binding_type_raises_error(self):
        """Verify invalid binding type string raises descriptive ValueError."""
        with self.assertRaises(ValueError):
            calculate_creep(page=1, total_pages=10, binding_type="SPIRAL_COMB_UNSUPPORTED")

if __name__ == "__main__":
    unittest.main()
