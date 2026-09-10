"""
tests/tier2_boundaries/test_boundary_color_tac.py
Feature 5 (Tier 2): Color spaces, untagged RGB, and TAC exceeding 320% limits
Authoritative Source: ORIGINAL_REQUEST.md §R5, spec_miner_print_engine/report.md §6.5
"""

import unittest
import os
import io
import tempfile
import fitz
import numpy as np
from PIL import Image

def calculate_tac_for_image_bytes(cmyk_bytes: bytes, max_tac_allowed: float = 320.0) -> dict:
    """Calculates pixel-wise TAC on CMYK image bytes and checks against threshold."""
    pil_img = Image.open(io.BytesIO(cmyk_bytes))
    if pil_img.mode != "CMYK":
        return {"colorspace": pil_img.mode, "status": "FAIL", "reason": "UNTAGGED_RGB_OR_NON_CMYK", "peak_tac": 0.0}

    arr = np.array(pil_img, dtype=np.float32)
    # arr shape: (H, W, 4)
    tac_map = (arr[:, :, 0] + arr[:, :, 1] + arr[:, :, 2] + arr[:, :, 3]) / 255.0 * 100.0
    peak_tac = float(np.max(tac_map))
    viol_count = int(np.sum(tac_map > max_tac_allowed))

    return {
        "colorspace": "CMYK",
        "peak_tac": round(peak_tac, 2),
        "violations": viol_count,
        "status": "FAIL" if peak_tac > max_tac_allowed else "PASS"
    }

class TestBoundaryColorTAC(unittest.TestCase):
    """
    Validates ink limits, untagged RGB detection, and TAC boundary triggers.
    """

    def test_01_rgb_colorspace_detected_and_flagged(self):
        """Verify non-CMYK RGB image is flagged for print compliance."""
        rgb_arr = np.full((50, 50, 3), 128, dtype=np.uint8)
        buf = io.BytesIO()
        Image.fromarray(rgb_arr, mode="RGB").save(buf, format="JPEG")
        res = calculate_tac_for_image_bytes(buf.getvalue(), max_tac_allowed=320.0)
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["reason"], "UNTAGGED_RGB_OR_NON_CMYK")

    def test_02_tac_exceeding_320_fails(self):
        """Verify TAC of 350% (uncontrolled rich black) triggers preflight failure."""
        # 350% TAC: channel values ~ 223 each
        val = int(round((350.0 / 400.0) * 255.0)) # 223
        cmyk_arr = np.full((20, 20, 4), val, dtype=np.uint8)
        buf = io.BytesIO()
        Image.fromarray(cmyk_arr, mode="CMYK").save(buf, format="TIFF")
        res = calculate_tac_for_image_bytes(buf.getvalue(), max_tac_allowed=320.0)
        self.assertEqual(res["status"], "FAIL")
        self.assertGreater(res["peak_tac"], 320.0)
        self.assertEqual(res["violations"], 400) # All 20x20 pixels violate

    def test_03_tac_at_280_passes(self):
        """Verify FOGRA51 standard coated TAC (280%) passes cleanly."""
        val = int(round((280.0 / 400.0) * 255.0))
        cmyk_arr = np.full((20, 20, 4), val, dtype=np.uint8)
        buf = io.BytesIO()
        Image.fromarray(cmyk_arr, mode="CMYK").save(buf, format="TIFF")
        res = calculate_tac_for_image_bytes(buf.getvalue(), max_tac_allowed=320.0)
        self.assertEqual(res["status"], "PASS")
        self.assertLessEqual(res["peak_tac"], 320.0)
        self.assertEqual(res["violations"], 0)

    def test_04_tac_boundary_exact_320(self):
        """Verify TAC exactly at 320.0% passes while 320.5% fails."""
        # 320% TAC: (4 * 204) / 255 * 100 = 320.0%
        val_320 = 204
        cmyk_arr = np.full((10, 10, 4), val_320, dtype=np.uint8)
        buf = io.BytesIO()
        Image.fromarray(cmyk_arr, mode="CMYK").save(buf, format="TIFF")
        res = calculate_tac_for_image_bytes(buf.getvalue(), max_tac_allowed=320.0)
        self.assertEqual(res["status"], "PASS")

        # 321.5% TAC: val = 205
        cmyk_arr_high = np.full((10, 10, 4), 205, dtype=np.uint8)
        buf_high = io.BytesIO()
        Image.fromarray(cmyk_arr_high, mode="CMYK").save(buf_high, format="TIFF")
        res_high = calculate_tac_for_image_bytes(buf_high.getvalue(), max_tac_allowed=320.0)
        self.assertEqual(res_high["status"], "FAIL")

    def test_05_extreme_400_percent_tac_stress(self):
        """Verify 100% C, 100% M, 100% Y, 100% K (400% TAC) is caught with maximum violations."""
        cmyk_arr = np.full((10, 10, 4), 255, dtype=np.uint8)
        buf = io.BytesIO()
        Image.fromarray(cmyk_arr, mode="CMYK").save(buf, format="TIFF")
        res = calculate_tac_for_image_bytes(buf.getvalue(), max_tac_allowed=320.0)
        self.assertEqual(res["status"], "FAIL")
        self.assertAlmostEqual(res["peak_tac"], 400.0, places=1)
        self.assertEqual(res["violations"], 100)

    def test_06_blank_zero_ink_plate_handled(self):
        """Verify 0% ink (white background) calculates 0.0% TAC without error."""
        cmyk_arr = np.zeros((10, 10, 4), dtype=np.uint8)
        buf = io.BytesIO()
        Image.fromarray(cmyk_arr, mode="CMYK").save(buf, format="TIFF")
        res = calculate_tac_for_image_bytes(buf.getvalue(), max_tac_allowed=320.0)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["peak_tac"], 0.0)

if __name__ == "__main__":
    unittest.main()
