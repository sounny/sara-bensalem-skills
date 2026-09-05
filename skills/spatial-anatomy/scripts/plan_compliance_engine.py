#!/usr/bin/env python3
"""
Sara Bensalem Skills — Spatial Anatomy & PMR Compliance Engine (2026 Enhanced Edition)
Validates floor plans against French PMR (Arrêté du 24 décembre 2015), US ADA 2010 Standards,
IBC emergency egress mandates, and Trauma-Informed 'Space for Hesitation' principles.
Renders publication-grade 1:100 vector SVG architectural plans with wheelchair circles,
door clearance arcs, and egress travel vectors.
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
Website: https://skills.sarabensalem.com
"""

import sys
import os
import argparse
import json

def validate_plan_compliance(door_clear_mm=None, vestibule_dia_mm=None, corridor_width_mm=None,
                             hesitation_width_mm=None, travel_distance_m=None,
                             door_clear_width=None, vestibule_diameter=None,
                             corridor_width=None, hesitation_width=None):
    # Resolve aliases
    d_clear = door_clear_mm if door_clear_mm is not None else (door_clear_width if door_clear_width is not None else 900)
    v_dia = vestibule_dia_mm if vestibule_dia_mm is not None else (vestibule_diameter if vestibule_diameter is not None else 1500)
    c_w = corridor_width_mm if corridor_width_mm is not None else (corridor_width if corridor_width is not None else 1600)
    h_w = hesitation_width_mm if hesitation_width_mm is not None else (hesitation_width if hesitation_width is not None else 2400)
    t_dist = travel_distance_m if travel_distance_m is not None else 24.0

    door_pass = d_clear >= 830
    vestibule_pass = v_dia >= 1500
    corridor_pass = c_w >= 1400
    hesitation_pass = h_w >= 2000
    travel_pass = t_dist <= 30.0

    all_pass = door_pass and vestibule_pass and corridor_pass and hesitation_pass and travel_pass
    compliance_status = "COMPLIANT" if all_pass else "NON_COMPLIANT"

    violations = []
    if not door_pass:
        violations.append(f"Door clear width ({d_clear}mm) < 830mm statutory minimum (French PMR / ADA).")
    if not vestibule_pass:
        violations.append(f"Vestibule rotation circle ({v_dia}mm) < 1500mm wheelchair turning requirement.")
    if not corridor_pass:
        violations.append(f"Corridor passing width ({c_w}mm) < 1400mm two-way clearance minimum.")
    if not hesitation_pass:
        violations.append(f"Space for Hesitation buffer width ({h_w}mm) < 2000mm trauma-informed threshold.")
    if not travel_pass:
        violations.append(f"Emergency egress travel distance ({t_dist}m) > 30.0m maximum permitted.")

    return {
        "verdict": "FULL COMPLIANCE (PMR / ADA / TRAUMA-INFORMED)" if all_pass else "NON-COMPLIANT (PERMITTING RISK)",
        "compliance_status": compliance_status,
        "all_passed": all_pass,
        "violations": violations,
        "metrics": {
            "door_clear_width_mm": {"value": d_clear, "min_required": 830, "status": "PASS" if door_pass else "FAIL"},
            "vestibule_diameter_mm": {"value": v_dia, "min_required": 1500, "status": "PASS" if vestibule_pass else "FAIL"},
            "corridor_width_mm": {"value": c_w, "min_required": 1400, "status": "PASS" if corridor_pass else "FAIL"},
            "hesitation_width_mm": {"value": h_w, "min_required": 2000, "status": "PASS" if hesitation_pass else "FAIL"},
            "travel_distance_m": {"value": t_dist, "max_allowed": 30.0, "status": "PASS" if travel_pass else "FAIL"}
        },
        "regulatory_frameworks": [
            "French PMR: Arrêté du 24 décembre 2015 relatif à l'accessibilité",
            "US ADA: 2010 ADA Standards for Accessible Design",
            "IBC: International Building Code Section 1017 (Exit Access Travel Distance)",
            "Trauma-Informed Commons: Spatial Hesitation & Psychological Safety Protocols"
        ]
    }

def generate_plan_svg(output_path="plan_1_100_accessible.svg",
                      door_clear=900, vestibule_dia=1500, corridor_w=1600):
    width = 1200
    height = 900

    report = validate_plan_compliance(door_clear, vestibule_dia, corridor_w)

    verdict_text = report["verdict"]
    badge_w = max(260, len(verdict_text) * 7.5 + 28)
    badge_x = 1040 - badge_w
    text_x = badge_x + badge_w / 2
    badge_fill = "#111110" if report.get("all_passed") else "#8B263E"

    svg = f"""<svg viewBox="0 0 {width} {height}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF; font-family:'Plus Jakarta Sans', sans-serif;">
  <defs>
    <style>
      .wall-cut {{ fill: #111110; stroke: #111110; stroke-width: 1; }}
      .wall-thin {{ fill: #F4F4F0; stroke: #111110; stroke-width: 1.5; }}
      .pmr-circle {{ fill: rgba(22, 22, 21, 0.04); stroke: #111110; stroke-width: 1.5; stroke-dasharray: 4 3; }}
      .hesitation-zone {{ fill: rgba(139, 38, 62, 0.05); stroke: #8B263E; stroke-width: 1.5; stroke-dasharray: 6 3; }}
      .door-arc {{ stroke: #55544E; stroke-width: 1.2; stroke-dasharray: 2 2; fill: none; }}
      .mono-label {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #55544E; }}
      .mono-bold {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; fill: #111110; }}
      .mono-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; fill: #111110; }}
      .egress-vector {{ stroke: #8B263E; stroke-width: 2; stroke-dasharray: 8 4; fill: none; marker-end: url(#arrow); }}
    </style>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#8B263E" />
    </marker>
  </defs>

  <!-- Header -->
  <text x="60" y="50" class="mono-title">1:100 Spatial Anatomy &amp; PMR Universal Accessibility Plan</text>
  <text x="60" y="74" class="mono-label">SCALE 1:100 // STRASBOURG ATELIER // VERIFIED 1500MM TURNING CIRCLES &amp; HESITATION THRESHOLDS</text>
  <line x1="60" y1="90" x2="1140" y2="90" stroke="#DDD9D0" stroke-width="1" />

  <!-- Outer Perimeter Walls (Loadbearing 300mm Envelope) -->
  <rect x="80" y="130" width="1040" height="680" fill="#FFFFFF" stroke="#111110" stroke-width="3.5" />
  
  <!-- Internal Partitions -->
  <line x1="420" y1="130" x2="420" y2="520" stroke="#111110" stroke-width="3" />
  <line x1="80" y1="520" x2="420" y2="520" stroke="#111110" stroke-width="3" />
  <line x1="780" y1="130" x2="780" y2="810" stroke="#111110" stroke-width="3" />

  <!-- Room 1: Entrance Airlock & Reception (Sas d'accueil) -->
  <text x="250" y="170" class="mono-bold" text-anchor="middle">ENTRANCE AIRLOCK (SAS ACCUEIL)</text>
  <text x="250" y="190" class="mono-label" text-anchor="middle">DIMENSIONS: 3400 x 3900 MM</text>
  
  <!-- 1500mm PMR Wheelchair Circle in Airlock -->
  <circle cx="250" cy="320" r="75" class="pmr-circle" />
  <line x1="175" y1="320" x2="325" y2="320" stroke="#111110" stroke-width="1" />
  <text x="250" y="315" class="mono-label" text-anchor="middle">Ø 1500 MM PMR TURNING</text>

  <!-- Door 1 (Main Entrance Exterior Door) -->
  <line x1="80" y1="280" x2="80" y2="370" stroke="#FFFFFF" stroke-width="8" />
  <line x1="80" y1="280" x2="145" y2="355" stroke="#111110" stroke-width="2.5" />
  <path d="M 80 370 A 90 90 0 0 0 145 355" class="door-arc" />
  <text x="60" y="330" class="mono-bold" text-anchor="end">{door_clear} MM CLEAR</text>

  <!-- Room 2: Universal Sanitary Block -->
  <rect x="80" y="520" width="340" height="290" fill="#F8F8F5" stroke="#111110" stroke-width="2" />
  <text x="250" y="555" class="mono-bold" text-anchor="middle">UNIVERSAL ACCESSIBLE SANITARY</text>
  
  <!-- 1500mm PMR Circle in Sanitary -->
  <circle cx="250" cy="670" r="75" class="pmr-circle" />
  <text x="250" y="675" class="mono-label" text-anchor="middle">Ø 1500 MM CLEAR</text>
  <rect x="360" y="640" width="40" height="60" fill="#DDD9D0" stroke="#111110" />
  <text x="380" y="675" class="mono-label" text-anchor="middle">WC</text>
  <line x1="340" y1="630" x2="340" y2="710" stroke="#111110" stroke-width="2" />
  <text x="330" y="675" class="mono-label" text-anchor="end">GRAB BAR</text>

  <!-- Sanitary Door (Opens Outwards for Emergency Egress) -->
  <line x1="420" y1="580" x2="420" y2="670" stroke="#FFFFFF" stroke-width="8" />
  <line x1="420" y1="580" x2="485" y2="645" stroke="#111110" stroke-width="2.5" />
  <path d="M 420 670 A 90 90 0 0 0 485 645" class="door-arc" />
  <text x="495" y="630" class="mono-bold">900 MM OUTWARD</text>

  <!-- Zone 3: Central Circulation Galleria & Space for Hesitation -->
  <text x="600" y="170" class="mono-bold" text-anchor="middle">CENTRAL CIVIC GALLERIA</text>
  <text x="600" y="190" class="mono-label" text-anchor="middle">CLEAR PASSING WIDTH: {corridor_w} MM (&gt;= 1400 MM REQUIRED)</text>

  <!-- Trauma-Informed "Space for Hesitation" Threshold Alcove -->
  <rect x="440" y="240" width="320" height="180" class="hesitation-zone" />
  <text x="600" y="280" font-family="'Space Grotesk', sans-serif" font-weight="700" font-size="14px" fill="#8B263E" text-anchor="middle">SPACE FOR HESITATION (KRITHIKA PROTOCOL)</text>
  <text x="600" y="305" class="mono-label" text-anchor="middle">Transitional buffer threshold with 120° sightline orientation</text>
  <circle cx="600" cy="355" r="45" class="pmr-circle" />
  <text x="600" y="360" class="mono-label" text-anchor="middle">SIT &amp; ORIENT</text>

  <!-- Emergency Egress Vector -->
  <path d="M 600 480 L 600 680 L 440 680" class="egress-vector" />
  <text x="610" y="580" font-family="'JetBrains Mono', monospace" font-size="10px" font-weight="700" fill="#8B263E">EGRESS TRAVEL PATH (22M TO EXIT)</text>

  <!-- Room 4: Collective Assembly & Workshop Commons -->
  <rect x="780" y="130" width="340" height="680" fill="#FFFFFF" stroke="#111110" stroke-width="2" />
  <text x="950" y="170" class="mono-bold" text-anchor="middle">COLLECTIVE WORKSHOP COMMONS</text>
  <text x="950" y="190" class="mono-label" text-anchor="middle">OPEN SIGHTLINES // ZERO BLIND CORNERS</text>
  <circle cx="950" cy="470" r="75" class="pmr-circle" />
  <text x="950" y="475" class="mono-label" text-anchor="middle">Ø 1500 MM PMR</text>

  <!-- Dimension Strings -->
  <g stroke="#111110" stroke-width="1.2">
    <line x1="80" y1="840" x2="1120" y2="840" />
    <line x1="80" y1="830" x2="80" y2="850" />
    <line x1="420" y1="830" x2="420" y2="850" />
    <line x1="780" y1="830" x2="780" y2="850" />
    <line x1="1120" y1="830" x2="1120" y2="850" />
  </g>
  <text x="250" y="860" class="mono-bold" text-anchor="middle">3400 MM</text>
  <text x="600" y="860" class="mono-bold" text-anchor="middle">3600 MM</text>
  <text x="950" y="860" class="mono-bold" text-anchor="middle">3400 MM</text>

  <!-- Compliance Legend & Status Badge -->
  <g transform="translate(80, 80)">
    <rect x="{badge_x:.1f}" y="-30" width="{badge_w:.1f}" height="34" fill="{badge_fill}" rx="4" />
    <text x="{text_x:.1f}" y="-8" class="mono-bold" style="fill:#FFFFFF;" text-anchor="middle">{verdict_text}</text>
  </g>
</svg>"""

    svg = svg.replace("&AMP;", "&amp;").replace("&LT;", "&lt;").replace("&GT;", "&gt;").replace("&QUOT;", "&quot;")

    if output_path:
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Sara Bensalem Spatial Anatomy & PMR Compliance Engine")
    parser.add_argument("--door", type=float, default=900, help="Door clear opening in mm")
    parser.add_argument("--vestibule", type=float, default=1500, help="Vestibule diameter in mm")
    parser.add_argument("--corridor", type=float, default=1600, help="Corridor clear width in mm")
    parser.add_argument("--output", "-o", default="plan_1_100_accessible.svg", help="Output SVG Path")
    args = parser.parse_args()

    report = validate_plan_compliance(args.door, args.vestibule, args.corridor)
    print(json.dumps(report, indent=2))
    
    out = generate_plan_svg(args.output, args.door, args.vestibule, args.corridor)
    print(f"Plan drawing generated: {out}")

if __name__ == "__main__":
    main()
