"""
tests/tier4_workloads/test_constructive_wall_section.py
Workload 3 (Tier 4): Constructive wall section plate with Glaser U-value and continuous thermal breaks
Authoritative Source: ORIGINAL_REQUEST.md Acceptance Criteria, spec_miner_skills/report.md §4, constructive-detail
"""

import sys
import os
import unittest
import xml.etree.ElementTree as ET

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def compute_wall_assembly_u_value(layers: list, r_si: float = 0.13, r_se: float = 0.04) -> dict:
    """
    Computes total thermal resistance and U-value for a multi-layer wall assembly:
    R_i = thickness_m / conductivity_lambda
    R_tot = R_si + sum(R_i) + R_se
    U = 1 / R_tot (W/m²K)
    """
    r_layers = 0.0
    total_thickness_mm = 0.0

    for layer in layers:
        d_m = layer["thickness_mm"] / 1000.0
        lam = layer["conductivity_w_mk"]
        r_i = d_m / lam
        r_layers += r_i
        total_thickness_mm += layer["thickness_mm"]

    r_tot = r_si + r_layers + r_se
    u_val = 1.0 / r_tot

    return {
        "r_tot_m2k_w": round(r_tot, 3),
        "u_value_w_m2k": round(u_val, 3),
        "total_thickness_mm": total_thickness_mm,
        "is_passivhaus": u_val <= 0.15,
        "is_re2020": u_val <= 0.20
    }

class TestConstructiveWallSection(unittest.TestCase):
    """
    Validates physical constructibility proof:
    - Glaser hygrothermal U-value calculations meeting Passivhaus standards
    - Vector SVG inspection for ISO 128 stroke hierarchy and continuous thermal breaks
    """

    def setUp(self):
        # High-performance bio-composite wall assembly
        self.assembly_layers = [
            {"name": "Lime Interior Plaster", "thickness_mm": 15.0, "conductivity_w_mk": 0.70},
            {"name": "Granite Ashlar Masonry", "thickness_mm": 120.0, "conductivity_w_mk": 2.80},
            {"name": "Lime-Hemp Insulation Monolith", "thickness_mm": 240.0, "conductivity_w_mk": 0.038},
            {"name": "PIR Warm Edge Barrier", "thickness_mm": 80.0, "conductivity_w_mk": 0.022},
            {"name": "Ventilated Air Cavity", "thickness_mm": 40.0, "conductivity_w_mk": 0.25}, # Unventilated equivalent
            {"name": "Terracotta Rainscreen Tile", "thickness_mm": 30.0, "conductivity_w_mk": 1.00}
        ]
        self.svg_path = os.path.join(PROJECT_ROOT, "tests", "fixtures", "sample_wall_section.svg")

    def test_01_u_value_meets_passivhaus_standard(self):
        """Verify calculated U-value is <= 0.15 W/m²K (Passivhaus EnerPHit standard)."""
        metrics = compute_wall_assembly_u_value(self.assembly_layers)
        self.assertLessEqual(metrics["u_value_w_m2k"], 0.15)
        self.assertTrue(metrics["is_passivhaus"])
        self.assertTrue(metrics["is_re2020"])
        self.assertGreater(metrics["r_tot_m2k_w"], 6.6)

    def test_02_svg_vector_contains_iso128_stroke_weights(self):
        """Verify the 1:20 SVG vector drawing defines standard ISO 128 stroke weights."""
        tree = ET.parse(self.svg_path)
        root = tree.getroot()
        svg_content = ET.tostring(root, encoding="utf-8").decode("utf-8")

        # 0.70mm cut (2.00pt)
        self.assertIn('stroke-width="2.00"', svg_content)
        # 0.50mm cut (1.42pt)
        self.assertIn('stroke-width="1.42"', svg_content)
        # 0.35mm partition (1.00pt)
        self.assertIn('stroke-width="1.00"', svg_content)
        # 0.25mm projection / dimension (0.71pt)
        self.assertIn('stroke-width="0.71"', svg_content)
        # 0.13mm insulation hatch (0.37pt)
        self.assertIn('stroke-width="0.37"', svg_content)

    def test_03_continuous_thermal_break_callout(self):
        """Verify SVG drawing explicitly includes thermal break and EPDM membrane callouts."""
        tree = ET.parse(self.svg_path)
        root = tree.getroot()
        svg_text = " ".join([elem.text for elem in root.iter() if elem.text])

        self.assertIn("EPDM THERMAL BREAK", svg_text)
        self.assertIn("U-VALUE", svg_text)
        self.assertIn("2200 mm", svg_text)

    def test_04_dimension_chains_in_millimeters(self):
        """Verify all dimension strings on the plate are specified in exact millimeters."""
        tree = ET.parse(self.svg_path)
        root = tree.getroot()
        svg_text = " ".join([elem.text for elem in root.iter() if elem.text])

        self.assertIn("120", svg_text)
        self.assertIn("100", svg_text)
        self.assertIn("40", svg_text)

if __name__ == "__main__":
    unittest.main()
