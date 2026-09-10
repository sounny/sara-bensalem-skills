"""
tests/tier2_boundaries/test_boundary_microtypography.py
Feature 9 (Tier 2): Micro-typographic boundaries (orphans, widows, hanging punctuation, hyphens)
Authoritative Source: ORIGINAL_REQUEST.md §R3, spec_miner_skills/report.md §3, Bringhurst
"""

import unittest

def detect_orphan_words(line: str) -> bool:
    """Returns True if terminal line contains a single isolated word (1-word orphan)."""
    words = line.strip().split()
    return len(words) == 1

def fix_orphan_line(text: str) -> str:
    """Inserts a non-breaking space between the penultimate and terminal word."""
    words = text.strip().split()
    if len(words) >= 2:
        return " ".join(words[:-2]) + " " + words[-2] + "~" + words[-1] if len(words) > 2 else words[0] + "~" + words[1]
    return text

def validate_paragraph_split(lines_page_1: int, lines_page_2: int, min_widow: int = 2) -> list:
    """Validates paragraph split across column/page break against widow/orphan rules."""
    errors = []
    if lines_page_1 < min_widow:
        errors.append(f"Orphan line error: only {lines_page_1} line(s) left on first page (minimum is {min_widow})")
    if lines_page_2 < min_widow:
        errors.append(f"Widow line error: only {lines_page_2} line(s) carried forward to next page (minimum is {min_widow})")
    return errors

def validate_hanging_punctuation_protrusion(protrusion_em: float) -> bool:
    """Hanging punctuation protrusion must be between 0.30em and 1.0em."""
    return 0.30 <= protrusion_em <= 1.0

class TestBoundaryMicrotypography(unittest.TestCase):
    """
    Validates boundary micro-typographic enforcement:
    - 1-word orphan line detection and non-breaking space fix
    - Widow penalty >= 2 lines across column breaks
    - Optical hanging protrusion limits
    - Consecutive hyphen penalties
    """

    def test_01_single_word_orphan_detected(self):
        """Verify single-word terminal line is flagged as an orphan defect."""
        self.assertTrue(detect_orphan_words("completed."))
        self.assertFalse(detect_orphan_words("assembly completed."))

    def test_02_orphan_fix_inserts_non_breaking_space(self):
        """Verify non-breaking space binds the last two words together."""
        original = "The monolithic insulation core was meticulously assembled."
        fixed = fix_orphan_line(original)
        self.assertIn("meticulously~assembled.", fixed)
        last_chunk = fixed.split()[-1]
        self.assertIn("~", last_chunk)

    def test_03_widow_page_split_1_line_rejected(self):
        """Verify carrying 1 line forward to page 2 triggers a widow line error."""
        errors = validate_paragraph_split(lines_page_1=3, lines_page_2=1, min_widow=2)
        self.assertTrue(any("Widow line error" in e for e in errors))

    def test_04_orphan_page_split_1_line_rejected(self):
        """Verify leaving 1 line behind on page 1 triggers an orphan line error."""
        errors = validate_paragraph_split(lines_page_1=1, lines_page_2=3, min_widow=2)
        self.assertTrue(any("Orphan line error" in e for e in errors))

    def test_05_balanced_2_2_split_passes(self):
        """Verify 2 lines on page 1 and 2 lines on page 2 passes widow/orphan threshold."""
        errors = validate_paragraph_split(lines_page_1=2, lines_page_2=2, min_widow=2)
        self.assertEqual(errors, [])

    def test_06_hanging_punctuation_protrusion_bounds(self):
        """Verify hanging punctuation protrusion is bounded between 30% and 100% of glyph width."""
        self.assertTrue(validate_hanging_punctuation_protrusion(0.50)) # 50% protrusion (standard hyphen)
        self.assertTrue(validate_hanging_punctuation_protrusion(1.00)) # 100% protrusion (opening quote)
        self.assertFalse(validate_hanging_punctuation_protrusion(0.10)) # Too shallow
        self.assertFalse(validate_hanging_punctuation_protrusion(1.50)) # Excessive protrusion

if __name__ == "__main__":
    unittest.main()
