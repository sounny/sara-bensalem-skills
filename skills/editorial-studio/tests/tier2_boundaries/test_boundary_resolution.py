"""
tests/tier2_boundaries/test_boundary_resolution.py
Feature 7 (Tier 2): Effective image resolution boundaries (299 DPI vs 300 DPI, <250 DPI failure)
Authoritative Source: ORIGINAL_REQUEST.md §R5, spec_miner_print_engine/report.md §6.4
"""

import unittest

def evaluate_image_resolution(
    pixel_width: int,
    pixel_height: int,
    box_width_pt: float,
    box_height_pt: float
) -> dict:
    """
    Computes effective DPI: DPI = (pixels / (points / 72.0))
    Returns verdict: PASS (>=300), WARNING (250-299), FAIL (<250)
    """
    if box_width_pt <= 0 or box_height_pt <= 0:
        raise ValueError("Printed bounding box dimensions must be positive")

    dpi_x = (pixel_width * 72.0) / box_width_pt
    dpi_y = (pixel_height * 72.0) / box_height_pt
    effective_dpi = min(dpi_x, dpi_y)

    if effective_dpi >= 300.0:
        status = "PASS"
        severity = "INFO"
        msg = f"Effective resolution {effective_dpi:.1f} DPI meets or exceeds 300 DPI target."
    elif effective_dpi >= 250.0:
        status = "PASS"
        severity = "WARNING"
        msg = f"Effective resolution {effective_dpi:.1f} DPI is below 300 DPI (acceptable for uncoated stock only)."
    else:
        status = "FAIL"
        severity = "ERROR"
        msg = f"Effective resolution {effective_dpi:.1f} DPI is below 250 DPI minimum print threshold."

    return {
        "effective_dpi": round(effective_dpi, 1),
        "dpi_x": round(dpi_x, 1),
        "dpi_y": round(dpi_y, 1),
        "status": status,
        "severity": severity,
        "message": msg
    }

class TestBoundaryResolution(unittest.TestCase):
    """
    Validates effective DPI calculation and boundary classification (299 vs 300 DPI, <250 DPI).
    """

    def test_01_exact_300_dpi_passes_cleanly(self):
        """Verify 300.0 DPI image achieves PASS with no warnings."""
        # Box: 144 pt (2 inches). Pixels: 600 px -> 300 DPI
        res = evaluate_image_resolution(600, 600, 144.0, 144.0)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["severity"], "INFO")
        self.assertEqual(res["effective_dpi"], 300.0)

    def test_02_299_dpi_emits_warning(self):
        """Verify 299.0 DPI image is flagged with WARNING severity."""
        # Box: 144 pt. Pixels: 598 px -> 299.0 DPI
        res = evaluate_image_resolution(598, 598, 144.0, 144.0)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["severity"], "WARNING")
        self.assertEqual(res["effective_dpi"], 299.0)
        self.assertIn("below 300 DPI", res["message"])

    def test_03_249_dpi_fails_preflight(self):
        """Verify 249.0 DPI image fails preflight with ERROR severity (< 250 DPI)."""
        # Box: 144 pt. Pixels: 498 px -> 249.0 DPI
        res = evaluate_image_resolution(498, 498, 144.0, 144.0)
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["severity"], "ERROR")
        self.assertEqual(res["effective_dpi"], 249.0)

    def test_04_asymmetric_scaling_uses_minimum_axis(self):
        """Verify non-uniform image scaling (e.g. 350 DPI horizontal, 240 DPI vertical) evaluates to 240 DPI FAIL."""
        # 700 px on 144 pt (350 DPI), 480 px on 144 pt (240 DPI)
        res = evaluate_image_resolution(700, 480, 144.0, 144.0)
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["effective_dpi"], 240.0)
        self.assertEqual(res["dpi_x"], 350.0)
        self.assertEqual(res["dpi_y"], 240.0)

    def test_05_high_res_1200_dpi_passes(self):
        """Verify ultra high-res 1200 DPI line art scan passes cleanly."""
        res = evaluate_image_resolution(2400, 2400, 144.0, 144.0)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["effective_dpi"], 1200.0)

    def test_06_invalid_zero_box_raises_error(self):
        """Verify zero or negative bounding box dimensions raise ValueError."""
        with self.assertRaises(ValueError):
            evaluate_image_resolution(100, 100, 0.0, 100.0)

if __name__ == "__main__":
    unittest.main()
