#!/usr/bin/env python3
"""
Sara Bensalem Skills MCP Server
Exposes spatial design, portfolio auditing, and architectural critique tools
via the Model Context Protocol (MCP stdio JSON-RPC).
Author: Sara Bensalem <sara@sarabensalem.com>
Website: https://skills.sarabensalem.com
"""

import sys
import json
import os

# Try importing fitz for PDF geometry
try:
    import fitz
except ImportError:
    fitz = None

# Load bundled archetypes and rubric
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_RES_DIR = os.path.join(SCRIPT_DIR, "..", "skills", "portfolio-design", "resources")

def load_json_resource(filename, fallback):
    p = os.path.join(SKILL_RES_DIR, filename)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

ARCHETYPES = load_json_resource("archetypes.json", [])
RUBRIC = load_json_resource("rubric_100pt.json", {})

TOOLS = [
    {
        "name": "list_sara_skills",
        "description": "Lists all available architectural and design skills in the Sara Bensalem Skills Studio (skills.sarabensalem.com).",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "audit_portfolio",
        "description": "Performs an automated technical audit of a PDF architectural portfolio against the Sara Bensalem 100-Point Rubric, checking page budget, aspect ratio, text density, and detecting 'render traps'.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pdf_path": {
                    "type": "string",
                    "description": "Absolute path to the portfolio PDF file to audit."
                }
            },
            "required": ["pdf_path"]
        }
    },
    {
        "name": "recommend_archetype",
        "description": "Recommends the best layout archetype from the 10 empirical portfolio archetypes based on candidate discipline, target firm types, and career stage.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "discipline": {
                    "type": "string",
                    "description": "Candidate's discipline (e.g., 'Interior Architecture', 'Urban Design', 'Technical Office', 'BIM Housing', 'Vernacular')."
                },
                "target_firms": {
                    "type": "string",
                    "description": "Types of firms targeted (e.g., 'Parisian boutique atelier', 'Corporate contractor AECOM', 'International design studio Foster/BIG')."
                }
            },
            "required": ["discipline"]
        }
    },
    {
        "name": "generate_5act_structure",
        "description": "Generates a complete 5-act spatial case study structure (Hook, Conflict, Strategy, Constructive Proof, Atmosphere) tailored for a specific project.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_title": {"type": "string", "description": "Title of the project"},
                "location": {"type": "string", "description": "Geographic location of the project"},
                "typology": {"type": "string", "description": "Building or space typology"},
                "problem_statement": {"type": "string", "description": "The primary socio-spatial or environmental conflict"}
            },
            "required": ["project_title", "location", "typology"]
        }
    },
    {
        "name": "get_100pt_rubric",
        "description": "Returns the complete Sara Bensalem 100-Point Spatial Portfolio Audit Rubric across the 6 core pillars.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def handle_tool_call(name, args):
    if name == "list_sara_skills":
        return {
            "studio": "Sara Bensalem Design Skills (skills.sarabensalem.com)",
            "author": "Sara Bensalem <sara@sarabensalem.com>",
            "available_skills": [
                {
                    "id": "portfolio-design",
                    "name": "Spatial Portfolio Architecture & Curation",
                    "status": "Production / Active",
                    "description": "Swiss editorial typography, 10 layout archetypes, 5-act case study structure, and 100-point audit rubric to eliminate render traps."
                },
                {
                    "id": "heritage-adaptive-reuse",
                    "name": "Heritage Longère & Vernacular Adaptive Reuse",
                    "status": "In Development",
                    "description": "Breton vernacular masonry, timber truss stabilization, modern glazed thermal transitions, and PMR compliance."
                },
                {
                    "id": "interior-joinery-scenography",
                    "name": "Interior Joinery & Tactile Scenography",
                    "status": "In Development",
                    "description": "Tactile material triptychs, custom millwork details, luminaire schedules, and sensory space curation."
                },
                {
                    "id": "gender-equitable-urbanism",
                    "name": "Gender-Equitable Public Realm & Safety Auditing",
                    "status": "In Development",
                    "description": "Empirical safety audits, 24/7 eyes on the street, bio-buffered pedestrian boulevards, and inclusive street design."
                }
            ]
        }

    elif name == "audit_portfolio":
        pdf_path = args.get("pdf_path")
        if not os.path.exists(pdf_path):
            return {"error": f"File does not exist: {pdf_path}"}
        
        file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        if not fitz:
            return {"filename": os.path.basename(pdf_path), "file_size_mb": round(file_size_mb, 2), "error": "PyMuPDF not installed"}
            
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        total_text_len = 0
        landscape_count = 0
        portrait_count = 0
        
        for i in range(page_count):
            p = doc[i]
            if p.rect.width > p.rect.height:
                landscape_count += 1
            else:
                portrait_count += 1
            total_text_len += len(p.get_text().strip())
            
        avg_text = total_text_len / max(page_count, 1)
        traps = []
        if file_size_mb > 50:
            traps.append("Excessive File Size (> 50 MB) - Risk of HR email rejection")
        if avg_text > 450:
            traps.append("Wall of Text Warning - Reviewers scan in 30 seconds")
        if avg_text < 30:
            traps.append("Potential Render Trap - Verify presence of dimension chains and technical callouts")
            
        return {
            "filename": os.path.basename(pdf_path),
            "total_pages": page_count,
            "file_size_mb": round(file_size_mb, 2),
            "orientation": "Landscape Dominant" if landscape_count >= portrait_count else "Portrait Dominant",
            "avg_text_per_page": round(avg_text, 1),
            "traps_detected": traps,
            "recommendation": "Aim for 20-30 landscape spreads with at least one detailed constructive wall section per project.",
            "studio_credit": "Audited by Sara Bensalem Skills Studio (skills.sarabensalem.com)"
        }

    elif name == "recommend_archetype":
        disc = args.get("discipline", "").lower()
        firms = args.get("target_firms", "").lower()
        
        matched = []
        for arch in ARCHETYPES:
            text_blob = (arch["name"] + " " + arch["target_firms"] + " " + arch["benchmark"]).lower()
            score = 0
            for term in disc.split():
                if term in text_blob:
                    score += 2
            for term in firms.split():
                if term in text_blob:
                    score += 1
            matched.append((score, arch))
            
        matched.sort(key=lambda x: x[0], reverse=True)
        top_choice = matched[0][1] if matched else (ARCHETYPES[0] if ARCHETYPES else {})
        
        return {
            "recommended_archetype": top_choice,
            "alternative_archetypes": [m[1]["name"] for m in matched[1:3]] if len(matched) > 1 else [],
            "advice": "Ensure your first project spread follows the 5-act narrative and includes structural/constructive proof."
        }

    elif name == "generate_5act_structure":
        title = args.get("project_title", "Untitled Project")
        loc = args.get("location", "Unspecified Location")
        typ = args.get("typology", "Mixed-Use")
        prob = args.get("problem_statement", "Balancing spatial efficiency with human well-being")
        
        return {
            "project_title": title,
            "act_1_hook": {
                "spread": "Spread 1 (Left)",
                "content": f"Project Passport ({title}, {loc}, {typ}), client brief, and 2-sentence executive thesis statement."
            },
            "act_2_conflict": {
                "spread": "Spread 1 (Right)",
                "content": f"Contextual & Environmental Conflict: {prob}. Sun/wind diagrams and site constraints."
            },
            "act_3_strategy": {
                "spread": "Spread 2 (Left)",
                "content": "Volumetric evolution diagrams (3-4 step massing) and exploded programmatic axonometric."
            },
            "act_4_constructive_proof": {
                "spread": "Spread 2 (Right) & Spread 3 (Left)",
                "content": "ANTI-TRAP PROOF: Scaled technical floor plans (1:50/1:100), layered wall sections (1:20) with insulation/waterproofing callouts, and PMR clearance circles."
            },
            "act_5_atmosphere": {
                "spread": "Spread 3 (Right)",
                "content": "Material triptych (tactile finishes, joinery details), day vs. night lighting scenography, and verified project outcome."
            }
        }

    elif name == "get_100pt_rubric":
        return RUBRIC

    else:
        return {"error": f"Unknown tool: {name}"}

def main():
    """Simple JSON-RPC 2.0 stdio loop conforming to the Model Context Protocol"""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception as e:
            continue
            
        msg_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "initialize":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "sara-bensalem-skills",
                        "version": "1.0.0"
                    },
                    "capabilities": {
                        "tools": {}
                    }
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
            
        elif method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": TOOLS
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
            
        elif method == "tools/call":
            tname = params.get("name")
            targs = params.get("arguments", {})
            output = handle_tool_call(tname, targs)
            res = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(output, indent=2)
                        }
                    ]
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
