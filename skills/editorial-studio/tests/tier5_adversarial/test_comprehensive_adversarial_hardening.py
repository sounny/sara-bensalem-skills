"""
tests/tier5_adversarial/test_comprehensive_adversarial_hardening.py
Milestone 7 Tier 5 Comprehensive Adversarial Hardening Test Suite.
Author: Challenger 1 (Empirical Challenger M7)

Exhaustively verifies:
1. Multi-lingual and special character support in Project Passport (Arabic, accents, unicode, CJK).
2. Extreme binding creep calculations (e.g. 1000 pages, zero caliper, safety clamps).
3. Extreme vector downsampling ratios (Sr = 0.001, Sr = 100.0, boundary thresholds).
4. CLI flag combinations and error propagation in compile.py and audit_publication.py.
5. Malformed, damaged, and corrupt PDF inputs to PublicationAuditor.
"""

import os
import sys
import json
import math
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

# Ensure project root in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import fitz

from engine.grid.creep_calculator import calculate_gutter_creep, SUPPORTED_BINDING_TYPES
from engine.grid.baseline import snap_to_baseline, snap_container_height, compute_leading
from engine.drafting.iso_128 import (
    downsample_stroke,
    downsample_hatch,
    filter_annotations,
    downsample_strokes,
    MIN_STROKE_MM,
    MIN_STROKE_PT,
    STANDARD_ISO_128_STROKES
)
from engine.drafting.project_passport import (
    ProjectPassport,
    validate_passport,
    generate_svg_badge,
    generate_typst_block,
    generate_html_component,
    _xml_escape,
    PASSPORT_REQUIRED_FIELDS
)
from engine.compile import (
    compile_document,
    parse_bleed_to_mm,
    resolve_engine_for_input
)
from preflight.audit_publication import (
    PublicationAuditor,
    audit_pdf,
    check_aabb_intersection,
    compute_contrast_ratio,
    evaluate_text_image_collision,
    evaluate_image_resolution
)


# ==============================================================================
# CATEGORY 1: Multi-Lingual & Special Character Support in Project Passport
# ==============================================================================

class TestMultilingualSpecialCharPassport(unittest.TestCase):
    """
    Verifies that Project Passport robustly handles Right-to-Left (Arabic),
    accented European characters, CJK scripts, and complex Unicode typography entities.
    """

    def setUp(self):
        self.arabic_data = {
            "title": "مجمع الفنون والتصميم الإسلامي المعاصر — Al-Markaz",
            "typology": "Cultural Center & Spatial Archive (مركز ثقافي)",
            "location": "أبو ظبي، الإمارات العربية المتحدة (Abu Dhabi, UAE)",
            "coordinates": "24°28'0\"N 54°22'0\"E",
            "year": "2026",
            "area_m2": 42500.75,
            "client": "دائرة الثقافة والسياحة - أبوظبي",
            "stage": "RIBA Stage 4 / التنفيذ الفني",
            "candidate_role": "Lead Tectonic Detailer & مهندس تفاصيل إنشائية",
            "line_item_contributions": [
                "تصميم تفاصيل الإكساء الحجري والوصلات الإنشائية بمقياس 1:20 مع فواصل العزل",
                "تطوير الواجهات الحركية الذكية المستوحاة من المشربية مع كفاءة الطاقة",
                "إعداد المخططات التنفيذية وجداول الكميات والتنسيق الكهروميكانيكي المتكامل"
            ],
            "software_stack": ["Revit", "Rhino", "Typst", "AutoCAD 2026"],
            "work_authorization": "UAE Golden Visa / تصريح عمل كامل",
            "executive_premise": "تطوير صرح معماري يدمج الهوية التكتونية التراثية مع الفيزياء البيوكليماتية المعاصرة لتحقيق أقصى كفاءة بيئية."
        }

        self.european_data = {
            "title": "Bibliothèque Nationale & Centre Élysée-Grand-Paris",
            "typology": "Équipement Public d'Envergure Métropolitaine",
            "location": "München, Großhadern (Bayern) / Paris (Île-de-France) / København Ø",
            "coordinates": "48°51'24\"N 2°21'07\"E",
            "year": "2025-2026",
            "area_m2": 18750.0,
            "client": "Société du Grand Paris & Ministère de l'Enseignement",
            "stage": "Loi MOP Phase PRO / DCE (HOAI Leistungsphase 5)",
            "candidate_role": "Architecte Chef de Projet Détails & Façades Hygrothermiques",
            "line_item_contributions": [
                "Modélisation des nœuds constructifs 1:20 intégrant rupteurs Schöck Isokorb T-type",
                "Calcul hygrothermique Glaser selon RE2020 avec membrane d'étanchéité EPDM 1.52mm",
                "Coordination des menuiseries intérieures 1:5 avec joints creux d'ombre 3mm"
            ],
            "software_stack": ["Archicad", "Typst", "Python / Shapely", "Vectorworks"],
            "work_authorization": "Citoyen UE / Carte d'Identité Française & Titre de Séjour",
            "executive_premise": "Conception d'une enveloppe bioclimatique décarbonée en pisé stabilisé et ossature bois lamellé-collé certifié FSC."
        }

        self.cjk_data = {
            "title": "东京国立新美术馆扩建项目 — The National Art Center Expansion",
            "typology": "Museum & Spatial Research Laboratory (国立新美術館)",
            "location": "北京市朝阳区 & 東京都港区六本木 7-22-2",
            "coordinates": "35°39'55\"N 139°43'35\"E",
            "year": "2026",
            "area_m2": 31200.0,
            "client": "National Museum Authority of East Asia (国立美術館)",
            "stage": "AIA Stage CD / 実施設計",
            "candidate_role": "Senior Façade Engineer & 意匠設計主任",
            "line_item_contributions": [
                "Development of parametric seismic drift bellows for 4-sided structural silicone glazing",
                "Detailed acoustic baffles for primary mechanical ducts meeting NC-30 standards",
                "Full compliance auditing for universal wheelchair accessibility (PMR 1500mm)"
            ],
            "software_stack": ["Revit 2026", "Rhino", "Typst Engine", "Catia"],
            "work_authorization": "Permanent Resident / 永住者",
            "executive_premise": "Integration of resilient seismic detailing with passive daylight harvesting louvers achieving net-zero operational carbon emissions."
        }

    def test_01_arabic_passport_validation(self):
        """Arabic passport data must pass Draft 2020-12 schema validation with zero errors."""
        passport = ProjectPassport(self.arabic_data)
        errors = passport.validate()
        self.assertEqual(errors, [], f"Arabic passport had validation errors: {errors}")
        self.assertTrue(passport.is_valid())

    def test_02_arabic_passport_to_svg_well_formed_xml(self):
        """Arabic passport SVG rendering must produce well-formed, parseable XML."""
        passport = ProjectPassport(self.arabic_data)
        svg_str = passport.to_svg()
        self.assertIsInstance(svg_str, str)
        self.assertIn("<svg", svg_str)
        root = ET.fromstring(svg_str)
        self.assertEqual(root.tag.split("}")[-1], "svg")

    def test_03_arabic_passport_to_html_and_typst(self):
        """Arabic passport must render without error into HTML component and Typst block."""
        passport = ProjectPassport(self.arabic_data)
        html_str = passport.to_html()
        typst_str = passport.to_typst()
        self.assertIn("project-passport", html_str)
        self.assertIn("#block(", typst_str)
        self.assertIn("مجمع الفنون", html_str)
        self.assertIn("مجمع الفنون", typst_str)

    def test_04_european_diacritics_validation_and_svg(self):
        """European accented text (é, è, ü, ß, ø, ç) must validate and generate valid SVG."""
        passport = ProjectPassport(self.european_data)
        errors = passport.validate()
        self.assertEqual(errors, [])
        svg_str = passport.to_svg()
        root = ET.fromstring(svg_str)
        self.assertIsNotNone(root)
        self.assertIn("Bibliothèque", svg_str)
        self.assertIn("München", svg_str)

    def test_05_cjk_scripts_validation_and_svg(self):
        """CJK scripts (Chinese, Japanese, Korean) must validate and render valid SVG."""
        passport = ProjectPassport(self.cjk_data)
        errors = passport.validate()
        self.assertEqual(errors, [])
        svg_str = passport.to_svg()
        root = ET.fromstring(svg_str)
        self.assertIsNotNone(root)
        self.assertIn("东京国立新美术馆", svg_str)

    def test_06_xml_escape_special_characters(self):
        """_xml_escape safely sanitizes ampersands, quotes, brackets."""
        raw = 'Foster & Partners <Tectonic> "Studio\'s" © 2026 — ±5mm & 100%'
        esc = _xml_escape(raw)
        self.assertIn("&amp;", esc)
        self.assertIn("&quot;", esc)
        self.assertIn("&lt;", esc)
        root = ET.fromstring(f"<text>{esc}</text>")
        self.assertEqual(root.text, raw)

    def test_07_json_roundtrip_preserves_unicode(self):
        """JSON roundtrip preserves Arabic and Unicode characters."""
        passport = ProjectPassport(self.arabic_data)
        json_repr = passport.to_json()
        reconstructed = ProjectPassport.from_json(json_repr)
        self.assertEqual(passport.data["title"], reconstructed.data["title"])


# ==============================================================================
# CATEGORY 2: Extreme Binding Creep Calculations
# ==============================================================================

class TestExtremeBindingCreepCalculations(unittest.TestCase):
    """
    Adversarial stress-testing of bindery physics and gutter creep calculus:
    - 1,000 page monographs (Smyth-sewn and Perfect-bound).
    - Zero paper caliper (0.0mm) across all binding types.
    - Outer margin safety clamping (>= 5.0mm).
    - Saddle-stitch N > 64 rejection and boundary checks.
    """

    def test_01_extreme_1000_pages_smyth_sewn_cyclical_boundedness(self):
        """
        In Smyth-sewn binding of 1000 pages, creep MUST remain strictly bounded
        within each 16-page signature (leaf <= 3), never accumulating across signatures.
        """
        N = 1000
        caliper = 0.15
        base_inner = 20.0
        base_outer = 18.0

        for p in [1, 8, 16, 17, 24, 32, 496, 500, 512, 992, 999, 1000]:
            res = calculate_gutter_creep(
                page=p,
                total_pages=N,
                binding_type="SMYTH_SEWN",
                paper_caliper_mm=caliper,
                signature_size=16,
                base_inner_margin_mm=base_inner,
                base_outer_margin_mm=base_outer
            )
            self.assertLessEqual(res["creep_offset_mm"], caliper * 4)
            self.assertGreaterEqual(res["outer_margin_mm"], 5.0)
            self.assertGreaterEqual(res["inner_margin_mm"], base_inner)

    def test_02_extreme_1000_pages_perfect_bound_single_leaf_zero_shingle(self):
        """
        In 1000-page single-leaf PUR binding, individual cut leaves have zero shingle;
        inner margin expands by spine glue draw (G_draw = 8.0mm), outer margin remains base.
        """
        N = 1000
        res = calculate_gutter_creep(
            page=500,
            total_pages=N,
            binding_type="PERFECT_BOUND",
            paper_caliper_mm=0.15,
            gutter_draw_mm=8.0,
            base_inner_margin_mm=20.0,
            base_outer_margin_mm=18.0,
            folded_signature=False
        )
        self.assertEqual(res["shingle_mm"], 0.0)
        self.assertEqual(res["gutter_draw_mm"], 8.0)
        self.assertEqual(res["inner_margin_mm"], 28.0)
        self.assertEqual(res["outer_margin_mm"], 18.0)

    def test_03_zero_caliper_all_supported_binding_types(self):
        """Zero paper caliper (0.0mm) must yield strictly 0.0mm creep across all bindings."""
        for b_type in ["SMYTH_SEWN", "PERFECT_BOUND", "LAY_FLAT", "SADDLE_STITCHED"]:
            total_p = 64 if b_type == "SADDLE_STITCHED" else 200
            for p in [1, total_p // 2, total_p]:
                res = calculate_gutter_creep(
                    page=p,
                    total_pages=total_p,
                    binding_type=b_type,
                    paper_caliper_mm=0.0,
                    base_inner_margin_mm=22.0,
                    base_outer_margin_mm=18.0
                )
                self.assertEqual(res["creep_offset_mm"], 0.0)
                self.assertEqual(res["shingle_mm"], 0.0)
                if b_type == "PERFECT_BOUND":
                    self.assertEqual(res["inner_margin_mm"], 30.0)
                else:
                    self.assertEqual(res["inner_margin_mm"], 22.0)
                self.assertEqual(res["outer_margin_mm"], 18.0)

    def test_04_outer_margin_safety_clamping_under_extreme_creep(self):
        """Outer margin MUST be clamped to >= 5.0mm safety threshold."""
        res = calculate_gutter_creep(
            page=8,
            total_pages=64,
            binding_type="SADDLE_STITCHED",
            paper_caliper_mm=2.5,
            base_inner_margin_mm=20.0,
            base_outer_margin_mm=6.0
        )
        self.assertEqual(res["outer_margin_mm"], 5.0)

    def test_05_lay_flat_invariant_across_all_pages(self):
        """Lay-flat binding must produce zero creep and constant margins on all 1000 pages."""
        for p in [1, 250, 500, 750, 1000]:
            res = calculate_gutter_creep(
                page=p,
                total_pages=1000,
                binding_type="LAY_FLAT",
                paper_caliper_mm=0.25,
                base_inner_margin_mm=25.0,
                base_outer_margin_mm=20.0
            )
            self.assertEqual(res["inner_margin_mm"], 25.0)
            self.assertEqual(res["outer_margin_mm"], 20.0)
            self.assertEqual(res["creep_offset_mm"], 0.0)
            self.assertEqual(res["gutter_draw_mm"], 0.0)

    def test_06_saddle_stitch_strictly_rejects_pages_greater_than_64(self):
        """Saddle-stitched binding must raise ValueError for N > 64 pages."""
        for n in [65, 66, 80, 100, 500]:
            with self.assertRaises(ValueError) as ctx:
                calculate_gutter_creep(page=1, total_pages=n, binding_type="SADDLE_STITCHED")
            self.assertIn("Saddle-stitched binding is strictly restricted", str(ctx.exception))

    def test_07_invalid_page_indices_raise_value_error(self):
        """Page indices out of [1, total_pages] or total_pages < 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_gutter_creep(page=0, total_pages=10, binding_type="SMYTH_SEWN")
        with self.assertRaises(ValueError):
            calculate_gutter_creep(page=11, total_pages=10, binding_type="SMYTH_SEWN")
        with self.assertRaises(ValueError):
            calculate_gutter_creep(page=1, total_pages=0, binding_type="SMYTH_SEWN")


# ==============================================================================
# CATEGORY 3: Extreme Vector Downsampling Ratios (Sr = 0.001 and Sr = 100.0)
# ==============================================================================

class TestExtremeVectorDownsamplingRatios(unittest.TestCase):
    """
    Verifies scale-aware vector downsampling algorithms across extreme boundaries:
    - Micro-scale downsampling: Sr = 0.001 (1:1000 reduction).
    - Macro-scale upsampling: Sr = 100.0 (100x enlargement).
    - Annotation culling filters and hatch decimation / poché replacement.
    """

    def test_01_extreme_downsample_stroke_clamped_to_min_stroke(self):
        """At Sr = 0.001, every ISO 128 stroke weight must be clamped to >= MIN_STROKE_MM (0.08mm)."""
        for stroke in STANDARD_ISO_128_STROKES:
            w_eff = downsample_stroke(w_native_mm=stroke, scale_factor=0.001)
            self.assertAlmostEqual(w_eff, MIN_STROKE_MM, places=5)

    def test_02_extreme_upsample_stroke_scales_proportionally(self):
        """At Sr = 100.0, stroke weights scale proportionally without artificial cap."""
        for stroke in [0.13, 0.25, 0.35, 0.50, 0.70]:
            w_eff = downsample_stroke(w_native_mm=stroke, scale_factor=100.0)
            self.assertAlmostEqual(w_eff, stroke * 100.0, places=5)

    def test_03_extreme_downsample_hatch_converts_to_poche(self):
        """At Sr = 0.001, native 10mm hatch spacing scales to 0.01mm < 0.35mm -> POCHE_REPLACE."""
        res = downsample_hatch(native_spacing_mm=10.0, scale_factor=0.001)
        self.assertEqual(res["action"], "POCHE_REPLACE")
        self.assertIsNone(res["spacing_mm"])
        self.assertEqual(res["fill"], "#F1F1EB")

    def test_04_extreme_upsample_hatch_retains_lines(self):
        """At Sr = 100.0, native 1mm hatch spacing scales to 100mm >= 0.75mm -> RETAIN."""
        res = downsample_hatch(native_spacing_mm=1.0, scale_factor=100.0)
        self.assertEqual(res["action"], "RETAIN")
        self.assertEqual(res["spacing_mm"], 100.0)
        self.assertEqual(res["fill"], "none")

    def test_05_annotation_filtering_levels_at_boundaries(self):
        """Verifies exact annotation levels across threshold boundaries."""
        self.assertEqual(filter_annotations(0.001), "GRAPHIC_SCALE_BAR_ONLY")
        self.assertEqual(filter_annotations(0.399), "GRAPHIC_SCALE_BAR_ONLY")
        self.assertEqual(filter_annotations(0.400), "MAJOR_DIMENSIONS_ONLY")
        self.assertEqual(filter_annotations(0.749), "MAJOR_DIMENSIONS_ONLY")
        self.assertEqual(filter_annotations(0.750), "FULL_ANNOTATIONS")
        self.assertEqual(filter_annotations(100.0), "FULL_ANNOTATIONS")

    def test_06_svg_downsample_at_0_001_clamps_strokes_in_xml(self):
        """Processing SVG through downsample_strokes at Sr=0.001 clamps stroke-widths in XML."""
        sample_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
          <line x1="0" y1="0" x2="100" y2="100" stroke="#111110" stroke-width="0.70mm" />
          <rect x="10" y="10" width="80" height="80" stroke="#33322E" stroke-width="0.35mm" />
        </svg>"""
        processed_svg = downsample_strokes(sample_svg, target_scale=0.001)
        root = ET.fromstring(processed_svg)
        lines = root.findall(".//{http://www.w3.org/2000/svg}line") + root.findall(".//line")
        self.assertTrue(len(lines) > 0)
        sw = lines[0].get("stroke-width", "")
        val = float(sw.replace("mm", "").replace("pt", ""))
        self.assertGreaterEqual(val, 0.08)

    def test_07_invalid_scale_factors_raise_value_error(self):
        """Scale factors <= 0.0 or non-numeric types must raise ValueError."""
        with self.assertRaises(ValueError):
            downsample_stroke(0.5, 0.0)
        with self.assertRaises(ValueError):
            downsample_stroke(0.5, -0.5)
        with self.assertRaises(ValueError):
            downsample_stroke(0.5, False)
        with self.assertRaises(ValueError):
            downsample_strokes("<svg></svg>", target_scale=-1.0)


# ==============================================================================
# CATEGORY 4: CLI Flag Combinations & Error Propagation
# ==============================================================================

class TestCLIExecutionAndErrorPropagation(unittest.TestCase):
    """
    Verifies CLI invocation contracts, exit codes, and error propagation:
    - compile.py CLI argument parsing and error exits.
    - audit_publication.py CLI argument parsing and error exits.
    - Bleed parsing robustness across formatted strings.
    """

    def test_01_parse_bleed_to_mm_edge_cases(self):
        """parse_bleed_to_mm handles diverse string inputs cleanly."""
        self.assertEqual(parse_bleed_to_mm("3mm"), 3.0)
        self.assertEqual(parse_bleed_to_mm("3.0mm"), 3.0)
        self.assertEqual(parse_bleed_to_mm("5"), 5.0)
        self.assertEqual(parse_bleed_to_mm("0mm"), 0.0)
        self.assertEqual(parse_bleed_to_mm("0"), 0.0)
        self.assertEqual(parse_bleed_to_mm(""), 3.0)
        self.assertEqual(parse_bleed_to_mm(None), 3.0)
        self.assertEqual(parse_bleed_to_mm("invalid_text"), 3.0)

    def test_02_compile_cli_missing_input_exits_code_2(self):
        """Invoking compile.py without -i or -m must exit with code 2."""
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, "engine", "compile.py")]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("Either --input or --manifest must be specified", proc.stderr)

    def test_03_compile_cli_nonexistent_file_exits_code_1(self):
        """Invoking compile.py with non-existent file must exit with code 1."""
        cmd = [
            sys.executable,
            os.path.join(PROJECT_ROOT, "engine", "compile.py"),
            "-i", os.path.join(PROJECT_ROOT, "nonexistent_source_file.typ")
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("not found", proc.stderr.lower())

    def test_04_compile_cli_empty_file_exits_code_1(self):
        """Invoking compile.py with a 0-byte empty file must exit with code 1."""
        with tempfile.NamedTemporaryFile(suffix=".typ", delete=False) as f:
            empty_path = f.name

        try:
            cmd = [
                sys.executable,
                os.path.join(PROJECT_ROOT, "engine", "compile.py"),
                "-i", empty_path
            ]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("empty", proc.stderr.lower())
        finally:
            if os.path.exists(empty_path):
                os.unlink(empty_path)

    def test_05_compile_cli_engine_mismatch_rejection(self):
        """Compiling an HTML file with --engine typst must raise error and exit code 1."""
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            f.write(b"<!DOCTYPE html><html><body>Content</body></html>")
            html_path = f.name

        try:
            cmd = [
                sys.executable,
                os.path.join(PROJECT_ROOT, "engine", "compile.py"),
                "-i", html_path,
                "-e", "typst"
            ]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("Mismatched engine", proc.stderr)
        finally:
            if os.path.exists(html_path):
                os.unlink(html_path)

    def test_06_audit_cli_missing_args_exits_code_2(self):
        """Invoking audit_publication.py without arguments must exit with code 2."""
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py")]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(proc.returncode, 2)

    def test_07_audit_cli_nonexistent_file_exits_code_1_with_fail_report(self):
        """Invoking audit_publication.py with non-existent file exits code 1 and outputs structured FAIL."""
        cmd = [
            sys.executable,
            os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"),
            os.path.join(PROJECT_ROOT, "nonexistent_doc.pdf")
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("Overall Status: FAIL", proc.stdout)

    def test_08_audit_cli_json_export_on_failure(self):
        """audit_publication.py --json exports structured JSON even when audit fails."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as jf:
            json_out = jf.name

        try:
            cmd = [
                sys.executable,
                os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"),
                os.path.join(PROJECT_ROOT, "nonexistent_doc.pdf"),
                "--json", json_out
            ]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.assertEqual(proc.returncode, 1)
            self.assertTrue(os.path.exists(json_out))
            with open(json_out, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["status"], "FAIL")
            self.assertIn("checks", data)
            self.assertEqual(data["summary"]["failed"], 7)
        finally:
            if os.path.exists(json_out):
                os.unlink(json_out)


# ==============================================================================
# CATEGORY 5: Malformed & Damaged PDF Inputs to PublicationAuditor
# ==============================================================================

class TestMalformedDamagedPDFInputs(unittest.TestCase):
    """
    Verifies that PublicationAuditor and audit_pdf handle corrupt, damaged,
    or invalid PDF files gracefully without unhandled exceptions.
    """

    def test_01_zero_byte_empty_pdf_handled_gracefully(self):
        """0-byte empty file triggers structured FAIL report with error details."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            empty_path = f.name

        try:
            with self.assertRaises(ValueError) as ctx:
                PublicationAuditor(empty_path)
            self.assertIn("empty (0 bytes)", str(ctx.exception))

            report = audit_pdf(empty_path)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["scorecard"]["total_score"], 0)
            self.assertEqual(report["scorecard"]["verdict"], "REJECTED")
            self.assertIn("ValueError", report["error"])
        finally:
            if os.path.exists(empty_path):
                os.unlink(empty_path)

    def test_02_corrupted_binary_data_pdf_handled_gracefully(self):
        """Corrupted PDF containing random bytes triggers FAIL report."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"%PDF-1.4\nGARBAGE_BYTES_BINARY_CORRUPT\x00\xff\xfe\x01\x02\x03")
            corrupt_path = f.name

        try:
            report = audit_pdf(corrupt_path)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["scorecard"]["total_score"], 0)
            self.assertIn("error", report)
        finally:
            if os.path.exists(corrupt_path):
                os.unlink(corrupt_path)

    def test_03_plain_text_renamed_as_pdf(self):
        """A plain text file renamed with .pdf extension triggers FAIL report."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"This is just a plain text document, definitely not a valid PDF file.\n")
            fake_path = f.name

        try:
            report = audit_pdf(fake_path)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["scorecard"]["total_score"], 0)
        finally:
            if os.path.exists(fake_path):
                os.unlink(fake_path)

    def test_04_auditor_report_schema_contract_preserved_on_failure(self):
        """
        Even on corrupted inputs, the returned report MUST satisfy the exact schema
        contract: file, status, summary, scorecard, checks (7 checks each with status).
        """
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"%PDF-CORRUPT-RANDOM-DATA")
            bad_path = f.name

        try:
            report = audit_pdf(bad_path)
            self.assertIn("file", report)
            self.assertIn("status", report)
            self.assertIn("summary", report)
            self.assertIn("scorecard", report)
            self.assertIn("checks", report)

            required_checks = [
                "dimensions_and_bleed",
                "margin_safety_zone",
                "font_embedding",
                "image_resolution",
                "color_and_tac",
                "pdfx4_compliance",
                "layout_collisions"
            ]
            for chk in required_checks:
                self.assertIn(chk, report["checks"], f"Missing check dimension: {chk}")
                self.assertEqual(report["checks"][chk]["status"], "FAIL")
        finally:
            if os.path.exists(bad_path):
                os.unlink(bad_path)

    def test_05_aabb_bounding_box_edge_cases(self):
        """Edge case AABB collision evaluations: touching edges, intentional overlay."""
        box_a = [0.0, 0.0, 50.0, 50.0]
        box_b = [50.0, 0.0, 100.0, 50.0]
        self.assertFalse(check_aabb_intersection(box_a, box_b))

        box_inner = [10.0, 10.0, 40.0, 40.0]
        self.assertTrue(check_aabb_intersection(box_a, box_inner))

        res = evaluate_text_image_collision(
            text_box=[10.0, 10.0, 40.0, 40.0],
            image_box=[0.0, 0.0, 50.0, 50.0],
            text_lum=0.95,
            bg_lum=0.05
        )
        self.assertTrue(res["collides"])
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["reason"], "INTENTIONAL_LEGIBLE_OVERLAY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
