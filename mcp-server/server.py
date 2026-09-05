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
            {"name": "portfolio-monograph", "role": "Multi-spread Swiss monograph publishing, 19 curated looks & Project Passports"},
            {"name": "constructive-detail", "role": "1:20 buildable wall sections across 6 assemblies & Glaser U-values"},
            {"name": "grill-my-design", "role": "Socratic architectural review jury across 5 personas (including Visual Curator)"},
            {"name": "spatial-anatomy", "role": "1:100 plans, circulation vectors, 1500mm PMR wheelchair turning & Space for Hesitation"},
            {"name": "bioclimatic-flows", "role": "Solar geometry vectors, shading overhang depth & stack ventilation draft across 5 climate zones"},
            {"name": "interior-joinery", "role": "1:5 custom millwork reveals, shadow reveals (joint creux) & concealed hardware tolerances"}
        ],
        "total_empirical_looks": len(load_json_resource("portfolio_looks_library.json", {})),
        "total_archetypes": len(ARCHETYPES)
    }

def handle_grill(submission_text, persona="full"):
    sys.path.insert(0, os.path.join(SKILLS_DIR, "grill-my-design", "engine"))
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
        report = engine.grill(submission_text, p_enum)
        return {
            "verdict": report.verdict,
            "overall_score": report.overall_score,
            "15s_takeaway": report.recruiter_15s_takeaway,
            "dimension_scores": [{"name": d.name, "score": d.score, "critique": d.critique} for d in report.dimension_scores],
            "vulnerabilities": [{"question": v.interrogation_question, "vulnerability": v.vulnerability_detected, "remedy": v.redline_fix} for v in report.top_vulnerabilities],
            "defense_remedies": report.defense_remedies,
            "next_crit_prompt": report.next_crit_prompt
        }
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
        return handle_grill(arguments.get("submission_text", ""), arguments.get("persona", "full"))
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
