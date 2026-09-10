"""
tests/tier4_workloads/test_e2e_preflight_audit.py
Workload 5 (Tier 4): Complete preflight audit execution on compiled artifacts
Authoritative Source: ORIGINAL_REQUEST.md §R5, Acceptance Criteria, spec_miner_print_engine/report.md §6-7
"""

import sys
import os
import unittest
import tempfile
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.fixtures.pdf_generator import create_synthetic_pdf
from tests.tier1_features.test_preflight_cli import StandalonePreflightAuditor

class TestE2EPreflightAudit(unittest.TestCase):
    """
    Validates complete end-to-end preflight auditing against production publication artifacts.
    """

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.publication_pdf = os.path.join(self.temp_dir.name, "production_publication.pdf")
        # Generate fully compliant 4-page publication
        create_synthetic_pdf(
            output_path=self.publication_pdf,
            page_count=4,
            bleed_mm=3.0,
            safety_margin_mm=5.0,
            add_safety_breach=False,
            effective_dpi=300.0,
            tac_percentage=275.0,
            is_cmyk=True
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_01_full_preflight_audit_execution_and_itemized_report(self):
        """
        Execute full preflight audit on compiled publication artifact
        and verify itemized pass/fail results across all preflight checks.
        """
        auditor = StandalonePreflightAuditor(self.publication_pdf)
        results = auditor.audit_all()

        # Overall Status must be PASS
        self.assertEqual(results["status"], "PASS")
        self.assertEqual(results["summary"]["failed"], 0)
        self.assertGreaterEqual(results["summary"]["passed"], 4)

        # Itemized check validations:
        # 1. Dimensions & Bleed
        self.assertEqual(results["checks"]["dimensions_and_bleed"]["status"], "PASS")
        self.assertEqual(len(results["checks"]["dimensions_and_bleed"]["details"]), 4)

        # 2. Margin Safety Zone
        self.assertEqual(results["checks"]["margin_safety_zone"]["status"], "PASS")

        # 3. Font Embedding
        self.assertEqual(results["checks"]["font_embedding"]["status"], "PASS")

        # 4. Image Resolution
        self.assertEqual(results["checks"]["image_resolution"]["status"], "PASS")
        self.assertGreaterEqual(results["checks"]["image_resolution"]["min_dpi"], 300.0)

        # 5. Color & TAC
        self.assertEqual(results["checks"]["color_and_tac"]["status"], "PASS")

        # 6. Collisions
        self.assertEqual(results["checks"]["layout_collisions"]["status"], "PASS")

    def test_02_json_export_and_cli_serializability(self):
        """Verify report serializes cleanly to valid JSON matching schema."""
        auditor = StandalonePreflightAuditor(self.publication_pdf)
        results = auditor.audit_all()

        json_str = json.dumps(results, indent=2)
        parsed = json.loads(json_str)

        self.assertEqual(parsed["status"], "PASS")
        self.assertEqual(parsed["file"], os.path.basename(self.publication_pdf))

if __name__ == "__main__":
    unittest.main()
