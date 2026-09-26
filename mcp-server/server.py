#!/usr/bin/env python3
"""
Sara Bensalem Skills MCP Server (2026 Enhanced Edition)
Exposes physical architectural design, portfolio auditing, 1:20 constructive detailing,
bioclimatic thermodynamics, 1:5 joinery, and Socratic design crits via the Model Context Protocol (MCP stdio JSON-RPC).
Distilled from empirical analysis of 20+ premier international spatial portfolios.
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
Website: https://skills.sarabensalem.com
"""

import sys
import json
import os
import contextlib

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
SKILLS_DIR = os.path.join(BASE_DIR, "skills")

# Load bundled archetypes and rubric
def load_json_resource(filename, fallback):
    p = os.path.join(SKILLS_DIR, "portfolio-monograph", "resources", filename)
    if not os.path.exists(p):
        p = os.path.join(SKILLS_DIR, "portfolio-design", "resources", filename)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

ARCHETYPES = load_json_resource("archetypes.json", [])
RUBRIC = load_json_resource("rubric_100pt.json", {})

TOOLS = [
    {
        "name": "list_sara_skills",
        "description": "Lists all available physical architectural skills in the Sara Bensalem Skills Studio (skills.sarabensalem.com).",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "audit_portfolio",
        "description": "Performs an automated technical audit of an architectural portfolio PDF against the Sara Bensalem 100-Point Rubric, evaluating multi-scalar presence and detecting 'render traps'.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pdf_path": {"type": "string", "description": "Absolute path to the portfolio PDF file to audit."}
            },
            "required": ["pdf_path"]
        }
    },
    {
        "name": "grill_my_design",
        "description": "Runs an unsparing Socratic critique jury (Harvard GSD / Foster + Partners hiring standards) across 5 personas to detect thermal bridges, egress bottlenecks, scalar disconnects, and recruiter trust risks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "submission_text": {"type": "string", "description": "Project statement, portfolio description, or design rationale."},
                "persona": {"type": "string", "enum": ["full", "technical", "recruiter", "spatial", "environmental", "visual"], "description": "Jury persona to emphasize."}
            },
            "required": ["submission_text"]
        }
    },
    {
        "name": "build_1_20_wall_section",
        "description": "Generates a buildable 1:20 constructive wall section drawing with Glaser U-value calculation, thermal breaks, and material callouts across 6 empirical assemblies.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "assembly": {"type": "string", "enum": ["granite_hemp", "tropical_timber", "terracotta_cavity", "nubian_sandstone", "alpine_monocoque", "commercial_curtain"], "description": "Assembly preset type."},
                "output_path": {"type": "string", "description": "Target SVG output file path."}
            },
            "required": []
        }
    },
    {
        "name": "validate_pmr_and_egress",
        "description": "Audits floor plans for French PMR / US ADA wheelchair compliance (1500mm turning circles, 900mm doors), IBC emergency egress, and trauma-informed hesitation buffer zones.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "door_clear_width": {"type": "number", "description": "Clear passage width of doors in mm (min 830mm required)."},
                "vestibule_diameter": {"type": "number", "description": "Clear unobstructed diameter in airlock in mm (min 1500mm required)."},
                "corridor_width": {"type": "number", "description": "Corridor width in mm (min 1400mm for two-way passing)."},
                "hesitation_width": {"type": "number", "description": "Space for Hesitation threshold buffer width in mm (min 2000mm)."},
                "output_path": {"type": "string", "description": "Optional SVG plan output path."}
            },
            "required": ["door_clear_width", "vestibule_diameter"]
        }
    },
    {
        "name": "calculate_bioclimatic_flows",
        "description": "Computes seasonal solar altitude angles, optimal overhang depths, and natural thermal stack cross-ventilation buoyancy loops across 5 empirical climate zones.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "climate_zone": {"type": "string", "enum": ["temperate_strasbourg", "mediterranean_alexandria", "hot_arid_aswan", "composite_bhopal", "tropical_bandung"], "description": "Bioclimatic zone preset."},
                "latitude": {"type": "number", "description": "Site latitude in decimal degrees (overrides preset)."},
                "output_path": {"type": "string", "description": "Target SVG output file path."}
            },
            "required": []
        }
    },
    {
        "name": "generate_1_5_joinery",
        "description": "Generates 1:5 custom cabinetry, shadow reveals (joint creux), and concealed Blum/Hettich/HAWA hardware details across 5 joinery typologies.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "detail_type": {"type": "string", "enum": ["cabinetry_reveal", "riparian_deck_pin", "jali_screen_pocket", "sliding_pocket_door", "stone_wood_shadow"], "description": "Joinery detail typology."},
                "output_path": {"type": "string", "description": "Target SVG output file path."}
            },
            "required": []
        }
    },
    {
        "name": "compile_monograph_spread",
        "description": "Compiles a complete publication-grade Swiss architectural monograph spread with Project Passport, Swiss modular grid, and multi-scalar evidence matrix from 19 empirical portfolio looks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Project title."},
                "location": {"type": "string", "description": "Project location."},
                "typology": {"type": "string", "description": "Typology description."},
                "look": {"type": "string", "description": "Look ID from 19 looks library (e.g. 'swiss_editorial', 'urban_morphology', 'tropical_resilience', 'speculative_critical', 'trauma_informed_commons', 'environmental_simulation', 'commercial_courtyard')."},
                "columns": {"type": "integer", "description": "Swiss grid column count (6, 8, 9, 10, 12, 16)."},
                "aspect": {"type": "string", "description": "Aspect ratio (16:9, 2:1, 1:1, 4:3, a4_landscape)."},
                "output_path": {"type": "string", "description": "Target SVG file path."}
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_portfolio_looks",
        "description": "Retrieves the 19 empirical publication-grade portfolio design looks, palettes, and typographic pairings.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "look_id": {"type": "string", "description": "Optional specific look ID."}
            },
            "required": []
        }
    },
    {
        "name": "get_architectural_movement",
        "description": "Retrieves architectural theory, concepts, and critique rubrics for 20 canonical movements and contemporary design systems.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "movement": {"type": "string", "description": "Movement ID or name (e.g. 'brutalist', 'urban_morphology', 'tropical_resilience', 'speculative_critical', 'trauma_informed_commons', 'indic_spatial_systems')."}
            },
            "required": ["movement"]
        }
    },
    {
        "name": "generate_spatial_journey",
        "description": "Generates a 3-part phenomenological spatial journey (luminance gradient, acoustic sanctuary attenuation, volumetric compression/expansion) across spatial sequences.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "preset": {"type": "string", "enum": ["temperate_museum", "desert_sanctuary", "urban_courtyard"], "description": "Spatial sequence preset."},
                "output_path": {"type": "string", "description": "Target SVG output file path."}
            },
            "required": []
        }
    },
    {
        "name": "generate_monograph_spread",
        "description": "Generates a publication-grade vector SVG monograph spread from 10 architectural archetypes using the Spatial Stitch generative design engine.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "archetype": {"type": "string", "description": "Layout archetype name (e.g. 'THE_CONSTRUCTIVE_PROOF', 'THE_PASSPORT', 'THE_5_ACT_PORTFOLIO', 'THE_MONOGRAPH_SPREAD')."},
                "format": {"type": "string", "enum": ["LANDSCAPE_16_9", "SPREAD_A4_LANDSCAPE", "SINGLE_A4_PORTRAIT", "SQUARE_1_1"], "description": "Canvas format."},
                "title": {"type": "string", "description": "Project title."},
                "output_path": {"type": "string", "description": "Target output file path (.svg or .html)."}
            },
            "required": []
        }
    },
    {
        "name": "audit_monograph_spread",
        "description": "Runs the Sara Bensalem 100-Point Anti-Render-Trap Audit on a generated or existing architectural spread SVG.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "svg_file": {"type": "string", "description": "Absolute path to the SVG spread file to audit."}
            },
            "required": ["svg_file"]
        }
    },
    {
        "name": "extract_design_tokens",
        "description": "Extracts dominant color palettes, relative luminance, and WCAG 2.1 contrast hierarchies from architectural images/renderings to generate DESIGN.md tokens.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Path to the architectural rendering or photograph."}
            },
            "required": ["image_path"]
        }
    },
    {
        "name": "audit_publication_preflight",
        "description": "Performs prepress print preflight validation (FOGRA51/52 CMYK, Total Area Coverage, bleed zones, font embedding, image DPI) for editorial publications.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to PDF publication file to preflight."},
                "pdf_path": {"type": "string", "description": "Alternative path parameter to PDF publication file."}
            },
            "required": []
        }
    },
    {
        "name": "model_spatial_journey",
        "description": "Models and evaluates a multi-threshold phenomenological spatial journey (luminance lux gradients, acoustic attenuation, volumetric compression) across custom zones or named sequences.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sequence_name": {"type": "string", "description": "Optional preset sequence name or colon-delimited sequence string."},
                "zones": {"type": "array", "description": "List of spatial zone objects or colon-delimited zone strings ('Name:lux:dba:height_m:material:title')."},
                "output_svg": {"type": "string", "description": "Target SVG output file path."}
            },
            "required": []
        }
    },
    {
        "name": "audit_courtyard_shading",
        "description": "Audits subtractive courtyard stereotomy for self-shading adequacy against the desert standard (H/W >= 1.50).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "courtyard_height": {"type": "number", "description": "Courtyard wall height in meters."},
                "courtyard_width": {"type": "number", "description": "Courtyard width in meters."},
                "solar_altitude_deg": {"type": "number", "description": "Optional solar altitude angle in degrees (default: 65.0)."}
            },
            "required": ["courtyard_height", "courtyard_width"]
        }
    },
    {
        "name": "generate_spatial_stitch_spread",
        "description": "Generates a publication-grade vector SVG monograph spread from 10 architectural archetypes using the Spatial Stitch generative design engine.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "archetype": {"type": "string", "description": "Layout archetype name (e.g. 'THE_CONSTRUCTIVE_PROOF', 'THE_PASSPORT', 'THE_5_ACT_PORTFOLIO', 'THE_MONOGRAPH_SPREAD')."},
                "format": {"type": "string", "enum": ["LANDSCAPE_16_9", "SPREAD_A4_LANDSCAPE", "SINGLE_A4_PORTRAIT", "SQUARE_1_1"], "description": "Canvas format."},
                "title": {"type": "string", "description": "Project title."},
                "output_svg": {"type": "string", "description": "Target output file path (.svg)."}
            },
            "required": []
        }
    },
    {
        "name": "audit_spatial_spread",
        "description": "Runs the Sara Bensalem 100-Point Anti-Render-Trap Audit on a generated or existing architectural spread SVG.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "svg_path": {"type": "string", "description": "Absolute path to the SVG spread file to audit."},
                "svg_file": {"type": "string", "description": "Alternative path parameter to SVG spread file."}
            },
            "required": []
        }
    },
    {
        "name": "extract_design_system_pdf",
        "description": "Extracts typographic scales, column grids, margins, and color palettes from any architectural portfolio or monograph PDF to produce a Google Stitch design-system.json structure.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pdf_path": {"type": "string", "description": "Path to PDF monograph, portfolio, or brand guide."},
                "max_pages": {"type": "integer", "description": "Maximum pages to sample for typographic inspection (default: 10)."}
            },
            "required": ["pdf_path"]
        }
    },
    {
        "name": "compile_publication_monograph",
        "description": "Compiles a high-speed publication monograph via dual-engine Typst or W3C CSS Paged.js web-to-print pipelines.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_path": {"type": "string", "description": "Path to input document (.typ, .html, or manifest.json)."},
                "output_path": {"type": "string", "description": "Destination path for compiled PDF (optional)."},
                "engine": {"type": "string", "enum": ["typst", "pagedjs", "both", "auto"], "description": "Compilation engine (default: 'auto')."}
            },
            "required": ["input_path"]
        }
    }
]

@contextlib.contextmanager
def capture_stdout():
    old_stdout = sys.stdout
    sys.stdout = sys.stderr
    try:
        yield
    finally:
        sys.stdout = old_stdout

def handle_list_skills():
    return {
        "studio": 'Sara Bensalem Studio • Strasbourg Atelier [48°35\'05"N 07°45\'02"E]',
        "skills": [
            {"name": "portfolio-monograph", "alias": "sara-bensalem-portfolio-design", "role": "Multi-spread Swiss monograph publishing, 19 curated looks & Project Passports"},
            {"name": "constructive-detail", "role": "1:20 buildable wall sections across 6 assemblies & Glaser U-values (DIN 4108-3)"},
            {"name": "spatial-anatomy", "role": "1:100 regulatory plans, circulation vectors, 1500mm PMR wheelchair turning & Space for Hesitation"},
            {"name": "bioclimatic-flows", "role": "Solar geometry vectors, shading overhang depth & stack ventilation draft across 5 climate zones"},
            {"name": "interior-joinery", "role": "1:5 custom millwork reveals, shadow reveals (joint creux) & concealed hardware tolerances"},
            {"name": "grill-my-design", "role": "Socratic architectural review jury, 22 render traps & multi-round defense evaluation"},
            {"name": "spatial-choreography", "role": "Phenomenological spatial journeys, luminance lux gradients, acoustic sanctuary & subtractive courtyards"},
            {"name": "spatial-stitch", "role": "Generative Swiss 16:9 monograph vector spreads, layout archetypes & 100-point rubric audits"},
            {"name": "design-md-extractor", "role": "Design token reverse engineering from images/drawings, palette extraction & WCAG contrast audit"},
            {"name": "editorial-studio", "role": "Publication-grade prepress print preflight, FOGRA51 CMYK color compliance & typography audit"}
        ],
        "total_empirical_looks": len(load_json_resource("portfolio_looks_library.json", {})),
        "total_archetypes": len(ARCHETYPES)
    }

def handle_grill(submission_text, persona="full", output_svg=None, return_questions=False, answers=None, round_num=None, typology=None):
    grill_dir = os.path.join(SKILLS_DIR, "grill-my-design", "engine")
    if "models" in sys.modules:
        mod_file = getattr(sys.modules["models"], "__file__", "") or ""
        if not mod_file.startswith(grill_dir):
            del sys.modules["models"]
    if grill_dir in sys.path:
        sys.path.remove(grill_dir)
    sys.path.insert(0, grill_dir)
    try:
        from critique_engine import GrillEngine
        from models import JuryPersona
        p_str = str(persona).lower()
        p_enum = JuryPersona.FULL_TRIBUNAL
        if p_str in ("technical", "constructive_lead", "constructive"): p_enum = JuryPersona.CONSTRUCTIVE_LEAD
        elif p_str in ("recruiter", "hiring_director", "hiring"): p_enum = JuryPersona.HIRING_DIRECTOR
        elif p_str in ("spatial", "spatial_chair"): p_enum = JuryPersona.SPATIAL_CHAIR
        elif p_str in ("environmental", "environmental_auditor"): p_enum = JuryPersona.ENVIRONMENTAL_AUDITOR
        elif p_str in ("visual", "visual_curator", "curator"): p_enum = JuryPersona.VISUAL_CURATOR
        
        engine = GrillEngine()
        report = engine.grill(submission_text, p_enum, typology_override=typology, current_round=round_num or 1)
        
        if answers and isinstance(answers, dict):
            report = engine.evaluate_defense(report, answers)
            
        svg_file = None
        if output_svg:
            engine.generate_svg_stamp(report, output_path=output_svg)
            svg_file = output_svg

        res = {
            "verdict": report.verdict,
            "overall_score": report.overall_score,
            "pre_defense_score": report.pre_defense_score,
            "typology": report.typology,
            "15s_takeaway": report.recruiter_15s_takeaway,
            "dimension_scores": [{"name": d.name, "score": d.score, "critique": d.critique} for d in report.dimension_scores],
            "vulnerabilities": [{"question": v.interrogation_question, "vulnerability": v.vulnerability_detected, "remedy": v.redline_fix, "severity": v.severity.value, "trap_id": getattr(v, "trap_id", None)} for v in report.top_vulnerabilities],
            "defense_remedies": report.defense_remedies,
            "next_crit_prompt": report.next_crit_prompt
        }
        if svg_file:
            res["svg_plate"] = svg_file
        if return_questions:
            res["ask_questions_payload"] = engine.get_ask_question_payload(report, max_questions=3, round_num=round_num)
            
        return res
    except Exception as e:
        return {"error": str(e)}

def handle_pmr_audit(door_clear, vestibule_dia, corridor_w=1600, hesitation_w=2400, output_path=None):
    sys.path.insert(0, os.path.join(SKILLS_DIR, "spatial-anatomy", "scripts"))
    try:
        from plan_compliance_engine import validate_plan_compliance, generate_plan_svg
        report = validate_plan_compliance(door_clear, vestibule_dia, corridor_w, hesitation_w)
        if output_path:
            generate_plan_svg(output_path, door_clear, vestibule_dia, corridor_w)
            report["svg_generated"] = output_path
        return report
    except Exception as e:
        return {"error": str(e)}

def handle_call_tool(tool_name, arguments):
    if tool_name == "list_sara_skills":
        return handle_list_skills()
    elif tool_name == "grill_my_design":
        return handle_grill(
            arguments.get("submission_text", ""), 
            arguments.get("persona", "full"),
            output_svg=arguments.get("output_svg"),
            return_questions=arguments.get("return_questions", False),
            answers=arguments.get("answers"),
            round_num=arguments.get("round"),
            typology=arguments.get("typology")
        )
    elif tool_name == "validate_pmr_and_egress":
        door = arguments.get("door_clear_width") or arguments.get("door_clear_mm") or arguments.get("door_clear", 900)
        vest = arguments.get("vestibule_diameter") or arguments.get("vestibule_diameter_mm") or arguments.get("vestibule_dia", 1500)
        corr = arguments.get("corridor_width") or arguments.get("corridor_width_mm") or 1600
        hes = arguments.get("hesitation_width") or arguments.get("hesitation_width_mm") or 2400
        out_path = arguments.get("output_path")
        return handle_pmr_audit(door, vest, corr, hes, out_path)
    elif tool_name == "build_1_20_wall_section":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "constructive-detail", "scripts"))
        from wall_section_builder import generate_wall_section_svg, calculate_u_value, LAYERS_DB, ASSEMBLY_PRESETS
        assembly = arguments.get("assembly", "granite_hemp")
        out = arguments.get("output_path", "wall_section_1_20.svg")
        generate_wall_section_svg(out, assembly_key=assembly)
        preset = ASSEMBLY_PRESETS.get(assembly, ASSEMBLY_PRESETS["granite_hemp"])
        layers = [LAYERS_DB[k] for k in preset["layers"] if k in LAYERS_DB]
        u_val, thick = calculate_u_value(layers)
        return {"status": "success", "file": out, "assembly": assembly, "assembly_name": preset["name"], "u_value": u_val, "total_thickness_mm": thick}
    elif tool_name == "calculate_bioclimatic_flows":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "bioclimatic-flows", "scripts"))
        from bioclimatic_calculator import calculate_solar_altitude, calculate_overhang_depth, calculate_stack_ventilation, generate_bioclimatic_svg, CLIMATE_PRESETS
        zone = arguments.get("climate_zone", "temperate_strasbourg")
        lat = arguments.get("latitude")
        preset = CLIMATE_PRESETS.get(zone, CLIMATE_PRESETS["temperate_strasbourg"])
        actual_lat = lat if lat is not None else preset["latitude"]
        s, w, e = calculate_solar_altitude(actual_lat)
        overhang = calculate_overhang_depth(2.4, s)
        v, q = calculate_stack_ventilation(preset["chimney_height"], preset["delta_t"])
        out = arguments.get("output_path", "bioclimatic_flow_plate.svg")
        generate_bioclimatic_svg(out, climate_key=zone, custom_lat=lat)
        return {
            "climate_zone": zone,
            "zone_name": preset["name"],
            "latitude": actual_lat,
            "summer_solstice_noon": s,
            "winter_solstice_noon": w,
            "equinox_noon": e,
            "optimal_overhang_m": overhang,
            "stack_velocity_m_s": v,
            "stack_flow_m3_s": q,
            "file": out
        }
    elif tool_name == "generate_1_5_joinery":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "interior-joinery", "scripts"))
        from joinery_detailer import generate_joinery_svg, JOINERY_PRESETS
        detail = arguments.get("detail_type", "cabinetry_reveal")
        out = arguments.get("output_path", "joinery_1_5_detail.svg")
        generate_joinery_svg(out, detail_key=detail)
        preset = JOINERY_PRESETS.get(detail, JOINERY_PRESETS["cabinetry_reveal"])
        return {"status": "success", "file": out, "detail_type": detail, "detail_name": preset["name"], "shadow_reveal_mm": preset["shadow_reveal_mm"], "scale": "1:5"}
    elif tool_name == "compile_monograph_spread":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "portfolio-monograph", "scripts"))
        from monograph_compiler import generate_monograph_svg
        title = arguments.get("title", "Project Monograph")
        loc = arguments.get("location", "Strasbourg, France")
        typo = arguments.get("typology", "Heritage Renovation & Timber Pavilion")
        look = arguments.get("look", "swiss_editorial")
        cols = arguments.get("columns")
        asp = arguments.get("aspect")
        out = arguments.get("output_path", "monograph_spread.svg")
        out_dir = os.path.dirname(out)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        svg_code = generate_monograph_svg(title=title, location=loc, typology=typo, look_id=look, columns=cols, aspect_ratio=asp)
        with open(out, "w", encoding="utf-8") as f:
            f.write(svg_code)
        return {"status": "success", "file": out, "title": title, "look": look}
    elif tool_name == "audit_portfolio":
        pdf_path = arguments.get("pdf_path", "")
        sys.path.insert(0, os.path.join(SKILLS_DIR, "portfolio-monograph", "scripts"))
        try:
            from audit_portfolio import audit_pdf
            return audit_pdf(pdf_path)
        except Exception as e:
            return {"error": str(e), "file": pdf_path}
    elif tool_name == "list_portfolio_looks":
        looks = load_json_resource("portfolio_looks_library.json", {})
        look_id = arguments.get("look_id")
        if look_id:
            return looks.get(look_id, {"error": f"Look '{look_id}' not found.", "available": list(looks.keys())})
        return {"total_looks": len(looks), "looks": looks}
    elif tool_name == "get_architectural_movement":
        langs = load_json_resource("architectural_languages.json", {})
        m = arguments.get("movement", "").lower()
        if m in langs:
            return langs[m]
        # Search by keyword
        for k, v in langs.items():
            if m in k or m in v.get("name", "").lower():
                return v
        return {"error": f"Movement '{m}' not found.", "available_movements": list(langs.keys())}
    elif tool_name in ("generate_spatial_journey", "model_spatial_journey"):
        sys.path.insert(0, os.path.join(SKILLS_DIR, "spatial-choreography", "scripts"))
        from spatial_journey_matrix import DEFAULT_ZONES, parse_sequence_arg, evaluate_journey, generate_journey_svg, SpatialZone
        seq_str = arguments.get("sequence_name") or arguments.get("sequence") or arguments.get("preset")
        out = arguments.get("output_svg") or arguments.get("output_path", "spatial_journey.svg")
        zones_arg = arguments.get("zones")
        zones = None
        if isinstance(zones_arg, list):
            zones = []
            for z in zones_arg:
                if isinstance(z, dict):
                    zones.append(SpatialZone(
                        name=z.get("name", "Zone"),
                        phenomenological_title=z.get("phenomenological_title", z.get("title", "Threshold")),
                        target_lux=float(z.get("target_lux", z.get("lux", 300))),
                        target_dba=float(z.get("target_dba", z.get("dba", 35))),
                        ceiling_height_m=float(z.get("ceiling_height_m", z.get("height", 3.5))),
                        width_m=float(z.get("width_m", z.get("width", 3.0))),
                        material_finish=z.get("material_finish", z.get("material", "Hemp-Lime Plaster")),
                        nrc_rating=float(z.get("nrc_rating", 0.35))
                    ))
                elif isinstance(z, str):
                    parsed = parse_sequence_arg(z)
                    zones.extend(parsed)
        elif isinstance(seq_str, str) and ":" in seq_str:
            zones = parse_sequence_arg(seq_str)

        if not zones:
            zones = DEFAULT_ZONES
        out_svg, evaluation = generate_journey_svg(zones, output_path=out)
        return {
            "status": "success",
            "file": out_svg,
            "output_svg": out_svg,
            "verdict": evaluation["verdict"],
            "zones_count": len(zones),
            "warnings": evaluation.get("warnings", []),
            "transitions": evaluation.get("transitions", []),
            "evaluation": evaluation
        }
    elif tool_name == "audit_courtyard_shading":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "spatial-choreography", "scripts"))
        from spatial_journey_matrix import audit_courtyard
        h = float(arguments.get("courtyard_height") or arguments.get("height_m") or 12.0)
        w = float(arguments.get("courtyard_width") or arguments.get("width_m") or 6.0)
        sol = float(arguments.get("solar_altitude_deg") or arguments.get("solar_altitude") or 65.0)
        res = audit_courtyard(height_m=h, width_m=w, solar_altitude_deg=sol)
        return res
    elif tool_name in ("generate_spatial_stitch_spread", "generate_monograph_spread"):
        stitch_dir = os.path.join(SKILLS_DIR, "spatial-stitch", "engine")
        if "models" in sys.modules:
            mod_file = getattr(sys.modules["models"], "__file__", "") or ""
            if not mod_file.startswith(stitch_dir):
                del sys.modules["models"]
        if stitch_dir in sys.path:
            sys.path.remove(stitch_dir)
        sys.path.insert(0, stitch_dir)
        from spread_generator import SpreadGenerator
        from models import LayoutArchetype, CanvasFormat, ProjectPassport
        arch_str = arguments.get("archetype", "THE_CONSTRUCTIVE_PROOF")
        fmt_str = arguments.get("format", "LANDSCAPE_16_9")
        title = arguments.get("title", "Project Monograph")
        out = arguments.get("output_svg") or arguments.get("output_path", "monograph_spread.svg")
        generator = SpreadGenerator()
        archetype = getattr(LayoutArchetype, arch_str, LayoutArchetype.THE_CONSTRUCTIVE_PROOF)
        fmt = getattr(CanvasFormat, fmt_str, CanvasFormat.LANDSCAPE_16_9)
        passport = ProjectPassport(title=title, location="Strasbourg, France", role="Lead Architect")
        spread = generator.generate(
            project_id="mcp_proj",
            prompt="Architectural publication monograph spread",
            archetype=archetype,
            format=fmt,
            passport=passport
        )
        out_dir = os.path.dirname(out)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(spread.svg_content)
        return {"status": "success", "file": out, "output_svg": out, "archetype": arch_str, "format": fmt_str, "title": title}
    elif tool_name in ("audit_spatial_spread", "audit_monograph_spread"):
        stitch_dir = os.path.join(SKILLS_DIR, "spatial-stitch", "engine")
        if "models" in sys.modules:
            mod_file = getattr(sys.modules["models"], "__file__", "") or ""
            if not mod_file.startswith(stitch_dir):
                del sys.modules["models"]
        if stitch_dir in sys.path:
            sys.path.remove(stitch_dir)
        sys.path.insert(0, stitch_dir)
        from auditor import PortfolioAuditor
        from models import SpreadInstance, LayoutArchetype, CanvasFormat
        svg_file = arguments.get("svg_path") or arguments.get("svg_file", "")
        if not os.path.exists(svg_file):
            return {"error": f"SVG file not found: {svg_file}", "total_score": 0}
        with open(svg_file, "r", encoding="utf-8") as f:
            svg_content = f.read()
        spread = SpreadInstance(
            spread_id="mcp_audit",
            project_id="mcp",
            title=os.path.basename(svg_file),
            archetype=LayoutArchetype.THE_CONSTRUCTIVE_PROOF,
            format=CanvasFormat.LANDSCAPE_16_9,
            svg_content=svg_content,
            html_content=""
        )
        auditor = PortfolioAuditor()
        audit = auditor.audit(spread)
        return {
            "file": svg_file,
            "svg_path": svg_file,
            "total_score": audit.total_score,
            "passed_checks": audit.passed_checks,
            "critical_failures": audit.critical_failures,
            "constructive_remediations": audit.constructive_remediations,
            "category_scores": [
                {"name": c.category_name, "awarded": c.awarded_points, "max": c.max_points, "status": c.status}
                for c in audit.category_scores
            ]
        }
    elif tool_name == "extract_design_system_pdf":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "design-md-extractor", "scripts"))
        from extract_from_pdf import extract_pdf_design
        pdf_path = arguments.get("pdf_path", "")
        max_p = int(arguments.get("max_pages", 10))
        try:
            res = extract_pdf_design(pdf_path, max_pages=max_p)
            return {
                "status": "success",
                "pdf_path": pdf_path,
                "title": res.get("title", ""),
                "design_system": res.get("stitch_ds", {}),
                "stitch_ds": res.get("stitch_ds", {}),
                "design_md": res.get("design_md", "")
            }
        except Exception as e:
            return {"error": str(e), "pdf_path": pdf_path}
    elif tool_name == "compile_publication_monograph":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "editorial-studio"))
        from engine.compile import compile_document
        in_path = arguments.get("input_path", "")
        out_path = arguments.get("output_path")
        eng = arguments.get("engine", "auto")
        try:
            res = compile_document(input_path=in_path, output_path=out_path, engine=eng)
            return res
        except Exception as e:
            return {"status": "error", "error": str(e), "input_path": in_path}
    elif tool_name == "extract_design_tokens":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "design-md-extractor", "scripts"))
        from extract_from_image import extract_palette_from_image
        img_path = arguments.get("image_path", "")
        palette_data = extract_palette_from_image(img_path)
        return palette_data
    elif tool_name == "audit_publication_preflight":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "editorial-studio", "preflight"))
        from audit_publication import audit_pdf
        pdf_path = arguments.get("pdf_path") or arguments.get("file_path", "")
        try:
            res = audit_pdf(pdf_path)
            return res
        except Exception as e:
            return {"status": "error", "error": str(e), "file_path": pdf_path}
    else:
        return {"error": f"Tool '{tool_name}' not found."}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "initialize":
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "sara-bensalem-skills", "version": "1.1.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                res = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
            elif method == "tools/call":
                params = req.get("params", {})
                t_name = params.get("name")
                args = params.get("arguments", {})
                with capture_stdout():
                    result_data = handle_call_tool(t_name, args)
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result_data, indent=2)}]
                    }
                }
            else:
                res = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
