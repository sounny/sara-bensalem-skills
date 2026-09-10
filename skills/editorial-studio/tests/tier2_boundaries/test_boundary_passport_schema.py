"""
tests/tier2_boundaries/test_boundary_passport_schema.py
Feature 10 (Tier 2): Boundary conditions and validation failures for Project Passport schema
Authoritative Source: ORIGINAL_REQUEST.md §R4, spec_miner_skills/report.md §4
"""

import sys
import os
import unittest
import copy

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.tier1_features.test_project_passport import validate_passport

class TestBoundaryPassportSchema(unittest.TestCase):
    """
    Validates boundary schema failures for Project Passport blocks:
    - Missing required fields
    - Null values
    - Line item contributions < 3 items
    - Empty or truncated executive premise (<8 words)
    - Corrupted coordinate strings
    - Empty software stack
    """

    def setUp(self):
        self.valid_base = {
            "title": "Maison Bretonne Adaptive Reuse",
            "typology": "Heritage Renovation & Timber Pavilion",
            "location": "Finistère, France",
            "coordinates": "48°15'12\"N 04°08'45\"W",
            "year": "2026",
            "area_m2": 3200,
            "budget_eur": 4850000,
            "client": "Municipal Heritage Trust",
            "stage": "RIBA Stage 4 / AIA Construction Documents (CD)",
            "team_size": 4,
            "candidate_role": "Lead Project Architect & Construction Detailing",
            "line_item_contributions": [
                "1:20 constructive wall section envelope detailing",
                "Breton granite stone ashlar stabilization schedule",
                "Lime-hemp thermal insulation specifications (RE2020 net-negative)"
            ],
            "software_stack": ["Revit 2026", "Rhino 8"],
            "work_authorization": "Permanent EU Citizen / No Sponsorship Required",
            "executive_premise": "Reconciling historical granite masonry with contemporary bio-composite hygrothermal retrofits to achieve Passivhaus standards."
        }

    def test_01_missing_stage_field_rejected(self):
        """Verify omitting professional stage ('stage') field triggers validation error."""
        data = copy.deepcopy(self.valid_base)
        del data["stage"]
        errors = validate_passport(data)
        self.assertTrue(any("Missing required field: 'stage'" in e for e in errors))

    def test_02_line_item_contributions_less_than_three_rejected(self):
        """Verify line_item_contributions with only 2 items fails minimum 3 constraint."""
        data = copy.deepcopy(self.valid_base)
        data["line_item_contributions"] = ["Item 1", "Item 2"]
        errors = validate_passport(data)
        self.assertTrue(any("at least 3 items" in e for e in errors))

    def test_03_null_value_on_required_field_rejected(self):
        """Verify null candidate_role triggers non-null validation error."""
        data = copy.deepcopy(self.valid_base)
        data["candidate_role"] = None
        errors = validate_passport(data)
        self.assertTrue(any("cannot be null" in e for e in errors))

    def test_04_truncated_executive_premise_rejected(self):
        """Verify executive premise with fewer than 8 words is rejected as superficial."""
        data = copy.deepcopy(self.valid_base)
        data["executive_premise"] = "Nice building in France." # 4 words
        errors = validate_passport(data)
        self.assertTrue(any("at least 8 words" in e for e in errors))

    def test_05_corrupted_coordinates_rejected(self):
        """Verify invalid non-coordinate string ('Somewhere on Earth') is rejected."""
        data = copy.deepcopy(self.valid_base)
        data["coordinates"] = "Somewhere on Earth"
        errors = validate_passport(data)
        self.assertTrue(any("coordinates format" in e for e in errors))

    def test_06_empty_software_stack_rejected(self):
        """Verify empty software stack array is rejected."""
        data = copy.deepcopy(self.valid_base)
        data["software_stack"] = []
        errors = validate_passport(data)
        self.assertTrue(any("software_stack must be a non-empty list" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
