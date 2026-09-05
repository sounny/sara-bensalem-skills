#!/usr/bin/env python3
"""
Integrate Jill Mehta Case Study into Sara Bensalem Skills Suite as Look #20:
'crimson_chronograph' (Crimson Chronograph, Scalable Urban Transit & Statutory Blueprints).
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOOK_20 = {
    "id": "crimson_chronograph",
    "category": "architecture",
    "title": "20. Crimson Chronograph, Scalable Urban Transit & Statutory Blueprints",
    "archetype": "Transit-Oriented Modular Spine & University Working Drawing Package (Jill Mehta / PiCA)",
    "ideal_for": "Urban Transit Designers, Technical Delivery Architects, Statutory Working Drawing Specialists",
    "spread_aspect": "2:1 Panoramic Double-Square Spread (840 x 297 mm)",
    "grid": "12-Column Editorial Grid w/ Left Crimson Spine Anchor & Tabular Edge Index",
    "typography": {
        "display": "Helvetica Neue / Neue Haas Grotesk (700 Bold, Lowercase Titles)",
        "body": "Inter (400 Light, 500 Medium)",
        "technical": "JetBrains Mono / AutoCAD Standard (500)"
    },
    "palette": [
        {
            "name": "Spine Crimson",
            "hex": "#8B1E1E",
            "role": "Left Margin Spine Anchor & Section Callouts"
        },
        {
            "name": "Drafting White",
            "hex": "#FFFFFF",
            "role": "Spread Canvas & Drawing Background"
        },
        {
            "name": "Technical Charcoal",
            "hex": "#222222",
            "role": "Setting-Out Grids & Centerline Linework"
        },
        {
            "name": "Sandstone Buff",
            "hex": "#EADBC8",
            "role": "Transit Module Fills & Terrain Terracing"
        },
        {
            "name": "Plinth Brick",
            "hex": "#C86D51",
            "role": "Corbelled Brickwork & Sectional Foundations"
        }
    ],
    "key_proof_elements": "Multi-axis radial/orthogonal setting out plan (1:200), column foundation schedule (1:20), sunken slab sanitary plumbing details, 10x40m scalable urban design modules, MEP ceiling plenum sandwich."
}

files_to_update = [
    os.path.join(BASE_DIR, "skills", "portfolio-monograph", "resources", "portfolio_looks_library.json"),
    os.path.join(BASE_DIR, "skills", "portfolio-design", "resources", "portfolio_looks_library.json"),
]

for p in files_to_update:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["crimson_chronograph"] = LOOK_20
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Updated {p} -> {len(data)} looks registered.")

print("Successfully integrated crimson_chronograph look.")
