"""
tests/tier2_boundaries/test_boundary_strokes.py
Feature 3 (Tier 2): Stroke boundaries, sub-0.08mm hairweights, and invalid weights
Authoritative Source: ORIGINAL_REQUEST.md §R4, spec_miner_skills/report.md §4, ISO 128:2020
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.tier1_features.test_vector_downsampling import downsample_stroke

STANDARD_ISO_128_STROKES = {0.13, 0.25, 0.35, 0.50, 0.70}

def validate_stroke_weight(stroke_mm: float, allow_clamped: bool = True) -> list:
    """Validates vector stroke weight against ISO 128 standards and physical print limits."""
    errors = []
    if stroke_mm <= 0.0:
        errors.append(f"Stroke weight must be positive (got {stroke_mm}mm)")
        return errors

    if stroke_mm < 0.08:
        errors.append(f"Stroke weight {stroke_mm}mm is below the 0.08mm minimum print threshold (risk of dropped hairline)")

    if stroke_mm not in STANDARD_ISO_128_STROKES:
        is_close = any(abs(stroke_mm - std) < 0.02 for std in STANDARD_ISO_128_STROKES)
        if not is_close and stroke_mm > 0.08:
            errors.append(f"Non-standard ISO 128 stroke weight: {stroke_mm}mm (expected one of {sorted(list(STANDARD_ISO_128_STROKES))})")

    if stroke_mm > 5.0:
        errors.append(f"Excessive stroke weight {stroke_mm}mm exceeds architectural drafting bounds")

    return errors

class TestBoundaryStrokes(unittest.TestCase):
    """
    Validates boundary conditions on vector lineweights:
    - Sub-0.08mm hairline clamping and error detection
    - Zero and negative stroke weight rejection
    - Non-standard arbitrary weights
    - Extreme stroke weights
    """

    def test_01_sub_008_stroke_flagged(self):
        """Verify 0.05mm hairline stroke triggers minimum print threshold violation."""
        errors = validate_stroke_weight(0.05)
        self.assertTrue(any("below the 0.08mm minimum" in e for e in errors))

    def test_02_ultra_fine_001_hairline_clamped(self):
        """Verify downsample_stroke clamps 0.01mm stroke to 0.08mm print limit."""
        clamped = downsample_stroke(w_native_mm=0.01, scale_factor=1.0, min_clamp_mm=0.08)
        self.assertEqual(clamped, 0.08)

    def test_03_negative_stroke_rejected(self):
        """Verify negative stroke weight (-0.25mm) is rejected with an error."""
        errors = validate_stroke_weight(-0.25)
        self.assertTrue(any("must be positive" in e for e in errors))

    def test_04_zero_stroke_rejected(self):
        """Verify zero stroke weight (0.0mm) is rejected."""
        errors = validate_stroke_weight(0.0)
        self.assertTrue(any("must be positive" in e for e in errors))

    def test_05_non_standard_weight_detected(self):
        """Verify arbitrary non-standard weight (0.42mm) is flagged."""
        errors = validate_stroke_weight(0.42)
        self.assertTrue(any("Non-standard ISO 128" in e for e in errors))

    def test_06_excessive_stroke_weight_rejected(self):
        """Verify stroke weight > 5.0mm (e.g. 10.0mm) is flagged as excessive."""
        errors = validate_stroke_weight(10.0)
        self.assertTrue(any("Excessive stroke" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
