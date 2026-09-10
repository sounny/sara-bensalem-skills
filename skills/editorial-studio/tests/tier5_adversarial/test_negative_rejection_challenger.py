"""
tests/tier5_adversarial/test_negative_rejection_challenger.py
Challenger 2 Empirical Verification Test Suite: Negative Rejection & Contract Enforcement

Empirically tests:
1. Negative rejection criteria definition across SKILL.md and 5 personas:
   - Floating steps / ungrounded geometry (Render Traps)
   - Baseline grid drift (Delta y > 0.25pt)
   - Gutter collision & zero creep on thick perfect-bound spines
   - TAC > 320% and RGB / non-FOGRA51/52 color spaces
   - Un-embedded fonts and missing glyphs
   - Uncalibrated stroke weights (<0.08mm or missing ISO 128 weights)
2. Unambiguous Refusal / Quality Checklists in every persona.
3. Strict typing and automated negative payload rejection across all JSON schemas.
"""

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
            if "title" in data:
                schemas[data["title"]] = data
        except Exception:
            pass
    return schemas


class TestNegativeRejectionCriteria(unittest.TestCase):
    """
    Empirically verifies that personas and SKILL.md explicitly define
    negative rejection criteria for all 6 required failure modes.
    """

    @classmethod
    def setUpClass(cls):
        cls.skill_text = load_skill()
        cls.art_director_text = load_persona("art_director.md")
        cls.typographer_text = load_persona("typographer.md")
        cls.compositor_text = load_persona("compositor.md")
        cls.tectonic_detailer_text = load_persona("tectonic_detailer.md")
        cls.preflight_auditor_text = load_persona("preflight_auditor.md")

    def test_01_rejection_floating_steps_and_render_traps(self):
        """Verify explicit rejection of ungrounded geometry, floating stairs, and render traps."""
        # Tectonic detailer must explicitly identify "The Magic Cantilever Stair"
        self.assertIn("The Magic Cantilever Stair", self.tectonic_detailer_text,
                      "Tectonic Detailer must define 'The Magic Cantilever Stair' antipattern")
        self.assertIn("shear drywall", self.tectonic_detailer_text.lower(),
                      "Tectonic Detailer must identify physical failure mode (shear drywall)")
        self.assertIn("250x100x8", self.tectonic_detailer_text.replace(" ", "").replace("\\times", "x"),
                      "Tectonic Detailer must specify steel box stringer fix")
        
        # Check additional lethal render traps
        self.assertIn("The Floating Glass Box", self.tectonic_detailer_text)
        self.assertIn("The Cantilevered Stone Slab", self.tectonic_detailer_text)

        # Art director must have an explicit Anti-Render-Trap Gate
        self.assertIn("Anti-Render-Trap Gate", self.art_director_text,
                      "Art Director must enforce an explicit Anti-Render-Trap Gate")
        self.assertIn("rejected", self.art_director_text.lower(),
                      "Art Director must explicitly state that render-only projects are rejected")

        # SKILL.md 100-point rubric rejection condition
        self.assertIn("Reject if < 85 or any lethal antipattern", self.skill_text,
                      "SKILL.md rubric must explicitly mandate rejection for lethal antipatterns")

    def test_02_rejection_baseline_grid_drift(self):
        """Verify explicit rejection of cross-spine baseline drift > 0.25pt."""
        # Typographer must define maximum variance < 0.25pt
        self.assertIn("0.25", self.typographer_text)
        self.assertIn("cross-spine", self.typographer_text.lower())
        self.assertIn("y_{\\text{snapped}}", self.typographer_text)

        # Output schema must enforce maximum: 0.25
        schemas = extract_schemas_by_title(self.typographer_text)
        self.assertIn("TypographySpec", schemas)
        baseline_prop = schemas["TypographySpec"]["properties"]["baseline_grid"]["properties"]["cross_spine_variance_pt"]
        self.assertEqual(baseline_prop.get("maximum"), 0.25,
                         "TypographySpec schema must strictly cap cross_spine_variance_pt at 0.25")

        # Verification checklist item
        self.assertTrue(
            r"\Delta y < 0.25" in self.typographer_text or "Delta y < 0.25" in self.typographer_text,
            "Typographer must verify cross-spine offset Delta y < 0.25pt"
        )

    def test_03_rejection_gutter_collision_and_zero_creep(self):
        """Verify rejection of spine gutter collisions, zero creep on perfect-bound books, and margin breaches."""
        # Compositor must define spine glue consumption G_draw
        self.assertTrue(
            "G_{\\text{draw}}" in self.compositor_text or "G_draw" in self.compositor_text,
            "Compositor must define spine glue consumption G_draw"
        )
        self.assertTrue(
            "7.0" in self.compositor_text and "9.0" in self.compositor_text,
            "Compositor must specify 7.0-9.0mm spine glue consumption"
        )
        self.assertIn("PUR Perfect Bound", self.compositor_text)
        self.assertIn("Trim Safety Margin", self.compositor_text)
        self.assertIn("5.0", self.compositor_text)
        self.assertIn("Crossover", self.compositor_text)

        # Preflight Auditor must fail on safety margin breach (< 5.0mm)
        self.assertIn("5.0mm TrimBox Safety Zone", self.preflight_auditor_text)
        self.assertIn("FAIL", self.preflight_auditor_text)
        self.assertIn("margin_safety_zone", self.preflight_auditor_text)

    def test_04_rejection_tac_exceeding_320_and_rgb_color(self):
        """Verify explicit critical failure threshold for TAC > 320% and unseparated RGB."""
        # Preflight Auditor must define TAC > 320% as a Critical Failure Threshold
        self.assertTrue(
            bool(re.search(r"TAC.*?[\s\S]*?>\s*320", self.preflight_auditor_text)),
            "Preflight Auditor must define TAC > 320% failure threshold"
        )
        self.assertIn("Critical Failure Threshold", self.preflight_auditor_text)
        self.assertIn("Unseparated RGB", self.preflight_auditor_text)
        self.assertIn("FOGRA51", self.preflight_auditor_text)
        self.assertIn("FOGRA52", self.preflight_auditor_text)

        # Preflight input schema must have tac_limit_percent default 320.0
        schemas = extract_schemas_by_title(self.preflight_auditor_text)
        self.assertIn("PreflightAuditorInput", schemas)
        tac_limit = schemas["PreflightAuditorInput"]["properties"]["tac_limit_percent"]["default"]
        self.assertEqual(tac_limit, 320.0)

        # Report schema must have verdict enum with REJECTED
        report_schema = schemas["PreflightAuditReport"]
        verdict_enum = report_schema["properties"]["scorecard"]["properties"]["verdict"]["enum"]
        self.assertIn("REJECTED", verdict_enum)

    def test_05_rejection_unembedded_fonts_and_missing_glyphs(self):
        """Verify explicit rejection of non-embedded fonts, missing glyphs, and Type 3 bitmap fonts."""
        # Preflight Auditor must mandate 100% font subsetting
        self.assertIn("100% embedded", self.preflight_auditor_text.lower())
        self.assertIn("missing glyphs", self.preflight_auditor_text.lower())
        self.assertIn("Type 3", self.preflight_auditor_text)
        self.assertIn("^[A-Z]{6}\\+", self.preflight_auditor_text)

        # Preflight report schema font_embedding check
        schemas = extract_schemas_by_title(self.preflight_auditor_text)
        report_schema = schemas["PreflightAuditReport"]
        font_status = report_schema["properties"]["checks"]["properties"]["font_embedding"]["properties"]["status"]["enum"]
        self.assertIn("FAIL", font_status)

    def test_06_rejection_uncalibrated_stroke_weights(self):
        """Verify rejection of hairline strokes < 0.08mm and missing ISO 128 lineweights."""
        # Tectonic Detailer stroke clamping
        self.assertIn("0.08", self.tectonic_detailer_text)
        self.assertIn("STROKE CLAMPING", self.tectonic_detailer_text)
        
        # Schema min_stroke_mm minimum: 0.08
        schemas = extract_schemas_by_title(self.tectonic_detailer_text)
        self.assertIn("TectonicVectorPlate", schemas)
        min_stroke = schemas["TectonicVectorPlate"]["properties"]["iso_128_compliance"]["properties"]["min_stroke_mm"]["minimum"]
        self.assertEqual(min_stroke, 0.08, "min_stroke_mm must enforce minimum: 0.08")

        # Preflight Auditor hairline check
        self.assertIn("0.08", self.preflight_auditor_text)
        self.assertIn("drop out during plate imaging", self.preflight_auditor_text)


class TestPersonaRefusalAndQualityChecklists(unittest.TestCase):
    """
    Verifies that every persona contains an unambiguous Refusal / Quality Checklist
    with explicit binary checkboxes before artifact emission.
    """

    def test_01_art_director_checklist(self):
        content = load_persona("art_director.md")
        self.assertIn("## 9. Verification Checklist", content)
        checkboxes = re.findall(r"- \[[ xX]\] \*\*([^*]+)\*\*", content)
        self.assertGreaterEqual(len(checkboxes), 5, "Art Director must have at least 5 verification checkboxes")
        checklist_text = content[content.find("## 9. Verification Checklist"):]
        self.assertIn("Tectonic Core", checklist_text)
        self.assertIn("Whitespace Quota", checklist_text)
        self.assertIn("5-Act Completeness", checklist_text)

    def test_02_typographer_checklist(self):
        content = load_persona("typographer.md")
        self.assertIn("## 9. Verification Checklist", content)
        checkboxes = re.findall(r"- \[[ xX]\] \*\*([^*]+)\*\*", content)
        self.assertGreaterEqual(len(checkboxes), 5, "Typographer must have at least 5 verification checkboxes")
        checklist_text = content[content.find("## 9. Verification Checklist"):]
        self.assertIn("Tripartite Mapping", checklist_text)
        self.assertIn("Baseline Grid Snap", checklist_text)
        self.assertIn("Zero Cross-Spine Offset", checklist_text)
        self.assertIn("Zero 1-Word Orphans", checklist_text)

    def test_03_compositor_checklist(self):
        content = load_persona("compositor.md")
        self.assertIn("## 9. Verification Checklist", content)
        checkboxes = re.findall(r"- \[[ xX]\] \*\*([^*]+)\*\*", content)
        self.assertGreaterEqual(len(checkboxes), 5, "Compositor must have at least 5 verification checkboxes")
        checklist_text = content[content.find("## 9. Verification Checklist"):]
        self.assertIn("Gutter Creep Calculation", checklist_text)
        self.assertIn("Spine Draw Clearance", checklist_text)
        self.assertIn("Safety Margin Buffer", checklist_text)
        self.assertIn("Crossover Image Split", checklist_text)

    def test_04_tectonic_detailer_checklist(self):
        content = load_persona("tectonic_detailer.md")
        self.assertIn("## 11. Verification Checklist", content)
        checkboxes = re.findall(r"- \[[ xX]\] \*\*([^*]+)\*\*", content)
        self.assertGreaterEqual(len(checkboxes), 5, "Tectonic Detailer must have at least 5 verification checkboxes")
        checklist_text = content[content.find("## 11. Verification Checklist"):]
        self.assertIn("ISO 128 Stroke Compliance", checklist_text)
        self.assertIn("Stroke Clamping", checklist_text)
        self.assertIn("Hygrothermal Glaser Verification", checklist_text)
        self.assertIn("Thermal Break Continuity", checklist_text)

    def test_05_preflight_auditor_checklist(self):
        content = load_persona("preflight_auditor.md")
        self.assertIn("## 11. Verification Checklist", content)
        checkboxes = re.findall(r"- \[[ xX]\] \*\*([^*]+)\*\*", content)
        self.assertGreaterEqual(len(checkboxes), 5, "Preflight Auditor must have at least 5 verification checkboxes")
        checklist_text = content[content.find("## 11. Verification Checklist"):]
        self.assertIn("PDF/X-4 Conformance", checklist_text)
        self.assertIn("CMYK & TAC Compliance", checklist_text)
        self.assertIn("100% Font Subsetting", checklist_text)
        self.assertIn("Rubric Score", checklist_text)


class TestSchemaStrictTypingAndAdversarialRejections(unittest.TestCase):
    """
    Adversarial fuzzing and boundary stress testing on all persona JSON schemas.
    Asserts that negative, violating payloads are strictly and actively rejected.
    """

    @classmethod
    def setUpClass(cls):
        cls.schemas = {}
        files = [
            load_persona("art_director.md"),
            load_persona("typographer.md"),
            load_persona("compositor.md"),
            load_persona("tectonic_detailer.md"),
            load_persona("preflight_auditor.md")
        ]
        for f in files:
            cls.schemas.update(extract_schemas_by_title(f))

    def test_01_reject_baseline_drift_exceeding_tolerance(self):
        """Inject cross_spine_variance_pt = 0.35pt (> 0.25pt maximum) -> Must fail validation."""
        schema = self.schemas["TypographySpec"]
        validator = Draft202012Validator(schema)

        # Baseline compliant payload
        valid_payload = {
            "font_families": {
                "display_grotesque": "Space Grotesk",
                "body_serif": "Source Serif 4",
                "metadata_mono": "JetBrains Mono"
            },
            "modular_scale": {
                "title": {"size_pt": 24.0, "leading_pt": 30.0},
                "subhead": {"size_pt": 12.0, "leading_pt": 18.0},
                "body": {"size_pt": 9.5, "leading_pt": 14.0},
                "caption": {"size_pt": 7.5, "leading_pt": 10.0},
                "mono": {"size_pt": 7.0, "leading_pt": 8.0}
            },
            "baseline_grid": {
                "grid_unit_pt": 6,
                "cross_spine_variance_pt": 0.10,
                "snap_formula": "y_snapped = round(y / B) * B"
            },
            "micro_typography": {
                "hanging_punctuation": True,
                "widow_penalty_lines": 2,
                "orphan_words_prohibited": True
            },
            "processed_blocks": []
        }
        self.assertTrue(validator.is_valid(valid_payload))

        # Adversarial payload: variance = 0.35pt (drift)
        invalid_payload = json.loads(json.dumps(valid_payload))
        invalid_payload["baseline_grid"]["cross_spine_variance_pt"] = 0.35

        with self.assertRaises(ValidationError) as ctx:
            validator.validate(invalid_payload)
        self.assertIn("cross_spine_variance_pt", str(ctx.exception))

    def test_02_reject_stroke_clamping_below_0_08mm(self):
        """Inject min_stroke_mm = 0.05mm (< 0.08mm minimum) -> Must fail validation."""
        schema = self.schemas["TectonicVectorPlate"]
        validator = Draft202012Validator(schema)

        valid_payload = {
            "plate_id": "PLATE_1:20_01",
            "drawing_type": "WALL_SECTION_1_20",
            "scale": "1:20",
            "vector_content": {
                "format": "SVG",
                "data": "<svg></svg>"
            },
            "physics_metrics": {
                "calculated_u_value": 0.14,
                "total_thickness_mm": 450.0,
                "passivhaus_compliant": True
            },
            "iso_128_compliance": {
                "min_stroke_mm": 0.08,
                "max_stroke_mm": 0.70,
                "status": "COMPLIANT"
            }
        }
        self.assertTrue(validator.is_valid(valid_payload))

        # Adversarial payload: min_stroke_mm = 0.04
        invalid_payload = json.loads(json.dumps(valid_payload))
        invalid_payload["iso_128_compliance"]["min_stroke_mm"] = 0.04

        with self.assertRaises(ValidationError) as ctx:
            validator.validate(invalid_payload)
        self.assertIn("min_stroke_mm", str(ctx.exception))

    def test_03_reject_insufficient_whitespace_budget(self):
        """Inject whitespace_budget_pct = 20.0% (< 30.0% minimum) -> Must fail validation."""
        schema = self.schemas["SpreadBlueprint"]
        validator = Draft202012Validator(schema)

        valid_payload = {
            "blueprint_id": "BP_01",
            "project_title": "Maison Bretonne",
            "whitespace_budget_pct": 32.5,
            "palette": {
                "canvas_bone": "#F8F8F5",
                "ink_graphite": "#111110",
                "ink_secondary": "#55544E",
                "hairline": "#DDD9D0",
                "accent": "#7A4D3B"
            },
            "grid_spec": {
                "columns": 12,
                "gutter_mm": 4.5,
                "margin_inner_mm": 22.0,
                "margin_outer_mm": 18.0,
                "margin_top_mm": 16.0,
                "margin_bottom_mm": 18.0
            },
            "spreads": [
                {
                    "spread_index": 1,
                    "act": "ACT_1_HOOK_AND_PASSPORT",
                    "archetype": "THE_PASSPORT",
                    "verso": {"role": "COGNITIVE_ANCHOR", "target_whitespace_pct": 30.0, "components": []},
                    "recto": {"role": "VISUAL_LEAD", "target_whitespace_pct": 35.0, "components": []}
                },
                {
                    "spread_index": 2,
                    "act": "ACT_3_SPATIAL_ANATOMY",
                    "archetype": "THE_SPATIAL_ANATOMY",
                    "verso": {"role": "COGNITIVE_ANCHOR", "target_whitespace_pct": 30.0, "components": []},
                    "recto": {"role": "VISUAL_LEAD", "target_whitespace_pct": 30.0, "components": []}
                },
                {
                    "spread_index": 3,
                    "act": "ACT_4_TECTONIC_PROOF",
                    "archetype": "THE_CONSTRUCTIVE_PROOF",
                    "verso": {"role": "ANALYTICAL_DENSITY", "target_whitespace_pct": 25.0, "components": []},
                    "recto": {"role": "EXPANSIVE_HERO", "target_whitespace_pct": 30.0, "components": []}
                }
            ]
        }
        self.assertTrue(validator.is_valid(valid_payload))

        # Adversarial payload: whitespace = 22.0%
        invalid_payload = json.loads(json.dumps(valid_payload))
        invalid_payload["whitespace_budget_pct"] = 22.0

        with self.assertRaises(ValidationError) as ctx:
            validator.validate(invalid_payload)
        self.assertIn("whitespace_budget_pct", str(ctx.exception))

    def test_04_reject_invalid_bleed_dimension(self):
        """Inject bleed = 2.0mm (not exactly 3.0mm) -> Must fail validation."""
        schema = self.schemas["SpreadLayoutTree"]
        validator = Draft202012Validator(schema)

        valid_payload = {
            "document_id": "DOC_01",
            "binding_applied": "PERFECT_BOUND",
            "page_dimensions_mm": {
                "width": 297.0,
                "height": 210.0,
                "bleed": 3.0
            },
            "spread_nodes": []
        }
        self.assertTrue(validator.is_valid(valid_payload))

        # Adversarial payload: bleed = 2.0mm
        invalid_payload = json.loads(json.dumps(valid_payload))
        invalid_payload["page_dimensions_mm"]["bleed"] = 2.0

        with self.assertRaises(ValidationError) as ctx:
            validator.validate(invalid_payload)
        self.assertIn("bleed", str(ctx.exception))

    def test_05_reject_paper_caliper_out_of_bounds(self):
        """Inject caliper < 0.08mm or > 0.30mm -> Must fail validation."""
        schema = self.schemas["CompositorInput"]
        validator = Draft202012Validator(schema)

        valid_payload = {
            "blueprint": {},
            "typography_spec": {},
            "binding_spec": {
                "binding_type": "PERFECT_BOUND",
                "total_page_count": 32,
                "paper_caliper_mm": 0.15
            }
        }
        self.assertTrue(validator.is_valid(valid_payload))

        # Adversarial payload: caliper = 0.05mm
        invalid_payload = json.loads(json.dumps(valid_payload))
        invalid_payload["binding_spec"]["paper_caliper_mm"] = 0.05
        with self.assertRaises(ValidationError):
            validator.validate(invalid_payload)

        # Adversarial payload: caliper = 0.45mm
        invalid_payload["binding_spec"]["paper_caliper_mm"] = 0.45
        with self.assertRaises(ValidationError):
            validator.validate(invalid_payload)

    def test_06_reject_unsupported_binding_enum(self):
        """Inject binding_type = 'WIRE_O' (not in enum) -> Must fail validation."""
        schema = self.schemas["CompositorInput"]
        validator = Draft202012Validator(schema)

        invalid_payload = {
            "blueprint": {},
            "typography_spec": {},
            "binding_spec": {
                "binding_type": "WIRE_O",
                "total_page_count": 32,
                "paper_caliper_mm": 0.15
            }
        }
        with self.assertRaises(ValidationError) as ctx:
            validator.validate(invalid_payload)
        self.assertIn("binding_type", str(ctx.exception))

    def test_07_reject_invalid_palette_hex_format(self):
        """Inject non-hex pattern color value -> Must fail validation."""
        schema = self.schemas["SpreadBlueprint"]
        validator = Draft202012Validator(schema)

        valid_blueprint = {
            "blueprint_id": "BP_01",
            "project_title": "Maison",
            "whitespace_budget_pct": 30.0,
            "palette": {
                "canvas_bone": "rgb(255, 255, 255)",  # Invalid: not #RRGGBB
                "ink_graphite": "#111110",
                "ink_secondary": "#55544E",
                "hairline": "#DDD9D0",
                "accent": "#7A4D3B"
            },
            "grid_spec": {
                "columns": 12,
                "gutter_mm": 4.5,
                "margin_inner_mm": 22.0,
                "margin_outer_mm": 18.0,
                "margin_top_mm": 16.0,
                "margin_bottom_mm": 18.0
            },
            "spreads": [
                {
                    "spread_index": 1,
                    "act": "ACT_1_HOOK_AND_PASSPORT",
                    "archetype": "THE_PASSPORT",
                    "verso": {"role": "COGNITIVE_ANCHOR", "target_whitespace_pct": 30.0, "components": []},
                    "recto": {"role": "VISUAL_LEAD", "target_whitespace_pct": 30.0, "components": []}
                },
                {
                    "spread_index": 2,
                    "act": "ACT_2_TERRITORIAL_CONTEXT",
                    "archetype": "THE_CARTOGRAPHIC_CONTEXT",
                    "verso": {"role": "COGNITIVE_ANCHOR", "target_whitespace_pct": 30.0, "components": []},
                    "recto": {"role": "VISUAL_LEAD", "target_whitespace_pct": 30.0, "components": []}
                },
                {
                    "spread_index": 3,
                    "act": "ACT_4_TECTONIC_PROOF",
                    "archetype": "THE_CONSTRUCTIVE_PROOF",
                    "verso": {"role": "ANALYTICAL_DENSITY", "target_whitespace_pct": 25.0, "components": []},
                    "recto": {"role": "EXPANSIVE_HERO", "target_whitespace_pct": 30.0, "components": []}
                }
            ]
        }
        with self.assertRaises(ValidationError) as ctx:
            validator.validate(valid_blueprint)
        self.assertIn("canvas_bone", str(ctx.exception))

    def test_08_reject_preflight_invalid_scorecard_verdict(self):
        """Inject verdict = 'CONDITIONAL_APPROVAL' -> Must fail validation."""
        schema = self.schemas["PreflightAuditReport"]
        validator = Draft202012Validator(schema)

        invalid_payload = {
            "file": "test.pdf",
            "status": "PASS",
            "scorecard": {
                "total_score": 90,
                "passing_threshold": 85,
                "verdict": "CONDITIONAL_APPROVAL"  # Not in enum
            },
            "checks": {
                "dimensions_and_bleed": {},
                "margin_safety_zone": {},
                "font_embedding": {},
                "image_resolution": {},
                "color_and_tac": {},
                "pdfx4_compliance": {},
                "layout_collisions": {}
            }
        }
        with self.assertRaises(ValidationError) as ctx:
            validator.validate(invalid_payload)
        self.assertIn("verdict", str(ctx.exception))

    def test_09_reject_preflight_score_out_of_bounds(self):
        """Inject total_score > 100 or < 0 -> Must fail validation."""
        schema = self.schemas["PreflightAuditReport"]
        validator = Draft202012Validator(schema)

        payload = {
            "file": "test.pdf",
            "status": "PASS",
            "scorecard": {
                "total_score": 105,  # Max 100
                "passing_threshold": 85,
                "verdict": "APPROVED_FOR_PRESS"
            },
            "checks": {
                "dimensions_and_bleed": {},
                "margin_safety_zone": {},
                "font_embedding": {},
                "image_resolution": {},
                "color_and_tac": {},
                "pdfx4_compliance": {},
                "layout_collisions": {}
            }
        }
        with self.assertRaises(ValidationError):
            validator.validate(payload)

        payload["scorecard"]["total_score"] = -10
        with self.assertRaises(ValidationError):
            validator.validate(payload)

    def test_10_reject_passport_missing_required_fields_and_min_contributions(self):
        """Inject Project Passport missing required fields or with fewer than 3 contributions -> Must fail."""
        schema = self.schemas["ProjectPassport"]
        validator = Draft202012Validator(schema)

        valid_passport = {
            "title": "Maison Bretonne",
            "typology": "Heritage Renovation",
            "location": "Finistère, France",
            "coordinates": "48°15'12\"N 04°08'45\"W",
            "year": "2026",
            "area_m2": 3200,
            "client": "Heritage Trust",
            "stage": "RIBA Stage 4",
            "candidate_role": "Lead Architect",
            "line_item_contributions": [
                "1:20 constructive wall section envelope detailing",
                "Breton granite stone ashlar stabilization schedule",
                "PMR universal accessibility compliance"
            ],
            "software_stack": ["Revit", "Rhino", "InDesign"],
            "work_authorization": "Permanent EU Citizen",
            "executive_premise": "Adaptive reuse of historical granite structure."
        }
        self.assertTrue(validator.is_valid(valid_passport))

        # Test missing candidate_role
        invalid_1 = json.loads(json.dumps(valid_passport))
        del invalid_1["candidate_role"]
        with self.assertRaises(ValidationError) as ctx:
            validator.validate(invalid_1)
        self.assertIn("candidate_role", str(ctx.exception))

        # Test line_item_contributions < 3
        invalid_2 = json.loads(json.dumps(valid_passport))
        invalid_2["line_item_contributions"] = ["Only one contribution"]
        with self.assertRaises(ValidationError) as ctx:
            validator.validate(invalid_2)
        self.assertIn("line_item_contributions", str(ctx.exception))


class TestCrossContractConsistencyAndNegativeGates(unittest.TestCase):
    """
    Empirically verifies cross-contract consistency between SKILL.md and all 5 persona files,
    ensuring negative rejection gates and tolerances are harmonized across the entire system.
    """

    @classmethod
    def setUpClass(cls):
        cls.skill_text = load_skill()
        cls.art_director_text = load_persona("art_director.md")
        cls.typographer_text = load_persona("typographer.md")
        cls.compositor_text = load_persona("compositor.md")
        cls.tectonic_detailer_text = load_persona("tectonic_detailer.md")
        cls.preflight_auditor_text = load_persona("preflight_auditor.md")
        cls.schemas = {}
        for f in [cls.art_director_text, cls.typographer_text, cls.compositor_text,
                  cls.tectonic_detailer_text, cls.preflight_auditor_text]:
            cls.schemas.update(extract_schemas_by_title(f))

    def test_01_cross_contract_5_acts_parity(self):
        """Verify 5-act narrative titles and enums match between SKILL.md and art_director.md."""
        acts = [
            "ACT_1_HOOK_AND_PASSPORT",
            "ACT_2_TERRITORIAL_CONTEXT",
            "ACT_3_SPATIAL_ANATOMY",
            "ACT_4_TECTONIC_PROOF",
            "ACT_5_LIVED_CLIMAX"
        ]
        schema_acts = self.schemas["SpreadBlueprint"]["properties"]["spreads"]["items"]["properties"]["act"]["enum"]
        self.assertEqual(sorted(acts), sorted(schema_acts))
        for act in acts:
            self.assertIn(act, self.art_director_text)

    def test_02_cross_contract_tripartite_font_roles(self):
        """Verify Tripartite font roles match between SKILL.md and typographer.md."""
        for role in ["Structural Grotesque", "Rationalist Serif", "Technical Monospace"]:
            self.assertIn(role, self.skill_text)
            self.assertIn(role, self.typographer_text)

    def test_03_cross_contract_binding_mechanics(self):
        """Verify 4 binding styles match between SKILL.md and compositor.md."""
        binding_enums = self.schemas["CompositorInput"]["properties"]["binding_spec"]["properties"]["binding_type"]["enum"]
        expected_bindings = ["SMYTH_SEWN", "PERFECT_BOUND", "LAY_FLAT", "SADDLE_STITCHED"]
        self.assertEqual(sorted(binding_enums), sorted(expected_bindings))
        for b in ["Smyth-Sewn", "Perfect Bound", "Lay-Flat", "Saddle-Stitch"]:
            self.assertIn(b.lower(), self.skill_text.lower())
            self.assertIn(b.lower(), self.compositor_text.lower())

    def test_04_cross_contract_iso_128_stroke_hierarchy(self):
        """Verify metric stroke widths match between SKILL.md and tectonic_detailer.md."""
        strokes = ["0.70 mm", "0.50 mm", "0.35 mm", "0.25 mm", "0.13 mm"]
        for s in strokes:
            self.assertIn(s, self.skill_text)
            self.assertIn(s, self.tectonic_detailer_text)

    def test_05_cross_contract_preflight_thresholds(self):
        """Verify TAC <= 320%, bleed = 3.0mm, safety = 5.0mm, score >= 85 match across contracts."""
        self.assertIn("320%", self.skill_text)
        self.assertTrue("320" in self.preflight_auditor_text)
        self.assertIn("3.0", self.skill_text)
        self.assertIn("3.0", self.preflight_auditor_text)
        self.assertIn("5.0", self.skill_text)
        self.assertIn("5.0", self.preflight_auditor_text)
        self.assertIn("85", self.skill_text)
        self.assertIn("85", self.preflight_auditor_text)

    def test_06_reject_spread_whitespace_below_verso_recto_minimum(self):
        """Inject target_whitespace_pct = 15.0% on verso (< 25.0% minimum) -> Must fail validation."""
        schema = self.schemas["SpreadBlueprint"]
        validator = Draft202012Validator(schema)

        payload = {
            "blueprint_id": "BP_01",
            "project_title": "Maison",
            "whitespace_budget_pct": 30.0,
            "palette": {
                "canvas_bone": "#F8F8F5",
                "ink_graphite": "#111110",
                "ink_secondary": "#55544E",
                "hairline": "#DDD9D0",
                "accent": "#7A4D3B"
            },
            "grid_spec": {
                "columns": 12,
                "gutter_mm": 4.5,
                "margin_inner_mm": 22.0,
                "margin_outer_mm": 18.0,
                "margin_top_mm": 16.0,
                "margin_bottom_mm": 18.0
            },
            "spreads": [
                {
                    "spread_index": 1,
                    "act": "ACT_1_HOOK_AND_PASSPORT",
                    "archetype": "THE_PASSPORT",
                    "verso": {"role": "COGNITIVE_ANCHOR", "target_whitespace_pct": 15.0, "components": []},  # Below 25.0
                    "recto": {"role": "VISUAL_LEAD", "target_whitespace_pct": 30.0, "components": []}
                },
                {
                    "spread_index": 2,
                    "act": "ACT_2_TERRITORIAL_CONTEXT",
                    "archetype": "THE_CARTOGRAPHIC_CONTEXT",
                    "verso": {"role": "COGNITIVE_ANCHOR", "target_whitespace_pct": 30.0, "components": []},
                    "recto": {"role": "VISUAL_LEAD", "target_whitespace_pct": 30.0, "components": []}
                },
                {
                    "spread_index": 3,
                    "act": "ACT_4_TECTONIC_PROOF",
                    "archetype": "THE_CONSTRUCTIVE_PROOF",
                    "verso": {"role": "ANALYTICAL_DENSITY", "target_whitespace_pct": 25.0, "components": []},
                    "recto": {"role": "EXPANSIVE_HERO", "target_whitespace_pct": 30.0, "components": []}
                }
            ]
        }
        with self.assertRaises(ValidationError) as ctx:
            validator.validate(payload)
        self.assertIn("target_whitespace_pct", str(ctx.exception))

    def test_07_reject_missing_target_u_value(self):
        """Inject TectonicDetailerInput missing target_u_value -> Must fail validation."""
        schema = self.schemas["TectonicDetailerInput"]
        validator = Draft202012Validator(schema)

        invalid_input = {
            "drawing_type": "WALL_SECTION_1_20",
            "scale": "1:20",
            "viewport_dimensions_mm": {"width": 200.0, "height": 300.0},
            "assembly_specification": {
                "layers": []
                # missing target_u_value
            }
        }
        with self.assertRaises(ValidationError) as ctx:
            validator.validate(invalid_input)
        self.assertIn("target_u_value", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
