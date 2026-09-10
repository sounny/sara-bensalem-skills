"""
tests/tier3_combinations/test_passport_preflight_audit.py
Combination 3: Project Passport metadata block audited by preflight validator
Authoritative Source: ORIGINAL_REQUEST.md §R4, §R5, spec_miner_skills/report.md §4, spec_miner_print_engine/report.md §6
"""

import sys
import os
import unittest
import tempfile
import json
import fitz

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.fixtures.pdf_generator import create_synthetic_pdf, MM_TO_PT
from tests.tier1_features.test_project_passport import validate_passport
from tests.tier1_features.test_preflight_cli import StandalonePreflightAuditor

class TestPassportPreflightAudit(unittest.TestCase):
    """
    Tests cross-feature integration between:
    - Project Passport data schema
    - Typographic placement on opening spread
    - Preflight audit of margins, bleed safety, and font embedding
    """

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        fixture_path = os.path.join(PROJECT_ROOT, "tests", "fixtures", "sample_passport.json")
        with open(fixture_path, "r", encoding="utf-8") as f:
            self.passport_data = json.load(f)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_passport_schema_valid_before_placement(self):
        """Verify passport metadata is 100% valid before compiling to print."""
        errors = validate_passport(self.passport_data)
        self.assertEqual(errors, [])

    def test_02_compiled_passport_spread_preflight_audit(self):
        """
        Verify that a PDF containing a formatted Project Passport card on the verso page
        passes margin safety zone audit and bleed verification.
        """
        pdf_path = os.path.join(self.temp_dir.name, "passport_spread.pdf")
        doc = fitz.open()
        bleed_pt = 3.0 * MM_TO_PT

        # Create A4 landscape page with 3mm bleed
        w_pt = 841.89
        h_pt = 595.28
        media_rect = fitz.Rect(0, 0, w_pt + 2 * bleed_pt, h_pt + 2 * bleed_pt)
        trim_rect = fitz.Rect(bleed_pt, bleed_pt, bleed_pt + w_pt, bleed_pt + h_pt)
        bleed_rect = media_rect

        page = doc.new_page(width=media_rect.width, height=media_rect.height)
        page.set_mediabox(media_rect)
        page.set_trimbox(trim_rect)
        page.set_bleedbox(bleed_rect)

        # Place Passport Card within safe margins (5mm + 15mm inner margin = 20mm inside trim)
        card_x0 = trim_rect.x0 + (25.0 * MM_TO_PT) # 25mm inside gutter
        card_y0 = trim_rect.y0 + (20.0 * MM_TO_PT) # 20mm top margin
        card_w = 260.0 # pt (4 columns wide)

        # Draw passport title
        page.insert_text(fitz.Point(card_x0, card_y0), "PROJECT PASSPORT", fontsize=10)
        page.insert_text(fitz.Point(card_x0, card_y0 + 16), f"TITLE: {self.passport_data['title']}", fontsize=8)
        page.insert_text(fitz.Point(card_x0, card_y0 + 28), f"TYPOLOGY: {self.passport_data['typology']}", fontsize=8)
        page.insert_text(fitz.Point(card_x0, card_y0 + 40), f"STAGE: {self.passport_data['stage']}", fontsize=8)
        page.insert_text(fitz.Point(card_x0, card_y0 + 52), f"COORDINATES: {self.passport_data['coordinates']}", fontsize=8)

        doc.save(pdf_path)
        doc.close()

        auditor = StandalonePreflightAuditor(pdf_path, safety_margin_mm=5.0)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["dimensions_and_bleed"]["status"], "PASS")
        self.assertEqual(results["checks"]["margin_safety_zone"]["status"], "PASS")

    def test_03_passport_near_edge_triggers_safety_breach(self):
        """
        Verify that placing the passport card within 2mm of the TrimBox boundary
        is immediately caught as a margin safety zone breach by preflight audit.
        """
        pdf_path = os.path.join(self.temp_dir.name, "breaching_passport.pdf")
        doc = fitz.open()
        bleed_pt = 3.0 * MM_TO_PT
        w_pt = 841.89
        h_pt = 595.28

        media_rect = fitz.Rect(0, 0, w_pt + 2 * bleed_pt, h_pt + 2 * bleed_pt)
        trim_rect = fitz.Rect(bleed_pt, bleed_pt, bleed_pt + w_pt, bleed_pt + h_pt)

        page = doc.new_page(width=media_rect.width, height=media_rect.height)
        page.set_trimbox(trim_rect)
        page.set_bleedbox(media_rect)

        # Place text 2mm inside TrimBox (violates 5mm safety boundary)
        breach_x = trim_rect.x0 + (2.0 * MM_TO_PT)
        breach_y = trim_rect.y0 + (2.0 * MM_TO_PT) + 12
        page.insert_text(fitz.Point(breach_x, breach_y), "PROJECT PASSPORT - CRITICAL BREACH", fontsize=8)

        doc.save(pdf_path)
        doc.close()

        auditor = StandalonePreflightAuditor(pdf_path, safety_margin_mm=5.0)
        results = auditor.audit_all()
        self.assertEqual(results["checks"]["margin_safety_zone"]["status"], "FAIL")

if __name__ == "__main__":
    unittest.main()
