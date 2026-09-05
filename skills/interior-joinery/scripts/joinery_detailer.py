#!/usr/bin/env python3
"""
Sara Bensalem Skills — Interior Joinery & Millwork Detailer (2026 Enhanced Edition)
Generates publication-grade 1:5 scale custom cabinetry, bespoke architectural reveals (joint creux),
concealed hardware pockets (Blum / Hettich / HAWA tolerances), and demountable pin details.
Supports 5 empirical joinery typologies from premier international practices.
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
Website: https://skills.sarabensalem.com
"""

import sys
import os
import argparse
import json

JOINERY_PRESETS = {
    "cabinetry_reveal": {
        "name": "Bespoke Millwork & 5mm Shadow Reveal (Joint Creux)",
        "typology": "Haute Décoration Residential Casework (French Luxury Atelier)",
        "shadow_reveal_mm": 5.0,
        "carcase_mm": 19.0,
        "door_leaf_mm": 22.0,
        "hardware": "Blum Clip Top Blumotion 110° Concealed Hinge (Ø35mm cup, 12.8mm depth)",
        "plinth": "Honed Noir Saint-Laurent Stone Base Plinth (+100mm)",
        "facing": "0.8mm Quartersawn French Oak Veneer over MR-MDF Core"
    },
    "riparian_deck_pin": {
        "name": "Tropical Boardwalk Timber & Demountable Pin Joint",
        "typology": "Riparian Public Infrastructure & Marine Decking (David Romaldo Sitepu)",
        "shadow_reveal_mm": 6.0,
        "carcase_mm": 28.0,
        "door_leaf_mm": 35.0,
        "hardware": "Concealed Stainless Steel A4 Locking Pins & Slotted T-Clip Fasteners",
        "plinth": "Galvanized HSS Steel Sub-Frame Channel (100x50x4mm)",
        "facing": "Kiln-Dried Meranti / Teak Hardwood Decking w/ Non-Slip Chamfer"
    },
    "jali_screen_pocket": {
        "name": "Porous Terracotta Jali Screen & Reglet Pocket",
        "typology": "Passive Solar Screening & Artisan Bazaars (Sneha Goel / Pearl Gupta)",
        "shadow_reveal_mm": 8.0,
        "carcase_mm": 32.0,
        "door_leaf_mm": 30.0,
        "hardware": "Recessed Anodized Aluminum Reglet Pocket w/ Neoprene Acoustic Gasket",
        "plinth": "Cast Terracotta Curb Plinth (+150mm)",
        "facing": "Hand-Cast Porous Terracotta Modular Screen Tile"
    },
    "sliding_pocket_door": {
        "name": "Concealed Ceiling-Recessed Pocket Door Track",
        "typology": "Compact Residential & Accessible Egress (PMR / ADA Compliant)",
        "shadow_reveal_mm": 4.0,
        "carcase_mm": 40.0,
        "door_leaf_mm": 45.0,
        "hardware": "HAWA Junior 80/B Ceiling Track w/ Soft-Close Damping & Floor Guide Pin",
        "plinth": "Flush Zero-Threshold Egress Floor Plate (PMR Arrêté 2015)",
        "facing": "Solid Core White Ash with Acoustic Perimeter Brush Seals"
    },
    "stone_wood_shadow": {
        "name": "Limestone Cladding to Walnut Baseboard Reveal",
        "typology": "Minimalist High-End Commercial Ateliers (Yassin Saber / Avora)",
        "shadow_reveal_mm": 8.0,
        "carcase_mm": 20.0,
        "door_leaf_mm": 22.0,
        "hardware": "Concealed Z-Clip Wall Brackets & Black Anodized Shadow Reglet Channel",
        "plinth": "Recessed 8x15mm Negative Air Gap Plinth",
        "facing": "20mm Honed Roman Travertine Stone interfacing 22mm American Walnut"
    }
}

def xml_escape(val):
    if val is None:
        return ""
    return str(val).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_joinery_svg(output_path="joinery_1_5_detail.svg", detail_key="cabinetry_reveal"):
    preset = JOINERY_PRESETS.get(detail_key, JOINERY_PRESETS["cabinetry_reveal"])
    gap = preset["shadow_reveal_mm"]

    width = 1200
    height = 1000

    esc_name = xml_escape(preset['name'].upper())
    esc_typology = xml_escape(preset['typology'][:36])
    esc_hardware_1 = xml_escape(preset['hardware'][:44])
    esc_hardware_2 = xml_escape(preset['hardware'][44:85])
    esc_plinth = xml_escape(preset['plinth'][:42])
    esc_plinth_short = xml_escape(preset['plinth'][:38])
    esc_facing = xml_escape(preset['facing'][:38])

    svg = f"""<svg viewBox="0 0 {width} {height}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF; font-family:'Plus Jakarta Sans', sans-serif;">
  <defs>
    <style>
      .cut-timber {{ fill: #F3F0E8; stroke: #111110; stroke-width: 2.2; }}
      .cut-stone {{ fill: #EAEAE5; stroke: #111110; stroke-width: 2.2; }}
      .cut-metal {{ fill: #DDD9D0; stroke: #111110; stroke-width: 1.5; }}
      .shadow-gap {{ fill: #111110; }}
      .mono-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; fill: #111110; }}
      .mono-label {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #55544E; }}
      .mono-body {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #55544E; }}
      .mono-bold {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; fill: #111110; }}
    </style>
  </defs>

  <!-- Header -->
  <text x="60" y="50" class="mono-title">1:5 Custom Architectural Joinery &amp; Shadow Reveal Detail</text>
  <text x="60" y="74" class="mono-label">SCALE 1:5 // STRASBOURG ATELIER // {esc_name}</text>
  <line x1="60" y1="90" x2="1140" y2="90" stroke="#DDD9D0" stroke-width="1" />

  <!-- Technical Spec Box -->
  <g transform="translate(60, 110)">
    <rect x="0" y="0" width="340" height="260" fill="#F8F8F5" stroke="#DDD9D0" />
    <rect x="0" y="0" width="6" height="260" fill="#111110" />
    <text x="16" y="24" class="mono-bold">FABRICATION &amp; TOLERANCES</text>
    <text x="16" y="48" class="mono-label">Typology: {esc_typology}...</text>
    <text x="16" y="70" class="mono-bold">Shadow Reveal (Joint Creux): {gap:.1f} mm Negative Gap</text>
    <text x="16" y="92" class="mono-body">Primary Substrate: {preset['carcase_mm']:.0f} mm Core Carcase</text>
    <text x="16" y="114" class="mono-body">Door/Facing Leaf: {preset['door_leaf_mm']:.0f} mm Finished Panel</text>
    <text x="16" y="136" class="mono-bold">Hardware Specification:</text>
    <text x="16" y="154" font-size="10px" fill="#111110">{esc_hardware_1}</text>
    <text x="16" y="168" font-size="10px" fill="#55544E">{esc_hardware_2}</text>
    <text x="16" y="190" class="mono-bold">Base Plinth:</text>
    <text x="16" y="208" font-size="10px" fill="#111110">{esc_plinth}</text>
    <text x="16" y="230" class="mono-label">Finish: Natural Matte Hardwax Oil / Low-VOC</text>
  </g>

  <!-- Material Triptych Callout -->
  <g transform="translate(60, 400)">
    <text x="0" y="0" class="mono-bold" letter-spacing="1">MATERIAL TRIPTYCH SPECIFICATION</text>
    
    <g transform="translate(0, 18)">
      <rect x="0" y="0" width="22" height="22" fill="#EAEAE5" stroke="#111110" stroke-width="1.2" />
      <text x="11" y="15" class="mono-bold" text-anchor="middle">A</text>
      <text x="32" y="12" font-size="12px" font-weight="700" fill="#111110">Substrate Plinth / Ground Assembly</text>
      <text x="32" y="26" class="mono-label">{esc_plinth_short}</text>
    </g>

    <g transform="translate(0, 68)">
      <rect x="0" y="0" width="22" height="22" fill="#111110" stroke="#111110" stroke-width="1.2" />
      <text x="11" y="15" class="mono-bold" fill="#FFFFFF" text-anchor="middle">B</text>
      <text x="32" y="12" font-size="12px" font-weight="700" fill="#111110">Shadow Reveal Reglet Channel ({gap}mm)</text>
      <text x="32" y="26" class="mono-label">Recessed anodized aluminum reglet profile</text>
    </g>

    <g transform="translate(0, 118)">
      <rect x="0" y="0" width="22" height="22" fill="#F3F0E8" stroke="#111110" stroke-width="1.2" />
      <text x="11" y="15" class="mono-bold" text-anchor="middle">C</text>
      <text x="32" y="12" font-size="12px" font-weight="700" fill="#111110">Finished Facing / Joinery Leaf</text>
      <text x="32" y="26" class="mono-label">{esc_facing}</text>
    </g>
  </g>

  <!-- Drawing Viewport (1:5 Large Scale Visual Detailing) -->
  <g transform="translate(440, 110)">
    <rect x="0" y="0" width="700" height="740" fill="#FFFFFF" stroke="#DDD9D0" />
    
    <!-- Base Plinth Tile / Sub-Structure (A) -->
    <rect x="80" y="540" width="540" height="120" class="cut-stone" />
    <text x="350" y="610" class="mono-bold" text-anchor="middle">PLINTH SUBSTRATE // FFL +0.000</text>

    <!-- Shadow Gap / Negative Joint Creux (B) -->
    <rect x="180" y="{540 - gap * 8:.1f}" width="440" height="{gap * 8:.1f}" fill="#111110" />
    <text x="160" y="{540 - gap * 4 + 4:.1f}" class="mono-bold" fill="#111110" text-anchor="end">{gap:.0f} MM SHADOW REVEAL</text>

    <!-- Substrate Carcase Panel (19mm) -->
    <rect x="180" y="80" width="160" height="{460 - gap * 8:.1f}" class="cut-timber" />
    <text x="260" y="280" class="mono-bold" text-anchor="middle" transform="rotate(-90 260 280)">{preset['carcase_mm']:.0f} MM CARCASE PANEL</text>

    <!-- Front Door / Facing Leaf (22mm) -->
    <rect x="360" y="80" width="180" height="{460 - gap * 8:.1f}" class="cut-timber" />
    <text x="450" y="280" class="mono-bold" text-anchor="middle" transform="rotate(-90 450 280)">{preset['door_leaf_mm']:.0f} MM FINISHED LEAF</text>

    <!-- Concealed Hardware Hinge Cup Bore (Blum Ø35mm) -->
    <rect x="320" y="220" width="40" height="90" fill="#DDD9D0" stroke="#111110" stroke-width="1.8" />
    <circle cx="340" cy="265" r="14" fill="#55544E" />
    <text x="340" y="270" font-family="'JetBrains Mono', monospace" font-size="9px" font-weight="700" fill="#FFFFFF" text-anchor="middle">Ø35</text>
    <text x="310" y="265" class="mono-bold" text-anchor="end">CONCEALED HINGE POCKET</text>

    <!-- Dimension Chains -->
    <g stroke="#111110" stroke-width="1.2">
      <line x1="560" y1="80" x2="560" y2="{540 - gap * 8:.1f}" />
      <line x1="550" y1="80" x2="570" y2="80" />
      <line x1="550" y1="{540 - gap * 8:.1f}" x2="570" y2="{540 - gap * 8:.1f}" />
    </g>
    <text x="580" y="280" class="mono-bold" text-anchor="start">720 MM CABINET HEIGHT</text>

    <g stroke="#111110" stroke-width="1.2">
      <line x1="180" y1="50" x2="540" y2="50" />
      <line x1="180" y1="40" x2="180" y2="60" />
      <line x1="360" y1="40" x2="360" y2="60" />
      <line x1="540" y1="40" x2="540" y2="60" />
    </g>
    <text x="270" y="38" class="mono-label" text-anchor="middle">CARCASE</text>
    <text x="450" y="38" class="mono-label" text-anchor="middle">DOOR LEAF</text>
  </g>

  <!-- Folio Footer -->
  <line x1="60" y1="920" x2="1140" y2="920" stroke="#DDD9D0" stroke-width="1" />
  <text x="60" y="945" class="mono-label">SARA BENSALEM STUDIO • 1:5 CUSTOM JOINERY DETAILER • FABRICATION READY</text>
  <text x="1140" y="945" class="mono-bold" text-anchor="end">TYPOLOGY: {detail_key.upper()} // PLATE 01</text>
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
    parser = argparse.ArgumentParser(description="Sara Bensalem 1:5 Custom Joinery Detailer")
    parser.add_argument("--detail", default="cabinetry_reveal", choices=list(JOINERY_PRESETS.keys()), help="Joinery Preset Key")
    parser.add_argument("--output", "-o", default="joinery_1_5_detail.svg", help="Output SVG Path")
    args = parser.parse_args()

    out = generate_joinery_svg(args.output, args.detail)
    print(f"1:5 Joinery detail successfully generated: {out}")

if __name__ == "__main__":
    main()
