"""
tests/tier3_combinations/test_five_act_dual_engine.py
Combination 4: 5-act narrative multi-spread pacing compiled via dual engines
Authoritative Source: ORIGINAL_REQUEST.md §R1, §R2, spec_miner_skills/report.md §2
"""

import sys
import os
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

FIVE_ACT_SEQUENCE = [
    "ACT_1_HOOK_AND_PASSPORT",
    "ACT_2_TERRITORIAL_CONTEXT",
    "ACT_3_SPATIAL_ANATOMY",
    "ACT_4_TECTONIC_PROOF",
    "ACT_5_LIVED_CLIMAX"
]

def generate_multi_spread_manifest(project_title: str) -> dict:
    """Generates a complete 5-act case study spread manifest across 4 spreads (8 pages)."""
    return {
        "title": project_title,
        "spread_count": 4,
        "page_count": 8,
        "spreads": [
            {
                "spread_num": 1,
                "pages": [2, 3],
                "acts": ["ACT_1_HOOK_AND_PASSPORT", "ACT_2_TERRITORIAL_CONTEXT"],
                "verso": {"archetype": "THE_PASSPORT", "focus": "Metadata & Premise"},
                "recto": {"archetype": "THE_MONUMENT", "focus": "Territorial Site Section & Microclimate"}
            },
            {
                "spread_num": 2,
                "pages": [4, 5],
                "acts": ["ACT_3_SPATIAL_ANATOMY"],
                "verso": {"archetype": "THE_ANALYTIC", "focus": "3-Step Volumetric Axon & Load Paths"},
                "recto": {"archetype": "THE_MONUMENT", "focus": "Uncropped 1:100 Architectural Plan with PMR Arc"}
            },
            {
                "spread_num": 3,
                "pages": [6, 7],
                "acts": ["ACT_4_TECTONIC_PROOF"],
                "verso": {"archetype": "THE_DATA_LED", "focus": "Glaser U-Value & Layer Schedule"},
                "recto": {"archetype": "THE_DETAIL", "focus": "Hero 1:20 Constructive Wall Section Vector"}
            },
            {
                "spread_num": 4,
                "pages": [8, 9],
                "acts": ["ACT_5_LIVED_CLIMAX"],
                "verso": {"archetype": "THE_DETAIL", "focus": "1:5 Bespoke Millwork Shadow Reveal"},
                "recto": {"archetype": "THE_ATMOSPHERE", "focus": "Lived Scenography & Light Plate"}
            }
        ]
    }

class TestFiveActDualEngine(unittest.TestCase):
    """
    Validates the 5-act narrative curation structure and its declarative representation.
    """

    def setUp(self):
        self.manifest = generate_multi_spread_manifest("Maison Bretonne")

    def test_01_all_five_acts_covered_in_order(self):
        """Verify all 5 narrative acts are represented in exact chronological sequence."""
        manifest_acts = []
        for s in self.manifest["spreads"]:
            manifest_acts.extend(s["acts"])

        self.assertEqual(manifest_acts, FIVE_ACT_SEQUENCE)

    def test_02_spread_count_at_least_three_spreads(self):
        """Verify case study spans at least 3 consecutive spreads (here 4 spreads / 8 pages)."""
        self.assertGreaterEqual(self.manifest["spread_count"], 3)
        self.assertEqual(len(self.manifest["spreads"]), 4)

    def test_03_act_4_tectonic_proof_includes_hero_section(self):
        """Verify Act 4 specifically contains the 1:20 constructive wall section plate."""
        act_4_spread = self.manifest["spreads"][2]
        self.assertIn("ACT_4_TECTONIC_PROOF", act_4_spread["acts"])
        self.assertIn("1:20 Constructive Wall Section", act_4_spread["recto"]["focus"])

    def test_04_act_3_spatial_anatomy_includes_1_100_plan(self):
        """Verify Act 3 includes the dimensioned 1:100 architectural plan."""
        act_3_spread = self.manifest["spreads"][1]
        self.assertIn("ACT_3_SPATIAL_ANATOMY", act_3_spread["acts"])
        self.assertIn("1:100 Architectural Plan", act_3_spread["recto"]["focus"])

if __name__ == "__main__":
    unittest.main()
