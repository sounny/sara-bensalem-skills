"""
tests/tier1_features/test_iso128_strokes.py
Feature 5: ISO 128 calibrated stroke hierarchies
Authoritative Source: ORIGINAL_REQUEST.md §R4, spec_miner_skills/report.md §4
"""

import unittest

class TestISO128StrokeHierarchy(unittest.TestCase):
    """
    Validates metric stroke weight groups, point conversions, and architectural
    drafting roles according to ISO 128:2020.
    """

    def setUp(self):
        # 1 mm = 72 / 25.4 pt = 2.83464567 pt
        self.mm_to_pt = 72.0 / 25.4

        self.stroke_standards = {
            "ground_cut": {
                "metric_mm": 0.70,
                "hex_color": "#111110",
                "role": "Ground/Bedrock, Primary Mass Cut",
                "dash_array": None
            },
            "primary_structure": {
                "metric_mm": 0.50,
                "hex_color": "#111110",
                "role": "Structural Slabs, Columns, Shear Walls",
                "dash_array": None
            },
            "secondary_partitions": {
                "metric_mm": 0.35,
                "hex_color": "#33322E",
                "role": "Partitions, Joinery Carcase",
                "dash_array": None
            },
            "visible_projections": {
                "metric_mm": 0.25,
                "hex_color": "#55544E",
                "role": "Uncut Edges, Dimension Chains, Door Swings",
                "dash_array": None
            },
            "hatch_insulation": {
                "metric_mm": 0.13,
                "hex_color": "#84827A",
                "role": "Hatching, Insulation Batts, Background Grids",
                "dash_array": None
            },
            "epdm_membrane": {
                "metric_mm": 0.25,
                "hex_color": "#111110",
                "role": "EPDM Waterproofing, Vapour Retarder",
                "dash_array": "3,1"
            },
            "pmr_egress_path": {
                "metric_mm": 0.35,
                "hex_color": "#8B263E",
                "role": "PMR Accessibility Turning Circle, Egress Vector",
                "dash_array": "1,2"
            }
        }

    def test_01_ground_cut_stroke_conversion(self):
        """Verify 0.70mm cut stroke converts precisely to ~1.98-2.00 pt."""
        pt = self.stroke_standards["ground_cut"]["metric_mm"] * self.mm_to_pt
        self.assertAlmostEqual(pt, 1.984, places=2)
        self.assertEqual(self.stroke_standards["ground_cut"]["hex_color"], "#111110")

    def test_02_primary_structure_stroke_conversion(self):
        """Verify 0.50mm cut stroke converts to ~1.42 pt."""
        pt = self.stroke_standards["primary_structure"]["metric_mm"] * self.mm_to_pt
        self.assertAlmostEqual(pt, 1.417, places=2)
        self.assertEqual(self.stroke_standards["primary_structure"]["hex_color"], "#111110")

    def test_03_secondary_partitions_stroke_conversion(self):
        """Verify 0.35mm partition stroke converts to ~0.99-1.00 pt."""
        pt = self.stroke_standards["secondary_partitions"]["metric_mm"] * self.mm_to_pt
        self.assertAlmostEqual(pt, 0.992, places=2)
        self.assertEqual(self.stroke_standards["secondary_partitions"]["hex_color"], "#33322E")

    def test_04_visible_projections_stroke_conversion(self):
        """Verify 0.25mm projection and dimension stroke converts to ~0.71 pt."""
        pt = self.stroke_standards["visible_projections"]["metric_mm"] * self.mm_to_pt
        self.assertAlmostEqual(pt, 0.709, places=2)
        self.assertEqual(self.stroke_standards["visible_projections"]["hex_color"], "#55544E")

    def test_05_hatch_insulation_stroke_conversion(self):
        """Verify 0.13mm fine hatch stroke converts to ~0.37 pt."""
        pt = self.stroke_standards["hatch_insulation"]["metric_mm"] * self.mm_to_pt
        self.assertAlmostEqual(pt, 0.369, places=2)
        self.assertEqual(self.stroke_standards["hatch_insulation"]["hex_color"], "#84827A")

    def test_06_membrane_and_egress_dash_patterns(self):
        """Verify EPDM and PMR egress vector stroke weights and dash configurations."""
        epdm = self.stroke_standards["epdm_membrane"]
        pmr = self.stroke_standards["pmr_egress_path"]
        self.assertEqual(epdm["metric_mm"], 0.25)
        self.assertEqual(epdm["dash_array"], "3,1")
        self.assertEqual(pmr["metric_mm"], 0.35)
        self.assertEqual(pmr["dash_array"], "1,2")

if __name__ == "__main__":
    unittest.main()
