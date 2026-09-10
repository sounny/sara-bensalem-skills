"""
tests/tier3_combinations/test_cross_engine_parity.py
Combination 5: Cross-engine layout and margin parity between Typst and Paged.js
Authoritative Source: ORIGINAL_REQUEST.md §R2, spec_miner_print_engine/report.md §8
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.tier1_features.test_typst_pipeline import generate_typst_monograph_markup
from tests.tier1_features.test_pagedjs_pipeline import generate_pagedjs_css

class TestCrossEngineParity(unittest.TestCase):
    """
    Validates geometrical and typographic parity between the Typst engine
    and the Paged.js / HTML-CSS engine.
    """

    def setUp(self):
        self.typst_code = generate_typst_monograph_markup(inside_margin_mm=25.0, outside_margin_mm=15.0)
        self.pagedjs_css = generate_pagedjs_css(bleed_mm=3.0, inside_gutter_mm=25.0, outside_trim_mm=15.0)

    def test_01_page_dimension_parity(self):
        """Verify both engines target identical A4 Landscape sheet dimensions (297mm x 210mm)."""
        # Typst: paper: "a4", flipped: true -> 297mm x 210mm
        self.assertIn('paper: "a4"', self.typst_code)
        self.assertIn('flipped: true', self.typst_code)

        # Paged.js: size: 297mm 210mm;
        self.assertIn('size: 297mm 210mm;', self.pagedjs_css)

    def test_02_margin_gutter_parity(self):
        """Verify both engines specify 25mm inside spine gutter and 15mm outside trim margin."""
        # Typst: margin: (inside: 25.0mm, outside: 15.0mm, ...)
        self.assertIn('inside: 25.0mm', self.typst_code)
        self.assertIn('outside: 15.0mm', self.typst_code)

        # Paged.js: :left has margin-right: 25.0mm; :right has margin-left: 25.0mm;
        self.assertIn('margin-right: 25.0mm;', self.pagedjs_css)
        self.assertIn('margin-left: 25.0mm;', self.pagedjs_css)
        self.assertIn('margin-left: 15.0mm;', self.pagedjs_css)
        self.assertIn('margin-right: 15.0mm;', self.pagedjs_css)

    def test_03_grid_column_and_gutter_parity(self):
        """Verify both engines specify exactly 12 columns with 4mm gutters."""
        # Typst: columns: (1fr,) * 12, column-gutter: 4mm
        self.assertIn('columns: (1fr,) * 12', self.typst_code)
        self.assertIn('column-gutter: 4mm', self.typst_code)

        # Paged.js: grid-template-columns: repeat(12, 1fr); column-gap: 4mm;
        self.assertIn('grid-template-columns: repeat(12, 1fr);', self.pagedjs_css)
        self.assertIn('column-gap: 4mm;', self.pagedjs_css)

    def test_04_baseline_step_parity(self):
        """Verify both engines define line heights aligned to 6pt / 12pt baseline increments."""
        # Typst: baseline-step = 6.0pt, leading: 3pt (9pt font + 3pt = 12pt line pitch)
        self.assertIn('baseline-step = 6.0pt', self.typst_code)
        self.assertIn('leading: 3pt', self.typst_code)

        # Paged.js: font-size: 9pt; line-height: 12pt; row-gap: 12pt;
        self.assertIn('row-gap: 12pt;', self.pagedjs_css)

if __name__ == "__main__":
    unittest.main()
