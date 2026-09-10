"""
tests/tier5_adversarial/test_negative_rejection_m23_challenger2.py
Challenger 2 Empirical Verification Test Suite: Negative Rejection & Adversarial Gate Enforcement (M2 & M3)

Authoritative Requirements:
- ORIGINAL_REQUEST.md §R3, §R4
- PROJECT.md lines 23-30 (M2, M3)
- Deliverables under engine/grid/ and engine/drafting/

Empirically tests:
1. calculate_gutter_creep:
   - Rejection of invalid binding types with ValueError.
   - Rejection of N > 64 for saddle-stitched bindings with ValueError.
   - Rejection of out-of-bounds page indices (p < 1, p > N, N < 1).
2. ProjectPassport:
   - Rejection of payloads missing any of the 13 required fields.
   - Rejection of non-numeric area_m2 (strings, booleans, arrays, nulls).
   - Acceptance of valid numeric integer and float area_m2.
3. downsample_strokes:
   - Rejection of non-positive scale factors (scale <= 0) with ValueError.
   - Preservation of vector layer grouping (<g> hierarchy and element trees).
4. validate_cross_spine_alignment:
   - Detection and flagging of baseline alignment drift > 0.25pt across facing pages.
   - Correct acceptance of baseline alignment within tolerance (<= 0.25pt).
"""

import os
import sys
import copy
import xml.etree.ElementTree as ET
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engine.grid.creep_calculator import calculate_gutter_creep, SUPPORTED_BINDING_TYPES
from engine.grid.baseline import validate_cross_spine_alignment
from engine.drafting.project_passport import (
    ProjectPassport,
    validate_passport,
    PASSPORT_REQUIRED_FIELDS,
    PROJECT_PASSPORT_SCHEMA
)
from engine.drafting.iso_128 import (
    downsample_strokes,
    downsample_stroke,
    downsample_hatch,
    validate_stroke_weight,
    MIN_STROKE_MM
)


class TestGutterCreepNegativeRejection(unittest.TestCase):
    """
    Negative rejection tests for gutter creep calculus (engine/grid/creep_calculator.py).
    """

    def test_01_reject_invalid_binding_types(self):
        """Verify calculate_gutter_creep raises ValueError for invalid binding types."""
        invalid_types = [
            "SPIRAL",
            "COMB_BINDING",
            "WIRE_O",
            "THERMAL_TAPE",
            "LOOSE_LEAF",
            "",
            "   ",
            "UNKNOWN_BINDING"
        ]
        for b_type in invalid_types:
            with self.subTest(binding_type=b_type):
                with self.assertRaises(ValueError, msg=f"Should raise ValueError for '{b_type}'"):
                    calculate_gutter_creep(page=1, total_pages=16, binding_type=b_type)

    def test_02_reject_non_string_binding_type(self):
        """Verify calculate_gutter_creep raises ValueError when binding_type is not a string."""
        for invalid_val in [None, 123, 45.6, [], {}]:
            with self.subTest(binding_type=invalid_val):
                with self.assertRaises(ValueError):
                    calculate_gutter_creep(page=1, total_pages=16, binding_type=invalid_val)

    def test_03_reject_saddle_stitch_exceeding_64_pages(self):
        """Verify saddle-stitch binding strictly rejects total_pages N > 64 with ValueError."""
        excessive_page_counts = [65, 66, 68, 72, 80, 96, 128, 256, 500]
        for n in excessive_page_counts:
            with self.subTest(total_pages=n):
                with self.assertRaises(ValueError, msg=f"Should reject SADDLE_STITCHED with N={n}"):
                    calculate_gutter_creep(page=1, total_pages=n, binding_type="SADDLE_STITCHED")

    def test_04_accept_saddle_stitch_within_64_pages(self):
        """Verify saddle-stitch binding succeeds for total_pages N <= 64."""
        valid_page_counts = [4, 8, 16, 32, 48, 64]
        for n in valid_page_counts:
            with self.subTest(total_pages=n):
                res = calculate_gutter_creep(page=n // 2, total_pages=n, binding_type="SADDLE_STITCHED")
                self.assertEqual(res["binding_type"], "SADDLE_STITCHED")
                self.assertGreaterEqual(res["inner_margin_mm"], 20.0)
                self.assertGreaterEqual(res["outer_margin_mm"], 5.0)

    def test_05_reject_out_of_bounds_page_indices(self):
        """Verify calculate_gutter_creep rejects page < 1, page > total_pages, and total_pages < 1."""
        # page < 1
        with self.assertRaises(ValueError):
            calculate_gutter_creep(page=0, total_pages=16, binding_type="SMYTH_SEWN")
        with self.assertRaises(ValueError):
            calculate_gutter_creep(page=-5, total_pages=16, binding_type="SMYTH_SEWN")

        # page > total_pages
        with self.assertRaises(ValueError):
            calculate_gutter_creep(page=17, total_pages=16, binding_type="SMYTH_SEWN")

        # total_pages < 1
        with self.assertRaises(ValueError):
            calculate_gutter_creep(page=1, total_pages=0, binding_type="SMYTH_SEWN")
        with self.assertRaises(ValueError):
            calculate_gutter_creep(page=1, total_pages=-10, binding_type="SMYTH_SEWN")


class TestProjectPassportNegativeRejection(unittest.TestCase):
    """
    Negative rejection tests for Project Passport (engine/drafting/project_passport.py).
    """

    def setUp(self):
        self.valid_payload = {
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

    def test_01_verify_exactly_13_required_fields(self):
        """Verify the authoritative schema requires exactly 13 fields."""
        self.assertEqual(len(PASSPORT_REQUIRED_FIELDS), 13)
        expected = {
            "title", "typology", "location", "coordinates", "year", "area_m2",
            "client", "stage", "candidate_role", "line_item_contributions",
            "software_stack", "work_authorization", "executive_premise"
        }
        self.assertEqual(set(PASSPORT_REQUIRED_FIELDS), expected)

    def test_02_reject_missing_required_fields_individually(self):
        """Verify that omitting ANY single field from the 13 required fields triggers validation failure."""
        for field in PASSPORT_REQUIRED_FIELDS:
            with self.subTest(missing_field=field):
                corrupted = copy.deepcopy(self.valid_payload)
                del corrupted[field]
                passport = ProjectPassport(corrupted)
                self.assertFalse(passport.is_valid(), f"Passport must not be valid when '{field}' is missing")
                errors = passport.validate()
                self.assertTrue(
                    any(f"Missing required field: '{field}'" in e for e in errors),
                    f"Errors must mention missing '{field}': {errors}"
                )

    def test_03_reject_non_numeric_area_m2(self):
        """Verify that non-numeric area_m2 values are rejected with validation errors."""
        non_numeric_values = [
            ("string_number", "3200"),
            ("string_text", "three thousand square meters"),
            ("bool_true", True),
            ("bool_false", False),
            ("list", [3200]),
            ("dict", {"area": 3200}),
            ("none", None)
        ]
        for label, val in non_numeric_values:
            with self.subTest(area_m2_type=label):
                corrupted = copy.deepcopy(self.valid_payload)
                corrupted["area_m2"] = val
                passport = ProjectPassport(corrupted)
                self.assertFalse(passport.is_valid(), f"Passport must reject area_m2 = {val} ({type(val)})")
                errors = passport.validate()
                self.assertTrue(len(errors) > 0, f"Errors list must not be empty for area_m2={val}")

    def test_04_accept_numeric_area_m2_int_and_float(self):
        """Verify that both integer and float area_m2 are accepted as valid."""
        for numeric_val in [3200, 3200.0, 154.75, 45000]:
            with self.subTest(area_m2=numeric_val):
                payload = copy.deepcopy(self.valid_payload)
                payload["area_m2"] = numeric_val
                passport = ProjectPassport(payload)
                self.assertTrue(passport.is_valid(), f"Passport must accept area_m2={numeric_val}")
                self.assertEqual(len(passport.validate()), 0)


class TestCrossSpineAlignmentDrift(unittest.TestCase):
    """
    Verification tests for cross-spine baseline drift detection (engine/grid/baseline.py).
    """

    def test_01_perfect_alignment_accepted(self):
        """Verify identical baseline lines return True."""
        verso = [12.0 * i for i in range(1, 30)]
        recto = [12.0 * i for i in range(1, 30)]
        self.assertTrue(validate_cross_spine_alignment(verso, recto, tolerance=0.25))

    def test_02_alignment_within_tolerance_accepted(self):
        """Verify baseline offset <= 0.25pt is accepted."""
        verso = [10.0, 20.0, 30.0, 40.0]
        # Exactly 0.25pt positive offset
        recto_pos = [10.25, 20.25, 30.25, 40.25]
        self.assertTrue(validate_cross_spine_alignment(verso, recto_pos, tolerance=0.25))

        # Exactly 0.25pt negative offset
        recto_neg = [9.75, 19.75, 29.75, 39.75]
        self.assertTrue(validate_cross_spine_alignment(verso, recto_neg, tolerance=0.25))

    def test_03_alignment_drift_exceeding_tolerance_rejected(self):
        """Verify baseline offset > 0.25pt returns False."""
        verso = [10.0, 20.0, 30.0, 40.0]

        # 0.26pt positive drift
        recto_drift = [10.26, 20.0, 30.0, 40.0]
        self.assertFalse(validate_cross_spine_alignment(verso, recto_drift, tolerance=0.25))

        # 0.50pt positive drift
        recto_half_pt = [10.50, 20.0, 30.0, 40.0]
        self.assertFalse(validate_cross_spine_alignment(verso, recto_half_pt, tolerance=0.25))

        # -0.26pt negative drift
        recto_neg_drift = [9.74, 20.0, 30.0, 40.0]
        self.assertFalse(validate_cross_spine_alignment(verso, recto_neg_drift, tolerance=0.25))

    def test_04_isolated_drift_in_multiline_spread(self):
        """Verify a single drifting line among 50 lines flags the entire spread as invalid."""
        verso = [12.0 * i for i in range(1, 51)]
        recto = [12.0 * i for i in range(1, 51)]
        # Introduce drift on line 35 only (0.30pt)
        recto[34] += 0.30
        self.assertFalse(validate_cross_spine_alignment(verso, recto, tolerance=0.25))


class TestDownsampleStrokesLayerGroupingAndScaleValidation(unittest.TestCase):
    """
    Empirical challenge tests for downsample_strokes (engine/drafting/iso_128.py):
    - Rejection of non-positive scale factors (scale <= 0).
    - Preservation of vector layer grouping (<g> structure and attributes).
    """

    def test_01_vector_layer_grouping_preserved(self):
        """Verify that downsample_strokes preserves SVG <g> grouping, IDs, classes, and structure."""
        input_svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">'
            '  <g id="layer-structural" class="structural-elements">'
            '    <path id="col-1" stroke-width="0.70mm" d="M 10 10 L 10 100" />'
            '    <path id="beam-1" stroke-width="0.50mm" d="M 10 10 L 100 10" />'
            '  </g>'
            '  <g id="layer-partitions" class="partition-elements">'
            '    <line id="wall-1" stroke-width="0.35mm" x1="20" y1="20" x2="20" y2="80" />'
            '  </g>'
            '</svg>'
        )

        result_svg = downsample_strokes(input_svg, target_scale=0.5)
        root = ET.fromstring(result_svg)

        # 1. Structural layer group exists
        group_struct = root.find(".//{http://www.w3.org/2000/svg}g[@id='layer-structural']")
        if group_struct is None:
            group_struct = root.find(".//g[@id='layer-structural']")
        self.assertIsNotNone(group_struct, "Layer group 'layer-structural' must be preserved")
        self.assertEqual(group_struct.get("class"), "structural-elements")

        # 2. Children exist inside group
        children_tags = [c.tag.split("}")[-1] for c in group_struct]
        self.assertIn("path", children_tags)

        # 3. Scaled stroke weights are clamped correctly:
        # col-1: 0.70mm * 0.5 = 0.35mm
        # beam-1: 0.50mm * 0.5 = 0.25mm
        col1 = group_struct.find(".//{http://www.w3.org/2000/svg}path[@id='col-1']")
        if col1 is None:
            col1 = group_struct.find(".//path[@id='col-1']")
        self.assertIsNotNone(col1)
        self.assertEqual(col1.get("stroke-width"), "0.35mm")

        # 4. Partition layer group exists
        group_part = root.find(".//{http://www.w3.org/2000/svg}g[@id='layer-partitions']")
        if group_part is None:
            group_part = root.find(".//g[@id='layer-partitions']")
        self.assertIsNotNone(group_part, "Layer group 'layer-partitions' must be preserved")

    def test_02_element_dict_grouping_preserved(self):
        """Verify that downsample_strokes preserves structured dictionary elements and hierarchy."""
        elements = [
            {
                "group_id": "structural_grid",
                "stroke_mm": 0.50,
                "annotation_type": "GRID_LINE"
            },
            {
                "group_id": "dimensions",
                "stroke_mm": 0.25,
                "annotation_type": "MINOR_DIMENSION"
            }
        ]
        result = downsample_strokes(elements, target_scale=0.5)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["group_id"], "structural_grid")
        self.assertEqual(result[0]["stroke_mm"], 0.25)
        self.assertEqual(result[1]["group_id"], "dimensions")
        # Minor dimensions are culled at scale 0.5 (MAJOR_DIMENSIONS_ONLY)
        self.assertFalse(result[1]["visible"])

    def test_03_reject_non_positive_scale_factors(self):
        """
        Adversarial challenge: downsample_strokes must reject non-positive scale factors
        (target_scale <= 0) with a descriptive ValueError.

        Empirical test will verify whether the implementation raises ValueError
        or silently fails by accepting degenerate scales.
        """
        sample_svg = '<svg><path stroke-width="0.5mm" d="M0,0 L10,10"/></svg>'
        non_positive_scales = [0.0, -0.1, -0.5, -1.0, -10.0]

        for s in non_positive_scales:
            with self.subTest(target_scale=s):
                with self.assertRaises(ValueError, msg=f"downsample_strokes must reject non-positive scale target_scale={s} with ValueError"):
                    downsample_strokes(sample_svg, target_scale=s)


if __name__ == "__main__":
    unittest.main()
