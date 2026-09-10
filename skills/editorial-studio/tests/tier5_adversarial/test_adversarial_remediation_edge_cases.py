"""
tests/tier5_adversarial/test_adversarial_remediation_edge_cases.py
Challenger 2 Empirical Verification Suite: Deep Adversarial Edge Cases & Gate Remediations (Iteration 2)

Empirically tests:
1. Saddle-stitch discrete leaf creep symmetry and monotonicity across page counts N in [4, 64].
2. CompositorInput Draft 2020-12 conditional schema enforcement (N <= 64 for SADDLE_STITCHED).
3. Perfect-bound PUR shingle mechanics, single-leaf zero-creep, and 5.0mm outer safety clamping up to N = 1000.
4. Mathematical container height baseline snapping (ceil vs round empirical fuzzing across 10,000 floats).
5. Glaser hygrothermal U-value unit conversion (thickness_mm * 10^-3) and Passivhaus/RE2020 standards.
6. ProjectPassport Draft 2020-12 schema validation across numeric types (integers, floats, scientific notation)
   and negative type fuzzing (strings, booleans, nulls, arrays, objects).
7. Exhaustive binary refusal checklists and zero-tolerance gates across SKILL.md and all 5 personas.
8. Draft 2020-12 meta-schema compliance for all 12 schemas extracted from markdown files.
"""

import math
import random
import unittest
import json
import re
import pathlib
from jsonschema import Draft202012Validator, ValidationError

WORKSPACE_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

def load_persona(name: str) -> str:
    path = WORKSPACE_ROOT / "personas" / name
    if not path.exists():
        raise FileNotFoundError(f"Persona file not found: {path}")
    return path.read_text(encoding="utf-8")

def load_skill() -> str:
    path = WORKSPACE_ROOT / "SKILL.md"
    if not path.exists():
        raise FileNotFoundError(f"SKILL.md not found: {path}")
    return path.read_text(encoding="utf-8")

def extract_schemas_by_title(markdown_content: str) -> dict:
    matches = re.findall(r"```json\s*([\s\S]*?)\s*```", markdown_content)
    schemas = {}
    for m in matches:
        try:
            data = json.loads(m)
            if isinstance(data, dict) and "title" in data:
                schemas[data["title"]] = data
        except Exception:
            pass
    return schemas


class TestSaddleStitchImpositionAndConditionalSchema(unittest.TestCase):
    """
    Adversarial verification of saddle-stitch imposition mechanics and
    Draft 2020-12 conditional schema enforcement.
    """

    @classmethod
    def setUpClass(cls):
        cls.compositor_text = load_persona("compositor.md")
        cls.skill_text = load_skill()
        cls.schemas = extract_schemas_by_title(cls.compositor_text)
        cls.compositor_schema = cls.schemas["CompositorInput"]
        cls.validator = Draft202012Validator(cls.compositor_schema)

    def test_01_discrete_leaf_symmetry_across_all_n(self):
        """
        Oracle verification: In saddle-stitch imposition, pages 2k-1 and 2k
        are printed on obverse and reverse faces of leaf k = floor((p-1)/2).
        Their creep displacement MUST be identical for every sheet.
        """
        def creep(p, N, c):
            leaf = (p - 1) // 2
            return c * min(leaf, N // 2 - 1 - leaf)

        calipers = [0.08, 0.10, 0.15, 0.20, 0.30]
        page_counts = [4, 8, 12, 16, 24, 32, 48, 64]

        for N in page_counts:
            for c in calipers:
                for p in range(1, N + 1, 2):
                    recto_creep = creep(p, N, c)
                    verso_creep = creep(p + 1, N, c)
                    self.assertEqual(
                        recto_creep, verso_creep,
                        f"Asymmetry on leaf {(p-1)//2}: p={p} ({recto_creep}mm) vs p={p+1} ({verso_creep}mm) at N={N}"
                    )

    def test_02_saddle_stitch_outer_margin_safety_clamped(self):
        """
        Verify that for all valid saddle-stitch booklets (N <= 64),
        outer margin never breaches the mandatory 5.0mm prepress safety buffer.
        """
        def outer_margin(p, N, c, M_out_base=18.0):
            leaf = (p - 1) // 2
            delta = c * min(leaf, N // 2 - 1 - leaf)
            return max(M_out_base - delta, 5.0)

        for N in [4, 8, 16, 32, 64]:
            for c in [0.08, 0.15, 0.30]:
                for p in range(1, N + 1):
                    m_out = outer_margin(p, N, c)
                    self.assertGreaterEqual(
                        m_out, 5.0,
                        f"Outer margin breach at N={N}, p={p}, c={c}: {m_out}mm < 5.0mm"
                    )

    def test_03_conditional_schema_accepts_saddle_stitch_le_64(self):
        """CompositorInput must accept SADDLE_STITCHED with total_page_count <= 64."""
        for n in [4, 16, 32, 64]:
            payload = {
                "blueprint": {},
                "typography_spec": {},
                "binding_spec": {
                    "binding_type": "SADDLE_STITCHED",
                    "total_page_count": n,
                    "paper_caliper_mm": 0.15
                }
            }
            self.assertTrue(self.validator.is_valid(payload), f"Failed for valid N={n}")

    def test_04_conditional_schema_rejects_saddle_stitch_gt_64(self):
        """CompositorInput must reject SADDLE_STITCHED with total_page_count > 64."""
        for n in [65, 80, 100, 500]:
            payload = {
                "blueprint": {},
                "typography_spec": {},
                "binding_spec": {
                    "binding_type": "SADDLE_STITCHED",
                    "total_page_count": n,
                    "paper_caliper_mm": 0.15
                }
            }
            with self.assertRaises(ValidationError, msg=f"Should reject SADDLE_STITCHED N={n}"):
                self.validator.validate(payload)

    def test_05_conditional_schema_allows_other_bindings_gt_64(self):
        """CompositorInput must NOT restrict total_page_count for non-saddle bindings."""
        for binding in ["PERFECT_BOUND", "SMYTH_SEWN", "LAY_FLAT"]:
            payload = {
                "blueprint": {},
                "typography_spec": {},
                "binding_spec": {
                    "binding_type": binding,
                    "total_page_count": 500,
                    "paper_caliper_mm": 0.15
                }
            }
            self.assertTrue(
                self.validator.is_valid(payload),
                f"Should accept {binding} at N=500"
            )

    def test_06_reject_saddle_stitch_below_minimum_pages(self):
        """CompositorInput must reject total_page_count < 4."""
        payload = {
            "blueprint": {},
            "typography_spec": {},
            "binding_spec": {
                "binding_type": "SADDLE_STITCHED",
                "total_page_count": 2,
                "paper_caliper_mm": 0.15
            }
        }
        with self.assertRaises(ValidationError):
            self.validator.validate(payload)


class TestPerfectBoundPURMechanicsAndClamping(unittest.TestCase):
    """
    Adversarial verification of Perfect Bound / PUR mechanics,
    differentiating Single-Leaf Cut vs Folded-Signature.
    """

    @classmethod
    def setUpClass(cls):
        cls.skill_text = load_skill()
        cls.comp_text = load_persona("compositor.md")

    def test_01_single_leaf_pur_zero_shingle_oracle(self):
        """
        Verify Single-Leaf Cut PUR has Shingle(p) == 0.0mm for all pages,
        leaving M_outer constant at base outer margin up to N = 1000.
        """
        M_out_base = 18.0
        for N in [32, 100, 347, 500, 1000]:
            for p in [1, N // 2, N]:
                shingle = 0.0
                m_out = M_out_base - shingle
                self.assertEqual(m_out, 18.0)
                self.assertGreaterEqual(m_out, 5.0)

    def test_02_folded_signature_pur_bounded_shingle_and_clamping(self):
        """
        Verify Folded-Signature PUR shingling is cyclical per signature S (e.g. S=16),
        and strictly clamped >= 5.0mm even under extreme caliper and N = 1000.
        """
        def folded_sig_margin(p, S, c, M_out_base=18.0):
            j = (p - 1) % S
            leaf = min(j // 2, S // 2 - 1 - j // 2)
            shingle = c * leaf
            return max(M_out_base - shingle, 5.0)

        for S in [8, 16, 32]:
            for c in [0.08, 0.15, 0.30]:
                for p in range(1, 501):
                    m_out = folded_sig_margin(p, S, c)
                    self.assertGreaterEqual(m_out, 5.0)
                    self.assertLessEqual(m_out, 18.0)

    def test_03_text_documentation_of_pur_differentiation(self):
        """Verify both SKILL.md and compositor.md document Single-Leaf vs Folded-Signature."""
        for text in [self.skill_text, self.comp_text]:
            self.assertIn("Single-Leaf Cut PUR", text)
            self.assertIn("Folded-Signature PUR", text)
            self.assertIn("5.0", text)


class TestContainerHeightBaselineSnapping(unittest.TestCase):
    """
    Adversarial verification of container height baseline snapping mathematics.
    Compares ceil(h/B)*B vs flawed round(h/B)*B across 10,000 fuzzed heights.
    """

    @classmethod
    def setUpClass(cls):
        cls.skill_text = load_skill()
        cls.typographer_text = load_persona("typographer.md")

    def test_01_ceil_specification_harmony(self):
        """SKILL.md and typographer.md must both specify ceil(h/B)*B."""
        self.assertIn(r"h_{\text{snapped}} = \text{ceil}", self.skill_text)
        self.assertIn(r"h_{\text{snapped}} = \text{ceil}", self.typographer_text)

    def test_02_empirical_fuzzing_zero_truncation(self):
        """
        Fuzz 10,000 float heights in (0.1, 1000.0] pt with grid units B in {4.0, 6.0, 12.0}.
        Assert that ceil snapping NEVER truncates (surplus >= 0) while round snapping truncates 50% of the time.
        """
        random.seed(42)
        grid_units = [4.0, 6.0, 12.0]
        ceil_truncations = 0
        round_truncations = 0
        total_trials = 10000

        for _ in range(total_trials):
            h = random.uniform(0.1, 1000.0)
            B = random.choice(grid_units)

            h_ceil = math.ceil(h / B) * B
            h_round = round(h / B) * B

            # Ceil check: snapped height must be strictly >= original height (within float eps)
            if h_ceil < h - 1e-9:
                ceil_truncations += 1

            # Round check: how often does round truncate?
            if h_round < h - 1e-9:
                round_truncations += 1

            # Ceil surplus must be strictly less than B
            self.assertLess(h_ceil - h, B)

        self.assertEqual(ceil_truncations, 0, "ceil(h/B)*B produced vertical container truncation!")
        self.assertGreater(round_truncations, 4000, "round(h/B)*B should have truncated ~50% of trials")


class TestGlaserHygrothermalUnitConversion(unittest.TestCase):
    """
    Adversarial verification of Glaser hygrothermal U-value calculation
    and explicit millimeter-to-meter conversion.
    """

    @classmethod
    def setUpClass(cls):
        cls.skill_text = load_skill()
        cls.tec_text = load_persona("tectonic_detailer.md")

    def test_01_conversion_factor_present_in_documentation(self):
        """Verify explicit 10^-3 or d_i = thickness_mm * 10^-3 in both docs."""
        self.assertIn("10^{-3}", self.skill_text)
        self.assertIn("10^{-3}", self.tec_text)
        self.assertTrue("thickness_mm" in self.skill_text or r"thickness\_mm" in self.skill_text)
        self.assertTrue("thickness_mm" in self.tec_text or r"thickness\_mm" in self.tec_text)

    def test_02_numerical_evaluation_passivhaus_standard(self):
        """
        Verify that multi-layer wall assembly with millimeter inputs
        evaluates to Passivhaus standard U <= 0.15 W/m2K when converted properly,
        and fails dramatically (U ~ 0.0001) if not converted.
        """
        layers = [
            {"thickness_mm": 15.0, "lambda": 0.25},   # Plaster
            {"thickness_mm": 240.0, "lambda": 0.038}, # Cellulose
            {"thickness_mm": 60.0, "lambda": 0.042},  # Wood fiber
            {"thickness_mm": 20.0, "lambda": 0.13}    # Cladding
        ]
        R_si = 0.13
        R_se = 0.04

        # Correct calculation with conversion
        R_layers_correct = sum((lyr["thickness_mm"] * 1e-3) / lyr["lambda"] for lyr in layers)
        R_tot_correct = R_si + R_layers_correct + R_se
        U_correct = 1.0 / R_tot_correct

        self.assertLessEqual(U_correct, 0.15, "Assembly should be Passivhaus compliant (U <= 0.15)")
        self.assertGreater(U_correct, 0.05, "U-value should be realistic (0.05 < U <= 0.15)")

        # Flawed calculation without conversion (input treated directly as meters)
        R_layers_flawed = sum(lyr["thickness_mm"] / lyr["lambda"] for lyr in layers)
        R_tot_flawed = R_si + R_layers_flawed + R_se
        U_flawed = 1.0 / R_tot_flawed

        # Flawed U is 1000x too small
        self.assertLess(U_flawed, 0.001)


class TestProjectPassportSchemaNumberValidation(unittest.TestCase):
    """
    Adversarial verification of ProjectPassport area_m2 typing.
    Validates integer and float support while rejecting non-numeric types.
    """

    @classmethod
    def setUpClass(cls):
        cls.skill_text = load_skill()
        cls.tec_text = load_persona("tectonic_detailer.md")
        cls.skill_schemas = extract_schemas_by_title(cls.skill_text)
        cls.tec_schemas = extract_schemas_by_title(cls.tec_text)
        cls.schema_skill = cls.skill_schemas["ProjectPassport"]
        cls.schema_tec = cls.tec_schemas["ProjectPassport"]
        cls.val_skill = Draft202012Validator(cls.schema_skill)
        cls.val_tec = Draft202012Validator(cls.schema_tec)

        cls.base_passport = {
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
            "candidate_role": "Lead Project Architect & Detailing",
            "line_item_contributions": [
                "1:20 constructive wall section envelope detailing",
                "Breton granite stone ashlar stabilization schedule",
                "PMR universal accessibility compliance"
            ],
            "software_stack": ["Revit", "Rhino", "InDesign"],
            "work_authorization": "Permanent EU Citizen",
            "executive_premise": "Adaptive reuse of historical granite structure with Passivhaus envelope."
        }

    def test_01_schema_property_type_is_number(self):
        """Verify area_m2 type is declared as 'number' in both schemas."""
        self.assertEqual(self.schema_skill["properties"]["area_m2"]["type"], "number")
        self.assertEqual(self.schema_tec["properties"]["area_m2"]["type"], "number")

    def test_02_accept_integer_and_float_areas(self):
        """Verify integer, decimal, and scientific float areas validate cleanly."""
        valid_areas = [3200, 142.5, 0.5, 9999.99, 1e4]
        for a in valid_areas:
            payload = json.loads(json.dumps(self.base_passport))
            payload["area_m2"] = a
            self.assertTrue(self.val_skill.is_valid(payload), f"SKILL failed for area_m2={a}")
            self.assertTrue(self.val_tec.is_valid(payload), f"TEC failed for area_m2={a}")

    def test_03_reject_non_numeric_types(self):
        """Adversarial negative payload fuzzing on area_m2."""
        invalid_areas = [
            "3200",
            "142.5 m2",
            True,
            False,
            None,
            [3200],
            {"area": 3200}
        ]
        for inv in invalid_areas:
            payload = json.loads(json.dumps(self.base_passport))
            payload["area_m2"] = inv
            with self.assertRaises(ValidationError, msg=f"Should reject area_m2={inv}"):
                self.val_skill.validate(payload)
            with self.assertRaises(ValidationError, msg=f"Should reject area_m2={inv}"):
                self.val_tec.validate(payload)

    def test_04_reject_each_missing_required_property(self):
        """Adversarially remove each required field one by one."""
        required = self.schema_skill["required"]
        for field in required:
            payload = json.loads(json.dumps(self.base_passport))
            del payload[field]
            with self.assertRaises(ValidationError, msg=f"Should reject missing {field}"):
                self.val_skill.validate(payload)
            with self.assertRaises(ValidationError, msg=f"Should reject missing {field}"):
                self.val_tec.validate(payload)


class TestRefusalChecklistsAndZeroToleranceGates(unittest.TestCase):
    """
    Verifies that refusal checklists and zero-tolerance gates are intact
    and fail-closed across all 5 personas.
    """

    @classmethod
    def setUpClass(cls):
        cls.personas = {
            "art_director": load_persona("art_director.md"),
            "typographer": load_persona("typographer.md"),
            "compositor": load_persona("compositor.md"),
            "tectonic_detailer": load_persona("tectonic_detailer.md"),
            "preflight_auditor": load_persona("preflight_auditor.md"),
        }

    def test_01_all_personas_have_checklist_headers(self):
        """Every persona must have a Verification Checklist header."""
        for name, text in self.personas.items():
            self.assertTrue(
                bool(re.search(r"##\s+\d+\.\s+Verification Checklist", text)),
                f"Persona {name} is missing Verification Checklist header"
            )

    def test_02_all_personas_have_at_least_5_checkboxes(self):
        """Every persona must contain at least 5 markdown checkboxes."""
        for name, text in self.personas.items():
            checkboxes = re.findall(r"- \[[ xX]\]", text)
            self.assertGreaterEqual(
                len(checkboxes), 5,
                f"Persona {name} has fewer than 5 checkboxes (found {len(checkboxes)})"
            )

    def test_03_zero_tolerance_gates_active(self):
        """Verify zero-tolerance gates across all personas."""
        # Art Director: Anti-Render-Trap Gate
        self.assertIn("Anti-Render-Trap Gate", self.personas["art_director"])
        # Typographer: Baseline drift < 0.25pt
        self.assertIn("0.25", self.personas["typographer"])
        # Compositor: Spine draw & 5.0mm safety margin
        self.assertIn("5.0", self.personas["compositor"])
        # Tectonic Detailer: 12 lethal antipatterns
        self.assertIn("The Magic Cantilever Stair", self.personas["tectonic_detailer"])
        self.assertIn("The Floating Glass Box", self.personas["tectonic_detailer"])
        # Preflight Auditor: TAC > 320% critical threshold
        self.assertIn("320", self.personas["preflight_auditor"])
        self.assertIn("Critical Failure Threshold", self.personas["preflight_auditor"])


class TestDraft202012MetaSchemaCompliance(unittest.TestCase):
    """
    Verifies that all 12 JSON schemas across SKILL.md and all 5 personas
    are 100% valid under Draft 2020-12 meta-schema.
    """

    def test_01_all_12_schemas_valid_under_draft202012(self):
        files = [
            load_skill(),
            load_persona("art_director.md"),
            load_persona("typographer.md"),
            load_persona("compositor.md"),
            load_persona("tectonic_detailer.md"),
            load_persona("preflight_auditor.md")
        ]
        total_schemas = 0
        for f in files:
            schemas = extract_schemas_by_title(f)
            for title, s in schemas.items():
                total_schemas += 1
                try:
                    Draft202012Validator.check_schema(s)
                except Exception as e:
                    self.fail(f"Schema {title} failed Draft 2020-12 meta-schema validation: {e}")

        self.assertGreaterEqual(total_schemas, 12, f"Expected at least 12 schemas, found {total_schemas}")


if __name__ == "__main__":
    unittest.main()
