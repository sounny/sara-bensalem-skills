"""
tests/tier5_adversarial/test_negative_rejection_m7_challenger2.py
Challenger 2 Empirical Verification Test Suite: Milestone 7 Final E2E Acceptance & Adversarial Hardening.

Authoritative Requirements:
- ORIGINAL_REQUEST.md (§R1-R6, Acceptance Criteria)
- PROJECT.md (§Architecture, §Feature Inventory, §Milestones)
- TEST_INFRA.md (§E2E Test Architecture)

Test Dimensions:
1. End-to-End Workflow Verification:
   - Fresh custom Typst document compilation (<3.0s, valid TrimBox/BleedBox, audit 100/100)
   - Fresh custom Paged.js document compilation (valid PDF, valid TrimBox/BleedBox, audit 100/100)
2. Production Monograph Stress:
   - Audit examples/monograph/monograph_typst.pdf (100/100, APPROVED_FOR_PRESS, exit code 0)
   - Audit examples/monograph/monograph_pagedjs.pdf (100/100, APPROVED_FOR_PRESS, exit code 0)
3. Negative Ingestion & Error Handling:
   - Non-existent path, 0-byte file, plain text file, PNG image file, corrupted binary PDF
   - Graceful handling: exit code 1, structured error JSON, zero unhandled tracebacks
4. Engine Compilation Robustness & Boundary Sensitivity:
   - Non-existent file, empty file, mismatched engine, invalid engine
   - Threshold sensitivity: <10KB compiled PDF rejection behavior
"""

import os
import sys
import tempfile
import time
import json
import subprocess
import unittest
from typing import Dict, Any

import fitz  # PyMuPDF
from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from engine.compile import compile_document
from preflight.audit_publication import audit_pdf, MM_TO_PT


class TestE2EWorkflowVerification(unittest.TestCase):
    """
    End-to-End Workflow Verification for fresh custom documents:
    Compiles custom Typst and Paged.js documents and audits them with preflight.
    """

    def setUp(self):
        self.custom_typst_content = """#set document(
  title: "Empirical E2E Monograph Test",
  author: "Challenger 2",
  keywords: ("Testing", "E2E", "Typst")
)

#set page(
  paper: "a4",
  flipped: true,
  margin: (inside: 25mm, outside: 15mm, top: 20mm, bottom: 20mm)
)

= ACT 1: THE HOOK
== Mediterranean Vernacular Adaptation

The project investigates adaptive bioclimatic envelopes within high-density urban environments.
This multi-spread case study demonstrates Swiss 12-column modular rhythm and baseline grid locking.

#pagebreak()

= ACT 2: TECTONIC PROOF
== 1:20 Constructive Wall Section

Thermal break assembly featuring 75mm PIR rigid insulation, 1.52mm continuous EPDM weatherproofing,
and triple-glazed argon-filled low-E curtain wall modules. Glaser U-value calculation verifies 0.18 W/m2K.
"""

        self.custom_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Empirical E2E PagedJS Publication</title>
  <style>
    @page {
      size: 297mm 210mm;
      margin: 20mm 15mm 20mm 25mm;
      marks: crop cross;
      bleed: 3mm;
    }
    .page {
      page-break-after: always;
      break-after: page;
      width: 100%;
      height: 100%;
    }
  </style>
</head>
<body>
  <section class="page monograph-spread">
    <h1>ACT 1: HOOK & CONTEXT</h1>
    <div class="passport-card">
      <dl>
        <dt>Project</dt><dd>Atlas Terrace Cultural Pavilion</dd>
        <dt>Typology</dt><dd>Cultural Infrastructure</dd>
        <dt>Location</dt><dd>Casablanca, Morocco</dd>
        <dt>Year</dt><dd>2026</dd>
        <dt>Client</dt><dd>Fondation Nationale des Musees</dd>
        <dt>Area</dt><dd>4,200 m2 GIA</dd>
        <dt>Scale</dt><dd>1:20 / 1:100 / 1:500</dd>
        <dt>Stage</dt><dd>RIBA Stage 4 (Technical Design)</dd>
        <dt>Lead Architect</dt><dd>Sara Bensalem</dd>
      </dl>
    </div>
    <div class="vector-plate">
      <span>1:20 CONSTRUCTIVE WALL SECTION</span>
      <span>CALIBRATED ISO 128 STROKES & THERMAL BREAKS</span>
    </div>
  </section>

  <section class="page monograph-spread">
    <h1>ACT 2: TECTONIC PROOF</h1>
    <div class="vector-plate">
      <span>1:5 BESPOKE JOINERY & FACADE ANCHOR</span>
      <span>EPDM FLASHING & 75MM RIGID INSULATION</span>
    </div>
  </section>
</body>
</html>
"""

    def test_01_typst_custom_compilation_speed_and_boxes(self):
        """Compile fresh custom Typst doc in <3.0s and verify TrimBox/BleedBox geometry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = os.path.join(tmpdir, "custom_test.typ")
            out_pdf = os.path.join(tmpdir, "custom_test_typst.pdf")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(self.custom_typst_content)

            start = time.perf_counter()
            res = compile_document(
                input_path=src_path,
                output_path=out_pdf,
                engine="typst",
                bleed="3mm",
                benchmark=True
            )
            duration = time.perf_counter() - start

            self.assertTrue(res["success"], f"Typst compilation failed: {res}")
            self.assertTrue(os.path.isfile(out_pdf), "Output PDF was not generated")
            self.assertLess(duration, 3.0, f"Compilation took {duration:.3f}s, exceeding 3.0s limit")
            self.assertEqual(res["page_count"], 2, f"Expected 2 pages, got {res['page_count']}")

            # Verify TrimBox and BleedBox geometry with PyMuPDF
            doc = fitz.open(out_pdf)
            self.assertEqual(len(doc), 2)
            for page_idx, page in enumerate(doc):
                mb = page.rect
                bb = page.bleedbox
                tb = page.trimbox

                # MediaBox must enclose BleedBox
                self.assertLessEqual(mb.x0, bb.x0)
                self.assertLessEqual(mb.y0, bb.y0)
                self.assertGreaterEqual(mb.x1, bb.x1)
                self.assertGreaterEqual(mb.y1, bb.y1)

                # BleedBox must enclose TrimBox
                self.assertLessEqual(bb.x0, tb.x0)
                self.assertLessEqual(bb.y0, tb.y0)
                self.assertGreaterEqual(bb.x1, tb.x1)
                self.assertGreaterEqual(bb.y1, tb.y1)

                # Bleed delta must be approximately 3.0mm (8.5 pt +/- 0.6 pt)
                bleed_delta_x0 = tb.x0 - bb.x0
                bleed_delta_y0 = tb.y0 - bb.y0
                self.assertAlmostEqual(bleed_delta_x0, 3.0 * MM_TO_PT, delta=0.6)
                self.assertAlmostEqual(bleed_delta_y0, 3.0 * MM_TO_PT, delta=0.6)
            doc.close()

            # Audit using preflight/audit_publication.py
            audit_json_path = os.path.join(tmpdir, "audit_custom_typst.json")
            cmd = [
                sys.executable,
                os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"),
                out_pdf,
                "--json", audit_json_path
            ]
            audit_proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(audit_proc.returncode, 0, f"Audit exited with code {audit_proc.returncode}:\n{audit_proc.stdout}\n{audit_proc.stderr}")
            self.assertTrue(os.path.isfile(audit_json_path))

            with open(audit_json_path, "r", encoding="utf-8") as jf:
                report = json.load(jf)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["scorecard"]["total_score"], 100)
            self.assertEqual(report["scorecard"]["verdict"], "APPROVED_FOR_PRESS")
            self.assertEqual(report["summary"]["failed"], 0)

    def test_02_pagedjs_custom_compilation_and_audit(self):
        """Compile fresh custom Paged.js HTML doc and audit output PDF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_path = os.path.join(tmpdir, "custom_test.html")
            out_pdf = os.path.join(tmpdir, "custom_test_paged.pdf")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(self.custom_html_content)

            res = compile_document(
                input_path=src_path,
                output_path=out_pdf,
                engine="pagedjs",
                bleed="3mm",
                benchmark=True
            )

            self.assertTrue(res["success"], f"Paged.js compilation failed: {res}")
            self.assertTrue(os.path.isfile(out_pdf), "Output PDF was not generated")
            self.assertEqual(res["page_count"], 2, f"Expected 2 pages, got {res['page_count']}")

            # Verify geometry
            doc = fitz.open(out_pdf)
            self.assertEqual(len(doc), 2)
            for page in doc:
                mb = page.rect
                bb = page.bleedbox
                tb = page.trimbox
                self.assertLessEqual(bb.x0, tb.x0)
                self.assertGreaterEqual(bb.x1, tb.x1)
                bleed_delta_x0 = tb.x0 - bb.x0
                self.assertAlmostEqual(bleed_delta_x0, 3.0 * MM_TO_PT, delta=0.6)
            doc.close()

            # Audit using preflight/audit_publication.py
            audit_json_path = os.path.join(tmpdir, "audit_custom_paged.json")
            cmd = [
                sys.executable,
                os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"),
                out_pdf,
                "--json", audit_json_path
            ]
            audit_proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(audit_proc.returncode, 0, f"Audit exited with code {audit_proc.returncode}:\n{audit_proc.stdout}\n{audit_proc.stderr}")
            self.assertTrue(os.path.isfile(audit_json_path))

            with open(audit_json_path, "r", encoding="utf-8") as jf:
                report = json.load(jf)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["scorecard"]["total_score"], 100)
            self.assertEqual(report["scorecard"]["verdict"], "APPROVED_FOR_PRESS")
            self.assertEqual(report["summary"]["failed"], 0)


class TestProductionMonographStress(unittest.TestCase):
    """
    Production Monograph Stress:
    Audits examples/monograph/monograph_typst.pdf and examples/monograph/monograph_pagedjs.pdf.
    Asserts both achieve 100/100 score (APPROVED_FOR_PRESS) with exit code 0.
    """

    def setUp(self):
        self.typst_pdf = os.path.join(PROJECT_ROOT, "examples", "monograph", "monograph_typst.pdf")
        self.pagedjs_pdf = os.path.join(PROJECT_ROOT, "examples", "monograph", "monograph_pagedjs.pdf")
        self.assertTrue(os.path.isfile(self.typst_pdf), f"Missing monograph_typst.pdf: {self.typst_pdf}")
        self.assertTrue(os.path.isfile(self.pagedjs_pdf), f"Missing monograph_pagedjs.pdf: {self.pagedjs_pdf}")

    def test_01_monograph_typst_achieves_100_approved_for_press(self):
        """Verify monograph_typst.pdf scores 100/100 and APPROVED_FOR_PRESS via API & CLI."""
        res = audit_pdf(self.typst_pdf)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["scorecard"]["total_score"], 100)
        self.assertEqual(res["scorecard"]["verdict"], "APPROVED_FOR_PRESS")
        self.assertEqual(res["summary"]["failed"], 0)

        # Also verify CLI exit code 0 and JSON generation
        with tempfile.TemporaryDirectory() as tmpdir:
            json_out = os.path.join(tmpdir, "audit_typst.json")
            cmd = [
                sys.executable,
                os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"),
                self.typst_pdf,
                "--json", json_out
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, f"CLI exited with {proc.returncode}: {proc.stderr}")
            self.assertTrue(os.path.isfile(json_out))
            with open(json_out, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["scorecard"]["total_score"], 100)
            self.assertEqual(data["scorecard"]["verdict"], "APPROVED_FOR_PRESS")

    def test_02_monograph_pagedjs_achieves_100_approved_for_press(self):
        """Verify monograph_pagedjs.pdf scores 100/100 and APPROVED_FOR_PRESS via API & CLI."""
        res = audit_pdf(self.pagedjs_pdf)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["scorecard"]["total_score"], 100)
        self.assertEqual(res["scorecard"]["verdict"], "APPROVED_FOR_PRESS")
        self.assertEqual(res["summary"]["failed"], 0)

        # Also verify CLI exit code 0 and JSON generation
        with tempfile.TemporaryDirectory() as tmpdir:
            json_out = os.path.join(tmpdir, "audit_pagedjs.json")
            cmd = [
                sys.executable,
                os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"),
                self.pagedjs_pdf,
                "--json", json_out
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, f"CLI exited with {proc.returncode}: {proc.stderr}")
            self.assertTrue(os.path.isfile(json_out))
            with open(json_out, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["scorecard"]["total_score"], 100)
            self.assertEqual(data["scorecard"]["verdict"], "APPROVED_FOR_PRESS")


class TestNegativeIngestionAndErrorHandling(unittest.TestCase):
    """
    Negative Ingestion & Error Handling:
    Challenges audit_publication.py with non-existent paths, 0-byte files, non-PDF files,
    and corrupted binaries. Asserts graceful exit code 1, structured JSON, zero unhandled tracebacks.
    """

    def _run_audit_cli(self, target_path: str, json_path: str) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable,
            os.path.join(PROJECT_ROOT, "preflight", "audit_publication.py"),
            target_path,
            "--json", json_path
        ]
        return subprocess.run(cmd, capture_output=True, text=True)

    def test_01_non_existent_path(self):
        """Audit non-existent path: assert exit code 1, structured error JSON, zero tracebacks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_path = os.path.join(tmpdir, "non_existent_document.pdf")
            json_out = os.path.join(tmpdir, "error_res.json")

            proc = self._run_audit_cli(fake_path, json_out)

            self.assertEqual(proc.returncode, 1, "Expected exit code 1 for non-existent path")
            self.assertNotIn("Traceback (most recent call last):", proc.stderr)
            self.assertTrue(os.path.isfile(json_out), "Structured error JSON was not generated")

            with open(json_out, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["status"], "FAIL")
            self.assertEqual(data["scorecard"]["verdict"], "REJECTED")
            self.assertIn("FileNotFoundError", data.get("error", ""))

    def test_02_empty_zero_byte_file(self):
        """Audit 0-byte file: assert exit code 1, structured error JSON, zero tracebacks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            empty_file = os.path.join(tmpdir, "empty.pdf")
            json_out = os.path.join(tmpdir, "error_res.json")
            with open(empty_file, "wb"):
                pass  # 0 bytes

            proc = self._run_audit_cli(empty_file, json_out)

            self.assertEqual(proc.returncode, 1, "Expected exit code 1 for 0-byte file")
            self.assertNotIn("Traceback (most recent call last):", proc.stderr)
            self.assertTrue(os.path.isfile(json_out), "Structured error JSON was not generated")

            with open(json_out, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["status"], "FAIL")
            self.assertEqual(data["scorecard"]["verdict"], "REJECTED")
            self.assertIn("ValueError", data.get("error", ""))

    def test_03_plain_text_file(self):
        """Audit plain text file: assert exit code 1, structured error JSON, zero tracebacks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            txt_file = os.path.join(tmpdir, "not_a_pdf.txt")
            json_out = os.path.join(tmpdir, "error_res.json")
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write("This is a plain ASCII text file, not a valid PDF document.")

            proc = self._run_audit_cli(txt_file, json_out)

            self.assertEqual(proc.returncode, 1, "Expected exit code 1 for plain text file")
            self.assertNotIn("Traceback (most recent call last):", proc.stderr)
            self.assertTrue(os.path.isfile(json_out), "Structured error JSON was not generated")

            with open(json_out, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["status"], "FAIL")
            self.assertEqual(data["scorecard"]["verdict"], "REJECTED")

    def test_04_png_image_file(self):
        """Audit PNG image file: assert exit code 1, structured error JSON, zero tracebacks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            png_file = os.path.join(tmpdir, "image.png")
            json_out = os.path.join(tmpdir, "error_res.json")
            img = Image.new("RGB", (300, 300), color=(200, 50, 50))
            img.save(png_file)

            proc = self._run_audit_cli(png_file, json_out)

            self.assertEqual(proc.returncode, 1, "Expected exit code 1 for PNG file")
            self.assertNotIn("Traceback (most recent call last):", proc.stderr)
            self.assertTrue(os.path.isfile(json_out), "Structured error JSON was not generated")

            with open(json_out, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["status"], "FAIL")
            self.assertEqual(data["scorecard"]["verdict"], "REJECTED")

    def test_05_corrupted_pdf_binary(self):
        """Audit corrupted PDF file: assert exit code 1, structured error JSON, zero tracebacks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            corrupt_file = os.path.join(tmpdir, "corrupt.pdf")
            json_out = os.path.join(tmpdir, "error_res.json")
            with open(corrupt_file, "wb") as f:
                f.write(b"%PDF-1.4\n%corrupted_body_data\x00\xfe\xff\xba\xbe\xef\x00\x01\x02\x03\x04\x05")

            proc = self._run_audit_cli(corrupt_file, json_out)

            self.assertEqual(proc.returncode, 1, "Expected exit code 1 for corrupted PDF")
            self.assertNotIn("Traceback (most recent call last):", proc.stderr)
            self.assertTrue(os.path.isfile(json_out), "Structured error JSON was not generated")

            with open(json_out, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["status"], "FAIL")
            self.assertEqual(data["scorecard"]["verdict"], "REJECTED")
            self.assertIn("error", data)


class TestCompilationNegativeRejection(unittest.TestCase):
    """
    Engine Compilation Robustness:
    Ensures compile_document gracefully rejects invalid inputs, missing files,
    0-byte files, and mismatched engines. Also verifies 10KB minimum threshold boundary.
    """

    def test_01_compile_non_existent_file(self):
        """compile_document raises FileNotFoundError on non-existent input."""
        with self.assertRaises(FileNotFoundError):
            compile_document("non_existent_source.typ")

    def test_02_compile_empty_zero_byte_file(self):
        """compile_document raises ValueError on 0-byte file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            empty_file = os.path.join(tmpdir, "empty.typ")
            with open(empty_file, "w"):
                pass
            with self.assertRaises(ValueError) as ctx:
                compile_document(empty_file)
            self.assertIn("empty", str(ctx.exception).lower())

    def test_03_compile_invalid_engine_name(self):
        """compile_document raises ValueError on unsupported engine."""
        valid_typ = os.path.join(PROJECT_ROOT, "examples", "monograph", "source.typ")
        with self.assertRaises(ValueError) as ctx:
            compile_document(valid_typ, engine="latex_engine")
        self.assertIn("unsupported", str(ctx.exception).lower())

    def test_04_compile_mismatched_engine(self):
        """compile_document raises ValueError when engine and file extension conflict."""
        valid_typ = os.path.join(PROJECT_ROOT, "examples", "monograph", "source.typ")
        with self.assertRaises(ValueError) as ctx:
            compile_document(valid_typ, engine="pagedjs")
        self.assertIn("mismatched engine", str(ctx.exception).lower())

        valid_html = os.path.join(PROJECT_ROOT, "examples", "monograph", "source.html")
        with self.assertRaises(ValueError) as ctx:
            compile_document(valid_html, engine="typst")
        self.assertIn("mismatched engine", str(ctx.exception).lower())

    def test_05_lightweight_document_10kb_threshold_boundary(self):
        """
        Adversarial Boundary Test:
        Demonstrates that lightweight valid HTML documents with minimal content
        produce genuine PDFs < 10KB, triggering the 10KB threshold check in build_pagedjs.py.
        """
        tiny_html = "<html><body><section><h1>Minimal</h1><p>Short note.</p></section></body></html>"
        with tempfile.TemporaryDirectory() as tmpdir:
            src = os.path.join(tmpdir, "tiny.html")
            out = os.path.join(tmpdir, "tiny.pdf")
            with open(src, "w", encoding="utf-8") as f:
                f.write(tiny_html)
            # Must raise ValueError due to <10240 bytes threshold check in build_pagedjs.py
            with self.assertRaises(ValueError) as ctx:
                compile_document(src, out, engine="pagedjs")
            self.assertIn("10kb minimum", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main()
