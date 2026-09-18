#!/usr/bin/env python3
"""
spatial_journey_matrix.py
-------------------------
Sara Bensalem Skills — Spatial Choreography & Phenomenological Journey Engine
Models and visualizes spatial sequences across:
- Luminance Lux Gradients & Transitions (delta E log steps <= 1.8)
- Acoustic Noise Reduction (dBA attenuation & NRC absorption)
- Volumetric Compression/Expansion Ratios (H_threshold / H_hall)
- Subtractive Courtyard Self-Shading Aspect Ratio (H / W >= 1.5)
- Generates publication-grade vector SVG trajectory diagrams
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
Website: https://skills.sarabensalem.com
"""

import math
import json
import argparse
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class SpatialZone:
    name: str
    phenomenological_title: str
    target_lux: float
    target_dba: float
    ceiling_height_m: float
    width_m: float
    material_finish: str
    nrc_rating: float = 0.15

def evaluate_journey(zones: List[SpatialZone]) -> Dict[str, Any]:
    evaluation = {
        "zones": [asdict(z) for z in zones],
        "transitions": [],
        "warnings": [],
        "verdict": "PASS"
    }

    for i in range(len(zones) - 1):
        z_curr = zones[i]
        z_next = zones[i + 1]

        # 1. Lux log step:
        if z_curr.target_lux > 0 and z_next.target_lux > 0:
            log_delta = abs(math.log10(z_curr.target_lux) - math.log10(z_next.target_lux))
        else:
            log_delta = 0.0

        lux_warning = None
        if log_delta > 1.8:
            lux_warning = (
                f"Abrupt luminance transition between '{z_curr.name}' ({z_curr.target_lux:.0f} lux) "
                f"and '{z_next.name}' ({z_next.target_lux:.0f} lux). log10 delta = {log_delta:.2f} > 1.8. "
                f"Risk of temporary disorientation."
            )
            evaluation["warnings"].append(lux_warning)

        # 2. Acoustic step:
        dba_delta = z_curr.target_dba - z_next.target_dba

        # 3. Volumetric Compression:
        vol_ratio = z_curr.ceiling_height_m / max(0.1, z_next.ceiling_height_m)

        evaluation["transitions"].append({
            "from": z_curr.name,
            "to": z_next.name,
            "lux_delta_log": round(log_delta, 2),
            "dba_drop": round(dba_delta, 1),
            "volumetric_ratio": round(vol_ratio, 2),
            "lux_warning": lux_warning
        })

    if evaluation["warnings"]:
        evaluation["verdict"] = "REVISE"

    return evaluation

def audit_courtyard(height_m: float, width_m: float, solar_altitude_deg: float = 65.0) -> Dict[str, Any]:
    aspect_ratio = height_m / max(0.1, width_m)
    shadow_length = height_m / math.tan(math.radians(solar_altitude_deg))
    shaded_fraction = min(1.0, shadow_length / max(0.1, width_m))
    is_self_shading = aspect_ratio >= 1.5

    return {
        "height_m": height_m,
        "width_m": width_m,
        "aspect_ratio": round(aspect_ratio, 2),
        "target_aspect_ratio": ">= 1.50 (Desert Self-Shading Standard)",
        "solar_altitude_deg": solar_altitude_deg,
        "shaded_ground_fraction": f"{round(shaded_fraction * 100, 1)}%",
        "self_shading_verified": is_self_shading,
        "verdict": "PASS" if is_self_shading else "INSUFFICIENT_SHADING_DEEPEN_CARVE"
    }

def generate_journey_svg(zones: List[SpatialZone], output_path="spatial_journey.svg"):
    evaluation = evaluate_journey(zones)
    width = 1200
    height = 800

    n = len(zones)
    x_start = 120
    x_end = 1080
    dx = (x_end - x_start) / max(1, n - 1)

    lux_pts = []
    dba_pts = []
    vol_bars = []

    for i, z in enumerate(zones):
        cx = x_start + i * dx
        # Log lux mapping: 10^1 to 10^5 mapped to y: 350 to 120
        log_val = max(1.0, math.log10(max(1.0, z.target_lux)))
        cy_lux = 360 - (log_val / 5.0) * 220
        lux_pts.append(f"{cx:.1f},{cy_lux:.1f}")

        # dBA mapping: 30 to 80 mapped to y: 550 to 400
        cy_dba = 560 - ((z.target_dba - 30.0) / 50.0) * 140
        dba_pts.append(f"{cx:.1f},{cy_dba:.1f}")

        # Volumetric bar height: height 0 to 15m
        bar_h = min(140, (z.ceiling_height_m / 15.0) * 140)
        vol_bars.append((cx, bar_h, z.ceiling_height_m))

    verdict_color = "#111110" if evaluation["verdict"] == "PASS" else "#C8523D"

    svg = f"""<svg viewBox="0 0 {width} {height}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF; font-family:'Plus Jakarta Sans', sans-serif;">
  <defs>
    <style>
      .mono-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; fill: #111110; }}
      .mono-body {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #55544E; }}
      .mono-bold {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; fill: #111110; }}
      .lux-line {{ stroke: #E68A00; stroke-width: 2.5; fill: none; }}
      .dba-line {{ stroke: #2563EB; stroke-width: 2.5; fill: none; }}
    </style>
  </defs>

  <!-- Header -->
  <text x="60" y="50" class="mono-title">Spatial Choreography &amp; Phenomenological Trajectory</text>
  <text x="60" y="74" class="mono-body">STRASBOURG ATELIER // LUMINANCE LUX GRADIENT • ACOUSTIC ATTENUATION • VOLUMETRIC RHYTHM</text>
  <line x1="60" y1="90" x2="{width - 60}" y2="90" stroke="#DDD9D0" stroke-width="1" />

  <!-- Status Badge -->
  <g transform="translate({width - 240}, 35)">
    <rect x="0" y="0" width="180" height="34" fill="{verdict_color}" />
    <text x="90" y="22" class="mono-bold" fill="#FFFFFF" text-anchor="middle">VERDICT: {evaluation['verdict']}</text>
  </g>

  <!-- Section 1: Luminance Gradient Chart (Lux) -->
  <g transform="translate(0, 0)">
    <text x="60" y="130" class="mono-bold">LUMINANCE GRADIENT (LOG10 LUX)</text>
    <text x="60" y="148" class="mono-body">Target: log10 step &lt;= 1.8 to prevent sensory shock</text>

    <!-- Grid lines -->
    <line x1="{x_start}" y1="140" x2="{x_end}" y2="140" stroke="#EAEAE5" stroke-width="1" stroke-dasharray="4 2" />
    <text x="{x_start - 15}" y="145" class="mono-body" text-anchor="end">100k lx</text>
    <line x1="{x_start}" y1="250" x2="{x_end}" y2="250" stroke="#EAEAE5" stroke-width="1" stroke-dasharray="4 2" />
    <text x="{x_start - 15}" y="255" class="mono-body" text-anchor="end">1,000 lx</text>
    <line x1="{x_start}" y1="360" x2="{x_end}" y2="360" stroke="#EAEAE5" stroke-width="1" stroke-dasharray="4 2" />
    <text x="{x_start - 15}" y="365" class="mono-body" text-anchor="end">10 lx</text>

    <!-- Trajectory Line -->
    <polyline points="{' '.join(lux_pts)}" class="lux-line" />
"""

    for i, z in enumerate(zones):
        cx = x_start + i * dx
        log_val = max(1.0, math.log10(max(1.0, z.target_lux)))
        cy_lux = 360 - (log_val / 5.0) * 220
        svg += f"""    <circle cx="{cx:.1f}" cy="{cy_lux:.1f}" r="5" fill="#E68A00" stroke="#FFFFFF" stroke-width="2" />
    <text x="{cx:.1f}" y="{cy_lux - 12:.1f}" class="mono-bold" font-size="10px" text-anchor="middle">{z.target_lux:.0f} lx</text>
"""

    svg += f"""  </g>

  <!-- Section 2: Acoustic Noise Attenuation (dBA) -->
  <g transform="translate(0, 50)">
    <text x="60" y="370" class="mono-bold">ACOUSTIC SANCTUARY GRADIENT (dBA)</text>
    <text x="60" y="388" class="mono-body">Attenuation towards contemplative interior threshold</text>

    <!-- Grid lines -->
    <line x1="{x_start}" y1="420" x2="{x_end}" y2="420" stroke="#EAEAE5" stroke-width="1" stroke-dasharray="4 2" />
    <text x="{x_start - 15}" y="425" class="mono-body" text-anchor="end">80 dBA</text>
    <line x1="{x_start}" y1="490" x2="{x_end}" y2="490" stroke="#EAEAE5" stroke-width="1" stroke-dasharray="4 2" />
    <text x="{x_start - 15}" y="495" class="mono-body" text-anchor="end">55 dBA</text>
    <line x1="{x_start}" y1="560" x2="{x_end}" y2="560" stroke="#EAEAE5" stroke-width="1" stroke-dasharray="4 2" />
    <text x="{x_start - 15}" y="565" class="mono-body" text-anchor="end">30 dBA</text>

    <!-- Trajectory Line -->
    <polyline points="{' '.join(dba_pts)}" class="dba-line" />
"""

    for i, z in enumerate(zones):
        cx = x_start + i * dx
        cy_dba = 560 - ((z.target_dba - 30.0) / 50.0) * 140
        svg += f"""    <circle cx="{cx:.1f}" cy="{cy_dba:.1f}" r="5" fill="#2563EB" stroke="#FFFFFF" stroke-width="2" />
    <text x="{cx:.1f}" y="{cy_dba - 10:.1f}" class="mono-bold" font-size="10px" text-anchor="middle">{z.target_dba:.0f} dBA</text>
"""

    svg += f"""  </g>

  <!-- Section 3: Volumetric Rhythm & Zone Cards -->
  <g transform="translate(0, 110)">
    <text x="60" y="550" class="mono-bold">VOLUMETRIC COMPRESSION / EXPANSION RHYTHM (H_CEILING)</text>
    <line x1="{x_start}" y1="670" x2="{x_end}" y2="670" stroke="#111110" stroke-width="2" />
"""

    for i, z in enumerate(zones):
        cx = x_start + i * dx
        bh = max(10, (z.ceiling_height_m / 15.0) * 90) if z.ceiling_height_m > 0 else 5
        bar_color = "#111110" if z.ceiling_height_m < 4.0 else "#55544E"
        import html as html_lib
        esc_name = html_lib.escape(z.name)
        esc_title = html_lib.escape(z.phenomenological_title[:18])
        esc_mat = html_lib.escape(z.material_finish[:18])
        svg += f"""    <!-- Zone {i+1}: {esc_name} -->
    <rect x="{cx - 24:.1f}" y="{670 - bh:.1f}" width="48" height="{bh:.1f}" fill="{bar_color}" stroke="#111110" stroke-width="1.2" />
    <text x="{cx:.1f}" y="{660 - bh:.1f}" class="mono-bold" font-size="10px" text-anchor="middle">{z.ceiling_height_m:.1f}m</text>
    
    <!-- Zone Metadata Label -->
    <text x="{cx:.1f}" y="695" class="mono-bold" font-size="11px" text-anchor="middle">{esc_name}</text>
    <text x="{cx:.1f}" y="710" class="mono-body" font-size="9px" text-anchor="middle">{esc_title}</text>
    <text x="{cx:.1f}" y="724" class="mono-body" font-size="8px" text-anchor="middle">{esc_mat}</text>
"""

    svg += f"""  </g>

  <!-- Folio Footer -->
  <line x1="60" y1="750" x2="{width - 60}" y2="750" stroke="#DDD9D0" stroke-width="1" />
  <text x="60" y="775" class="mono-body">SARA BENSALEM STUDIO • PHENOMENOLOGICAL SPATIAL CHOREOGRAPHY • STRASBOURG ATELIER</text>
  <text x="{width - 60}" y="775" class="mono-bold" text-anchor="end">PLATE 04 // SPATIAL JOURNEY MATRIX</text>
</svg>"""

    if output_path:
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg)
    return output_path, evaluation

def parse_sequence_arg(seq_str: str) -> List[SpatialZone]:
    """
    Parses CLI sequence string:
    'Plaza:100000:68:0:Granite:Civic Threshold,Portico:1500:54:3.8:Oak:Acoustic Filter,Ramp:350:41:3.2:Lime:Subterranean Transition,Core:25000:48:11.5:Rammed Earth:Sacred Sanctuary'
    """
    zones = []
    parts = seq_str.split(",")
    for p in parts:
        tokens = [t.strip() for t in p.split(":")]
        if len(tokens) >= 5:
            name = tokens[0]
            lux = float(tokens[1])
            dba = float(tokens[2])
            height = float(tokens[3])
            material = tokens[4]
            title = tokens[5] if len(tokens) > 5 else name
            zones.append(SpatialZone(
                name=name,
                phenomenological_title=title,
                target_lux=lux,
                target_dba=dba,
                ceiling_height_m=height,
                width_m=6.0,
                material_finish=material
            ))
    return zones

DEFAULT_ZONES = [
    SpatialZone(
        name="Exterior Plaza",
        phenomenological_title="Civic Ingestion / Sky Exposure",
        target_lux=100000.0,
        target_dba=68.0,
        ceiling_height_m=0.0,
        width_m=45.0,
        material_finish="Split Breton Granite Paving",
        nrc_rating=0.05
    ),
    SpatialZone(
        name="Entry Portico",
        phenomenological_title="Compression & Deceleration",
        target_lux=700.0,
        target_dba=54.0,
        ceiling_height_m=3.8,
        width_m=4.2,
        material_finish="Charred Oak Soffit (Shou Sugi Ban)",
        nrc_rating=0.35
    ),
    SpatialZone(
        name="Subterranean Ramp",
        phenomenological_title="Tactile Shadow & Descent",
        target_lux=160.0,
        target_dba=41.0,
        ceiling_height_m=3.2,
        width_m=2.8,
        material_finish="Hemp-Lime Biotamping (Monolithic)",
        nrc_rating=0.60
    ),
    SpatialZone(
        name="Sunken Courtyard",
        phenomenological_title="Subtractive Sky Well (Oasis)",
        target_lux=360.0,
        target_dba=28.0,
        ceiling_height_m=11.5,
        width_m=6.2,
        material_finish="Aswan Sandstone Ashlar",
        nrc_rating=0.20
    ),
    SpatialZone(
        name="Memorial Core",
        phenomenological_title="Acoustic Sanctuary / Occulus",
        target_lux=70.0,
        target_dba=20.0,
        ceiling_height_m=14.0,
        width_m=8.0,
        material_finish="Porous Clay Earth Plaster",
        nrc_rating=0.75
    )
]

def main():
    parser = argparse.ArgumentParser(description="Sara Bensalem Spatial Choreography & Phenomenological Engine")
    parser.add_argument("--sequence", "-s", type=str, default=None, help="Custom sequence: 'Name:lux:dba:height_m:material:title,...'")
    parser.add_argument("--output", "-o", default="spatial_journey.svg", help="Output SVG Path")
    parser.add_argument("--json", action="store_true", help="Output JSON evaluation")
    parser.add_argument("--demo", action="store_true", help="Run demonstrator")
    args = parser.parse_args()

    zones = parse_sequence_arg(args.sequence) if args.sequence else DEFAULT_ZONES
    out_svg, eval_data = generate_journey_svg(zones, output_path=args.output)

    if args.json:
        print(json.dumps(eval_data, indent=2))
    else:
        print("=" * 72)
        print("SPATIAL CHOREOGRAPHY ENGINE -- PHENOMENOLOGICAL JOURNEY MATRIX")
        print(f"VERDICT: {eval_data['verdict']}")
        print(f"SVG PLATE: {out_svg}")
        print("=" * 72)
        print("Transition                          | Lux Log d  | dBA Drop   | Vol Ratio ")
        print("-" * 72)
        for t in eval_data["transitions"]:
            warn_str = f" [!] {t['lux_warning']}" if t["lux_warning"] else ""
            print(f"{t['from']:<35} | {t['lux_delta_log']:<10} | {t['dba_drop']:<10} | {t['volumetric_ratio']:<10}{warn_str}")
        print("=" * 72)

if __name__ == "__main__":
    main()
