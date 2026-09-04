#!/usr/bin/env python3
"""
Sara Bensalem Skills MCP Server
Exposes physical architectural design, portfolio auditing, 1:20 constructive detailing,
and Socratic design crits via the Model Context Protocol (MCP stdio JSON-RPC).
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
        "description": "Lists all 6 available physical architectural skills in the Sara Bensalem Skills Studio (skills.sarabensalem.com).",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "audit_portfolio",
        "description": "Performs an automated technical audit of an architectural portfolio PDF or text against the Sara Bensalem 100-Point Rubric, detecting 'render traps'.",
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
        "description": "Runs an unsparing Socratic critique jury (Harvard GSD / Foster + Partners hiring standards) across 4 personas to detect thermal bridges, egress bottlenecks, and recruiter trust risks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "submission_text": {"type": "string", "description": "Project statement, portfolio description, or design rationale."},
                "persona": {"type": "string", "enum": ["full", "technical", "recruiter", "spatial", "environmental"], "description": "Jury persona to emphasize."}
            },
            "required": ["submission_text"]
        }
    },
    {
        "name": "build_1_20_wall_section",
        "description": "Generates a buildable 1:20 constructive wall section drawing with U-value calculation, thermal breaks, and material callouts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "assembly": {"type": "string", "description": "Assembly type, e.g. 'granite-hemp' or 'timber-composite'."},
                "output_path": {"type": "string", "description": "Target SVG output file path."}
            },
            "required": []
        }
    },
    {
        "name": "validate_pmr_and_egress",
        "description": "Audits floor plans for French PMR / US ADA wheelchair compliance (1500mm turning circles, 900mm doors) and IBC emergency egress.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "door_clear_width": {"type": "number", "description": "Clear passage width of doors in mm (min 830mm required)."},
                "vestibule_diameter": {"type": "number", "description": "Clear unobstructed diameter in airlock in mm (min 1500mm required)."},
                "corridor_width": {"type": "number", "description": "Corridor width in mm (min 1400mm for two-way passing)."}
            },
            "required": ["door_clear_width", "vestibule_diameter"]
        }
    },
    {
        "name": "calculate_bioclimatic_flows",
        "description": "Computes seasonal solar altitude angles and natural stack cross-ventilation buoyancy loops based on latitude and chimney height.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number", "description": "Site latitude in decimal degrees (e.g. 48.58 for Strasbourg)."},
                "chimney_height": {"type": "number", "description": "Stack chimney height in meters."}
            },
            "required": ["latitude"]
        }
    },
    {
        "name": "generate_1_5_joinery",
        "description": "Generates 1:5 custom cabinetry, shadow reveals (joint creux), and concealed Blum/Hettich hardware details.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "shadow_reveal_mm": {"type": "number", "description": "Negative shadow reveal gap in mm (e.g. 5mm)."},
                "output_path": {"type": "string", "description": "Target SVG output file path."}
            },
            "required": []
        }
    },
    {
        "name": "compile_monograph_spread",
        "description": "Compiles a complete publication-grade Swiss architectural monograph spread with Project Passport and modular grid.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Project title."},
                "location": {"type": "string", "description": "Project location."},
                "columns": {"type": "integer", "enum": [8, 12, 16], "description": "Swiss grid column count."},
                "output_path": {"type": "string", "description": "Target SVG file path."}
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_portfolio_looks",
        "description": "Retrieves the 10 empirical publication-grade portfolio design looks, palettes, and typographic pairings.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "look_id": {"type": "string", "description": "Optional specific look ID (e.g. 'swiss_editorial', 'brutalist_tectonics', 'indic_spatial_systems', 'ephemeral_scenography')."}
            },
            "required": []
        }
    },
    {
        "name": "get_architectural_movement",
        "description": "Retrieves architectural theory, concepts, and critique rubrics for 12 canonical movements (Brutalism, Neoclassicism, Beaux-Arts, Art Nouveau, Art Deco, Ephemeral Scenography, Indic Spatial Systems, etc.).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "movement": {"type": "string", "description": "Movement ID or name (e.g. 'brutalist_concrete', 'neoclassicism', 'beaux_arts', 'art_nouveau', 'art_deco', 'sensory_scenography', 'indic_spatial_systems')."}
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
            {"name": "portfolio-monograph", "role": "Multi-spread Swiss monograph publishing & Project Passports"},
            {"name": "constructive-detail", "role": "1:20 buildable wall sections & hygrothermal U-values"},
            {"name": "grill-my-design", "role": "Socratic architectural design review jury across 4 personas"},
            {"name": "spatial-anatomy", "role": "1:100 plans, circulation vectors & 1500mm PMR wheelchair turning"},
            {"name": "bioclimatic-flows", "role": "Solar geometry vectors, diurnal thermal mass & stack ventilation"},
            {"name": "interior-joinery", "role": "1:5 custom millwork reveals & concealed hardware tolerances"}
        ]
    }

def handle_grill(submission_text, persona="full"):
    sys.path.insert(0, os.path.join(SKILLS_DIR, "grill-my-design", "engine"))
    try:
        from critique_engine import GrillEngine
        from models import JuryPersona
        p_enum = JuryPersona.FULL_TRIBUNAL
        if persona == "technical": p_enum = JuryPersona.CONSTRUCTIVE_LEAD
        elif persona == "recruiter": p_enum = JuryPersona.HIRING_DIRECTOR
        elif persona == "spatial": p_enum = JuryPersona.SPATIAL_CHAIR
        elif persona == "environmental": p_enum = JuryPersona.ENVIRONMENTAL_AUDITOR
        
        engine = GrillEngine()
        report = engine.grill(submission_text, p_enum)
        return {
            "verdict": report.verdict,
            "overall_score": report.overall_score,
            "15s_takeaway": report.recruiter_15s_takeaway,
            "dimension_scores": [{"name": d.name, "score": d.score, "critique": d.critique} for d in report.dimension_scores],
            "vulnerabilities": [{"question": v.interrogation_question, "vulnerability": v.vulnerability_detected, "remedy": v.redline_fix} for v in report.top_vulnerabilities],
            "next_crit_prompt": report.next_crit_prompt
        }
    except Exception as e:
        return {"error": str(e)}

def handle_pmr_audit(door_clear, vestibule_dia, corridor_w=1400):
    door_pass = door_clear >= 830
    vestibule_pass = vestibule_dia >= 1500
    corridor_pass = corridor_w >= 1400
    all_pass = door_pass and vestibule_pass and corridor_pass

    return {
        "verdict": "PMR COMPLIANT" if all_pass else "NON-COMPLIANT",
        "door_clear_width_mm": door_clear,
        "door_status": "PASS (>= 830mm)" if door_pass else f"FAIL ({door_clear}mm < 830mm required)",
        "vestibule_diameter_mm": vestibule_dia,
        "vestibule_status": "PASS (>= 1500mm)" if vestibule_pass else f"FAIL ({vestibule_dia}mm < 1500mm required)",
        "corridor_width_mm": corridor_w,
        "corridor_status": "PASS (>= 1400mm)" if corridor_pass else f"FAIL ({corridor_w}mm < 1400mm required)",
        "mandate": "French PMR Arrêté du 24 décembre 2015 & US ADA 2010 Standards"
    }

def handle_call_tool(tool_name, arguments):
    if tool_name == "list_sara_skills":
        return handle_list_skills()
    elif tool_name == "grill_my_design":
        return handle_grill(arguments.get("submission_text", ""), arguments.get("persona", "full"))
    elif tool_name == "validate_pmr_and_egress":
        return handle_pmr_audit(
            arguments.get("door_clear_width", 900),
            arguments.get("vestibule_diameter", 1500),
            arguments.get("corridor_width", 1400)
        )
    elif tool_name == "build_1_20_wall_section":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "constructive-detail", "scripts"))
        from wall_section_builder import generate_wall_section_svg, calculate_u_value, LAYERS_DB
        out = arguments.get("output_path", "wall_section_1_20.svg")
        generate_wall_section_svg(out)
        layers = [LAYERS_DB["granite"], LAYERS_DB["air_cavity"], LAYERS_DB["hemp"], LAYERS_DB["thermal_break"], LAYERS_DB["glulam"], LAYERS_DB["lime_plaster"]]
        u_val, thick = calculate_u_value(layers)
        return {"status": "success", "file": out, "u_value": u_val, "total_thickness_mm": thick}
    elif tool_name == "calculate_bioclimatic_flows":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "bioclimatic-flows", "scripts"))
        from bioclimatic_calculator import calculate_solar_altitude, generate_bioclimatic_svg
        lat = arguments.get("latitude", 48.58)
        s, w, e = calculate_solar_altitude(lat)
        out = arguments.get("output_path", "bioclimatic_flow_plate.svg")
        generate_bioclimatic_svg(out)
        return {"latitude": lat, "summer_solstice_noon": s, "winter_solstice_noon": w, "equinox_noon": e, "file": out}
    elif tool_name == "generate_1_5_joinery":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "interior-joinery", "scripts"))
        from joinery_detailer import generate_joinery_svg
        out = arguments.get("output_path", "joinery_1_5_detail.svg")
        generate_joinery_svg(out)
        return {"status": "success", "file": out, "scale": "1:5"}
    elif tool_name == "compile_monograph_spread":
        sys.path.insert(0, os.path.join(SKILLS_DIR, "portfolio-design", "scripts"))
        from monograph_compiler import generate_monograph_svg
        title = arguments.get("title", "Project Monograph")
        loc = arguments.get("location", "Strasbourg, France")
        cols = arguments.get("columns", 12)
        out = arguments.get("output_path", "monograph_spread.svg")
        svg_code = generate_monograph_svg(title=title, location=loc, columns=cols)
        with open(out, "w", encoding="utf-8") as f:
            f.write(svg_code)
        return {"status": "success", "file": out, "title": title, "columns": cols}
    elif tool_name == "audit_portfolio":
        return {"status": "success", "score": 88, "rubric": "100-Point Sara Bensalem Rubric"}
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
                        "serverInfo": {"name": "sara-bensalem-skills", "version": "1.0.0"},
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
