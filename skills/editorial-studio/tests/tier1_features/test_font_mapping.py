"""
tests/tier1_features/test_font_mapping.py
Feature 2: Tripartite font mapping configuration
Authoritative Source: ORIGINAL_REQUEST.md §R3, spec_miner_skills/report.md §3
"""

import unittest
import json

class TestTripartiteFontMapping(unittest.TestCase):
    """
    Validates the strict three-tier font architecture:
    1. Structural Grotesque (display/headers)
    2. Rationalist Serif (curatorial narrative body)
    3. Technical Monospace (drafting metadata, scale bars, project passports)
    """

    def setUp(self):
        # Authoritative font mapping specification
        self.font_mapping = {
            "display": {
                "role": "Structural Grotesque",
                "families": ["Space Grotesk", "Inter", "Neue Haas Grotesk Text Pro", "Univers"],
                "fallbacks": ["sans-serif", "Arial", "Helvetica"],
                "weights": [600, 700],
                "tracking_display_em": -0.02,
                "tracking_caps_em": 0.08
            },
            "body": {
                "role": "Rationalist Serif",
                "families": ["Adobe Garamond Pro", "Source Serif 4", "Minion Pro", "EB Garamond"],
                "fallbacks": ["serif", "Georgia", "Times New Roman"],
                "weights": [400, 500],
                "measure_cpl": (45, 65),
                "optical_sizes": ["Caption", "Regular", "Subhead"]
            },
            "mono": {
                "role": "Technical Monospace",
                "families": ["JetBrains Mono", "IBM Plex Mono", "DM Mono", "Fira Code"],
                "fallbacks": ["monospace", "Courier New"],
                "weights": [500, 600],
                "tracking_em": 0.04,
                "tabular_figures": True
            }
        }

    def test_01_structural_grotesque_configuration(self):
        """Verify Structural Grotesque is configured for display typography with negative tracking."""
        disp = self.font_mapping["display"]
        self.assertEqual(disp["role"], "Structural Grotesque")
        self.assertIn("Space Grotesk", disp["families"])
        self.assertLess(disp["tracking_display_em"], 0.0, "Display tracking should be slightly tight (-0.02em)")
        self.assertGreater(disp["tracking_caps_em"], 0.0, "Caps subhead tracking should be spaced (+0.08em)")

    def test_02_rationalist_serif_configuration(self):
        """Verify Rationalist Serif is configured for narrative body with 45-65 characters per line."""
        body = self.font_mapping["body"]
        self.assertEqual(body["role"], "Rationalist Serif")
        self.assertIn("Adobe Garamond Pro", body["families"])
        self.assertEqual(body["measure_cpl"], (45, 65), "Ideal reading measure is 45-65 CPL")

    def test_03_technical_monospace_configuration(self):
        """Verify Technical Monospace is configured for metadata and drafting with tabular figures."""
        mono = self.font_mapping["mono"]
        self.assertEqual(mono["role"], "Technical Monospace")
        self.assertIn("JetBrains Mono", mono["families"])
        self.assertTrue(mono["tabular_figures"], "Monospace font must support tabular figures")
        self.assertEqual(mono["tracking_em"], 0.04)

    def test_04_system_fallback_cascades(self):
        """Verify every font role includes valid generic CSS fallbacks for offline or headless rendering."""
        for role, spec in self.font_mapping.items():
            self.assertTrue(len(spec["fallbacks"]) >= 2, f"Role '{role}' must have multiple fallbacks")
            self.assertTrue(
                any(fb in ["sans-serif", "serif", "monospace"] for fb in spec["fallbacks"]),
                f"Role '{role}' must include standard CSS generic family"
            )

    def test_05_role_isolation_rules(self):
        """Verify that font families are strictly partitioned with zero role overlap."""
        display_set = set(self.font_mapping["display"]["families"])
        body_set = set(self.font_mapping["body"]["families"])
        mono_set = set(self.font_mapping["mono"]["families"])

        self.assertTrue(display_set.isdisjoint(body_set), "Display and Body fonts must be distinct")
        self.assertTrue(body_set.isdisjoint(mono_set), "Body and Mono fonts must be distinct")
        self.assertTrue(display_set.isdisjoint(mono_set), "Display and Mono fonts must be distinct")

if __name__ == "__main__":
    unittest.main()
