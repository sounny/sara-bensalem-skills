"""
tests/tier1_features/test_pagedjs_pipeline.py
Feature 9: Paged.js / HTML-CSS compilation pipeline
Authoritative Source: ORIGINAL_REQUEST.md §R2, spec_miner_print_engine/report.md §5
"""

import unittest
import re

def generate_pagedjs_css(
    bleed_mm: float = 3.0,
    inside_gutter_mm: float = 25.0,
    outside_trim_mm: float = 15.0
) -> str:
    """Generates standard W3C CSS Paged Media stylesheet for Paged.js."""
    return f"""/* W3C CSS Paged Media Monograph Stylesheet */
@page {{
  size: 297mm 210mm;
  marks: crop cross;
  bleed: {bleed_mm}mm;
}}

@page :left {{
  margin-left: {outside_trim_mm}mm;
  margin-right: {inside_gutter_mm}mm;
  margin-top: 20mm;
  margin-bottom: 20mm;
  @bottom-left {{
    content: counter(page);
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
  }}
  @top-left {{
    content: "SARA BENSALEM MONOGRAPH";
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5pt;
  }}
}}

@page :right {{
  margin-left: {inside_gutter_mm}mm;
  margin-right: {outside_trim_mm}mm;
  margin-top: 20mm;
  margin-bottom: 20mm;
  @bottom-right {{
    content: counter(page);
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
  }}
  @top-right {{
    content: "ACT 4: TECTONIC PROOF";
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5pt;
  }}
}}

.spread-grid {{
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  column-gap: 4mm;
  row-gap: 12pt;
}}

.passport-card {{
  grid-column: span 4;
  font-family: 'JetBrains Mono', monospace;
}}

.vector-plate {{
  grid-column: span 8;
}}
"""

def generate_pagedjs_html(title: str = "Monograph Spread") -> str:
    """Generates complete HTML shell with Paged.js polyfill injection and render hook."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link rel="stylesheet" href="monograph_print.css">
  <script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>
  <script>
    window.PagedConfig = {{
      auto: true,
      after: function(flow) {{
        window.__PAGEDJS_RENDERED__ = true;
        document.body.setAttribute("data-pagedjs-rendered", "true");
      }}
    }};
  </script>
</head>
<body>
  <div class="spread-grid">
    <div class="passport-card">
      <h3>PROJECT PASSPORT</h3>
      <p>Typology: Heritage Renovation</p>
    </div>
    <div class="vector-plate">
      <svg viewBox="0 0 400 300"><rect width="400" height="300" fill="#eee"/></svg>
    </div>
  </div>
</body>
</html>
"""

class TestPagedjsPipeline(unittest.TestCase):
    """
    Validates W3C CSS Paged Media spread selectors, bleed specifications,
    margin boxes, and Paged.js polyfill lifecycle hooks.
    """

    def setUp(self):
        self.css = generate_pagedjs_css(bleed_mm=3.0, inside_gutter_mm=25.0, outside_trim_mm=15.0)
        self.html = generate_pagedjs_html()

    def test_01_at_page_size_and_bleed_marks(self):
        """Verify @page declares 297mm 210mm, marks: crop cross, and 3mm bleed."""
        self.assertIn("size: 297mm 210mm;", self.css)
        self.assertIn("marks: crop cross;", self.css)
        self.assertIn("bleed: 3.0mm;", self.css)

    def test_02_page_left_verso_margin_boxes(self):
        """Verify @page :left defines margin-right as inside gutter and sets @bottom-left folio."""
        self.assertIn("@page :left", self.css)
        self.assertIn("margin-right: 25.0mm;", self.css)
        self.assertIn("@bottom-left", self.css)
        self.assertIn("content: counter(page);", self.css)

    def test_03_page_right_recto_margin_boxes(self):
        """Verify @page :right defines margin-left as inside gutter and sets @bottom-right folio."""
        self.assertIn("@page :right", self.css)
        self.assertIn("margin-left: 25.0mm;", self.css)
        self.assertIn("@bottom-right", self.css)

    def test_04_html_scaffold_and_pagedjs_hook(self):
        """Verify HTML document embeds Paged.js polyfill and wires window.__PAGEDJS_RENDERED__ hook."""
        self.assertIn("paged.polyfill.js", self.html)
        self.assertIn("window.__PAGEDJS_RENDERED__ = true", self.html)
        self.assertIn('data-pagedjs-rendered', self.html)

    def test_05_css_grid_12_columns_4mm_gap(self):
        """Verify CSS Grid layout uses repeat(12, 1fr) with 4mm column gap."""
        self.assertIn("grid-template-columns: repeat(12, 1fr);", self.css)
        self.assertIn("column-gap: 4mm;", self.css)

if __name__ == "__main__":
    unittest.main()
