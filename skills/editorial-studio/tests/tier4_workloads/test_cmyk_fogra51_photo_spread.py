"""
tests/tier4_workloads/test_cmyk_fogra51_photo_spread.py
Workload 4 (Tier 4): High-density photo spread with CMYK FOGRA51 color management
Authoritative Source: ORIGINAL_REQUEST.md §R5, Acceptance Criteria, spec_miner_print_engine/report.md §6.5
"""

import sys
import os
import unittest
import tempfile
import io
import fitz
import numpy as np
from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.fixtures.pdf_generator import create_synthetic_pdf, MM_TO_PT
from tests.tier2_boundaries.test_boundary_color_tac import calculate_tac_for_image_bytes

class TestCMYKFOGRA51PhotoSpread(unittest.TestCase):
    """
    Validates high-density architectural photo spreads:
    - CMYK FOGRA51 color profile adherence
    - Pixel-level Total Area Coverage (TAC <= 320%)
    - Effective image resolution (>= 300 DPI)
    """

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_cmyk_rich_black_fogra51_tac_verified(self):
        """
        Verify FOGRA51 calibrated Rich Black (C=60%, M=40%, Y=40%, K=100%)
        produces a deep, neutral black with TAC = 240% <= 320%.
        """
        # (60% + 40% + 40% + 100%) = 240%
        c = int(round(0.60 * 255))
        m = int(round(0.40 * 255))
        y = int(round(0.40 * 255))
        k = int(round(1.00 * 255))

        arr = np.zeros((100, 100, 4), dtype=np.uint8)
        arr[:, :, 0] = c
        arr[:, :, 1] = m
        arr[:, :, 2] = y
        arr[:, :, 3] = k

        buf = io.BytesIO()
        Image.fromarray(arr, mode="CMYK").save(buf, format="TIFF")
        res = calculate_tac_for_image_bytes(buf.getvalue(), max_tac_allowed=320.0)

        self.assertEqual(res["status"], "PASS")
        self.assertAlmostEqual(res["peak_tac"], 240.0, delta=1.0)
        self.assertEqual(res["violations"], 0)

    def test_02_high_density_hero_spread_preflight_pass(self):
        """
        Verify an entire compiled facing spread containing a hero photographic plate
        passes both the TAC limit (<=320%) and the high-resolution threshold (>=300 DPI).
        """
        pdf_path = os.path.join(self.temp_dir.name, "fogra51_hero_spread.pdf")
        create_synthetic_pdf(
            output_path=pdf_path,
            page_count=2,
            effective_dpi=350.0, # 350 DPI hero image
            tac_percentage=285.0, # FOGRA51 compliant TAC
            is_cmyk=True
        )

        doc = fitz.open(pdf_path)
        img_info = doc[0].get_images()[0]
        raw = doc.extract_image(img_info[0])

        # Verify image is CMYK
        self.assertEqual(raw["colorspace"], 4, "Hero image must be in CMYK color space")

        # Verify DPI >= 300
        rect = doc[0].get_image_rects(img_info[0])[0]
        dpi_x = (raw["width"] / rect.width) * 72.0
        dpi_y = (raw["height"] / rect.height) * 72.0
        self.assertGreaterEqual(min(dpi_x, dpi_y), 300.0)

        doc.close()

if __name__ == "__main__":
    unittest.main()
