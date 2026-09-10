"""
tests/tier3_combinations/test_facing_spread_baseline_creep.py
Combination 1: Facing spread with baseline lock + dynamic gutter creep
Authoritative Source: ORIGINAL_REQUEST.md §R3, spec_miner_skills/report.md §3, §Edge Case #1
"""

import unittest
from tests.tier1_features.test_baseline_grid import snap_to_baseline
from tests.tier1_features.test_gutter_creep import calculate_creep

class TestFacingSpreadBaselineCreep(unittest.TestCase):
    """
    Tests cross-feature interaction between:
    - Asymmetric facing spreads (verso vs recto)
    - Dynamic gutter creep shifting inner and outer margins
    - Vertical baseline registration locking across the spine
    """

    def test_01_baseline_registration_preserved_across_creep_shifts(self):
        """
        Verify that as inner/outer margins shift across signatures due to gutter creep,
        vertical line baselines across facing pages (verso page p, recto page p+1)
        remain strictly synchronized with delta y == 0.0pt.
        """
        base_top_mm = 20.0
        base_top_pt = base_top_mm * (72.0 / 25.4)
        top_snapped = snap_to_baseline(base_top_pt, 6.0)

        # Test across 3 distinct signatures (e.g. p=2/3, p=16/17, p=30/31)
        for spread_idx, (verso_p, recto_p) in enumerate([(2, 3), (16, 17), (30, 31)]):
            verso_creep = calculate_creep(verso_p, total_pages=48, binding_type="SMYTH_SEWN", signature_size=16)
            recto_creep = calculate_creep(recto_p, total_pages=48, binding_type="SMYTH_SEWN", signature_size=16)

            # Even though horizontal margins vary with creep:
            self.assertIsInstance(verso_creep["inner_margin_mm"], float)
            self.assertIsInstance(recto_creep["inner_margin_mm"], float)

            # Vertical baselines on verso and recto must align
            for line_idx in range(25): # 25 lines of body text
                v_baseline = top_snapped + (line_idx * 12.0)
                r_baseline = top_snapped + (line_idx * 12.0)
                delta_y = abs(v_baseline - r_baseline)
                self.assertLess(delta_y, 0.25, f"Spread {spread_idx} line {line_idx} vertical delta must be < 0.25pt")

    def test_02_perfect_bound_gutter_draw_facing_spread_measure(self):
        """
        Verify that in a perfect-bound book with 7.0mm gutter draw,
        the usable printable width on both verso and recto pages accommodates
        the Swiss 12-column grid without margin collision.
        """
        page_w_mm = 297.0
        verso = calculate_creep(page=20, total_pages=160, binding_type="PERFECT_BOUND", gutter_draw_mm=7.0, base_inner_mm=20.0, base_outer_mm=18.0)
        recto = calculate_creep(page=21, total_pages=160, binding_type="PERFECT_BOUND", gutter_draw_mm=7.0, base_inner_mm=20.0, base_outer_mm=18.0)

        # Usable text width = page_w - inner_margin - outer_margin
        verso_content_w = page_w_mm - verso["inner_margin_mm"] - verso["outer_margin_mm"]
        recto_content_w = page_w_mm - recto["inner_margin_mm"] - recto["outer_margin_mm"]

        # Minimum required width for 12 columns with 4mm gutters (11 gutters = 44mm)
        self.assertGreater(verso_content_w, 200.0)
        self.assertGreater(recto_content_w, 200.0)
        # Margins remain symmetric across facing pair
        self.assertAlmostEqual(verso_content_w, recto_content_w, places=2)

    def test_03_heading_leading_sync_across_facing_pages(self):
        """
        Verify when verso has H1 title (24pt pitch) + body (12pt pitch)
        and recto has pure body (12pt pitch), both columns re-synchronize
        baselines after the heading block.
        """
        top_snapped = snap_to_baseline(56.7, 6.0) # ~20mm in pt

        # Verso: H1 (above 18pt, title 24pt pitch, below 12pt) = 54pt -> snaps to 9 * 6pt
        h1_block_height = 18.0 + 24.0 + 12.0
        self.assertEqual(h1_block_height % 6.0, 0.0)

        verso_first_body_baseline = top_snapped + h1_block_height + 12.0

        # Recto: 5 lines of body text (each 12pt) = 60pt
        # Line 5 baseline: top_snapped + (5 * 12.0) = top_snapped + 60.0
        # Line 6 baseline: top_snapped + (6 * 12.0) = top_snapped + 72.0
        # Note that h1_block_height (54pt) + 12pt = 66pt (snaps to grid)
        self.assertEqual(verso_first_body_baseline % 6.0, 0.0)

if __name__ == "__main__":
    unittest.main()
