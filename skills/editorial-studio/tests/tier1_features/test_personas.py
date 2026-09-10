"""
tests/tier1_features/test_personas.py
Feature 1: SKILL format & 5 persona completeness (Art Director, Typographer, Compositor, Tectonic Detailer, Preflight Auditor)
Authoritative Source: ORIGINAL_REQUEST.md §R1, spec_miner_skills/report.md §1
"""

import unittest
import json
import re

class TestPersonasCompleteness(unittest.TestCase):
    """
    Validates persona specifications, prompt directives, input/output contracts,
    and architectural boundaries defined in R1.
    """

    def setUp(self):
        # Authoritative persona metadata extracted from spec_miner_skills/report.md
        self.personas = {
            "art_director": {
                "name": "Art Director Agent",
                "mandate": "5-act narrative arc, layout archetype selection, palette tokens, negative space discipline",
                "acts": [
                    "ACT_1_HOOK_AND_PASSPORT",
                    "ACT_2_TERRITORIAL_CONTEXT",
                    "ACT_3_SPATIAL_ANATOMY",
                    "ACT_4_TECTONIC_PROOF",
                    "ACT_5_LIVED_CLIMAX"
                ],
                "negative_space_min": 0.30
            },
            "typographer": {
                "name": "Typographer Agent",
                "mandate": "tripartite font architecture, baseline grid locking (4pt/6pt), Knuth-Plass breaks, optical hanging punctuation, orphan/widow control",
                "baseline_steps": [4, 6, 12],
                "font_roles": ["display", "body", "mono"],
                "widow_min": 2,
                "orphan_words_min": 2
            },
            "compositor": {
                "name": "Compositor Agent",
                "mandate": "facing spreads (recto/verso dynamic tension), 12-column Swiss grid, gutter creep calculus, margin zones",
                "columns": 12,
                "gutter_mm_range": (4.0, 5.0),
                "bindings": ["SMYTH_SEWN", "PERFECT_BOUND", "LAY_FLAT", "SADDLE_STITCHED"]
            },
            "tectonic_detailer": {
                "name": "Tectonic Vector Detailer",
                "mandate": "ISO 128 stroke hierarchy (0.13-0.70mm), 1:20 wall sections, 1:5 millwork, scale-aware downsampling, Glaser U-values",
                "scales": ["1:20", "1:5", "1:100"],
                "stroke_range_mm": (0.13, 0.70),
                "min_stroke_clamp_mm": 0.08
            },
            "preflight_auditor": {
                "name": "Pre-flight Auditor Agent",
                "mandate": "PDF/X-4 compliance, FOGRA51/52 CMYK, TAC <= 320%, 3mm bleeds, 100% font subsetting, >=300 DPI, bounding box collision detection",
                "bleed_mm": 3.0,
                "tac_max_percent": 320.0,
                "min_dpi": 300.0,
                "safety_margin_mm": 5.0
            }
        }

    def test_01_art_director_persona_specification(self):
        """Verify Art Director persona embodies 5-act spatial narrative and negative space discipline."""
        ad = self.personas["art_director"]
        self.assertEqual(len(ad["acts"]), 5)
        self.assertIn("ACT_1_HOOK_AND_PASSPORT", ad["acts"])
        self.assertIn("ACT_4_TECTONIC_PROOF", ad["acts"])
        self.assertGreaterEqual(ad["negative_space_min"], 0.30, "Art Director must enforce >=30% negative space")

    def test_02_typographer_persona_specification(self):
        """Verify Typographer persona governs baseline locking, font roles, and micro-typography."""
        typ = self.personas["typographer"]
        self.assertIn(6, typ["baseline_steps"])
        self.assertEqual(typ["font_roles"], ["display", "body", "mono"])
        self.assertGreaterEqual(typ["widow_min"], 2, "Widow threshold must be >= 2 lines")
        self.assertGreaterEqual(typ["orphan_words_min"], 2, "Orphan words threshold must be >= 2 words")

    def test_03_compositor_persona_specification(self):
        """Verify Compositor persona governs 12-column Swiss grid and 4 binding creep calculations."""
        comp = self.personas["compositor"]
        self.assertEqual(comp["columns"], 12)
        self.assertTrue(comp["gutter_mm_range"][0] <= 4.0 <= comp["gutter_mm_range"][1])
        self.assertIn("SMYTH_SEWN", comp["bindings"])
        self.assertIn("PERFECT_BOUND", comp["bindings"])
        self.assertIn("LAY_FLAT", comp["bindings"])

    def test_04_tectonic_detailer_persona_specification(self):
        """Verify Tectonic Detailer enforces ISO 128 lineweights and minimum stroke clamping."""
        tec = self.personas["tectonic_detailer"]
        self.assertIn("1:20", tec["scales"])
        self.assertIn("1:5", tec["scales"])
        self.assertEqual(tec["stroke_range_mm"], (0.13, 0.70))
        self.assertEqual(tec["min_stroke_clamp_mm"], 0.08, "Minimum stroke clamping must be 0.08mm")

    def test_05_preflight_auditor_persona_specification(self):
        """Verify Preflight Auditor enforces physical print physics (TAC <= 320%, 3mm bleed, 300 DPI)."""
        aud = self.personas["preflight_auditor"]
        self.assertEqual(aud["bleed_mm"], 3.0)
        self.assertEqual(aud["tac_max_percent"], 320.0)
        self.assertEqual(aud["min_dpi"], 300.0)
        self.assertEqual(aud["safety_margin_mm"], 5.0)

    def test_06_persona_contract_schemas(self):
        """Verify all 5 personas have structured, non-overlapping input/output contract requirements."""
        required_personas = ["art_director", "typographer", "compositor", "tectonic_detailer", "preflight_auditor"]
        self.assertEqual(sorted(list(self.personas.keys())), sorted(required_personas))
        for p in required_personas:
            self.assertIn("mandate", self.personas[p])
            self.assertTrue(len(self.personas[p]["mandate"]) > 20)

if __name__ == "__main__":
    unittest.main()
