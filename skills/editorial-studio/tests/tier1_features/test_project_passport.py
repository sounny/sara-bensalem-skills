"""
tests/tier1_features/test_project_passport.py
Feature 7: Standardized Project Passport data schema
Authoritative Source: ORIGINAL_REQUEST.md §R4, spec_miner_skills/report.md §4
"""

import unittest
import json
import re
import os

PASSPORT_REQUIRED_FIELDS = [
    "title", "typology", "location", "coordinates", "year", "area_m2",
    "client", "stage", "candidate_role", "line_item_contributions",
    "software_stack", "work_authorization", "executive_premise"
]

def validate_passport(data: dict) -> list:
    """Validates passport data against authoritative schema; returns list of error messages."""
    errors = []
    for field in PASSPORT_REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")
        elif data[field] is None:
            errors.append(f"Field '{field}' cannot be null")

    if "coordinates" in data and isinstance(data["coordinates"], str):
        # Basic check for lat/lon representation
        if not re.search(r"\d+°|\d+\.\d+", data["coordinates"]):
            errors.append("Invalid coordinates format: must contain degree symbols or decimal coordinates")

    if "line_item_contributions" in data:
        items = data["line_item_contributions"]
        if not isinstance(items, list) or len(items) < 3:
            errors.append(f"line_item_contributions must be a list with at least 3 items (got {len(items) if isinstance(items, list) else 'non-list'})")

    if "software_stack" in data:
        sw = data["software_stack"]
        if not isinstance(sw, list) or len(sw) == 0:
            errors.append("software_stack must be a non-empty list of tools")

    if "executive_premise" in data and isinstance(data["executive_premise"], str):
        words = data["executive_premise"].split()
        if len(words) < 8:
            errors.append("executive_premise must be at least 8 words defining the architectural premise")

    return errors

class TestProjectPassportSchema(unittest.TestCase):
    """
    Validates Project Passport data block schema compliance and metadata fidelity.
    """

    def setUp(self):
        fixture_path = os.path.join(os.path.dirname(__file__), "..", "fixtures", "sample_passport.json")
        with open(fixture_path, "r", encoding="utf-8") as f:
            self.sample_data = json.load(f)

    def test_01_sample_fixture_passes_validation(self):
        """Verify the reference sample_passport.json passes all schema requirements."""
        errors = validate_passport(self.sample_data)
        self.assertEqual(errors, [], f"Reference passport should have no validation errors: {errors}")

    def test_02_all_13_required_fields_present(self):
        """Verify all 13 mandatory passport fields are defined in the schema."""
        for field in PASSPORT_REQUIRED_FIELDS:
            self.assertIn(field, self.sample_data, f"Required field '{field}' missing from sample passport")

    def test_03_coordinates_formatting(self):
        """Verify geographic coordinates field contains valid degree representation."""
        coords = self.sample_data["coordinates"]
        self.assertRegex(coords, r"\d+°\d+.*[NSEW]", "Coordinates must follow standard DMS format")

    def test_04_line_item_contributions_minimum_three(self):
        """Verify line_item_contributions contains at least 3 concrete contributions."""
        contribs = self.sample_data["line_item_contributions"]
        self.assertIsInstance(contribs, list)
        self.assertGreaterEqual(len(contribs), 3)

    def test_05_stage_and_role_attribution(self):
        """Verify professional stage (RIBA/AIA) and explicit candidate role are specified."""
        self.assertIn("RIBA", self.sample_data["stage"])
        self.assertTrue(len(self.sample_data["candidate_role"]) > 5)
        self.assertIn("work_authorization", self.sample_data)

    def test_06_executive_premise_depth(self):
        """Verify executive premise articulates a technical/spatial architectural premise."""
        premise = self.sample_data["executive_premise"]
        self.assertGreater(len(premise.split()), 10)
        self.assertTrue("granite" in premise.lower() or "retrofit" in premise.lower() or "passivhaus" in premise.lower())

if __name__ == "__main__":
    unittest.main()
