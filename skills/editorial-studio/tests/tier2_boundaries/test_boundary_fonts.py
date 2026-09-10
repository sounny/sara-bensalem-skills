"""
tests/tier2_boundaries/test_boundary_fonts.py
Feature 6 (Tier 2): Font embedding, missing glyph subsets, and Type 3 font prohibition
Authoritative Source: ORIGINAL_REQUEST.md §R5, spec_miner_print_engine/report.md §6.3, ISO 32000-1
"""

import unittest
import re

SUBSET_REGEX = re.compile(r"^[A-Z]{6}\+")

def audit_font_record(
    font_name: str,
    font_type: str,
    is_embedded: bool,
    missing_glyphs_count: int = 0
) -> dict:
    """Validates an extracted PDF font entry against preflight print rules."""
    errors = []
    warnings = []

    if not is_embedded:
        errors.append(f"Font '{font_name}' is NOT embedded (violates 100% embedding mandate)")

    if font_type.lower() == "type3":
        errors.append(f"Font '{font_name}' is Type 3 (forbidden in print production)")

    is_subsetted = bool(SUBSET_REGEX.match(font_name))
    if not is_subsetted and is_embedded:
        warnings.append(f"Font '{font_name}' is fully embedded but not subsetted (missing 6-char tag prefix)")

    if missing_glyphs_count > 0:
        errors.append(f"Font '{font_name}' contains {missing_glyphs_count} missing or undefined glyphs (.notdef)")

    return {
        "font_name": font_name,
        "is_embedded": is_embedded,
        "is_subsetted": is_subsetted,
        "is_type3": font_type.lower() == "type3",
        "errors": errors,
        "warnings": warnings,
        "status": "PASS" if len(errors) == 0 else "FAIL"
    }

class TestBoundaryFonts(unittest.TestCase):
    """
    Validates font embedding, subset naming regex, Type 3 rejection, and missing glyph detection.
    """

    def test_01_unembedded_font_fails(self):
        """Verify un-embedded system font triggers preflight failure."""
        res = audit_font_record(
            font_name="Helvetica",
            font_type="TrueType",
            is_embedded=False
        )
        self.assertEqual(res["status"], "FAIL")
        self.assertTrue(any("NOT embedded" in e for e in res["errors"]))

    def test_02_type3_font_rejected(self):
        """Verify Type 3 font is rejected even if embedded."""
        res = audit_font_record(
            font_name="ABCDEF+Type3IconFont",
            font_type="Type3",
            is_embedded=True
        )
        self.assertEqual(res["status"], "FAIL")
        self.assertTrue(any("Type 3" in e for e in res["errors"]))

    def test_03_compliant_subsetted_font_passes(self):
        """Verify compliant subsetted OpenType font with 6-char prefix passes."""
        res = audit_font_record(
            font_name="GHKLMN+SpaceGrotesk-Bold",
            font_type="Type1",
            is_embedded=True
        )
        self.assertEqual(res["status"], "PASS")
        self.assertTrue(res["is_subsetted"])
        self.assertEqual(len(res["errors"]), 0)

    def test_04_non_subsetted_font_warns(self):
        """Verify fully embedded font missing subset prefix emits a warning."""
        res = audit_font_record(
            font_name="Inter-Regular",
            font_type="TrueType",
            is_embedded=True
        )
        self.assertEqual(res["status"], "PASS")
        self.assertFalse(res["is_subsetted"])
        self.assertTrue(any("not subsetted" in w for w in res["warnings"]))

    def test_05_missing_glyphs_rejected(self):
        """Verify font with undefined .notdef glyphs triggers error."""
        res = audit_font_record(
            font_name="ABCDEF+GaramondPro",
            font_type="CFF",
            is_embedded=True,
            missing_glyphs_count=3
        )
        self.assertEqual(res["status"], "FAIL")
        self.assertTrue(any("missing or undefined glyphs" in e for e in res["errors"]))

    def test_06_subset_regex_validation(self):
        """Verify strict adherence to ISO 32000-1 6-uppercase-letter subset tag."""
        valid_tags = ["ABCDEF+Font", "ZZZZZZ+MyFont", "QWERTY+Mono"]
        invalid_tags = ["abc123+Font", "123456+Font", "ABCDE+Font", "ABCDEFG+Font", "Font"]
        for tag in valid_tags:
            self.assertTrue(bool(SUBSET_REGEX.match(tag)), f"Tag {tag} should match")
        for tag in invalid_tags:
            self.assertFalse(bool(SUBSET_REGEX.match(tag)), f"Tag {tag} should NOT match")

if __name__ == "__main__":
    unittest.main()
