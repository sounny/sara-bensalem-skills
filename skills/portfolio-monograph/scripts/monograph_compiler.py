#!/usr/bin/env python3
"""
Sara Bensalem Skills — Advanced Multi-Look Monograph Spread Compiler (2026 Enhanced Edition)
Generates publication-grade architectural monograph spreads with Swiss modular grids,
calibrated margins, Project Passports, multi-scalar viewports (Macro + Meso + Micro),
and authentic palettes distilled from 20+ premier international spatial portfolios.
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
Website: https://skills.sarabensalem.com
"""

import sys
import os
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
RESOURCES_DIR = os.path.join(SKILL_DIR, "resources")

def load_looks_library():
    p = os.path.join(RESOURCES_DIR, "portfolio_looks_library.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

LOOKS_DB = load_looks_library()
LOOKS = LOOKS_DB

DEFAULT_LOOK = {
    "title": "01. The Swiss Editorial Monograph",
    "archetype": "The Swiss International Style (Lars Müller / El Croquis)",
    "ideal_for": "Junior to Senior Architects targeting European Design Consultancies & Competitions",
    "spread_aspect": "16:9 Landscape / Double-A3",
    "grid": "12-Column Modular Grid w/ 8pt Baseline Rhythm",
    "typography": {
        "display": "Space Grotesk (700)",
        "body": "Inter / Plus Jakarta Sans (400, 500)",
        "technical": "JetBrains Mono (600)"
    },
    "palette": [
        {"name": "Archival Bone", "hex": "#F8F8F5", "role": "Spread Canvas Paper"},
        {"name": "Deep Graphite", "hex": "#111110", "role": "Primary Ink & Cut Lines"},
        {"name": "Muted Hairline", "hex": "#DDD9D0", "role": "Drafting Grid & Margins"},
        {"name": "Subtle Wash", "hex": "#F1F1EB", "role": "Sectional Poché & Cards"}
    ],
    "key_proof_elements": "Uncropped 1:20 constructive sections, 20% opacity folio numbering ('01'-'06'), Project Passports."
}

def xml_escape(val):
    if val is None:
        return ""
    return str(val).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_monograph_svg(title="Maison Bretonne Adaptive Reuse",
                            location="Finistère, France",
                            typology="Heritage Renovation & Timber Pavilion",
                            year="2026",
                            role="Lead Project Architect (Line-Item Envelope & Admin)",
                            act="ACT IV // CONSTRUCTIVE PROOF (1:20)",
                            spread_num="04",
                            look_id="swiss_editorial",
                            columns=None,
                            aspect_ratio=None):
    
    look = LOOKS_DB.get(look_id, DEFAULT_LOOK)
    palette = look.get("palette", DEFAULT_LOOK["palette"])
    
    # Resolve colors
    canvas_color = palette[0]["hex"] if len(palette) > 0 else "#F8F8F5"
    ink_color = palette[1]["hex"] if len(palette) > 1 else "#111110"
    hairline_color = palette[2]["hex"] if len(palette) > 2 else "#DDD9D0"
    accent_color = palette[3]["hex"] if len(palette) > 3 else "#7A4D3B"
    
    # Determine dimensions based on look or override
    aspect = aspect_ratio
    if not aspect:
        spread_aspect_str = look.get("spread_aspect", "").lower()
        if "2:1" in spread_aspect_str:
            aspect = "2:1"
        elif "square" in spread_aspect_str or "1:1" in spread_aspect_str:
            aspect = "1:1"
        elif "4:3" in spread_aspect_str:
            aspect = "4:3"
        elif "a4" in spread_aspect_str or "1.414" in spread_aspect_str:
            aspect = "a4_landscape"
        else:
            aspect = "16:9"

    if aspect == "2:1":
        width, height = 1920, 960
    elif aspect == "1:1":
        width, height = 1200, 1200
    elif aspect == "4:3":
        width, height = 1440, 1080
    elif aspect == "a4_landscape":
        width, height = 1600, 1131
    else:  # 16:9
        width, height = 1920, 1080

    margin_x = 64
    margin_y = 64
    content_w = width - (2 * margin_x)
    content_h = height - (2 * margin_y)
    
    # Resolve columns
    if columns is None:
        grid_str = look.get("grid", "")
        if "16-column" in grid_str.lower() or "16 column" in grid_str.lower():
            cols = 16
        elif "8-column" in grid_str.lower() or "8 column" in grid_str.lower():
            cols = 8
        elif "9-column" in grid_str.lower() or "9 column" in grid_str.lower():
            cols = 9
        elif "6-column" in grid_str.lower() or "6 column" in grid_str.lower():
            cols = 6
        elif "10-column" in grid_str.lower() or "10 column" in grid_str.lower():
            cols = 10
        else:
            cols = 12
    else:
        cols = columns

    gutter = 16
    col_w = (content_w - (cols - 1) * gutter) / cols
    
    grid_svg = ""
    for i in range(cols):
        cx = margin_x + i * (col_w + gutter)
        grid_svg += f'    <rect x="{cx:.1f}" y="{margin_y}" width="{col_w:.1f}" height="{content_h}" fill="{canvas_color}" stroke="{hairline_color}" stroke-dasharray="2 4" opacity="0.35" />\n'
    
    proof_snippet = look.get("key_proof_elements", "Verified multi-scalar drawings, continuous thermal breaks, PMR egress.")
    
    # XML Escaped Text
    esc_title = xml_escape(title)
    esc_location = xml_escape(location)
    esc_typology = xml_escape(typology)
    esc_year = xml_escape(year)
    esc_role = xml_escape(role)
    esc_act = xml_escape(act)
    esc_spread_num = xml_escape(spread_num)
    esc_look_title = xml_escape(look.get("title", look_id))
    esc_grid = xml_escape(look.get("grid", f"{cols}-Column Grid"))
    esc_archetype = xml_escape(look.get("archetype", "Tectonic"))

    svg = f"""<svg viewBox="0 0 {width} {height}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:{canvas_color}; font-family:'Plus Jakarta Sans', 'Inter', sans-serif;">
  <defs>
    <style>
      .hairline {{ stroke: {hairline_color}; stroke-width: 1; }}
      .hairline-dark {{ stroke: {ink_color}; stroke-width: 1; }}
      .mono-label {{ font-family: 'JetBrains Mono', 'Space Mono', monospace; font-size: 11px; fill: #55544E; }}
      .mono-bold {{ font-family: 'JetBrains Mono', 'Space Mono', monospace; font-size: 11px; font-weight: 700; fill: {ink_color}; }}
      .display-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 700; fill: {ink_color}; }}
      .dim-line {{ stroke: {ink_color}; stroke-width: 1.2; }}
      .accent-box {{ fill: {accent_color}; }}
    </style>
  </defs>

  <!-- Swiss Modular Baseline & Columns Grid -->
  <g id="swiss-modular-grid" opacity="0.4">
{grid_svg}
  </g>

  <!-- Framing Margins & Precision Registration Marks -->
  <g id="registration-marks">
    <rect x="{margin_x}" y="{margin_y}" width="{content_w}" height="{content_h}" fill="none" stroke="{ink_color}" stroke-width="1" stroke-opacity="0.2" />
    <circle cx="{margin_x}" cy="{margin_y}" r="2.5" fill="{ink_color}" />
    <circle cx="{width - margin_x}" cy="{margin_y}" r="2.5" fill="{ink_color}" />
    <circle cx="{margin_x}" cy="{height - margin_y}" r="2.5" fill="{ink_color}" />
    <circle cx="{width - margin_x}" cy="{height - margin_y}" r="2.5" fill="{ink_color}" />
  </g>

  <!-- Folio Header -->
  <text x="{margin_x}" y="{margin_y - 18}" class="mono-label" letter-spacing="1">PROJECT MONOGRAPH: {esc_title.upper()}</text>
  <text x="{width - margin_x}" y="{margin_y - 18}" class="mono-bold" text-anchor="end">{esc_act}</text>
  <line x1="{margin_x}" y1="{margin_y}" x2="{width - margin_x}" y2="{margin_y}" class="hairline" />

  <!-- Left Column: Project Passport & Multi-Scalar Index -->
  <g transform="translate({margin_x}, {margin_y + 36})">
    <text x="0" y="24" class="display-title">{esc_title}</text>
    <text x="0" y="48" class="mono-label">TYPOLOGY: {esc_typology.upper()}</text>
    <text x="0" y="66" class="mono-label">LOCATION: {esc_location.upper()} // YEAR: {esc_year}</text>
    <text x="0" y="84" class="mono-bold">ROLE: {esc_role.upper()}</text>
    <text x="0" y="102" class="mono-label">DESIGN LOOK: {esc_look_title.upper()}</text>
    
    <line x1="0" y1="116" x2="520" y2="116" class="hairline" />

    <!-- Project Passport Meta Box -->
    <g transform="translate(0, 130)">
      <rect x="0" y="0" width="520" height="84" fill="#FFFFFF" stroke="{hairline_color}" />
      <rect x="0" y="0" width="6" height="84" fill="{accent_color}" />
      <text x="16" y="22" class="mono-bold">PROJECT PASSPORT // STRASBOURG ATELIER</text>
      <text x="16" y="42" font-size="11px" fill="{ink_color}">Grid: {esc_grid} • Archetype: {esc_archetype}</text>
      <text x="16" y="62" font-size="11px" fill="#55544E">Verified individual line-item detailing and CAD/BIM execution.</text>
    </g>

    <!-- Multi-Scalar Evidence Matrix -->
    <g transform="translate(0, 230)">
      <text x="0" y="0" class="mono-bold" letter-spacing="1">MULTI-SCALAR DRAWING HIERARCHY</text>

      <g transform="translate(0, 18)">
        <rect x="0" y="0" width="22" height="22" fill="{ink_color}" />
        <text x="11" y="15" class="mono-bold" fill="#FFFFFF" text-anchor="middle">01</text>
        <text x="32" y="12" font-size="12px" font-weight="700" fill="{ink_color}">MACRO (1:500): Site Context &amp; Microclimate</text>
        <text x="32" y="26" font-size="11px" fill="#55544E">Topographical contours, wind funneling &amp; solar vectors</text>
      </g>

      <g transform="translate(0, 68)">
        <rect x="0" y="0" width="22" height="22" fill="#55544E" />
        <text x="11" y="15" class="mono-bold" fill="#FFFFFF" text-anchor="middle">02</text>
        <text x="32" y="12" font-size="12px" font-weight="700" fill="{ink_color}">MESO (1:100): Spatial Anatomy &amp; Egress</text>
        <text x="32" y="26" font-size="11px" fill="#55544E">Circulation loops, 1500mm PMR circles &amp; core zoning</text>
      </g>

      <g transform="translate(0, 118)">
        <rect x="0" y="0" width="22" height="22" fill="{accent_color}" />
        <text x="11" y="15" class="mono-bold" fill="#FFFFFF" text-anchor="middle">03</text>
        <text x="32" y="12" font-size="12px" font-weight="700" fill="{ink_color}">MICRO (1:20 / 1:5): Tectonic Assembly Proof</text>
        <text x="32" y="26" font-size="11px" fill="#55544E">Constructive wall envelope, thermal breaks &amp; joinery reveals</text>
      </g>
    </g>

    <!-- Material Palette Swatches -->
    <g transform="translate(0, 400)">
      <text x="0" y="0" class="mono-bold" letter-spacing="1">AUTHENTIC GEOLOGICAL PALETTE</text>
      <g transform="translate(0, 16)">
"""

    for idx, sw in enumerate(palette[:4]):
        sy = idx * 28
        sw_name = xml_escape(sw.get('name', ''))
        sw_hex = xml_escape(sw.get('hex', '#000000'))
        sw_role = xml_escape(sw.get('role', ''))
        svg += f"""        <rect x="0" y="{sy}" width="18" height="18" fill="{sw_hex}" stroke="{ink_color}" stroke-width="0.8" />
        <text x="26" y="{sy + 13}" font-size="11px" font-family="'JetBrains Mono', monospace" fill="{ink_color}">{sw_name} ({sw_hex}) — {sw_role}</text>
"""

    svg += f"""      </g>
    </g>

    <!-- Constructive Proof Guarantee -->
    <g transform="translate(0, 550)">
      <rect x="0" y="0" width="520" height="88" fill="#FFFFFF" stroke="{hairline_color}" />
      <text x="16" y="22" class="mono-bold">CONSTRUCTIVE PROOF GUARANTEE</text>
      <text x="16" y="42" font-size="11px" fill="{ink_color}">Zero render trap reliance. Every detail supported by verified</text>
      <text x="16" y="58" font-size="11px" fill="{ink_color}">working drawings, continuous thermal breaks, and PMR compliance.</text>
      <text x="16" y="76" class="mono-label">ANTI-RENDER-TRAP VALIDATED • 100% BUILDABLE</text>
    </g>
  </g>

  <!-- Right Viewport: Primary Technical Drawing (Multi-Scalar Technical Canvas) -->
  <g transform="translate({margin_x + 550}, {margin_y + 36})">
    <rect x="0" y="0" width="{content_w - 550}" height="{content_h - 56}" fill="#FFFFFF" stroke="{hairline_color}" stroke-width="1" />
    
    <!-- Drawing Viewport Header -->
    <rect x="0" y="0" width="{content_w - 550}" height="32" fill="{canvas_color}" stroke="{hairline_color}" />
    <text x="16" y="20" class="mono-bold">TECTONIC DRAWING VIEWPORT // SCALE 1:20 // {esc_act}</text>
    <text x="{content_w - 566}" y="20" class="mono-label" text-anchor="end">UNIT: MM</text>

    <!-- Embedded Scalable 1:20 Technical Plate Viewport -->
    <svg x="0" y="32" width="{content_w - 550}" height="{max(200, content_h - 88)}" viewBox="0 0 1020 620" preserveAspectRatio="xMinYMid meet">
    <!-- Foundation Plinth & Concrete Ground Slab -->
    <rect x="180" y="480" width="680" height="120" fill="#F4F4F0" stroke="{ink_color}" stroke-width="2" />
    <line x1="190" y1="520" x2="850" y2="520" stroke="#84827A" stroke-width="1" stroke-dasharray="8 6" />
    <line x1="190" y1="570" x2="850" y2="570" stroke="#84827A" stroke-width="1" stroke-dasharray="8 6" />
    <text x="520" y="550" class="mono-label" text-anchor="middle">REINFORCED CONCRETE GROUND SLAB // FFL +0.000</text>

    <!-- 01 Outer Cladding / Rainscreen Leaf -->
    <g>
      <rect x="180" y="40" width="160" height="440" fill="#EAEAE5" stroke="{ink_color}" stroke-width="2" />
      <line x1="180" y1="120" x2="340" y2="120" stroke="{ink_color}" stroke-width="1" />
      <line x1="180" y1="200" x2="340" y2="200" stroke="{ink_color}" stroke-width="1" />
      <line x1="180" y1="280" x2="340" y2="280" stroke="{ink_color}" stroke-width="1" />
      <line x1="180" y1="360" x2="340" y2="360" stroke="{ink_color}" stroke-width="1" />
      <text x="260" y="250" class="mono-bold" text-anchor="middle" transform="rotate(-90 260 250)">OUTER FACADE RAINSCREEN</text>
    </g>

    <!-- 02 Insulation Layer -->
    <rect x="340" y="40" width="120" height="440" fill="#F8F8F5" stroke="{ink_color}" stroke-width="1.5" stroke-dasharray="4 2" />
    <text x="400" y="250" class="mono-label" text-anchor="middle" transform="rotate(-90 400 250)">CONTINUOUS INSULATION (λ = 0.035)</text>

    <!-- 03 Thermal Break & EPDM Capillary Membrane -->
    <rect x="460" y="40" width="20" height="440" fill="{accent_color}" stroke="{ink_color}" stroke-width="1.5" />
    <line x1="460" y1="480" x2="480" y2="480" stroke="{ink_color}" stroke-width="3" />

    <!-- 04 Structural Post & Beam Framing -->
    <g>
      <rect x="480" y="40" width="140" height="440" fill="#F3F0E8" stroke="{ink_color}" stroke-width="2" />
      <line x1="480" y1="40" x2="620" y2="480" stroke="{hairline_color}" stroke-width="1" />
      <line x1="620" y1="40" x2="480" y2="480" stroke="{hairline_color}" stroke-width="1" />
      <text x="550" y="250" class="mono-bold" text-anchor="middle" transform="rotate(-90 550 250)">STRUCTURAL LOADBEARING FRAME</text>
    </g>

    <!-- 05 High-Performance Glazed Envelope -->
    <g>
      <rect x="620" y="140" width="360" height="260" fill="#F8F8F5" stroke="{ink_color}" stroke-width="2" />
      <line x1="620" y1="270" x2="980" y2="270" stroke="{ink_color}" stroke-width="1.5" />
      <text x="800" y="258" class="mono-bold" text-anchor="middle">HIGH-PERFORMANCE GLAZING // Uw = 0.80 W/m²K</text>
    </g>

    <!-- Dimension Chains -->
    <g stroke="{ink_color}" stroke-width="1.2">
      <line x1="120" y1="40" x2="120" y2="480" />
      <line x1="108" y1="40" x2="132" y2="40" />
      <line x1="108" y1="480" x2="132" y2="480" />
      <line x1="112" y1="44" x2="128" y2="36" stroke-width="2" />
      <line x1="112" y1="484" x2="128" y2="476" stroke-width="2" />
    </g>
    <text x="100" y="260" class="mono-bold" text-anchor="middle" transform="rotate(-90 100 260)">4400 MM CLEARANCE</text>

    <g stroke="{ink_color}" stroke-width="1.2">
      <line x1="180" y1="18" x2="480" y2="18" />
      <line x1="180" y1="8" x2="180" y2="28" />
      <line x1="480" y1="8" x2="480" y2="28" />
      <line x1="176" y1="22" x2="184" y2="14" stroke-width="2" />
      <line x1="476" y1="22" x2="484" y2="14" stroke-width="2" />
    </g>
    <text x="330" y="12" class="mono-bold" text-anchor="middle">300 MM COMPOSITE ENVELOPE</text>
    </svg>
  </g>

  <!-- Folio Footer -->
  <line x1="{margin_x}" y1="{height - margin_y}" x2="{width - margin_x}" y2="{height - margin_y}" class="hairline" />
  <text x="{margin_x}" y="{height - margin_y + 22}" class="mono-label">LEAD ARCHITECT: SARA BENSALEM • STRASBOURG ATELIER [48°35'05"N 07°45'02"E]</text>
  <text x="{width / 2}" y="{height - margin_y + 22}" class="mono-label" text-anchor="middle">WORK RIGHTS: EU CITIZEN // ZERO VISA SPONSORSHIP REQUIRED</text>
  <text x="{width - margin_x}" y="{height - margin_y + 22}" class="mono-bold" text-anchor="end">SPREAD {esc_spread_num}</text>
</svg>"""
    return svg.replace("&AMP;", "&amp;").replace("&LT;", "&lt;").replace("&GT;", "&gt;").replace("&QUOT;", "&quot;")

def main():
    parser = argparse.ArgumentParser(description="Sara Bensalem Monograph Spread Compiler")
    parser.add_argument("--title", default="Maison Bretonne Adaptive Reuse", help="Project Title")
    parser.add_argument("--location", default="Finistère, France", help="Project Location")
    parser.add_argument("--typology", default="Heritage Renovation & Timber Pavilion", help="Typology")
    parser.add_argument("--year", default="2026", help="Year")
    parser.add_argument("--role", default="Lead Project Architect (Line-Item Envelope & Admin)", help="Role")
    parser.add_argument("--act", default="ACT IV // CONSTRUCTIVE PROOF (1:20)", help="Act / Chapter Title")
    parser.add_argument("--spread-num", default="04", help="Spread Number")
    parser.add_argument("--look", default="swiss_editorial", help="Look ID from 19 portfolio looks")
    parser.add_argument("--columns", type=int, default=None, help="Swiss grid columns (6, 8, 9, 10, 12, 16)")
    parser.add_argument("--aspect", default=None, help="Aspect ratio (16:9, 2:1, 1:1, 4:3, a4_landscape)")
    parser.add_argument("--output", "-o", default="monograph_spread.svg", help="Output SVG path")
    args = parser.parse_args()

    svg_content = generate_monograph_svg(
        title=args.title,
        location=args.location,
        typology=args.typology,
        year=args.year,
        role=args.role,
        act=args.act,
        spread_num=args.spread_num,
        look_id=args.look,
        columns=args.columns,
        aspect_ratio=args.aspect
    )

    if args.output:
        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Monograph spread compiled successfully to: {args.output}")

if __name__ == "__main__":
    main()
