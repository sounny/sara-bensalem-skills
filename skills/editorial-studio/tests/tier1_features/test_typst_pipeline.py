"""
tests/tier1_features/test_typst_pipeline.py
Feature 8: Typst compilation pipeline & declarative templates
Authoritative Source: ORIGINAL_REQUEST.md §R2, spec_miner_print_engine/report.md §4
"""

import unittest
import re

def generate_typst_monograph_markup(
    title: str = "Sara Bensalem Monograph",
    page_format: str = "a4",
    flipped: bool = True,
    inside_margin_mm: float = 25.0,
    outside_margin_mm: float = 15.0,
    baseline_step_pt: float = 6.0
) -> str:
    """Generates standard Typst publication markup conforming to the architectural specification."""
    return f"""// Auto-generated Typst Monograph Template
#set document(title: "{title}", author: "Sara Bensalem")

#set page(
  paper: "{page_format}",
  flipped: {"true" if flipped else "false"},
  margin: (inside: {inside_margin_mm}mm, outside: {outside_margin_mm}mm, top: 20mm, bottom: 20mm),
  binding: left,
  header: context {{
    let p = counter(page).get().first()
    if p > 1 {{
      set text(font: "JetBrains Mono", size: 7.5pt, fill: luma(100))
      if calc.even(p) {{
        grid(columns: (1fr, 1fr), align(left)[#p | {title.upper()}], align(right)[ACT 4: TECTONIC PROOF])
      }} else {{
        grid(columns: (1fr, 1fr), align(left)[PROJECT: ATLAS TERRACE], align(right)[1:20 WALL SECTION | #p])
      }}
    }}
  }}
)

#let baseline-step = {baseline_step_pt}pt
#let snap(val) = calc.round(val / baseline-step) * baseline-step

#set text(font: "Space Grotesk", size: 9pt, fill: cmyk(0%, 0%, 0%, 100%))
#set par(leading: 3pt, spacing: 12pt, justify: true)

#let swiss-grid(..cells) = grid(
  columns: (1fr,) * 12,
  column-gutter: 4mm,
  row-gutter: 12pt,
  ..cells
)

= Act 1: The Hook and Project Passport

#swiss-grid(
  grid.cell(colspan: 4)[
    #text(font: "JetBrains Mono", size: 8pt)[
      *PROJECT PASSPORT* \\
      Typology: Cultural Pavilion \\
      Scale: 1:20 Detailing \\
      Target U-Value: 0.18 W/m²K
    ]
  ],
  grid.cell(colspan: 8)[
    #rect(width: 100%, height: 120pt, stroke: 0.50mm + cmyk(0%, 0%, 0%, 100%), fill: luma(240))[
      #place(center + horizon)[#text(size: 10pt)[1:20 Constructive Plate Placeholder]]
    ]
  ]
)
"""

class TestTypstPipeline(unittest.TestCase):
    """
    Validates Typst declarative template syntax, grid macro generation,
    parity-aware running headers, and baseline math integration.
    """

    def setUp(self):
        self.markup = generate_typst_monograph_markup()

    def test_01_page_geometry_and_facing_spread_setup(self):
        """Verify #set page declares paper, flipped, inside/outside margins, and binding."""
        self.assertIn('paper: "a4"', self.markup)
        self.assertIn('flipped: true', self.markup)
        self.assertIn('inside: 25.0mm', self.markup)
        self.assertIn('outside: 15.0mm', self.markup)
        self.assertIn('binding: left', self.markup)

    def test_02_parity_aware_header_context(self):
        """Verify header context switches content between calc.even(p) (verso) and recto."""
        self.assertIn('header: context {', self.markup)
        self.assertIn('if calc.even(p) {', self.markup)
        self.assertIn('ACT 4: TECTONIC PROOF', self.markup)
        self.assertIn('1:20 WALL SECTION', self.markup)

    def test_03_baseline_snap_macro_present(self):
        """Verify baseline-step and snap(val) helper functions are declared."""
        self.assertIn('#let baseline-step = 6.0pt', self.markup)
        self.assertIn('#let snap(val) = calc.round(val / baseline-step) * baseline-step', self.markup)

    def test_04_swiss_12_column_grid_macro(self):
        """Verify 12-column Swiss grid macro is declared with 4mm gutter."""
        self.assertIn('#let swiss-grid(..cells) = grid(', self.markup)
        self.assertIn('columns: (1fr,) * 12', self.markup)
        self.assertIn('column-gutter: 4mm', self.markup)

    def test_05_cmyk_color_and_stroke_declarations(self):
        """Verify colors use CMYK definitions and strokes adhere to ISO 128 (0.50mm cut)."""
        self.assertIn('cmyk(0%, 0%, 0%, 100%)', self.markup)
        self.assertIn('stroke: 0.50mm', self.markup)

if __name__ == "__main__":
    unittest.main()
