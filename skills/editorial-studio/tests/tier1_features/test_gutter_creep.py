"""
tests/tier1_features/test_gutter_creep.py
Feature 4: Gutter creep calculus for binding mechanics
Authoritative Source: ORIGINAL_REQUEST.md §R3, spec_miner_skills/report.md §3
"""

import unittest
import math

def calculate_creep(
    page: int,
    total_pages: int,
    binding_type: str,
    paper_caliper_mm: float = 0.14,
    signature_size: int = 16,
    base_inner_mm: float = 20.0,
    base_outer_mm: float = 18.0,
    gutter_draw_mm: float = 7.0
) -> dict:
    """
    Computes exact gutter creep offset and adjusted inner/outer margins
    per formulas in spec_miner_skills/report.md §3.
    """
    b_type = binding_type.upper()

    if b_type == "LAY_FLAT":
        delta_creep = 0.0
        g_draw = 0.0
    elif b_type == "SMYTH_SEWN":
        g_draw = 0.0
        # Page index in signature (0 to S-1)
        j = (page - 1) % signature_size
        # Leaf index from outside sheet 0 to center sheet S/4 - 1
        leaf = min(j // 2, (signature_size // 2) - 1 - (j // 2))
        delta_creep = paper_caliper_mm * leaf
    elif b_type == "PERFECT_BOUND":
        g_draw = gutter_draw_mm
        # Progressive shingling
        delta_creep = paper_caliper_mm * (abs(page - (total_pages / 2.0)) / 2.0)
    elif b_type == "SADDLE_STITCHED":
        g_draw = 0.0
        # Folded booklet creep
        delta_creep = paper_caliper_mm * ((total_pages / 4.0) - abs((page - 0.5 - (total_pages / 2.0)) / 2.0))
        delta_creep = max(0.0, delta_creep)
    else:
        raise ValueError(f"Unknown binding type: {binding_type}")

    inner_margin = base_inner_mm + g_draw + delta_creep
    outer_margin = base_outer_mm - delta_creep

    return {
        "page": page,
        "binding_type": b_type,
        "delta_creep_mm": round(delta_creep, 4),
        "gutter_draw_mm": g_draw,
        "inner_margin_mm": round(inner_margin, 4),
        "outer_margin_mm": round(outer_margin, 4)
    }

class TestGutterCreepCalculus(unittest.TestCase):
    """
    Validates dynamic margin compensation for sheet thickness and bindery mechanics.
    """

    def test_01_layflat_zero_creep(self):
        """Verify lay-flat board mounting has exactly 0mm gutter draw and 0mm creep."""
        res = calculate_creep(page=15, total_pages=32, binding_type="LAY_FLAT")
        self.assertEqual(res["delta_creep_mm"], 0.0)
        self.assertEqual(res["gutter_draw_mm"], 0.0)
        self.assertEqual(res["inner_margin_mm"], 20.0)
        self.assertEqual(res["outer_margin_mm"], 18.0)

    def test_02_smyth_sewn_signature_cyclic_reset(self):
        """Verify Smyth-sewn signature creep resets cyclically every 16 pages."""
        # Page 1 (outer leaf of sig 1)
        res_p1 = calculate_creep(page=1, total_pages=32, binding_type="SMYTH_SEWN", signature_size=16, paper_caliper_mm=0.15)
        self.assertEqual(res_p1["delta_creep_mm"], 0.0)

        # Page 8 (center leaf of sig 1, leaf = 3)
        res_p8 = calculate_creep(page=8, total_pages=32, binding_type="SMYTH_SEWN", signature_size=16, paper_caliper_mm=0.15)
        expected_creep = 0.15 * 3 # 0.45mm
        self.assertAlmostEqual(res_p8["delta_creep_mm"], expected_creep, places=3)

        # Page 17 (outer leaf of sig 2) -> resets to 0
        res_p17 = calculate_creep(page=17, total_pages=32, binding_type="SMYTH_SEWN", signature_size=16, paper_caliper_mm=0.15)
        self.assertEqual(res_p17["delta_creep_mm"], 0.0)

    def test_03_perfect_bound_gutter_draw(self):
        """Verify perfect-bound margins add fixed spine glue clamp gutter draw (7.0mm)."""
        res = calculate_creep(page=1, total_pages=160, binding_type="PERFECT_BOUND", gutter_draw_mm=7.0, base_inner_mm=20.0)
        self.assertGreaterEqual(res["inner_margin_mm"], 27.0)
        self.assertEqual(res["gutter_draw_mm"], 7.0)

    def test_04_saddle_stitched_booklet_progression(self):
        """Verify saddle-stitched booklet creep reaches maximum at center spread."""
        total_p = 32
        caliper = 0.12
        res_outer = calculate_creep(page=1, total_pages=total_p, binding_type="SADDLE_STITCHED", paper_caliper_mm=caliper)
        res_center = calculate_creep(page=16, total_pages=total_p, binding_type="SADDLE_STITCHED", paper_caliper_mm=caliper)

        self.assertGreater(res_center["delta_creep_mm"], res_outer["delta_creep_mm"])
        self.assertAlmostEqual(res_center["inner_margin_mm"] - res_outer["inner_margin_mm"], res_center["delta_creep_mm"] - res_outer["delta_creep_mm"])

    def test_05_margin_width_conservation(self):
        """Verify total spread margin width (inner + outer) is conserved across creep shifts (excluding gutter draw)."""
        base_inner = 20.0
        base_outer = 18.0
        for p in [2, 8, 14, 24, 30]:
            res = calculate_creep(page=p, total_pages=32, binding_type="SMYTH_SEWN", base_inner_mm=base_inner, base_outer_mm=base_outer)
            total_margin = res["inner_margin_mm"] + res["outer_margin_mm"]
            self.assertAlmostEqual(total_margin, base_inner + base_outer, places=3)

if __name__ == "__main__":
    unittest.main()
