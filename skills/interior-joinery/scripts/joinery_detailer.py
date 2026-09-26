#!/usr/bin/env python3
"""
Sara Bensalem Skills — Interior Joinery & Millwork Detailer (2026 Enhanced Edition)
Generates publication-grade 1:5 scale custom cabinetry, bespoke architectural reveals (joint creux),
concealed hardware pockets (Blum / Hettich / HAWA tolerances), and demountable pin details.
Supports dynamic dimensions, hardware specifications, and tactile material triptychs.
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
Website: https://skills.sarabensalem.com
"""

import sys
import os
import argparse
import json
import html

JOINERY_PRESETS = {
    "cabinetry_reveal": {
        "name": "Bespoke Millwork & 5mm Shadow Reveal (Joint Creux)",
        "typology": "Haute Décoration Residential Casework (French Luxury Atelier)",
        "shadow_reveal_mm": 5.0,
        "carcase_mm": 19.0,
        "door_leaf_mm": 22.0,
        "hardware": "Blum Clip Top Blumotion 110° Concealed Hinge (Ø35mm cup, 12.8mm depth)",
        "plinth": "Honed Noir Saint-Laurent Stone Base Plinth (+100mm)",
        "facing": "0.8mm Quartersawn French Oak Veneer over MR-MDF Core",
        "swatches": [
            {"label": "STONE", "material": "Noir Saint-Laurent", "hex": "#1E1E20", "finish": "Honed Matte / Anti-Stain"},
            {"label": "TIMBER", "material": "French Oak", "hex": "#D4B996", "finish": "Quartersawn / 5% Matt Varnish"},
            {"label": "METAL", "material": "Black Anodized Alu", "hex": "#2B2B2C", "finish": "Satin Brushed Reglet Profile"}
        ]
    },
    "riparian_deck_pin": {
        "name": "Tropical Boardwalk Timber & Demountable Pin Joint",
        "typology": "Riparian Public Infrastructure & Marine Decking (David Romaldo Sitepu)",
        "shadow_reveal_mm": 6.0,
        "carcase_mm": 28.0,
        "door_leaf_mm": 35.0,
        "hardware": "Concealed Stainless Steel A4 Locking Pins & Slotted T-Clip Fasteners",
        "plinth": "Galvanized HSS Steel Sub-Frame Channel (100x50x4mm)",
        "facing": "Kiln-Dried Meranti / Teak Hardwood Decking w/ Non-Slip Chamfer",
        "swatches": [
            {"label": "TIMBER", "material": "Meranti Hardwood", "hex": "#8D4E2D", "finish": "Marine Teak Oil Penetrating"},
            {"label": "STEEL", "material": "Stainless A4 Marine", "hex": "#A8B0B8", "finish": "Passivated Hot-Dip 80μm"},
            {"label": "POLYMER", "material": "EPDM Gasket Pad", "hex": "#1A1A1A", "finish": "Shore A 65 Vibration Damper"}
        ]
    },
    "jali_screen_pocket": {
        "name": "Porous Terracotta Jali Screen & Reglet Pocket",
        "typology": "Passive Solar Screening & Artisan Bazaars (Sneha Goel / Pearl Gupta)",
        "shadow_reveal_mm": 8.0,
        "carcase_mm": 32.0,
        "door_leaf_mm": 30.0,
        "hardware": "Recessed Anodized Aluminum Reglet Pocket w/ Neoprene Acoustic Gasket",
        "plinth": "Cast Terracotta Curb Plinth (+150mm)",
        "facing": "Hand-Cast Porous Terracotta Modular Screen Tile",
        "swatches": [
            {"label": "EARTH", "material": "Cast Terracotta", "hex": "#C8523D", "finish": "Porous Biscuit / Untreated"},
            {"label": "METAL", "material": "Bronze Reglet", "hex": "#826B4A", "finish": "Dark Chemical Patina"},
            {"label": "MORTAR", "material": "Hydraulic Lime NHL", "hex": "#E3DCCB", "finish": "Flush Recessed Joint"}
        ]
    },
    "sliding_pocket_door": {
        "name": "Concealed Ceiling-Recessed Pocket Door Track",
        "typology": "Compact Residential & Accessible Egress (PMR / ADA Compliant)",
        "shadow_reveal_mm": 4.0,
        "carcase_mm": 40.0,
        "door_leaf_mm": 45.0,
        "hardware": "HAWA Junior 80/B Ceiling Track w/ Soft-Close Damping & Floor Guide Pin",
        "plinth": "Flush Zero-Threshold Egress Floor Plate (PMR Arrêté 2015)",
        "facing": "Solid Core White Ash with Acoustic Perimeter Brush Seals",
        "swatches": [
            {"label": "TIMBER", "material": "Solid White Ash", "hex": "#DFD3BD", "finish": "Bleached Natural Hardwax"},
            {"label": "TRACK", "material": "Extruded Aluminum", "hex": "#C5CBD0", "finish": "Clear Anodized 20μm"},
            {"label": "ACOUSTIC", "material": "Schall-Ex Seal", "hex": "#333333", "finish": "Silicone Drop-Down Profile"}
        ]
    },
    "stone_wood_shadow": {
        "name": "Limestone Cladding to Walnut Baseboard Reveal",
        "typology": "Minimalist High-End Commercial Ateliers (Yassin Saber / Avora)",
        "shadow_reveal_mm": 8.0,
        "carcase_mm": 20.0,
        "door_leaf_mm": 22.0,
        "hardware": "Concealed Z-Clip Wall Brackets & Black Anodized Shadow Reglet Channel",
        "plinth": "Recessed 8x15mm Negative Air Gap Plinth",
        "facing": "20mm Honed Roman Travertine Stone interfacing 22mm American Walnut",
        "swatches": [
            {"label": "STONE", "material": "Roman Travertine", "hex": "#D8CEBE", "finish": "Open-Pore Honed Matte"},
            {"label": "TIMBER", "material": "American Walnut", "hex": "#583D28", "finish": "Deep Grain Satin Oil"},
            {"label": "METAL", "material": "Extruded Z-Channel", "hex": "#1F2326", "finish": "Matte Black Hard Anodized"}
        ]
    }
}

def xml_escape(val):
    if val is None:
        return ""
    val_str = html.unescape(str(val))
    return val_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_joinery_svg(output_path="joinery_1_5_detail.svg", detail_key="cabinetry_reveal",
                         custom_gap=None, custom_carcase=None, custom_door=None, custom_hardware=None,
                         custom_title=None, custom_deflection=None):
    preset = JOINERY_PRESETS.get(detail_key, JOINERY_PRESETS["cabinetry_reveal"])
    gap = custom_gap if custom_gap is not None else preset["shadow_reveal_mm"]
    carcase = custom_carcase if custom_carcase is not None else preset["carcase_mm"]
    door = custom_door if custom_door is not None else preset["door_leaf_mm"]
    hw = custom_hardware if custom_hardware is not None else preset["hardware"]
    title = custom_title if custom_title is not None else preset["name"]
    swatches = preset.get("swatches", [])
    deflection_mm = custom_deflection if custom_deflection is not None else 15.0

    width = 1200
    height = 1000

    esc_name = xml_escape(title.upper())
    esc_folio = xml_escape(title[:24].upper())
    esc_typology = xml_escape(preset['typology'][:42])
    esc_hw_1 = xml_escape(hw[:46])
    esc_hw_2 = xml_escape(hw[46:92])
    esc_plinth = xml_escape(preset['plinth'][:42])
    esc_facing = xml_escape(preset['facing'][:42])

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

  <!-- Left: Technical Spec Box -->
  <g transform="translate(60, 110)">
    <rect x="0" y="0" width="340" height="280" fill="#F8F8F5" stroke="#DDD9D0" />
    <rect x="0" y="0" width="6" height="280" fill="#111110" />
    <text x="16" y="24" class="mono-bold">FABRICATION &amp; TOLERANCES</text>
    <text x="16" y="48" class="mono-label">Typology: {esc_typology}...</text>
    <text x="16" y="70" class="mono-bold">Shadow Reveal (Joint Creux): {gap:.1f} mm Negative Gap</text>
    <text x="16" y="92" class="mono-body">Primary Substrate: {carcase:.0f} mm Core Carcase</text>
    <text x="16" y="114" class="mono-body">Door/Facing Leaf: {door:.0f} mm Finished Panel</text>
    <text x="16" y="136" class="mono-bold">Hardware Specification:</text>
    <text x="16" y="154" font-size="10px" fill="#111110">{esc_hw_1}</text>
    <text x="16" y="168" font-size="10px" fill="#55544E">{esc_hw_2}</text>
    <text x="16" y="190" class="mono-bold">Clearance &amp; Deflection Protocol:</text>
    <text x="16" y="206" class="mono-body">Blum Movento Bottom Clearance: 28.5 mm</text>
    <text x="16" y="222" class="mono-body">Live Slab Sag Channel: +15 mm Head Expansion</text>
    <text x="16" y="238" class="mono-body">Acoustic Perimeter Drop Seal: 42 dB Index</text>
    <text x="16" y="260" class="mono-label">Finish: Natural Matte Hardwax Oil / Zero-VOC</text>
  </g>

  <!-- Left: Tactile Material Swatch Triptych -->
  <g transform="translate(60, 420)">
    <text x="0" y="0" class="mono-bold" letter-spacing="1">TACTILE MATERIAL TRIPTYCH</text>
    <g transform="translate(0, 16)">
"""

    for i, sw in enumerate(swatches):
        sy = i * 44
        svg += f"""      <!-- Swatch {i+1}: {sw['label']} -->
      <g transform="translate(0, {sy})">
        <rect x="0" y="0" width="34" height="34" fill="{sw['hex']}" stroke="#111110" stroke-width="1.2" rx="3" />
        <text x="44" y="14" class="mono-bold">{sw['label']}: {sw['material']}</text>
        <text x="44" y="28" class="mono-body">{sw['finish']} ({sw['hex']})</text>
      </g>
"""

    svg += f"""    </g>
  </g>

  <!-- Drawing Viewport (1:5 Large Scale Visual Detailing) -->
  <g transform="translate(440, 110)">
    <!-- Top Junction: Structural R.C. Soffit & +15mm Live Slab Sag Deflection Head Channel -->
    <g id="deflection-head-channel">
      <!-- Structural R.C. Soffit -->
      <rect x="80" y="14" width="540" height="20" class="cut-stone" fill="#EAEAE5" stroke="#111110" stroke-width="2.0" />
      <text x="350" y="28" class="mono-bold" font-size="9px" text-anchor="middle">R.C. CEILING SLAB SOFFIT // LIVE LOAD DEFLECTION PLANE</text>

      <!-- Extruded Aluminum Deflection Channel (+15mm Live Sag Relief) -->
      <rect x="180" y="34" width="360" height="32" fill="#DDD9D0" stroke="#111110" stroke-width="1.8" />
      <line x1="180" y1="50" x2="540" y2="50" stroke="#111110" stroke-width="1.2" stroke-dasharray="4 2" />
      <text x="360" y="47" class="mono-bold" font-size="9px" text-anchor="middle">+{deflection_mm:.0f}MM LIVE SLAB SAG DEFLECTION CHANNEL</text>
      <text x="360" y="60" class="mono-body" font-size="8px" text-anchor="middle">Extruded Aluminum Reglet Profile (Acoustic Athmer Schall-Ex Seal)</text>

      <!-- Deflection Dimension Callout on Right -->
      <line x1="550" y1="34" x2="550" y2="66" stroke="#111110" stroke-width="1.2" />
      <line x1="545" y1="34" x2="555" y2="34" stroke="#111110" stroke-width="1.2" />
      <line x1="545" y1="66" x2="555" y2="66" stroke="#111110" stroke-width="1.2" />
      <text x="562" y="53" class="mono-bold" font-size="9px" fill="#111110">+{deflection_mm:.0f}mm sag</text>
    </g>

    <!-- Base Plinth Tile / Sub-Structure (A) -->
    <rect x="80" y="540" width="540" height="120" class="cut-stone" />
    <text x="350" y="610" class="mono-bold" text-anchor="middle">PLINTH SUBSTRATE // FFL +0.000</text>

    <!-- Shadow Gap / Negative Joint Creux (B) -->
    <rect x="180" y="{540 - gap * 8:.1f}" width="440" height="{gap * 8:.1f}" fill="#111110" />
    <text x="160" y="{540 - gap * 4 + 4:.1f}" class="mono-bold" fill="#111110" text-anchor="end">{gap:.0f} MM SHADOW REVEAL</text>

    <!-- Substrate Carcase Panel -->
    <rect x="180" y="80" width="160" height="{460 - gap * 8:.1f}" class="cut-timber" />
    <text x="260" y="280" class="mono-bold" text-anchor="middle" transform="rotate(-90 260 280)">{carcase:.0f} MM CARCASE PANEL</text>

    <!-- Front Door / Facing Leaf -->
    <rect x="360" y="80" width="180" height="{460 - gap * 8:.1f}" class="cut-timber" />
    <text x="450" y="280" class="mono-bold" text-anchor="middle" transform="rotate(-90 450 280)">{door:.0f} MM FINISHED LEAF</text>

    <!-- Concealed Hardware Hinge Cup Bore (Blum Ø35mm) -->
    <rect x="320" y="220" width="40" height="90" fill="#DDD9D0" stroke="#111110" stroke-width="1.8" />
    <circle cx="340" cy="265" r="14" fill="#55544E" />
    <text x="340" y="270" font-family="'JetBrains Mono', monospace" font-size="9px" font-weight="700" fill="#FFFFFF" text-anchor="middle">Ø35</text>
    <text x="310" y="265" class="mono-bold" text-anchor="end">CONCEALED HINGE POCKET</text>

    <!-- Blum Movento Runner 28.5mm Indicator -->
    <line x1="180" y1="500" x2="340" y2="500" stroke="#111110" stroke-width="1.2" stroke-dasharray="3 3" />
    <text x="260" y="490" class="mono-body" font-size="9px" text-anchor="middle">28.5mm MOVENTO CLEARANCE</text>

    <!-- Dimension Chains -->
    <g stroke="#111110" stroke-width="1.2">
      <line x1="560" y1="80" x2="560" y2="{540 - gap * 8:.1f}" />
      <line x1="550" y1="80" x2="570" y2="80" />
      <line x1="550" y1="{540 - gap * 8:.1f}" x2="570" y2="{540 - gap * 8:.1f}" />
    </g>
    <text x="585" y="300" class="mono-bold" text-anchor="middle" transform="rotate(90 585 300)">720 MM CABINET CARCASE HEIGHT</text>

    <!-- Horizontal Width Dimension Chains -->
    <g stroke="#111110" stroke-width="1.2">
      <line x1="180" y1="675" x2="540" y2="675" />
      <line x1="180" y1="665" x2="180" y2="685" />
      <line x1="340" y1="665" x2="340" y2="685" />
      <line x1="360" y1="665" x2="360" y2="685" />
      <line x1="540" y1="665" x2="540" y2="685" />
    </g>
    <text x="260" y="695" class="mono-body" text-anchor="middle">{carcase:.0f} MM CARCASE</text>
    <text x="450" y="695" class="mono-body" text-anchor="middle">{door:.0f} MM LEAF</text>

  </g>

  <!-- Folio Footer -->
  <line x1="60" y1="920" x2="1140" y2="920" stroke="#DDD9D0" stroke-width="1" />
  <text x="60" y="945" class="mono-label">SARA BENSALEM STUDIO • 1:5 ARCHITECTURAL MILLWORK &amp; JOINERY ENGINE • STRASBOURG ATELIER</text>
  <text x="1140" y="945" class="mono-bold" text-anchor="end">TYPOLOGY: {esc_folio} // PLATE 05</text>
</svg>"""

    if output_path:
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    meta = {
        "title": title,
        "shadow_reveal_mm": gap,
        "carcase_mm": carcase,
        "door_leaf_mm": door,
        "slab_deflection_mm": deflection_mm,
        "hardware": hw,
        "swatches": swatches,
        "output_svg": output_path
    }
    return output_path, meta

def main():
    parser = argparse.ArgumentParser(
        description="Sara Bensalem 1:5 Custom Joinery Detailer.\n"
                    "Exit codes: 0 = Compliant / buildable detail, 1 = Tectonic violation (shadow reveal < 3.0mm), 2 = CLI argument error."
    )
    parser.add_argument("--detail", default="cabinetry_reveal", choices=list(JOINERY_PRESETS.keys()), help="Joinery Preset Key")
    parser.add_argument("--gap", type=float, default=None, help="Custom shadow reveal in mm (e.g. 3.0, 5.0, 8.0)")
    parser.add_argument("--carcase", type=float, default=None, help="Custom carcase thickness in mm (e.g. 18.0, 19.0, 22.0)")
    parser.add_argument("--door", type=float, default=None, help="Custom door leaf thickness in mm (e.g. 20.0, 22.0, 25.0)")
    parser.add_argument("--deflection", type=float, default=None, help="Custom live slab sag deflection channel headroom in mm (default: 15.0)")
    parser.add_argument("--hardware", type=str, default=None, help="Custom hardware specification string")
    parser.add_argument("--title", type=str, default=None, help="Custom detail title")
    parser.add_argument("--output", "-o", default="joinery_1_5_detail.svg", help="Output SVG Path")
    parser.add_argument("--json", action="store_true", help="Output JSON metadata")
    args = parser.parse_args()

    out, meta = generate_joinery_svg(
        output_path=args.output,
        detail_key=args.detail,
        custom_gap=args.gap,
        custom_carcase=args.carcase,
        custom_door=args.door,
        custom_hardware=args.hardware,
        custom_title=args.title,
        custom_deflection=args.deflection
    )

    is_compliant = meta["shadow_reveal_mm"] >= 3.0

    if args.json:
        meta["status"] = "COMPLIANT" if is_compliant else "NON_COMPLIANT"
        print(json.dumps(meta, indent=2))
    else:
        CYAN = "\033[1;36m"
        GREEN = "\033[1;32m"
        RED = "\033[1;31m"
        RESET = "\033[0m"
        print(f"{CYAN}{'=' * 72}{RESET}")
        print(f"{CYAN}SARA BENSALEM 1:5 CUSTOM JOINERY & MILLWORK ENGINE{RESET}")
        print(f"Plate Generated : {out}")
        print(f"Shadow Reveal   : {meta['shadow_reveal_mm']} mm | Carcase: {meta['carcase_mm']} mm | Leaf: {meta['door_leaf_mm']} mm")
        print(f"Hardware Spec   : {meta['hardware'][:60]}...")
        if is_compliant:
            print(f"{GREEN}[PASS] Tectonic Integrity Verified: Shadow reveal >= 3.0mm avoids door binding.{RESET}")
        else:
            print(f"{RED}[FAIL] Tectonic Violation: Shadow reveal {meta['shadow_reveal_mm']}mm < 3.0mm (Zero-Reveal Millwork Antipattern).{RESET}")
        print(f"{CYAN}{'=' * 72}{RESET}")

    sys.exit(0 if is_compliant else 1)

if __name__ == "__main__":
    main()

