"""
tests/tier2_boundaries/test_boundary_bleeds.py
Feature 4 (Tier 2): Bleed boundaries, missing bleeds (0mm vs 3mm), and geometry violations
Authoritative Source: ORIGINAL_REQUEST.md §R5, spec_miner_print_engine/report.md §6.1
"""

import sys
import os
import unittest
import tempfile
import fitz

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.fixtures.pdf_generator import create_synthetic_pdf, MM_TO_PT
from tests.tier1_features.test_preflight_cli import StandalonePreflightAuditor

class TestBoundaryBleeds(unittest.TestCase):
    """
    Validates boundary and error conditions for PDF box geometries and bleeds:
    - Zero bleed (0mm vs required 3mm)
    - Asymmetric bleed delta
    - TrimBox not enclosed in BleedBox
    - Corrupt BleedBox delta exceeding tolerance
    """

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_zero_bleed_causes_preflight_failure(self):
        """Verify PDF with 0.0mm bleed fails dimensions_and_bleed check."""
        pdf_path = os.path.join(self.temp_dir.name, "zero_bleed.pdf")
        doc = fitz.open()
        page = doc.new_page(width=841.89, height=595.28)
        trim_rect = fitz.Rect(0, 0, 841.89, 595.28)
        page.set_trimbox(trim_rect)
        page.set_bleedbox(trim_rect)
        doc.save(pdf_path)
        doc.close()

        auditor = StandalonePreflightAuditor(pdf_path)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["dimensions_and_bleed"]["status"], "FAIL")

    def test_02_asymmetric_bleed_detected(self):
        """Verify PDF with asymmetric bleed (e.g. 3mm left, 1mm right) fails bleed check."""
        pdf_path = os.path.join(self.temp_dir.name, "asymmetric_bleed.pdf")
        doc = fitz.open()
        pt_3mm = 3.0 * MM_TO_PT
        pt_1mm = 1.0 * MM_TO_PT

        page = doc.new_page(width=1000, height=800)
        trim_rect = fitz.Rect(50, 50, 50 + 841.89, 50 + 595.28)
        bleed_rect = fitz.Rect(50 - pt_3mm, 50 - pt_3mm, trim_rect.x1 + pt_1mm, trim_rect.y1 + pt_3mm)
        page.set_trimbox(trim_rect)
        page.set_bleedbox(bleed_rect)
        doc.save(pdf_path)
        doc.close()

        auditor = StandalonePreflightAuditor(pdf_path)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["dimensions_and_bleed"]["status"], "FAIL")

    def test_03_bleed_box_smaller_than_trim_box_detected(self):
        """Verify inverted boxes where BleedBox is smaller than TrimBox fails check."""
        pdf_path = os.path.join(self.temp_dir.name, "inverted_boxes.pdf")
        doc = fitz.open()
        page = doc.new_page(width=900, height=650)
        trim_rect = fitz.Rect(50, 50, 50 + 841.89, 50 + 595.28)
        bleed_rect = fitz.Rect(60, 60, trim_rect.x1 - 10, trim_rect.y1 - 10)
        page.set_trimbox(trim_rect)
        page.set_bleedbox(bleed_rect)
        doc.save(pdf_path)
        doc.close()

        auditor = StandalonePreflightAuditor(pdf_path)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["dimensions_and_bleed"]["status"], "FAIL")

    def test_04_exact_3mm_bleed_passes(self):
        """Verify exact 3.0mm bleed passes cleanly."""
        pdf_path = os.path.join(self.temp_dir.name, "exact_3mm.pdf")
        create_synthetic_pdf(output_path=pdf_path, bleed_mm=3.0)
        auditor = StandalonePreflightAuditor(pdf_path)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["dimensions_and_bleed"]["status"], "PASS")

    def test_05_excessive_bleed_flagged(self):
        """Verify excessive bleed (10.0mm instead of 3.0mm) fails strict 3mm print specification."""
        pdf_path = os.path.join(self.temp_dir.name, "excessive_10mm.pdf")
        create_synthetic_pdf(output_path=pdf_path, bleed_mm=10.0)
        auditor = StandalonePreflightAuditor(pdf_path)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["dimensions_and_bleed"]["status"], "FAIL")

if __name__ == "__main__":
    unittest.main()
