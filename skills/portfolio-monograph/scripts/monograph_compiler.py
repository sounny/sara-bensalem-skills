#!/usr/bin/env python3
"""
Sara Bensalem Skills — Monograph Spread Compiler
Generates publication-grade architectural monograph spreads with Swiss modular grids,
calibrated margins, Project Passports, and 1:100 / 1:20 drawing viewports.
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
"""

import sys
import os
import json
import argparse

def generate_monograph_svg(title="Maison Bretonne Adaptive Reuse",
                            location="Finistère, France",
                            typology="Heritage Renovation & Timber Pavilion",
                            year="2025",
                            role="Lead Project Architect (Line-Item Envelope & Admin)",
                            act="ACT IV // CONSTRUCTIVE PROOF (1:20)",
                            spread_num="04",
                            columns=12,
                            aspect_ratio="16:9"):
    
    width = 1920
    height = 1080 if aspect_ratio == "16:9" else 1358
    margin_x = 64
    margin_y = 64
    content_w = width - (2 * margin_x)
    content_h = height - (2 * margin_y)
    
    gutter = 16
    col_w = (content_w - (columns - 1) * gutter) / columns
    
    grid_svg = ""
    for i in range(columns):
        cx = margin_x + i * (col_w + gutter)
        grid_svg += f'    <rect x="{cx:.1f}" y="{margin_y}" width="{col_w:.1f}" height="{content_h}" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" opacity="0.45" />\n'
    
    svg = f"""<svg viewBox="0 0 {width} {height}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF; font-family:'Plus Jakarta Sans', 'Inter', sans-serif;">
  <defs>
    <style>
      .hairline {{ stroke: #DDD9D0; stroke-width: 1; }}
      .hairline-dark {{ stroke: #111110; stroke-width: 1; }}
      .mono-label {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #55544E; }}
      .mono-bold {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; fill: #111110; }}
      .display-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 700; fill: #111110; }}
      .dim-line {{ stroke: #111110; stroke-width: 1.2; }}
    </style>
  </defs>

  <!-- Swiss Modular Grid Layer -->
  <g id="swiss-grid-cols">
{grid_svg}
  </g>

  <!-- Framing Margins & Registration Marks -->
  <g id="registration-marks">
    <rect x="{margin_x}" y="{margin_y}" width="{content_w}" height="{content_h}" fill="none" stroke="#111110" stroke-width="1" stroke-opacity="0.2" />
    <circle cx="{margin_x}" cy="{margin_y}" r="2" fill="#111110" />
    <circle cx="{width - margin_x}" cy="{margin_y}" r="2" fill="#111110" />
    <circle cx="{margin_x}" cy="{height - margin_y}" r="2" fill="#111110" />
    <circle cx="{width - margin_x}" cy="{height - margin_y}" r="2" fill="#111110" />
  </g>

  <!-- Folio Header -->
  <text x="{margin_x}" y="{margin_y - 18}" class="mono-label" letter-spacing="1">PROJECT MONOGRAPH: {title.upper()}</text>
  <text x="{width - margin_x}" y="{margin_y - 18}" class="mono-bold" text-anchor="end">{act}</text>
  <line x1="{margin_x}" y1="{margin_y}" x2="{width - margin_x}" y2="{margin_y}" class="hairline" />

  <!-- Left Column: Project Passport & Material Index -->
  <g transform="translate({margin_x}, {margin_y + 40})">
    <text x="0" y="24" class="display-title">{title}</text>
    <text x="0" y="48" class="mono-label">TYPOLOGY: {typology.upper()}</text>
    <text x="0" y="66" class="mono-label">LOCATION: {location.upper()} // YEAR: {year}</text>
    <text x="0" y="84" class="mono-bold">ROLE: {role.upper()}</text>
    
    <line x1="0" y1="104" x2="520" y2="104" class="hairline" />

    <!-- Project Passport Meta Box -->
    <g transform="translate(0, 120)">
      <rect x="0" y="0" width="520" height="90" fill="#F8F8F5" stroke="#E8E5DC" />
      <text x="16" y="24" class="mono-bold">PROJECT PASSPORT // STRASBOURG ATELIER</text>
      <text x="16" y="46" font-size="12px" fill="#111110">Eurocode 5 Timber Compliance • RE2020 Carbon Standard</text>
      <text x="16" y="66" font-size="12px" fill="#55544E">Verified individual line-item detailing and CAD execution.</text>
    </g>

    <!-- Material Index Callouts -->
    <g transform="translate(0, 240)">
      <text x="0" y="0" class="mono-bold" letter-spacing="1">TECTONIC MATERIAL SCHEDULE</text>

      <g transform="translate(0, 20)">
        <rect x="0" y="0" width="22" height="22" fill="#111110" />
        <text x="11" y="15" class="mono-bold" fill="#FFFFFF" text-anchor="middle">01</text>
        <text x="32" y="12" font-size="13px" font-weight="700" fill="#111110">Breton Granite Ashlar (180mm)</text>
        <text x="32" y="28" font-size="11px" fill="#55544E">Ventilated rainscreen, lime NHL 3.5 joint mortar</text>
      </g>

      <g transform="translate(0, 75)">
        <rect x="0" y="0" width="22" height="22" fill="#55544E" />
        <text x="11" y="15" class="mono-bold" fill="#FFFFFF" text-anchor="middle">02</text>
        <text x="32" y="12" font-size="13px" font-weight="700" fill="#111110">Lime-Hemp Biotamping (140mm)</text>
        <text x="32" y="28" font-size="11px" fill="#55544E">Hygrothermal monolithic core, λ = 0.076 W/m·K</text>
      </g>

      <g transform="translate(0, 130)">
        <rect x="0" y="0" width="22" height="22" fill="#111110" />
        <text x="11" y="15" class="mono-bold" fill="#FFFFFF" text-anchor="middle">03</text>
        <text x="32" y="12" font-size="13px" font-weight="700" fill="#111110">Structural Thermal Break & EPDM</text>
        <text x="32" y="28" font-size="11px" fill="#55544E">Continuous capillary seal, plinth elevation +150mm</text>
      </g>

      <g transform="translate(0, 185)">
        <rect x="0" y="0" width="22" height="22" fill="#55544E" />
        <text x="11" y="15" class="mono-bold" fill="#FFFFFF" text-anchor="middle">04</text>
        <text x="32" y="12" font-size="13px" font-weight="700" fill="#111110">French Oak Glulam Post & Beam (160x280)</text>
        <text x="32" y="28" font-size="11px" fill="#55544E">PEFC certified mass timber frame w/ concealed flitch plates</text>
      </g>
    </g>

    <!-- Recruiter Proof Guarantee -->
    <g transform="translate(0, 580)">
      <rect x="0" y="0" width="520" height="96" fill="#F8F8F5" stroke="#E8E5DC" />
      <text x="16" y="24" class="mono-bold">CONSTRUCTIVE PROOF GUARANTEE</text>
      <text x="16" y="44" font-size="11px" fill="#111110">Zero render trap reliance. Every detail supported by verified</text>
      <text x="16" y="60" font-size="11px" fill="#111110">working drawings, thermal continuity, and PMR egress.</text>
      <text x="16" y="82" class="mono-label">ANTI-RENDER-TRAP VALIDATED • 100% BUILDABLE</text>
    </g>
  </g>

  <!-- Right Viewport: Primary Technical Drawing (1:20 Wall Section) -->
  <g transform="translate({margin_x + 560}, {margin_y + 40})">
    <rect x="0" y="0" width="{content_w - 560}" height="{content_h - 60}" fill="#FFFFFF" stroke="#E8E5DC" stroke-width="1" />
    
    <!-- Foundation Plinth & Concrete Ground Slab -->
    <rect x="180" y="480" width="680" height="120" fill="#F4F4F0" stroke="#111110" stroke-width="2" />
    <line x1="190" y1="520" x2="850" y2="520" stroke="#84827A" stroke-width="1" stroke-dasharray="8 6" />
    <line x1="190" y1="570" x2="850" y2="570" stroke="#84827A" stroke-width="1" stroke-dasharray="8 6" />

    <!-- 01 Breton Granite Ashlar Outer Leaf -->
    <g>
      <rect x="180" y="40" width="160" height="440" fill="#EAEAE5" stroke="#111110" stroke-width="2" />
      <line x1="180" y1="120" x2="340" y2="120" stroke="#111110" stroke-width="1" />
      <line x1="180" y1="200" x2="340" y2="200" stroke="#111110" stroke-width="1" />
      <line x1="180" y1="280" x2="340" y2="280" stroke="#111110" stroke-width="1" />
      <line x1="180" y1="360" x2="340" y2="360" stroke="#111110" stroke-width="1" />
    </g>

    <!-- 02 Lime-Hemp Biotamping Insulation -->
    <rect x="340" y="40" width="120" height="440" fill="#F8F8F5" stroke="#111110" stroke-width="1.5" stroke-dasharray="4 2" />

    <!-- 03 Thermal Break & EPDM Capillary Membrane -->
    <rect x="460" y="40" width="20" height="440" fill="#DDD9D0" stroke="#111110" stroke-width="1.5" />
    <line x1="460" y1="480" x2="480" y2="480" stroke="#111110" stroke-width="3" />

    <!-- 04 Oak Glulam Framing Column -->
    <g>
      <rect x="480" y="40" width="140" height="440" fill="#F3F0E8" stroke="#111110" stroke-width="2" />
      <line x1="480" y1="40" x2="620" y2="480" stroke="#DDD9D0" stroke-width="1" />
      <line x1="620" y1="40" x2="480" y2="480" stroke="#DDD9D0" stroke-width="1" />
    </g>

    <!-- 05 Triple Glazed Timber-Alu Envelope -->
    <g>
      <rect x="620" y="140" width="360" height="260" fill="#F8F8F5" stroke="#111110" stroke-width="2" />
      <line x1="620" y1="270" x2="980" y2="270" stroke="#111110" stroke-width="1.5" />
      <text x="800" y="258" class="mono-bold" text-anchor="middle">TRIPLE GLAZED TIMBER-ALU // Uw = 0.78 W/m²K</text>
    </g>

    <!-- Dimension Chains -->
    <g stroke="#111110" stroke-width="1.2">
      <line x1="120" y1="40" x2="120" y2="480" />
      <line x1="108" y1="40" x2="132" y2="40" />
      <line x1="108" y1="480" x2="132" y2="480" />
      <line x1="112" y1="44" x2="128" y2="36" stroke-width="2" />
      <line x1="112" y1="484" x2="128" y2="476" stroke-width="2" />
    </g>
    <text x="100" y="260" class="mono-bold" text-anchor="middle" transform="rotate(-90 100 260)">4400 MM CLEARANCE</text>

    <g stroke="#111110" stroke-width="1.2">
      <line x1="180" y1="18" x2="480" y2="18" />
      <line x1="180" y1="8" x2="180" y2="28" />
      <line x1="480" y1="8" x2="480" y2="28" />
      <line x1="176" y1="22" x2="184" y2="14" stroke-width="2" />
      <line x1="476" y1="22" x2="484" y2="14" stroke-width="2" />
    </g>
    <text x="330" y="12" class="mono-bold" text-anchor="middle">300 MM COMPOSITE ENVELOPE</text>
  </g>

  <!-- Folio Footer -->
  <line x1="{margin_x}" y1="{height - margin_y}" x2="{width - margin_x}" y2="{height - margin_y}" class="hairline" />
  <text x="{margin_x}" y="{height - margin_y + 22}" class="mono-label">LEAD ARCHITECT: SARA BENSALEM • STRASBOURG ATELIER [48°35'05"N 07°45'02"E]</text>
  <text x="{width / 2}" y="{height - margin_y + 22}" class="mono-label" text-anchor="middle">WORK RIGHTS: EU CITIZEN // ZERO VISA SPONSORSHIP REQUIRED</text>
  <text x="{width - margin_x}" y="{height - margin_y + 22}" class="mono-bold" text-anchor="end">SPREAD {spread_num}</text>
</svg>"""
    return svg

def main():
    parser = argparse.ArgumentParser(description="Sara Bensalem Monograph Spread Compiler")
    parser.add_argument("--title", default="Maison Bretonne Adaptive Reuse", help="Project Title")
    parser.add_argument("--location", default="Finistère, France", help="Project Location")
    parser.add_argument("--typology", default="Heritage Renovation & Timber Pavilion", help="Typology")
    parser.add_argument("--columns", type=int, default=12, help="Swiss grid columns (8, 12, 16)")
    parser.add_argument("--output", "-o", default="monograph_spread.svg", help="Output SVG path")
    args = parser.parse_args()

    svg_content = generate_monograph_svg(
        title=args.title,
        location=args.location,
        typology=args.typology,
        columns=args.columns
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Monograph spread compiled successfully to: {args.output}")

if __name__ == "__main__":
    main()
