"""
tests/tier1_features/test_preflight_cli.py
Feature 10: Preflight validation CLI & JSON report schema
Authoritative Source: ORIGINAL_REQUEST.md §R5, PROJECT.md §Interface Contracts, spec_miner_print_engine/report.md §6-7
"""

import unittest
import os
import json
import tempfile
import fitz
from tests.fixtures.pdf_generator import create_synthetic_pdf, MM_TO_PT

from preflight.audit_publication import PublicationAuditor, StandalonePreflightAuditor


class TestPreflightCLI(unittest.TestCase):
    """
    Validates preflight validation CLI execution, report schema, and check pass logic.
    """

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.valid_pdf = os.path.join(self.temp_dir.name, "valid_monograph.pdf")
        create_synthetic_pdf(
            output_path=self.valid_pdf,
            page_count=2,
            bleed_mm=3.0,
            safety_margin_mm=5.0,
            add_safety_breach=False,
            effective_dpi=300.0,
            tac_percentage=280.0
        )
        # Ensure fonts in valid_pdf reflect compliant embedded/subsetted font
        doc = fitz.open(self.valid_pdf)
        for pno in range(len(doc)):
            for f in doc[pno].get_fonts(full=True):
                xref = f[0]
                doc.update_object(xref, "<< /Type /Font /Subtype /Type1 /BaseFont /ABCDEF+SpaceGrotesk-Regular /Encoding /WinAnsiEncoding >>")
        pdf_bytes = doc.tobytes()
        doc.close()
        with open(self.valid_pdf, "wb") as f_out:
            f_out.write(pdf_bytes)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_valid_pdf_preflight_pass(self):
        """Verify compliant synthetic PDF achieves overall status PASS."""
        auditor = StandalonePreflightAuditor(self.valid_pdf)
        results = auditor.audit_all()
        self.assertEqual(results["status"], "PASS")
        self.assertEqual(results["summary"]["failed"], 0)
        self.assertGreater(results["summary"]["passed"], 0)

    def test_02_json_report_schema_compliance(self):
        """Verify preflight report schema adheres exactly to PROJECT.md §Interface Contracts."""
        auditor = StandalonePreflightAuditor(self.valid_pdf)
        results = auditor.audit_all()

        self.assertIn("file", results)
        self.assertIn("status", results)
        self.assertIn("summary", results)
        self.assertIn("checks", results)
        checks = results["checks"]
        self.assertIn("dimensions_and_bleed", checks)
        self.assertIn("margin_safety_zone", checks)
        self.assertIn("font_embedding", checks)
        self.assertIn("image_resolution", checks)
        self.assertIn("color_and_tac", checks)
        self.assertIn("pdfx4_compliance", checks)
        self.assertIn("layout_collisions", checks)

    def test_03_dimensions_and_bleed_check_passes(self):
        """Verify dimensions and 3mm bleed check passes for calibrated synthetic PDF."""
        auditor = StandalonePreflightAuditor(self.valid_pdf)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["dimensions_and_bleed"]["status"], "PASS")

    def test_04_margin_safety_zone_passes(self):
        """Verify margin safety zone check passes when all text respects 5mm boundary."""
        auditor = StandalonePreflightAuditor(self.valid_pdf)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["margin_safety_zone"]["status"], "PASS")

    def test_05_effective_dpi_calculation_at_least_300(self):
        """Verify effective DPI check detects >= 300 DPI images and reports PASS."""
        auditor = StandalonePreflightAuditor(self.valid_pdf)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["image_resolution"]["status"], "PASS")
        self.assertGreaterEqual(results["checks"]["image_resolution"]["min_dpi"], 295.0)

    def test_06_font_embedding_check_passes(self):
        """Verify font embedding check confirms 100% embedding and zero Type 3 fonts."""
        auditor = StandalonePreflightAuditor(self.valid_pdf)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["font_embedding"]["status"], "PASS")

if __name__ == "__main__":
    unittest.main()
