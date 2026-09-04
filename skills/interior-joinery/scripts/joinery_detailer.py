#!/usr/bin/env python3
"""
Sara Bensalem Skills — Interior Joinery Detailer
Generates 1:5 scale custom cabinetry and shadow reveal (joint creux) vector SVG drawings,
with hardware clearances and dimension chains.
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
"""

import sys
import os

def generate_joinery_svg(output_path="joinery_1_5_detail.svg"):
    width = 1200
    height = 900

    svg = f"""<svg viewBox="0 0 {width} {height}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF; font-family:'Plus Jakarta Sans', sans-serif;">
  <defs>
    <style>
      .cut-timber {{ fill: #F3F0E8; stroke: #111110; stroke-width: 2.2; }}
      .cut-stone {{ fill: #EAEAE5; stroke: #111110; stroke-width: 2.2; }}
      .cut-metal {{ fill: #DDD9D0; stroke: #111110; stroke-width: 1.5; }}
      .shadow-gap {{ fill: #111110; }}
      .mono-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; fill: #111110; }}
      .mono-label {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #55544E; }}
      .mono-bold {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; fill: #111110; }}
    </style>
  </defs>

  <!-- Header -->
  <text x="60" y="50" class="mono-title">1:5 Bespoke Millwork & Shadow Reveal (Joint Creux) Detail</text>
  <text x="60" y="74" class="mono-label">SCALE 1:5 // STRASBOURG ATELIER // CONCEALED BLUM HARDWARE TOLERANCES</text>
  <line x1="60" y1="90" x2="1140" y2="90" stroke="#DDD9D0" stroke-width="1" />

  <!-- Technical Spec Box -->
  <g transform="translate(60, 110)">
    <rect x="0" y="0" width="340" height="200" fill="#F8F8F5" stroke="#DDD9D0" />
    <text x="16" y="24" class="mono-bold">FABRICATION SPECIFICATION</text>
    <text x="16" y="50" class="mono-label">Primary Substrate: 19mm Black MDF Core</text>
    <text x="16" y="72" class="mono-bold">Facing: 0.8mm Quartersawn French Oak</text>
    <text x="16" y="94" class="mono-bold">Shadow Reveal: 5mm Negative Air Gap</text>
    <text x="16" y="116" class="mono-label">Hardware: Blum Clip Top Blumotion 110°</text>
    <text x="16" y="138" class="mono-label">Hinge Cup Depth: 12.8mm Bore (Ø 35mm)</text>
    <text x="16" y="160" class="mono-bold">Base Plinth: Honed Noir Saint-Laurent Stone</text>
    <text x="16" y="180" class="mono-label">Finish: Natural Matte Hardwax Oil</text>
  </g>

  <!-- Material Index Callout -->
  <g transform="translate(60, 340)">
    <text x="0" y="0" class="mono-bold" letter-spacing="1">MATERIAL TRIPTYCH</text>
    
    <g transform="translate(0, 20)">
      <rect x="0" y="0" width="20" height="20" fill="#EAEAE5" stroke="#111110" />
      <text x="10" y="14" class="mono-bold" text-anchor="middle">A</text>
      <text x="30" y="14" class="mono-bold">Honed Limestone Floor Tile (20mm)</text>
    </g>
    <g transform="translate(0, 60)">
      <rect x="0" y="0" width="20" height="20" fill="#111110" />
      <text x="10" y="14" class="mono-bold" fill="#FFFFFF" text-anchor="middle">B</text>
      <text x="30" y="14" class="mono-bold">Recessed Anodized Aluminum Reglet (5x15mm)</text>
    </g>
    <g transform="translate(0, 100)">
      <rect x="0" y="0" width="20" height="20" fill="#F3F0E8" stroke="#111110" />
      <text x="10" y="14" class="mono-bold" text-anchor="middle">C</text>
      <text x="30" y="14" class="mono-bold">Oak Veneered Cabinetry Door Leaf (22mm)</text>
    </g>
  </g>

  <!-- Drawing Viewport (1:5 Scale) -->
  <g transform="translate(440, 110)">
    <rect x="0" y="0" width="700" height="720" fill="#FFFFFF" stroke="#DDD9D0" />

    <!-- Floor Substrate & Screed -->
    <rect x="80" y="560" width="560" height="120" fill="#F4F4F0" stroke="#111110" stroke-width="2" />
    <text x="360" y="630" class="mono-bold" text-anchor="middle">FLOOR SCREED & ACOUSTIC UNDERLAYMENT</text>

    <!-- Limestone Finish Floor -->
    <rect x="80" y="520" width="560" height="40" class="cut-stone" />
    <text x="360" y="545" class="mono-bold" text-anchor="middle">HONED LIMESTONE SLAB (20MM)</text>

    <!-- Plinth Baseboard with Negative Reveal -->
    <!-- Recessed Shadow Baseboard Reglet (5mm gap) -->
    <rect x="180" y="490" width="20" height="30" class="cut-metal" />
    <line x1="180" y1="490" x2="200" y2="490" stroke="#111110" stroke-width="3" />
    <text x="160" y="510" class="mono-bold" text-anchor="end">5MM NEGATIVE SHADOW REVEAL</text>

    <!-- Cabinet Carcase Side Panel -->
    <rect x="200" y="120" width="120" height="400" class="cut-timber" />
    <line x1="200" y1="120" x2="320" y2="520" stroke="#DDD9D0" stroke-width="1" />
    <text x="260" y="320" class="mono-bold" text-anchor="middle" transform="rotate(-90 260 320)">19MM CARCASE</text>

    <!-- Concealed Blum Hinge Pocket -->
    <rect x="300" y="240" width="20" height="60" fill="#DDD9D0" stroke="#111110" stroke-width="1.5" />
    <text x="280" y="275" class="mono-label" text-anchor="end">BLUM 110°</text>

    <!-- Cabinet Door Leaf (22mm) -->
    <rect x="325" y="100" width="45" height="415" class="cut-timber" />
    
    <!-- 2.5mm Door Reveal Gap -->
    <line x1="320" y1="100" x2="320" y2="515" stroke="#111110" stroke-width="1.5" stroke-dasharray="2 2" />
    <text x="322" y="80" class="mono-bold" text-anchor="middle">2.5MM GAP</text>

    <!-- Dimension Callouts -->
    <g stroke="#111110" stroke-width="1.2">
      <line x1="400" y1="100" x2="400" y2="515" />
      <line x1="390" y1="100" x2="410" y2="100" />
      <line x1="390" y1="515" x2="410" y2="515" />
    </g>
    <text x="425" y="310" class="mono-bold">830 MM DOOR HEIGHT</text>
  </g>

  <!-- Footer -->
  <line x1="60" y1="850" x2="1140" y2="850" stroke="#DDD9D0" stroke-width="1" />
  <text x="60" y="874" class="mono-label">SARA BENSALEM SKILLS • 1:5 MILLWORK DETAILING • STRASBOURG ATELIER</text>
  <text x="1140" y="874" class="mono-bold" text-anchor="end">EXECUTION READY</text>
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Interior joinery detail written to: {output_path}")

if __name__ == "__main__":
    generate_joinery_svg()
