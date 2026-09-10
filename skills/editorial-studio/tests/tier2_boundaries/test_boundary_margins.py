"""
tests/tier2_boundaries/test_boundary_margins.py
Feature 2 (Tier 2): Margin boundaries, negative values, and page dimension overflow
Authoritative Source: ORIGINAL_REQUEST.md §R3, spec_miner_skills/report.md §3, spec_miner_print_engine/report.md §6.2
"""

import unittest

def validate_spread_margins(
    page_width_mm: float,
    page_height_mm: float,
    inner_margin_mm: float,
    outer_margin_mm: float,
    top_margin_mm: float,
    bottom_margin_mm: float,
    min_safe_zone_mm: float = 5.0
) -> list:
    """Validates margin parameters against page boundaries and safety constraints."""
    errors = []

    # Non-negative checks
    for name, val in [
        ("inner_margin", inner_margin_mm),
        ("outer_margin", outer_margin_mm),
        ("top_margin", top_margin_mm),
        ("bottom_margin", bottom_margin_mm)
    ]:
        if val < 0.0:
            errors.append(f"{name} cannot be negative (got {val}mm)")

    # Page dimension overflow checks
    horizontal_margins = inner_margin_mm + outer_margin_mm
    vertical_margins = top_margin_mm + bottom_margin_mm

    if horizontal_margins >= page_width_mm:
        errors.append(f"Combined horizontal margins ({horizontal_margins}mm) exceed page width ({page_width_mm}mm)")

    if vertical_margins >= page_height_mm:
        errors.append(f"Combined vertical margins ({vertical_margins}mm) exceed page height ({page_height_mm}mm)")

    # Safety zone breach
    if 0.0 < outer_margin_mm < min_safe_zone_mm:
        errors.append(f"outer_margin ({outer_margin_mm}mm) breaches {min_safe_zone_mm}mm safety zone")

    if inner_margin_mm == 0.0:
        errors.append("inner_margin cannot be 0.0mm: binding crease requires non-zero gutter")

    return errors

class TestBoundaryMargins(unittest.TestCase):
    """
    Validates boundary margin conditions, zero/negative rejection, and page overflow limits.
    """

    def setUp(self):
        self.a4_w = 297.0 # Landscape width in mm
        self.a4_h = 210.0 # Landscape height in mm

    def test_01_negative_inner_margin_rejected(self):
        """Verify negative inner margin is flagged with validation error."""
        errors = validate_spread_margins(self.a4_w, self.a4_h, inner_margin_mm=-5.0, outer_margin_mm=15.0, top_margin_mm=15.0, bottom_margin_mm=15.0)
        self.assertTrue(any("negative" in e for e in errors))

    def test_02_negative_outer_margin_rejected(self):
        """Verify negative outer margin is flagged with validation error."""
        errors = validate_spread_margins(self.a4_w, self.a4_h, inner_margin_mm=20.0, outer_margin_mm=-2.0, top_margin_mm=15.0, bottom_margin_mm=15.0)
        self.assertTrue(any("negative" in e for e in errors))

    def test_03_zero_inner_margin_rejected(self):
        """Verify 0.0mm inner margin is rejected due to binding crease requirement."""
        errors = validate_spread_margins(self.a4_w, self.a4_h, inner_margin_mm=0.0, outer_margin_mm=15.0, top_margin_mm=15.0, bottom_margin_mm=15.0)
        self.assertTrue(any("0.0mm" in e for e in errors))

    def test_04_margins_exceeding_page_width(self):
        """Verify margins totaling >= page width are rejected as overflow."""
        # 160mm inner + 150mm outer = 310mm > 297mm
        errors = validate_spread_margins(self.a4_w, self.a4_h, inner_margin_mm=160.0, outer_margin_mm=150.0, top_margin_mm=15.0, bottom_margin_mm=15.0)
        self.assertTrue(any("exceed page width" in e for e in errors))

    def test_05_margins_exceeding_page_height(self):
        """Verify vertical margins totaling >= page height are rejected."""
        # 120mm top + 100mm bottom = 220mm > 210mm
        errors = validate_spread_margins(self.a4_w, self.a4_h, inner_margin_mm=20.0, outer_margin_mm=15.0, top_margin_mm=120.0, bottom_margin_mm=100.0)
        self.assertTrue(any("exceed page height" in e for e in errors))

    def test_06_outer_margin_breaching_safety_zone(self):
        """Verify outer margin < 5mm is flagged as a safety zone breach."""
        errors = validate_spread_margins(self.a4_w, self.a4_h, inner_margin_mm=20.0, outer_margin_mm=3.0, top_margin_mm=15.0, bottom_margin_mm=15.0)
        self.assertTrue(any("breaches" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
