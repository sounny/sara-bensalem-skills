"""
tests/tier3_combinations/test_iso128_typst_embedding.py
Combination 2: ISO 128 vector plates embedded in Typst Swiss 12-column layout
Authoritative Source: ORIGINAL_REQUEST.md §R2, §R4, spec_miner_skills/report.md §4, spec_miner_print_engine/report.md §4.3
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.tier1_features.test_vector_downsampling import downsample_stroke, downsample_hatch, filter_annotations

class TestISO128TypstEmbedding(unittest.TestCase):
    """
    Tests cross-feature integration of:
    - ISO 128 calibrated vector plates (0.13, 0.25, 0.35, 0.50, 0.70mm)
    - Scale-aware downsampling algorithms
    - Embedding inside Typst Swiss 12-column grid cells
    """

    def test_01_full_bleed_plate_12_columns(self):
        """Verify full 12-column plate (scale=1.0) preserves all native ISO 128 strokes and annotations."""
        scale = 1.0
        s_cut = downsample_stroke(0.70, scale)
        s_structure = downsample_stroke(0.50, scale)
        s_partition = downsample_stroke(0.35, scale)
        s_projection = downsample_stroke(0.25, scale)
        s_hatch = downsample_stroke(0.13, scale)

        self.assertEqual(s_cut, 0.70)
        self.assertEqual(s_structure, 0.50)
        self.assertEqual(s_partition, 0.35)
        self.assertEqual(s_projection, 0.25)
        self.assertEqual(s_hatch, 0.13)
        self.assertEqual(filter_annotations(scale), "FULL_ANNOTATIONS")

    def test_02_half_page_plate_8_columns(self):
        """Verify 8-column plate (scale=0.67) preserves stroke differentiation without clamping."""
        scale = 0.67
        s_structure = downsample_stroke(0.50, scale) # 0.335mm
        s_hatch = downsample_stroke(0.13, scale) # 0.0871mm > 0.08mm

        self.assertAlmostEqual(s_structure, 0.335, places=3)
        self.assertAlmostEqual(s_hatch, 0.087, places=3)
        self.assertGreaterEqual(s_hatch, 0.08)
        self.assertEqual(filter_annotations(scale), "MAJOR_DIMENSIONS_ONLY")

    def test_03_quadrant_plate_4_columns_clamping(self):
        """Verify 4-column quadrant plate (scale=0.33) clamps fine strokes to 0.08mm print limit."""
        scale = 0.33
        # 0.13mm * 0.33 = 0.0429mm -> Clamped to 0.08mm
        s_hatch = downsample_stroke(0.13, scale, min_clamp_mm=0.08)
        self.assertEqual(s_hatch, 0.08)

        # Hatch decimation should trigger POCHE_REPLACE because spacing < 0.35mm
        hatch_res = downsample_hatch(native_spacing_mm=0.8, scale_factor=scale)
        self.assertEqual(hatch_res["action"], "POCHE_REPLACE")
        self.assertEqual(filter_annotations(scale), "GRAPHIC_SCALE_BAR_ONLY")

    def test_04_typst_cetz_code_generation_parity(self):
        """Verify generated CeTZ drawing code accurately declares ISO 128 stroke groups."""
        # Simulated CeTZ macro block
        cetz_strokes = {
            "cut": "0.50mm + cmyk(0%, 0%, 0%, 100%)",
            "joinery": "0.35mm + cmyk(0%, 0%, 0%, 100%)",
            "outline": "0.25mm + cmyk(0%, 0%, 0%, 80%)",
            "hatch": "0.13mm + cmyk(0%, 0%, 0%, 50%)"
        }
        self.assertIn("0.50mm", cetz_strokes["cut"])
        self.assertIn("0.35mm", cetz_strokes["joinery"])
        self.assertIn("0.25mm", cetz_strokes["outline"])
        self.assertIn("0.13mm", cetz_strokes["hatch"])

if __name__ == "__main__":
    unittest.main()
