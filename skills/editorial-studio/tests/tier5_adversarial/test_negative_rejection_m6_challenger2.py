"""
tests/tier5_adversarial/test_negative_rejection_m6_challenger2.py
Challenger 2 Empirical Verification Test Suite: Negative Rejection, Re-compilation Stress,
and Preflight Defect Sensitivity Harness for Milestone 6 (Production Demonstration Monograph).

Authoritative Requirements:
- ORIGINAL_REQUEST.md §R1-R6, Acceptance Criteria
- PROJECT.md §Milestone 6 (Examples/Monograph)
- preflight/audit_publication.py (Sara Bensalem 100-Point Audit Rubric)
- engine/compile.py (Unified Dual-Engine Compilation CLI)

Test Dimensions:
1. Re-compilation Stress Test (Typst & Paged.js with custom bleed, output paths, benchmarks)
2. Clean Monograph Preflight Baseline (Typst & Paged.js 100/100, 0 failures, exit code 0)
3. Defect Sensitivity & Negative Rejection (Safe margin breaches, low-res images, TAC > 320%, untagged RGB)
4. Monograph Asset Integrity (SVG XML & ISO 128 strokes, CMYK mode, DPI >= 300, TAC <= 320%)
"""

import os
import sys
import tempfile
import subprocess
import xml.etree.ElementTree as ET
import unittest
import numpy as np
from PIL import Image
import fitz

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engine.compile import compile_document
from preflight.audit_publication import audit_pdf, MM_TO_PT


class TestMonographRecompilationStress(unittest.TestCase):
    """
    Stress-tests compilation of monograph source templates (Typst & Paged.js)
    with non-standard bleed allowances and custom destinations.
    """

    def setUp(self):
        self.typst_src = os.path.join(PROJECT_ROOT, "examples", "monograph", "source.typ")
        self.html_src = os.path.join(PROJECT_ROOT, "examples", "monograph", "source.html")
        self.assertTrue(os.path.isfile(self.typst_src), f"Missing Typst source: {self.typst_src}")
        self.assertTrue(os.path.isfile(self.html_src), f"Missing HTML source: {self.html_src}")

    def test_01_typst_recompile_custom_bleed_5mm(self):
        """Verify Typst recompilation with 5.0mm bleed generates valid 10-page PDF with 5mm bleed delta."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_pdf = os.path.join(tmpdir, "typst_bleed_5mm.pdf")
            res = compile_document(
                input_path=self.typst_src,
                output_path=out_pdf,
                engine="typst",
                bleed="5mm",
                benchmark=True
            )
            self.assertTrue(res["success"])
            self.assertEqual(res["page_count"], 10)
            self.assertLess(res["duration_sec"], 3.0, "Typst compilation must complete in < 3.0s")
            self.assertTrue(os.path.isfile(out_pdf))
            self.assertGreater(os.path.getsize(out_pdf), 10240)

            doc = fitz.open(out_pdf)
            self.assertEqual(len(doc), 10)
            p0 = doc[0]
            tb = p0.trimbox
            bb = p0.bleedbox
            delta_pt = tb.x0 - bb.x0
            delta_mm = delta_pt * 25.4 / 72.0
            self.assertAlmostEqual(delta_mm, 5.0, places=1)
            doc.close()

    def test_02_typst_recompile_custom_bleed_2mm(self):
        """Verify Typst recompilation with 2.0mm bleed generates valid 10-page PDF with 2mm bleed delta."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_pdf = os.path.join(tmpdir, "typst_bleed_2mm.pdf")
            res = compile_document(
                input_path=self.typst_src,
                output_path=out_pdf,
                engine="typst",
                bleed="2mm",
                benchmark=True
            )
            self.assertTrue(res["success"])
            self.assertEqual(res["page_count"], 10)
            self.assertLess(res["duration_sec"], 3.0)

            doc = fitz.open(out_pdf)
            p0 = doc[0]
            delta_pt = p0.trimbox.x0 - p0.bleedbox.x0
            delta_mm = delta_pt * 25.4 / 72.0
            self.assertAlmostEqual(delta_mm, 2.0, places=1)
            doc.close()

    def test_03_pagedjs_recompile_custom_bleed_5mm(self):
        """Verify Paged.js recompilation with 5.0mm bleed generates valid 10-page PDF with 5mm bleed delta."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_pdf = os.path.join(tmpdir, "pagedjs_bleed_5mm.pdf")
            res = compile_document(
                input_path=self.html_src,
                output_path=out_pdf,
                engine="pagedjs",
                bleed="5mm",
                benchmark=True
            )
            self.assertTrue(res["success"])
            self.assertEqual(res["page_count"], 10)
            self.assertTrue(os.path.isfile(out_pdf))
            self.assertGreater(os.path.getsize(out_pdf), 10240)

            doc = fitz.open(out_pdf)
            self.assertEqual(len(doc), 10)
            p0 = doc[0]
            delta_pt = p0.trimbox.x0 - p0.bleedbox.x0
            delta_mm = delta_pt * 25.4 / 72.0
            self.assertAlmostEqual(delta_mm, 5.0, places=1)
            doc.close()

    def test_04_pagedjs_recompile_custom_bleed_2mm(self):
        """Verify Paged.js recompilation with 2.0mm bleed generates valid 10-page PDF with 2mm bleed delta."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_pdf = os.path.join(tmpdir, "pagedjs_bleed_2mm.pdf")
            res = compile_document(
                input_path=self.html_src,
                output_path=out_pdf,
                engine="pagedjs",
                bleed="2mm",
                benchmark=True
            )
            self.assertTrue(res["success"])
            self.assertEqual(res["page_count"], 10)

            doc = fitz.open(out_pdf)
            p0 = doc[0]
            delta_pt = p0.trimbox.x0 - p0.bleedbox.x0
            delta_mm = delta_pt * 25.4 / 72.0
            self.assertAlmostEqual(delta_mm, 2.0, places=1)
            doc.close()

    def test_05_unified_compile_both_engines(self):
        """Verify unified CLI dispatcher compiles both engines when engine='both'."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_combined = os.path.join(tmpdir, "monograph_combined.pdf")
            res = compile_document(
                input_path=self.typst_src,
                output_path=out_combined,
                engine="both",
                bleed="3mm"
            )
            self.assertTrue(res["success"])
            self.assertTrue(res["outputs"]["typst"]["success"])
            self.assertTrue(res["outputs"]["pagedjs"]["success"])
            self.assertEqual(res["page_count"], 10)


class TestPreflightCleanMonographs(unittest.TestCase):
    """
    Verifies that unmodified production monograph deliverables achieve 100/100
    Sara Bensalem score, status PASS, and CLI exit code 0.
    """

    def setUp(self):
        self.typst_pdf = os.path.join(PROJECT_ROOT, "examples", "monograph", "monograph_typst.pdf")
        self.pagedjs_pdf = os.path.join(PROJECT_ROOT, "examples", "monograph", "monograph_pagedjs.pdf")
        self.assertTrue(os.path.isfile(self.typst_pdf), f"Missing: {self.typst_pdf}")
        self.assertTrue(os.path.isfile(self.pagedjs_pdf), f"Missing: {self.pagedjs_pdf}")

    def test_01_clean_typst_monograph_score_100(self):
        """Clean monograph_typst.pdf scores 100/100 and passes all 7 prepress checks."""
        res = audit_pdf(self.typst_pdf)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["scorecard"]["total_score"], 100)
        self.assertEqual(res["scorecard"]["verdict"], "APPROVED_FOR_PRESS")
        self.assertEqual(res["summary"]["failed"], 0)
        self.assertEqual(res["summary"]["passed"], 7)

    def test_02_clean_typst_monograph_cli_exit_0(self):
        """CLI preflight invocation on monograph_typst.pdf exits with code 0."""
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"), self.typst_pdf]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"CLI stderr: {proc.stderr}")

    def test_03_clean_pagedjs_monograph_score_100(self):
        """Clean monograph_pagedjs.pdf scores 100/100 and passes all 7 prepress checks."""
        res = audit_pdf(self.pagedjs_pdf)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["scorecard"]["total_score"], 100)
        self.assertEqual(res["scorecard"]["verdict"], "APPROVED_FOR_PRESS")
        self.assertEqual(res["summary"]["failed"], 0)
        self.assertEqual(res["summary"]["passed"], 7)

    def test_04_clean_pagedjs_monograph_cli_exit_0(self):
        """CLI preflight invocation on monograph_pagedjs.pdf exits with code 0."""
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"), self.pagedjs_pdf]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"CLI stderr: {proc.stderr}")


class TestDefectSensitivityAndRejection(unittest.TestCase):
    """
    Negative rejection and defect sensitivity harness:
    Injects deliberate prepress defects into temporary copies of monograph PDFs and asserts
    that preflight audit correctly detects violations, deducts points, and exits with code 1.
    """

    def setUp(self):
        self.typst_pdf = os.path.join(PROJECT_ROOT, "examples", "monograph", "monograph_typst.pdf")
        self.pagedjs_pdf = os.path.join(PROJECT_ROOT, "examples", "monograph", "monograph_pagedjs.pdf")

    def test_01_margin_safety_breach_detection_typst(self):
        """Injected text at 1.0mm breaches 5mm safe margin, triggers FAIL, deductions, exit code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            defect_pdf = os.path.join(tmpdir, "breach_typst.pdf")
            doc = fitz.open(self.typst_pdf)
            p0 = doc[0]
            tb = p0.trimbox
            breach_pt = fitz.Point(tb.x0 + 1.0 * MM_TO_PT, tb.y0 + 1.0 * MM_TO_PT + 8.0)
            fbuf = fitz.Font("helv").buffer
            p0.insert_font(fontname="fbreach", fontbuffer=fbuf)
            p0.insert_text(breach_pt, "DEFECT: MARGIN BREACH", fontsize=10, fontname="fbreach")
            doc.save(defect_pdf)
            doc.close()

            res = audit_pdf(defect_pdf)
            self.assertEqual(res["status"], "FAIL")
            self.assertEqual(res["checks"]["margin_safety_zone"]["status"], "FAIL")
            self.assertGreaterEqual(res["checks"]["margin_safety_zone"]["violating_elements_count"], 1)
            self.assertLessEqual(res["scorecard"]["total_score"], 80)
            self.assertEqual(res["scorecard"]["verdict"], "REJECTED")

            cmd = [sys.executable, os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"), defect_pdf]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 1)

    def test_02_margin_safety_breach_detection_pagedjs(self):
        """Injected text at 1.0mm in Paged.js PDF triggers margin FAIL, deductions, exit code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            defect_pdf = os.path.join(tmpdir, "breach_pagedjs.pdf")
            doc = fitz.open(self.pagedjs_pdf)
            p0 = doc[0]
            tb = p0.trimbox
            breach_pt = fitz.Point(tb.x0 + 1.0 * MM_TO_PT, tb.y0 + 1.0 * MM_TO_PT + 8.0)
            fbuf = fitz.Font("helv").buffer
            p0.insert_font(fontname="fbreach", fontbuffer=fbuf)
            p0.insert_text(breach_pt, "DEFECT: MARGIN BREACH", fontsize=10, fontname="fbreach")
            doc.save(defect_pdf)
            doc.close()

            res = audit_pdf(defect_pdf)
            self.assertEqual(res["status"], "FAIL")
            self.assertEqual(res["checks"]["margin_safety_zone"]["status"], "FAIL")
            self.assertGreaterEqual(res["checks"]["margin_safety_zone"]["violating_elements_count"], 1)
            self.assertLessEqual(res["scorecard"]["total_score"], 80)
            self.assertEqual(res["scorecard"]["verdict"], "REJECTED")

            cmd = [sys.executable, os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"), defect_pdf]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 1)

    def test_03_low_res_image_rejection_typst(self):
        """Injected 36 DPI image (<200 DPI) triggers image_resolution FAIL, deductions, exit code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            defect_pdf = os.path.join(tmpdir, "lowres_typst.pdf")
            img_path = os.path.join(tmpdir, "lowres.jpg")
            img = Image.new("CMYK", (100, 100), (0, 0, 0, 100))
            img.save(img_path)

            doc = fitz.open(self.typst_pdf)
            p0 = doc[0]
            tb = p0.trimbox
            # 200x200 pt box -> 36 DPI effective resolution
            img_rect = fitz.Rect(tb.x0 + 100, tb.y0 + 100, tb.x0 + 300, tb.y0 + 300)
            p0.insert_image(img_rect, filename=img_path)
            doc.save(defect_pdf)
            doc.close()

            res = audit_pdf(defect_pdf)
            self.assertEqual(res["status"], "FAIL")
            self.assertEqual(res["checks"]["image_resolution"]["status"], "FAIL")
            self.assertLess(res["checks"]["image_resolution"]["min_dpi"], 200.0)
            self.assertGreaterEqual(len(res["checks"]["image_resolution"]["violating_images"]), 1)
            self.assertLessEqual(res["scorecard"]["total_score"], 90)
            self.assertEqual(res["scorecard"]["verdict"], "REJECTED")

            cmd = [sys.executable, os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"), defect_pdf]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 1)

    def test_04_low_res_image_rejection_pagedjs(self):
        """Injected 36 DPI image in Paged.js triggers image_resolution FAIL, deductions, exit code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            defect_pdf = os.path.join(tmpdir, "lowres_pagedjs.pdf")
            img_path = os.path.join(tmpdir, "lowres.jpg")
            img = Image.new("CMYK", (100, 100), (0, 0, 0, 100))
            img.save(img_path)

            doc = fitz.open(self.pagedjs_pdf)
            p0 = doc[0]
            tb = p0.trimbox
            img_rect = fitz.Rect(tb.x0 + 100, tb.y0 + 100, tb.x0 + 300, tb.y0 + 300)
            p0.insert_image(img_rect, filename=img_path)
            doc.save(defect_pdf)
            doc.close()

            res = audit_pdf(defect_pdf)
            self.assertEqual(res["status"], "FAIL")
            self.assertEqual(res["checks"]["image_resolution"]["status"], "FAIL")
            self.assertLess(res["checks"]["image_resolution"]["min_dpi"], 200.0)
            self.assertLessEqual(res["scorecard"]["total_score"], 90)
            self.assertEqual(res["scorecard"]["verdict"], "REJECTED")

            cmd = [sys.executable, os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"), defect_pdf]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 1)

    def test_05_high_tac_ink_coverage_rejection(self):
        """Injected image with 380% TAC (>320%) triggers color_and_tac FAIL, deductions, exit code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            defect_pdf = os.path.join(tmpdir, "hightac_typst.pdf")
            img_path = os.path.join(tmpdir, "hightac.tif")
            img = Image.new("CMYK", (300, 300), (255, 255, 255, 204))  # 380% TAC
            img.save(img_path, dpi=(300, 300))

            doc = fitz.open(self.typst_pdf)
            p0 = doc[0]
            tb = p0.trimbox
            img_rect = fitz.Rect(tb.x0 + 100, tb.y0 + 100, tb.x0 + 172, tb.y0 + 172)
            p0.insert_image(img_rect, filename=img_path)
            doc.save(defect_pdf)
            doc.close()

            res = audit_pdf(defect_pdf)
            self.assertEqual(res["status"], "FAIL")
            self.assertEqual(res["checks"]["color_and_tac"]["status"], "FAIL")
            self.assertGreater(res["checks"]["color_and_tac"]["max_tac"], 320.0)
            self.assertLessEqual(res["scorecard"]["total_score"], 85)
            self.assertEqual(res["scorecard"]["verdict"], "REJECTED")

            cmd = [sys.executable, os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"), defect_pdf]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 1)

    def test_06_unseparated_rgb_image_rejection(self):
        """Injected untagged RGB image triggers color_and_tac FAIL, deductions, exit code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            defect_pdf = os.path.join(tmpdir, "rgb_typst.pdf")
            img_path = os.path.join(tmpdir, "rgb.png")
            img = Image.new("RGB", (300, 300), (255, 0, 0))
            img.save(img_path, dpi=(300, 300))

            doc = fitz.open(self.typst_pdf)
            p0 = doc[0]
            tb = p0.trimbox
            img_rect = fitz.Rect(tb.x0 + 100, tb.y0 + 100, tb.x0 + 172, tb.y0 + 172)
            p0.insert_image(img_rect, filename=img_path)
            doc.save(defect_pdf)
            doc.close()

            res = audit_pdf(defect_pdf)
            self.assertEqual(res["status"], "FAIL")
            self.assertEqual(res["checks"]["color_and_tac"]["status"], "FAIL")
            self.assertTrue(res["checks"]["color_and_tac"]["unseparated_rgb_found"])
            self.assertLessEqual(res["scorecard"]["total_score"], 85)
            self.assertEqual(res["scorecard"]["verdict"], "REJECTED")

            cmd = [sys.executable, os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"), defect_pdf]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 1)


class TestAssetIntegrity(unittest.TestCase):
    """
    Validates physical print readiness of all static assets in examples/monograph/assets/:
    - SVGs: Valid XML, root <svg>, viewBox, ISO 128 stroke hierarchy
    - Rasters: CMYK color space, >= 300 DPI effective resolution, TAC <= 320%
    """

    def setUp(self):
        self.assets_dir = os.path.join(PROJECT_ROOT, "examples", "monograph", "assets")
        self.assertTrue(os.path.isdir(self.assets_dir), f"Missing assets directory: {self.assets_dir}")

    def test_01_svg_assets_valid_xml_and_dimensions(self):
        """Verify all SVG assets parse as valid XML with root <svg> and dimensions/viewBox."""
        svg_files = ["millwork_reveal_1_5.svg", "spatial_plan_1_100.svg", "wall_section_1_20.svg"]
        for fname in svg_files:
            p = os.path.join(self.assets_dir, fname)
            self.assertTrue(os.path.isfile(p), f"Missing SVG: {fname}")
            tree = ET.parse(p)
            root = tree.getroot()
            self.assertTrue(root.tag.endswith("svg"), f"{fname} root is not <svg>")
            has_viewbox = "viewBox" in root.attrib or ("width" in root.attrib and "height" in root.attrib)
            self.assertTrue(has_viewbox, f"{fname} missing viewBox or width/height")

    def test_02_svg_assets_iso128_stroke_hierarchy(self):
        """Verify all SVG assets adhere to calibrated ISO 128 stroke weights (0.13mm to 0.70mm)."""
        svg_files = ["millwork_reveal_1_5.svg", "spatial_plan_1_100.svg", "wall_section_1_20.svg"]
        for fname in svg_files:
            p = os.path.join(self.assets_dir, fname)
            tree = ET.parse(p)
            strokes = set()
            for el in tree.iter():
                sw = el.attrib.get("stroke-width")
                if sw:
                    try:
                        strokes.add(float(sw.replace("px", "").replace("pt", "")))
                    except ValueError:
                        pass
                style = el.attrib.get("style", "")
                if "stroke-width" in style:
                    for part in style.split(";"):
                        if "stroke-width" in part:
                            try:
                                val = part.split(":")[1].strip().replace("px", "").replace("pt", "")
                                strokes.add(float(val))
                            except ValueError:
                                pass
            self.assertGreater(len(strokes), 0, f"{fname} contains no strokes")
            # Verify strokes are within calibrated range (approx 0.35pt ~ 2.5pt)
            for s in strokes:
                self.assertGreaterEqual(s, 0.25, f"{fname} stroke too thin: {s}pt")
                self.assertLessEqual(s, 3.0, f"{fname} stroke too heavy: {s}pt")

    def test_03_raster_assets_cmyk_color_mode(self):
        """Verify all raster images are strictly in CMYK color mode."""
        raster_files = [
            "lived_scenography_cmyk.jpg",
            "lived_scenography_cmyk.tif",
            "site_context_cmyk.jpg",
            "site_context_cmyk.tif"
        ]
        for fname in raster_files:
            p = os.path.join(self.assets_dir, fname)
            self.assertTrue(os.path.isfile(p), f"Missing raster asset: {fname}")
            with Image.open(p) as img:
                self.assertEqual(img.mode, "CMYK", f"{fname} is in mode {img.mode}, expected CMYK")

    def test_04_raster_assets_resolution_dpi_ge_300(self):
        """Verify all raster images have resolution >= 300 DPI."""
        raster_files = [
            "lived_scenography_cmyk.jpg",
            "lived_scenography_cmyk.tif",
            "site_context_cmyk.jpg",
            "site_context_cmyk.tif"
        ]
        for fname in raster_files:
            p = os.path.join(self.assets_dir, fname)
            with Image.open(p) as img:
                dpi = img.info.get("dpi")
                self.assertIsNotNone(dpi, f"{fname} missing DPI metadata")
                dpi_x, dpi_y = dpi
                self.assertGreaterEqual(dpi_x, 299.0, f"{fname} DPI X < 300 ({dpi_x})")
                self.assertGreaterEqual(dpi_y, 299.0, f"{fname} DPI Y < 300 ({dpi_y})")

    def test_05_raster_assets_tac_within_limits(self):
        """Verify all raster images have peak Total Area Coverage (TAC) <= 320%."""
        raster_files = [
            "lived_scenography_cmyk.jpg",
            "lived_scenography_cmyk.tif",
            "site_context_cmyk.jpg",
            "site_context_cmyk.tif"
        ]
        for fname in raster_files:
            p = os.path.join(self.assets_dir, fname)
            with Image.open(p) as img:
                arr = np.array(img, dtype=np.float32)
                tac_map = (arr[:, :, 0] + arr[:, :, 1] + arr[:, :, 2] + arr[:, :, 3]) / 255.0 * 100.0
                peak_tac = float(np.max(tac_map))
                self.assertLessEqual(
                    peak_tac,
                    320.0,
                    f"{fname} exceeds TAC limit: {peak_tac:.2f}% > 320.0%"
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
