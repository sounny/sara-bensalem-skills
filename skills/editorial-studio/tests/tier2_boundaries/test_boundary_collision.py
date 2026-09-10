"""
tests/tier2_boundaries/test_boundary_collision.py
Feature 8 (Tier 2): Vision-in-the-loop bounding-box collision detection & contrast analysis
Authoritative Source: ORIGINAL_REQUEST.md §R5, spec_miner_print_engine/report.md §6.7
"""

import unittest

def check_aabb_intersection(box_a: list, box_b: list) -> bool:
    """Checks Axis-Aligned Bounding Box (AABB) intersection: [x0, y0, x1, y1]."""
    return (
        box_a[0] < box_b[2] and
        box_a[2] > box_b[0] and
        box_a[1] < box_b[3] and
        box_a[3] > box_b[1]
    )

def compute_contrast_ratio(lum_text: float, lum_bg: float) -> float:
    """Calculates WCAG/Print relative luminance contrast ratio: (L1 + 0.05) / (L2 + 0.05)."""
    l1 = max(lum_text, lum_bg)
    l2 = min(lum_text, lum_bg)
    return round((l1 + 0.05) / (l2 + 0.05), 2)

def evaluate_text_image_collision(text_box: list, image_box: list, text_lum: float, bg_lum: float) -> dict:
    """Evaluates potential text-image collision; if colliding, verifies contrast ratio >= 4.5:1."""
    intersects = check_aabb_intersection(text_box, image_box)
    if not intersects:
        return {"collides": False, "status": "PASS", "contrast_ratio": None, "reason": "NO_COLLISION"}

    contrast = compute_contrast_ratio(text_lum, bg_lum)
    if contrast >= 4.5:
        return {
            "collides": True,
            "status": "PASS",
            "contrast_ratio": contrast,
            "reason": "INTENTIONAL_LEGIBLE_OVERLAY"
        }
    else:
        return {
            "collides": True,
            "status": "FAIL",
            "contrast_ratio": contrast,
            "reason": "ILLEGIBLE_COLLISION_LOW_CONTRAST"
        }

class TestBoundaryCollision(unittest.TestCase):
    """
    Validates AABB collision detection, contrast evaluation, and visual linting rules.
    """

    def test_01_disjoint_boxes_no_collision(self):
        """Verify non-overlapping text and image boxes report no collision and PASS."""
        text_box = [50, 50, 150, 80]
        img_box = [200, 50, 400, 300]
        res = evaluate_text_image_collision(text_box, img_box, text_lum=0.0, bg_lum=0.8)
        self.assertFalse(res["collides"])
        self.assertEqual(res["status"], "PASS")

    def test_02_overlapping_boxes_low_contrast_fails(self):
        """Verify text overlapping an image with low contrast (e.g. 1.8:1) fails visual lint."""
        text_box = [100, 100, 250, 140]
        img_box = [50, 50, 300, 300] # Intersects text_box
        # Grey text on dark grey background
        res = evaluate_text_image_collision(text_box, img_box, text_lum=0.3, bg_lum=0.2)
        self.assertTrue(res["collides"])
        self.assertEqual(res["status"], "FAIL")
        self.assertLess(res["contrast_ratio"], 4.5)
        self.assertEqual(res["reason"], "ILLEGIBLE_COLLISION_LOW_CONTRAST")

    def test_03_overlapping_boxes_high_contrast_caption_passes(self):
        """Verify intentional white caption text over a dark atmospheric image (contrast >= 4.5) passes."""
        text_box = [80, 200, 220, 240]
        img_box = [50, 50, 400, 400]
        # White text (lum=1.0) on dark shadow (lum=0.05) -> contrast ~ 10.5:1
        res = evaluate_text_image_collision(text_box, img_box, text_lum=1.0, bg_lum=0.05)
        self.assertTrue(res["collides"])
        self.assertEqual(res["status"], "PASS")
        self.assertGreaterEqual(res["contrast_ratio"], 4.5)
        self.assertEqual(res["reason"], "INTENTIONAL_LEGIBLE_OVERLAY")

    def test_04_touching_edges_no_intersection(self):
        """Verify boxes that touch at the exact boundary line (x1 == x0) do not intersect."""
        box_a = [0, 0, 100, 100]
        box_b = [100, 0, 200, 100]
        self.assertFalse(check_aabb_intersection(box_a, box_b))

    def test_05_contained_box_intersection(self):
        """Verify text box completely enclosed inside image box detects intersection."""
        img_box = [0, 0, 500, 500]
        text_box = [100, 100, 200, 150]
        self.assertTrue(check_aabb_intersection(text_box, img_box))

    def test_06_contrast_ratio_formula_symmetry(self):
        """Verify contrast ratio computes identically regardless of text vs bg order."""
        c1 = compute_contrast_ratio(0.8, 0.1)
        c2 = compute_contrast_ratio(0.1, 0.8)
        self.assertEqual(c1, c2)

if __name__ == "__main__":
    unittest.main()
