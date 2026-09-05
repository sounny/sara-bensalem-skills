#!/usr/bin/env python3
"""
Sara Bensalem Architectural Skills & MCP Server — Comprehensive Automated Test Suite
Validates:
1. monograph_compiler.py (19 empirical looks, Swiss grids, aspect ratios, SVG rendering)
2. audit_portfolio.py (100-point rubric evaluation, keyword matching, redline alerts)
3. wall_section_builder.py (6 assemblies, Glaser U-values, SVG lineweights)
4. plan_compliance_engine.py (PMR 1500mm, 900mm doors, egress corridors, Hesitation buffers)
5. bioclimatic_calculator.py (5 climate zones, solar geometry, stack ventilation, phase lag)
6. joinery_detailer.py (5 joinery typologies, shadow reveals, Blum/Hettich clearances)
7. grill-my-design (5 personas including Visual Curator, 5 dimensions, Socratic crit)
8. mcp-server (JSON-RPC protocol, tool registry, tool dispatching)
"""

import sys
import os
import unittest
import json
import tempfile
import xml.etree.ElementTree as ET

# Configure paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(BASE_DIR, "skills")
MCP_DIR = os.path.join(BASE_DIR, "mcp-server")

sys.path.insert(0, os.path.join(SKILLS_DIR, "portfolio-monograph", "scripts"))
sys.path.insert(0, os.path.join(SKILLS_DIR, "constructive-detail", "scripts"))
sys.path.insert(0, os.path.join(SKILLS_DIR, "spatial-anatomy", "scripts"))
sys.path.insert(0, os.path.join(SKILLS_DIR, "bioclimatic-flows", "scripts"))
sys.path.insert(0, os.path.join(SKILLS_DIR, "interior-joinery", "scripts"))
sys.path.insert(0, os.path.join(SKILLS_DIR, "grill-my-design", "engine"))
sys.path.insert(0, MCP_DIR)


class TestMonographCompiler(unittest.TestCase):
    """Tests the Swiss architectural monograph compiler engine."""

    def setUp(self):
        from monograph_compiler import generate_monograph_svg, LOOKS
        self.generate_svg = generate_monograph_svg
        self.looks = LOOKS

    def test_looks_count(self):
        """Verify that at least 19 empirical looks are registered."""
        self.assertGreaterEqual(len(self.looks), 19)
        expected_looks = [
            "swiss_editorial", "french_luxury", "technical_blueprints",
            "brutalist_tectonics", "vernacular_bioclimatic", "art_deco_moderne",
            "phenomenological_story", "structural_expression", "indic_spatial_systems",
            "ephemeral_scenography", "japandi_wabi_sabi", "alpine_bivouac",
            "landscape_ecology", "urban_morphology", "tropical_resilience",
            "speculative_critical", "trauma_informed_commons", "environmental_simulation",
            "commercial_courtyard"
        ]
        for look_id in expected_looks:
            self.assertIn(look_id, self.looks, f"Expected look '{look_id}' not found in LOOKS.")

    def test_svg_generation_default(self):
        """Test default spread compilation and valid SVG output."""
        svg = self.generate_svg(title="Strasbourg Atelier Pavilion")
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)
        self.assertIn("Strasbourg Atelier Pavilion", svg)
        # Parse XML to guarantee valid SVG syntax
        root = ET.fromstring(svg)
        self.assertEqual(root.tag.split("}")[-1], "svg")

    def test_svg_generation_across_looks(self):
        """Test compiling spreads for multiple distinctive architectural looks."""
        test_looks = ["urban_morphology", "tropical_resilience", "environmental_simulation", "speculative_critical"]
        for lk in test_looks:
            svg = self.generate_svg(title=f"Test {lk}", look_id=lk, columns=12, aspect_ratio="16:9")
            self.assertIn("<svg", svg)
            self.assertIn(f"Test {lk}", svg)
            root = ET.fromstring(svg)
            self.assertIsNotNone(root)

    def test_aspect_ratios(self):
        """Test compilation across supported aspect ratios."""
        ratios = ["16:9", "2:1", "1:1", "4:3", "a4_landscape"]
        for asp in ratios:
            svg = self.generate_svg(title="Aspect Test", aspect_ratio=asp)
            self.assertIn("<svg", svg)
            root = ET.fromstring(svg)
            self.assertIsNotNone(root)

    def test_column_grid_variations(self):
        """Test column configurations (6, 8, 12, 16)."""
        for cols in [6, 8, 12, 16]:
            svg = self.generate_svg(title="Grid Test", columns=cols)
            self.assertIn("swiss-modular-grid", svg)
            root = ET.fromstring(svg)
            self.assertIsNotNone(root)

    def test_nested_svg_viewport_scaling(self):
        """Verify responsive nested SVG technical viewport exists across all aspect ratios."""
        for asp in ["16:9", "2:1", "1:1", "4:3", "a4_landscape"]:
            svg = self.generate_svg(title="Responsive Viewport", aspect_ratio=asp)
            self.assertIn('viewBox="0 0 1020 620"', svg)
            self.assertIn('preserveAspectRatio="xMinYMid meet"', svg)
            root = ET.fromstring(svg)
            self.assertIsNotNone(root)


class TestAuditPortfolio(unittest.TestCase):
    """Tests the 100-point structural portfolio audit engine."""

    def setUp(self):
        from audit_portfolio import audit_pdf
        self.audit_pdf = audit_pdf

    def test_missing_pdf(self):
        """Auditing a nonexistent file returns a descriptive error dictionary with zero score."""
        result = self.audit_pdf("nonexistent_path_to_portfolio_9999.pdf")
        self.assertIn("error", result)
        self.assertEqual(result.get("status"), "error")
        self.assertEqual(result.get("total_score"), 0)
        self.assertEqual(result.get("score"), 0)

    def test_sample_portfolio_audit(self):
        """Audit an existing real portfolio PDF from the library."""
        sample_pdf = os.path.join(
            "g:\\", "My Drive", "Portfolios", "Palak_Bhattad_MUD_CEPT",
            "Palak_Bhattad_Selected_Works_MUD_CEPT.pdf"
        )
        if os.path.exists(sample_pdf):
            result = self.audit_pdf(sample_pdf)
            self.assertNotIn("error", result)
            self.assertIn("filename", result)
            self.assertIn("total_score", result)
            self.assertIn("score", result)
            self.assertIn("overall_score", result)
            self.assertEqual(result["score"], result["total_score"])
            self.assertEqual(result["total_score"], result["overall_score"])
            self.assertIn("category_scores", result)
            self.assertIn("traps_detected", result)
            self.assertIn("prescribed_remedies", result)
            self.assertGreater(result["total_score"], 0)
            self.assertLessEqual(result["total_score"], 100)

    def test_empty_pdf_handled_gracefully(self):
        """Auditing a 0-byte file returns an error dictionary with zero score."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
            empty_path = tf.name
        try:
            result = self.audit_pdf(empty_path)
            self.assertEqual(result.get("status"), "error")
            self.assertIn("Empty file", result.get("error", ""))
            self.assertEqual(result.get("total_score"), 0)
            self.assertEqual(result.get("score"), 0)
        finally:
            if os.path.exists(empty_path):
                os.remove(empty_path)

    def test_corrupted_pdf_handled_gracefully(self):
        """Auditing corrupted/invalid non-PDF bytes returns an error dictionary."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
            tf.write(b"NOT A VALID PDF FILE HEADER")
            corrupt_path = tf.name
        try:
            result = self.audit_pdf(corrupt_path)
            self.assertEqual(result.get("status"), "error")
            self.assertIn("Corrupted or invalid", result.get("error", ""))
            self.assertEqual(result.get("total_score"), 0)
            self.assertEqual(result.get("score"), 0)
        finally:
            if os.path.exists(corrupt_path):
                os.remove(corrupt_path)

    def test_score_aliases_present(self):
        """Verify score, total_score, and overall_score aliases are present and consistent."""
        import fitz
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tf:
            test_path = tf.name
        try:
            doc = fitz.open()
            page = doc.new_page(width=842, height=595)
            page.insert_text((50, 50), "1:100 Floor Plan Setting Out 1:20 Wall Section EPDM Thermal Break 1500mm PMR Egress Travel")
            page.insert_text((50, 100), "Project Passport: Lead Project Architect Role Typology Gross Floor Area Macro Meso Micro")
            doc.save(test_path)
            doc.close()

            result = self.audit_pdf(test_path)
            self.assertIn("score", result)
            self.assertIn("total_score", result)
            self.assertIn("overall_score", result)
            self.assertEqual(result["score"], result["total_score"])
            self.assertEqual(result["total_score"], result["overall_score"])
            self.assertGreater(result["total_score"], 0)
        finally:
            if os.path.exists(test_path):
                os.remove(test_path)


class TestWallSectionBuilder(unittest.TestCase):
    """Tests 1:20 constructive wall section generation and U-value calculations."""

    def setUp(self):
        from wall_section_builder import (
            calculate_u_value, generate_wall_section_svg,
            ASSEMBLY_PRESETS, LAYERS_DB
        )
        self.calc_u = calculate_u_value
        self.gen_svg = generate_wall_section_svg
        self.presets = ASSEMBLY_PRESETS
        self.layers_db = LAYERS_DB

    def test_assembly_presets_count(self):
        """Verify all 6 empirical wall assemblies exist."""
        expected = [
            "granite_hemp", "tropical_timber", "terracotta_cavity",
            "nubian_sandstone", "alpine_monocoque", "commercial_curtain"
        ]
        for key in expected:
            self.assertIn(key, self.presets)

    def test_terracotta_cavity_has_thermal_break(self):
        """Verify regional terracotta cavity assembly contains thermal_break for continuity."""
        layers = self.presets["terracotta_cavity"]["layers"]
        self.assertIn("thermal_break", layers)

    def test_u_value_calculation(self):
        """Verify physical thermal resistance and U-value calculations."""
        preset = self.presets["granite_hemp"]
        layers = [self.layers_db[k] for k in preset["layers"] if k in self.layers_db]
        u_val, thickness = self.calc_u(layers)
        self.assertGreater(thickness, 200)
        self.assertGreater(u_val, 0.05)
        self.assertLess(u_val, 1.5)

    def test_svg_export(self):
        """Test generating SVG wall section to temporary file."""
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            temp_path = tf.name
        try:
            for assembly in ["granite_hemp", "tropical_timber", "terracotta_cavity"]:
                self.gen_svg(temp_path, assembly_key=assembly)
                self.assertTrue(os.path.exists(temp_path))
                with open(temp_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertIn("<svg", content)
                self.assertIn("Constructive Wall Section", content)
                root = ET.fromstring(content)
                self.assertIsNotNone(root)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_subfolder_output_path_creation(self):
        """Verify generators create missing nested parent directories automatically."""
        import shutil
        temp_dir = tempfile.mkdtemp()
        try:
            nested_path = os.path.join(temp_dir, "nested", "sub", "test_wall.svg")
            self.gen_svg(nested_path, assembly_key="granite_hemp")
            self.assertTrue(os.path.exists(nested_path))
            with open(nested_path, "r", encoding="utf-8") as f:
                self.assertIn("<svg", f.read())
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)


class TestPlanComplianceEngine(unittest.TestCase):
    """Tests 1:100 floor plan PMR / ADA accessibility and egress verification."""

    def setUp(self):
        from plan_compliance_engine import validate_plan_compliance, generate_plan_svg
        self.validate = validate_plan_compliance
        self.gen_plan = generate_plan_svg

    def test_compliant_plan(self):
        """Verify compliant dimensions pass French PMR and US ADA standards."""
        res = self.validate(
            door_clear_width=900,
            vestibule_diameter=1500,
            corridor_width=1600,
            hesitation_width=2400
        )
        self.assertEqual(res["compliance_status"], "COMPLIANT")
        self.assertEqual(len(res["violations"]), 0)

    def test_non_compliant_door_and_vestibule(self):
        """Verify undersized doors and turning circles trigger non-compliance."""
        res = self.validate(
            door_clear_width=750,
            vestibule_diameter=1200,
            corridor_width=1100,
            hesitation_width=1500
        )
        self.assertEqual(res["compliance_status"], "NON_COMPLIANT")
        self.assertGreaterEqual(len(res["violations"]), 2)
        v_str = " ".join(res["violations"])
        self.assertIn("Door clear width", v_str)
        self.assertIn("Vestibule rotation", v_str)

    def test_plan_svg_generation(self):
        """Verify vector SVG floor plan generation with accessibility circles."""
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            temp_path = tf.name
        try:
            self.gen_plan(temp_path, door_clear=900, vestibule_dia=1500, corridor_w=1600)
            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("<svg", content)
            self.assertIn("Spatial Anatomy", content)
            self.assertIn("1500", content)
            root = ET.fromstring(content)
            self.assertIsNotNone(root)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_compliance_badge_styling(self):
        """Verify compliance badge style override prevents dark-on-dark text and includes verdict."""
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            temp_path = tf.name
        try:
            self.gen_plan(temp_path, door_clear=900, vestibule_dia=1500, corridor_w=1600)
            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn('style="fill:#FFFFFF;"', content)
            self.assertIn("FULL COMPLIANCE", content)
            root = ET.fromstring(content)
            self.assertIsNotNone(root)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestBioclimaticCalculator(unittest.TestCase):
    """Tests solar altitude, shading overhang, and stack ventilation calculations."""

    def setUp(self):
        from bioclimatic_calculator import (
            calculate_solar_altitude, calculate_overhang_depth,
            calculate_stack_ventilation, generate_bioclimatic_svg,
            CLIMATE_PRESETS
        )
        self.calc_solar = calculate_solar_altitude
        self.calc_overhang = calculate_overhang_depth
        self.calc_stack = calculate_stack_ventilation
        self.gen_svg = generate_bioclimatic_svg
        self.presets = CLIMATE_PRESETS

    def test_solar_altitudes(self):
        """Verify solar altitude angles across northern latitudes."""
        # Strasbourg: 48.58°N
        summer, winter, equinox = self.calc_solar(48.58)
        self.assertAlmostEqual(summer, 64.87, delta=0.5)
        self.assertAlmostEqual(winter, 17.97, delta=0.5)
        self.assertAlmostEqual(equinox, 41.42, delta=0.5)
        self.assertGreater(summer, equinox)
        self.assertGreater(equinox, winter)

    def test_southern_hemisphere_calculation(self):
        """Verify southern hemisphere latitude correctly calculates solar geometry."""
        # Bandung: -6.91°S
        summer, winter, eq = self.calc_solar(-6.91)
        self.assertGreater(summer, 50.0)
        self.assertGreater(winter, 50.0)
        self.assertGreater(eq, 80.0)

    def test_overhang_depth(self):
        """Verify optimal overhang depth for shading."""
        overhang = self.calc_overhang(2.4, 65.0)
        self.assertGreater(overhang, 0.5)
        self.assertLess(overhang, 2.5)

    def test_stack_ventilation(self):
        """Verify stack ventilation buoyancy velocity and airflow rate."""
        velocity, flow_rate = self.calc_stack(9.2, 6.0)
        self.assertGreater(velocity, 0.5)
        self.assertGreater(flow_rate, 1.0)

    def test_climate_presets(self):
        """Verify all 5 climate presets exist."""
        expected = [
            "temperate_strasbourg", "mediterranean_alexandria",
            "hot_arid_aswan", "composite_bhopal", "tropical_bandung"
        ]
        for key in expected:
            self.assertIn(key, self.presets)

    def test_svg_generation(self):
        """Verify vector bioclimatic flow diagram generation."""
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            temp_path = tf.name
        try:
            self.gen_svg(temp_path, climate_key="hot_arid_aswan")
            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("<svg", content)
            self.assertIn("Bioclimatic Vectors", content)
            root = ET.fromstring(content)
            self.assertIsNotNone(root)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_solar_ray_geometry_in_svg(self):
        """Verify vector solar angles are dynamically rendered in SVG geometry."""
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            temp_path = tf.name
        try:
            self.gen_svg(temp_path, climate_key="temperate_strasbourg")
            with open(temp_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("solar-summer", content)
            self.assertIn("solar-winter", content)
            self.assertIn("D = ", content)
            root = ET.fromstring(content)
            self.assertIsNotNone(root)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestInteriorJoinery(unittest.TestCase):
    """Tests 1:5 custom millwork, shadow reveals, and hardware clearances."""

    def setUp(self):
        from joinery_detailer import generate_joinery_svg, JOINERY_PRESETS
        self.gen_svg = generate_joinery_svg
        self.presets = JOINERY_PRESETS

    def test_joinery_presets_count(self):
        """Verify all 5 empirical joinery typologies."""
        expected = [
            "cabinetry_reveal", "riparian_deck_pin", "jali_screen_pocket",
            "sliding_pocket_door", "stone_wood_shadow"
        ]
        for key in expected:
            self.assertIn(key, self.presets)

    def test_joinery_svg_generation(self):
        """Verify vector 1:5 joinery detail generation."""
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            temp_path = tf.name
        try:
            for detail in ["cabinetry_reveal", "stone_wood_shadow", "jali_screen_pocket"]:
                self.gen_svg(temp_path, detail_key=detail)
                self.assertTrue(os.path.exists(temp_path))
                with open(temp_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertIn("<svg", content)
                self.assertIn("1:5 Custom Architectural Joinery", content)
                root = ET.fromstring(content)
                self.assertIsNotNone(root)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestGrillMyDesign(unittest.TestCase):
    """Tests the Socratic jury review engine and the 5 critique personas."""

    def setUp(self):
        from critique_engine import GrillEngine
        from models import JuryPersona
        self.engine = GrillEngine()
        self.personas = JuryPersona

    def test_full_tribunal_grill(self):
        """Run full tribunal critique on a submission text."""
        submission = (
            "Heritage timber library in Strasbourg with 1:20 Breton granite wall sections, "
            "1500mm PMR wheelchair turning circles, continuous EPDM waterproofing, and 12-column Swiss grid."
        )
        report = self.engine.grill(submission, persona=self.personas.FULL_TRIBUNAL)
        self.assertIsNotNone(report.verdict)
        self.assertGreaterEqual(report.overall_score, 0)
        self.assertLessEqual(report.overall_score, 100)
        self.assertIsNotNone(report.recruiter_15s_takeaway)
        self.assertGreaterEqual(len(report.dimension_scores), 5)
        # Ensure 5th dimension is evaluated
        dim_names = [d.name for d in report.dimension_scores]
        self.assertTrue(any("Visual" in name or "Swiss" in name for name in dim_names))

    def test_visual_curator_persona(self):
        """Run critique with the dedicated Visual Curator persona."""
        submission = "A portfolio project with 4-image grid and 1000-word text essay without white space."
        report = self.engine.grill(submission, persona=self.personas.VISUAL_CURATOR)
        self.assertIsNotNone(report.verdict)
        self.assertGreater(len(report.top_vulnerabilities), 0)

    def test_render_trap_detection(self):
        """Verify that pure rendering fluff triggers a render trap alert."""
        fluff_submission = "Photorealistic 3D Lumion exterior views, sunset golden hour renders, high-end CGI visualization."
        report = self.engine.grill(fluff_submission, persona=self.personas.HIRING_DIRECTOR)
        self.assertIn("RENDER TRAP", report.verdict)


class TestMCPServerHandlers(unittest.TestCase):
    """Tests MCP tool definitions and tool handlers in mcp-server/server.py."""

    def setUp(self):
        import server
        self.server = server

    def test_tools_list(self):
        """Verify all 10 MCP tools are registered with schemas."""
        self.assertEqual(len(self.server.TOOLS), 10)
        tool_names = [t["name"] for t in self.server.TOOLS]
        expected_tools = [
            "list_sara_skills", "audit_portfolio", "grill_my_design",
            "build_1_20_wall_section", "validate_pmr_and_egress",
            "calculate_bioclimatic_flows", "generate_1_5_joinery",
            "compile_monograph_spread", "list_portfolio_looks",
            "get_architectural_movement"
        ]
        for t in expected_tools:
            self.assertIn(t, tool_names)

    def test_handle_list_skills(self):
        """Test handle_list_skills tool response."""
        res = self.server.handle_call_tool("list_sara_skills", {})
        self.assertIn("studio", res)
        self.assertIn("skills", res)
        self.assertEqual(len(res["skills"]), 6)

    def test_handle_list_portfolio_looks(self):
        """Test retrieving all looks and a specific look."""
        res = self.server.handle_call_tool("list_portfolio_looks", {})
        self.assertIn("total_looks", res)
        self.assertGreaterEqual(res["total_looks"], 19)

        single = self.server.handle_call_tool("list_portfolio_looks", {"look_id": "urban_morphology"})
        self.assertIn("title", single)
        self.assertIn("palette", single)

    def test_handle_get_architectural_movement(self):
        """Test retrieving architectural movement theory and rubrics."""
        res = self.server.handle_call_tool("get_architectural_movement", {"movement": "brutalist"})
        self.assertIn("name", res)
        self.assertIn("spatial_concepts", res)

    def test_handle_build_wall_section(self):
        """Test wall section MCP tool."""
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            out_file = tf.name
        try:
            res = self.server.handle_call_tool("build_1_20_wall_section", {"assembly": "granite_hemp", "output_path": out_file})
            self.assertEqual(res["status"], "success")
            self.assertIn("u_value", res)
            self.assertTrue(os.path.exists(out_file))
        finally:
            if os.path.exists(out_file):
                os.remove(out_file)

    def test_handle_validate_pmr(self):
        """Test PMR / egress MCP tool."""
        res = self.server.handle_call_tool("validate_pmr_and_egress", {"door_clear_width": 920, "vestibule_diameter": 1600})
        self.assertEqual(res["compliance_status"], "COMPLIANT")

    def test_handle_calculate_bioclimatic(self):
        """Test bioclimatic calculation MCP tool."""
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            out_file = tf.name
        try:
            res = self.server.handle_call_tool("calculate_bioclimatic_flows", {"climate_zone": "temperate_strasbourg", "output_path": out_file})
            self.assertIn("summer_solstice_noon", res)
            self.assertIn("optimal_overhang_m", res)
            self.assertTrue(os.path.exists(out_file))
        finally:
            if os.path.exists(out_file):
                os.remove(out_file)

    def test_handle_generate_joinery(self):
        """Test joinery MCP tool."""
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            out_file = tf.name
        try:
            res = self.server.handle_call_tool("generate_1_5_joinery", {"detail_type": "cabinetry_reveal", "output_path": out_file})
            self.assertEqual(res["status"], "success")
            self.assertTrue(os.path.exists(out_file))
        finally:
            if os.path.exists(out_file):
                os.remove(out_file)

    def test_handle_compile_monograph_spread(self):
        """Test monograph compilation MCP tool."""
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            out_file = tf.name
        try:
            res = self.server.handle_call_tool("compile_monograph_spread", {
                "title": "Al-Qarawiyyin Archive",
                "location": "Fez, Morocco",
                "typology": "Civic Archive",
                "look": "desert_vernacular",
                "output_path": out_file
            })
            self.assertEqual(res["status"], "success")
            self.assertTrue(os.path.exists(out_file))
        finally:
            if os.path.exists(out_file):
                os.remove(out_file)

    def test_handle_grill(self):
        """Test grill_my_design MCP tool."""
        res = self.server.handle_call_tool("grill_my_design", {
            "submission_text": "Mass timber library with continuous insulation and 1500mm wheelchair circulation.",
            "persona": "visual"
        })
        self.assertIn("verdict", res)
        self.assertIn("overall_score", res)
        self.assertIn("dimension_scores", res)

    def test_handle_grill_persona_synonyms(self):
        """Verify persona aliases (e.g. constructive_lead, visual_curator) are accepted."""
        for p in ["constructive_lead", "hiring_director", "spatial_chair", "environmental_auditor", "visual_curator"]:
            res = self.server.handle_call_tool("grill_my_design", {
                "submission_text": "Mass timber library with 1:20 constructive sections, 1500mm PMR turning, 12-column Swiss grid.",
                "persona": p
            })
            self.assertIn("verdict", res)
            self.assertIn("overall_score", res)

    def test_handle_pmr_aliases(self):
        """Test PMR / egress MCP tool with alias argument names."""
        res = self.server.handle_call_tool("validate_pmr_and_egress", {"door_clear_mm": 900, "vestibule_dia": 1550})
        self.assertEqual(res["compliance_status"], "COMPLIANT")


if __name__ == "__main__":
    unittest.main()
