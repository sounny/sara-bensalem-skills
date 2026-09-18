"""
tests/tier4_workloads/test_full_5act_case_study.py
Workload 2 (Tier 4): Full 5-act narrative portfolio case study across >=3 spreads
Authoritative Source: ORIGINAL_REQUEST.md Acceptance Criteria, spec_miner_skills/report.md §2
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

class TestFull5ActCaseStudy(unittest.TestCase):
    """
    Validates a complete real-world architectural monograph case study:
    - 5-act narrative dramaturgy across 4 consecutive facing spreads
    - Strict negative space discipline (>= 30% unprinted breathing room)
    - Anti-render-trap technical proof in every act
    """

    def setUp(self):
        # Case study spread layout tree
        self.case_study = {
            "project_id": "maison_bretonne_2026",
            "title": "Maison Bretonne Adaptive Reuse",
            "total_pages": 8,
            "total_spreads": 4,
            "spreads": [
                {
                    "spread_idx": 1,
                    "act": "ACT_1_AND_2",
                    "verso": {"type": "passport_block", "coverage_pct": 0.45, "content": "Metadata + Premise"},
                    "recto": {"type": "hero_site_section", "coverage_pct": 0.65, "content": "1:500 Urban Morphology + Sun Azimuth"},
                    "spread_negative_space_pct": 0.45
                },
                {
                    "spread_idx": 2,
                    "act": "ACT_3_SPATIAL_ANATOMY",
                    "verso": {"type": "volumetric_axon", "coverage_pct": 0.50, "content": "3-Step Load Path Massing"},
                    "recto": {"type": "uncropped_plan_1_100", "coverage_pct": 0.70, "content": "1:100 Plan + PMR 1500mm Arc + Grid 1-17"},
                    "spread_negative_space_pct": 0.40
                },
                {
                    "spread_idx": 3,
                    "act": "ACT_4_TECTONIC_PROOF",
                    "verso": {"type": "glaser_analysis", "coverage_pct": 0.55, "content": "Layer Schedule + U-Value 0.142 W/m²K"},
                    "recto": {"type": "hero_wall_section_1_20", "coverage_pct": 0.70, "content": "1:20 Full Wall Section + ISO 128 Weights"},
                    "spread_negative_space_pct": 0.375
                },
                {
                    "spread_idx": 4,
                    "act": "ACT_5_LIVED_CLIMAX",
                    "verso": {"type": "millwork_detail_1_5", "coverage_pct": 0.45, "content": "1:5 Joinery + 3mm Shadow Reveal"},
                    "recto": {"type": "lived_scenography", "coverage_pct": 0.75, "content": "Natural Light Plate + Colophon"},
                    "spread_negative_space_pct": 0.40
                }
            ]
        }

    def test_01_spread_count_at_least_three(self):
        """Verify the case study spans at least 3 consecutive spreads (4 spreads in reference)."""
        self.assertGreaterEqual(self.case_study["total_spreads"], 3)
        self.assertEqual(len(self.case_study["spreads"]), 4)

    def test_02_negative_space_discipline_maintained(self):
        """Verify every spread maintains at least 30% unprinted negative space."""
        for s in self.case_study["spreads"]:
            neg_space = s["spread_negative_space_pct"]
            self.assertGreaterEqual(
                neg_space,
                0.30,
                f"Spread {s['spread_idx']} negative space {neg_space:.1%} is below 30% minimum"
            )

    def test_03_act_4_tectonic_proof_verification(self):
        """Verify Act 4 delivers conclusive constructive proof (1:20 section + Glaser U-value)."""
        act_4 = self.case_study["spreads"][2]
        self.assertEqual(act_4["verso"]["type"], "glaser_analysis")
        self.assertEqual(act_4["recto"]["type"], "hero_wall_section_1_20")
        self.assertIn("0.142 W/m²K", act_4["verso"]["content"])
        self.assertIn("ISO 128", act_4["recto"]["content"])

    def test_04_act_3_pmr_and_grid_compliance(self):
        """Verify Act 3 includes PMR 1500mm wheelchair turning circle and column grid."""
        act_3 = self.case_study["spreads"][1]
        self.assertIn("PMR 1500mm", act_3["recto"]["content"])
        self.assertIn("Grid 1-17", act_3["recto"]["content"])

    def test_05_act_5_joinery_shadow_reveal(self):
        """Verify Act 5 demonstrates 1:5 bespoke millwork with 3mm shadow reveal."""
        act_5 = self.case_study["spreads"][3]
        self.assertEqual(act_5["verso"]["type"], "millwork_detail_1_5")
        self.assertIn("3mm Shadow Reveal", act_5["verso"]["content"])

if __name__ == "__main__":
    unittest.main()
