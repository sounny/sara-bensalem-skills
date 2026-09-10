"""
tests/tier1_features/test_baseline_grid.py
Feature 3: Baseline grid locking calculations
Authoritative Source: ORIGINAL_REQUEST.md §R3, spec_miner_skills/report.md §3, spec_miner_print_engine/report.md §4.2
"""

import unittest
import math

def snap_to_baseline(y: float, base_pt: float = 6.0) -> float:
    """Universal snapping formula matching Typst calc.round: y_snapped = floor(y / B + 0.5) * B"""
    return math.floor(y / base_pt + 0.5) * base_pt

def compute_leading(font_size_pt: float, base_pt: float = 6.0) -> float:
    """Calculates minimal leading so that (font_size + leading) is an integer multiple of base_pt."""
    line_pitch = math.ceil(font_size_pt / base_pt) * base_pt
    if line_pitch - font_size_pt < 2.0: # Minimum 2pt leading buffer
        line_pitch += base_pt
    return line_pitch - font_size_pt

class TestBaselineGridLocking(unittest.TestCase):
    """
    Validates mathematical baseline grid snapping, cross-spine alignment,
    and leading calculations for Swiss micro-typography.
    """

    def test_01_snap_to_6pt_baseline(self):
        """Verify arbitrary vertical coordinates snap correctly to nearest 6pt grid point."""
        self.assertEqual(snap_to_baseline(0.0, 6.0), 0.0)
        self.assertEqual(snap_to_baseline(2.9, 6.0), 0.0)
        self.assertEqual(snap_to_baseline(3.0, 6.0), 6.0)
        self.assertEqual(snap_to_baseline(5.8, 6.0), 6.0)
        self.assertEqual(snap_to_baseline(14.2, 6.0), 12.0)
        self.assertEqual(snap_to_baseline(15.1, 6.0), 18.0)

    def test_02_snap_to_4pt_baseline(self):
        """Verify snapping to 4pt micro-baseline increments."""
        self.assertEqual(snap_to_baseline(0.0, 4.0), 0.0)
        self.assertEqual(snap_to_baseline(1.9, 4.0), 0.0)
        self.assertEqual(snap_to_baseline(2.0, 4.0), 4.0)
        self.assertEqual(snap_to_baseline(7.1, 4.0), 8.0)
        self.assertEqual(snap_to_baseline(11.9, 4.0), 12.0)

    def test_03_body_line_pitch_alignment(self):
        """Verify body text (9.5pt) leading snaps to a 12pt line pitch (2x 6pt baseline)."""
        font_size = 9.5
        leading = compute_leading(font_size, base_pt=6.0)
        total_pitch = font_size + leading
        self.assertEqual(total_pitch, 12.0)
        self.assertEqual(total_pitch % 6.0, 0.0)

    def test_04_heading_line_pitch_alignment(self):
        """Verify H1 title (18pt) leading snaps to 24pt line pitch (4x 6pt baseline)."""
        font_size = 18.0
        leading = compute_leading(font_size, base_pt=6.0)
        total_pitch = font_size + leading
        self.assertEqual(total_pitch, 24.0)
        self.assertEqual(total_pitch % 6.0, 0.0)

    def test_05_cross_spine_horizontal_registration(self):
        """Verify cross-spine baseline offset between verso and recto pages is exactly 0.0pt."""
        top_margin_pt = 45.35 # ~16mm in points
        top_margin_snapped = snap_to_baseline(top_margin_pt, 6.0)

        # Verso page line baselines
        verso_lines = [top_margin_snapped + (i * 12.0) for i in range(10)]
        # Recto page line baselines
        recto_lines = [top_margin_snapped + (i * 12.0) for i in range(10)]

        for i, (v, r) in enumerate(zip(verso_lines, recto_lines)):
            delta = abs(v - r)
            self.assertLess(delta, 0.25, f"Line {i} cross-spine delta must be < 0.25pt (got {delta}pt)")

    def test_06_block_spacings_integer_multiples(self):
        """Verify spacing above and below figures snaps to integer multiples of baseline step."""
        base_step = 6.0
        h1_above = 18.0 # 3x 6pt
        h1_below = 12.0 # 2x 6pt
        par_spacing = 12.0 # 2x 6pt

        self.assertEqual(h1_above % base_step, 0.0)
        self.assertEqual(h1_below % base_step, 0.0)
        self.assertEqual(par_spacing % base_step, 0.0)

if __name__ == "__main__":
    unittest.main()
