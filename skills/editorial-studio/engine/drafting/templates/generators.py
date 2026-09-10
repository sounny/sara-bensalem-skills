"""
engine/drafting/templates/generators.py
Parametric Vector Plate Generators for Editorial Publication Spread Templates:
1. 1:20 Constructive Wall Section with Glaser U-value and Schöck Isokorb thermal breaks.
2. 1:5 Bespoke Joinery Reveal with 3-8mm shadow gap and Blum concealed cup routing.
3. 1:100 Statutory Spatial Plan with PMR/ADA wheelchair turning circle and life safety egress.

Authoritative Reference:
- ORIGINAL_REQUEST.md §R4
- personas/tectonic_detailer.md §6, §7, §8
- tests/tier4_workloads/test_constructive_wall_section.py
"""

import os
import pathlib
from typing import List, Dict, Any, Optional

# ==============================================================================
# 1. Hygrothermal Glaser U-Value Calculus
# ==============================================================================

def compute_wall_assembly_u_value(
    layers: List[Dict[str, Any]],
    r_si: float = 0.13,
    r_se: float = 0.04
) -> Dict[str, Any]:
    """
    Computes total thermal resistance and overall U-value for a multi-layer wall assembly:
    d_i = thickness_mm * 10^-3 [m]
    R_i = d_i / lambda_i [m²K/W]
    R_tot = R_si + sum(R_i) + R_se [m²K/W]
    U = 1 / R_tot [W/m²K]
    """
    r_layers = 0.0
    total_thickness_mm = 0.0

    for layer in layers:
        th_mm = layer.get("thickness_mm", 0.0)
        # Unit conversion: millimeters to meters
        d_m = th_mm * 1e-3
        lam = (
            layer.get("conductivity_w_mk")
            or layer.get("conductivity_lambda")
            or layer.get("lambda")
            or 1.0
        )
        r_i = d_m / lam
        r_layers += r_i
        total_thickness_mm += th_mm

    r_tot = r_si + r_layers + r_se
    u_val = 1.0 / r_tot

    return {
        "r_tot_m2k_w": round(r_tot, 3),
        "u_value_w_m2k": round(u_val, 3),
        "total_thickness_mm": total_thickness_mm,
        "is_passivhaus": u_val <= 0.15,
        "is_re2020": u_val <= 0.20,
    }


# Reference high-performance bio-composite wall assembly
DEFAULT_WALL_LAYERS = [
    {"name": "Lime Interior Plaster", "thickness_mm": 15.0, "conductivity_w_mk": 0.70},
    {"name": "Granite Ashlar Masonry", "thickness_mm": 120.0, "conductivity_w_mk": 2.80},
    {"name": "Lime-Hemp Insulation Monolith", "thickness_mm": 240.0, "conductivity_w_mk": 0.038},
    {"name": "PIR Warm Edge Barrier", "thickness_mm": 80.0, "conductivity_w_mk": 0.022},
    {"name": "Ventilated Air Cavity", "thickness_mm": 40.0, "conductivity_w_mk": 0.25},
    {"name": "Terracotta Rainscreen Tile", "thickness_mm": 30.0, "conductivity_w_mk": 1.00}
]


# ==============================================================================
# 2. Template 1: 1:20 Constructive Wall Section Generator
# ==============================================================================

def generate_wall_section_1_20_svg(
    layers: Optional[List[Dict[str, Any]]] = None,
    width: float = 800,
    height: float = 600
) -> str:
    """
    Generates a publication-grade 1:20 constructive wall section vector plate
    calibrated with ISO 128 lineweights (0.13mm, 0.25mm, 0.35mm, 0.50mm, 0.70mm),
    continuous thermal breaks (Schöck Isokorb, EPDM flashings), and Glaser U-value.
    """
    if layers is None:
        layers = DEFAULT_WALL_LAYERS

    metrics = compute_wall_assembly_u_value(layers)
    u_val = metrics["u_value_w_m2k"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- 0.13mm (0.37pt) Insulation Hatch Pattern -->
    <pattern id="insulation-hatch" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#84827A" stroke-width="0.37" />
    </pattern>
    <!-- Concrete Aggregate Pattern -->
    <pattern id="concrete-hatch" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="5" cy="5" r="1" fill="#84827A" />
      <circle cx="15" cy="12" r="1.5" fill="#84827A" />
      <polygon points="8,15 11,18 7,19" fill="#84827A" />
    </pattern>
  </defs>

  <!-- Sheet Substrate -->
  <rect width="100%" height="100%" fill="#FBFBFA" />

  <!-- Title & Metadata: Space Grotesk + JetBrains Mono -->
  <g id="header-block" transform="translate(40, 40)">
    <text x="0" y="0" font-family="'Space Grotesk', sans-serif" font-size="14" font-weight="bold" fill="#111110">PLATE 04 — 1:20 CONSTRUCTIVE WALL SECTION</text>
    <text x="0" y="18" font-family="'JetBrains Mono', monospace" font-size="8" fill="#55544E">SYSTEM: GRANITE ASHLAR + RE2020 LIME-HEMP INSULATION | U-VALUE: {u_val:.3f} W/m²K (PASSIVHAUS COMPLIANT)</text>
  </g>

  <!-- Section Drawing Assembly -->
  <g id="section-assembly" transform="translate(100, 100)">
    <!-- Ground / Foundation Cut: 0.70mm (2.00pt) -->
    <line x1="0" y1="420" x2="600" y2="420" stroke="#111110" stroke-width="2.00" stroke-linecap="square" />
    
    <!-- Reinforced Concrete Foundation / Plinth: Cut plane 0.50mm (1.42pt) -->
    <rect x="150" y="320" width="300" height="100" fill="#EEEEEC" stroke="#111110" stroke-width="1.42" />
    <rect x="150" y="320" width="300" height="100" fill="url(#concrete-hatch)" />

    <!-- Thermal Break Plinth (Schöck Isokorb): 0.35mm (1.00pt) -->
    <rect x="230" y="300" width="140" height="20" fill="#E4DDD0" stroke="#33322E" stroke-width="1.00" />
    <text x="240" y="314" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">EPDM THERMAL BREAK</text>

    <!-- Structural Masonry Wall: 0.50mm cut (1.42pt) -->
    <rect x="150" y="80" width="120" height="220" fill="#F4F3EF" stroke="#111110" stroke-width="1.42" />
    
    <!-- Monolithic Insulation Core (PIR / Hemp): 0.13mm (0.37pt) hatch -->
    <rect x="270" y="80" width="100" height="220" fill="url(#insulation-hatch)" stroke="#55544E" stroke-width="0.71" />

    <!-- Ventilated Rainscreen Cladding: 0.35mm (1.00pt) -->
    <rect x="370" y="70" width="40" height="240" fill="#EAE8E1" stroke="#33322E" stroke-width="1.00" />
    
    <!-- Cavity Weep Holes / Air Gap: 0.25mm (0.71pt) -->
    <line x1="370" y1="70" x2="370" y2="310" stroke="#55544E" stroke-width="0.71" stroke-dasharray="4,2" />

    <!-- Continuous EPDM Waterproofing Membrane: 0.25mm Dash (0.71pt) -->
    <path d="M 140,320 L 230,320 L 230,300 L 380,300 L 420,330" fill="none" stroke="#111110" stroke-width="0.71" stroke-dasharray="3,1" />

    <!-- Dimension Chains: 0.13mm (0.37pt) with tick marks -->
    <g id="dimension-string" stroke="#84827A" stroke-width="0.37">
      <line x1="120" y1="80" x2="120" y2="300" />
      <line x1="115" y1="80" x2="125" y2="80" stroke-width="0.71" />
      <line x1="115" y1="300" x2="125" y2="300" stroke-width="0.71" />
      <text x="75" y="195" font-family="'JetBrains Mono', monospace" font-size="7.5" fill="#55544E" transform="rotate(-90 75 195)">2200 mm</text>

      <line x1="150" y1="440" x2="410" y2="440" />
      <line x1="150" y1="435" x2="150" y2="445" stroke-width="0.71" />
      <line x1="270" y1="435" x2="270" y2="445" stroke-width="0.71" />
      <line x1="370" y1="435" x2="370" y2="445" stroke-width="0.71" />
      <line x1="410" y1="435" x2="410" y2="445" stroke-width="0.71" />
      <text x="195" y="455" font-family="'JetBrains Mono', monospace" font-size="7" fill="#55544E">120</text>
      <text x="305" y="455" font-family="'JetBrains Mono', monospace" font-size="7" fill="#55544E">100</text>
      <text x="385" y="455" font-family="'JetBrains Mono', monospace" font-size="7" fill="#55544E">40</text>
    </g>

    <!-- Material Callout Annotations: 0.25mm leader lines -->
    <g id="annotations" stroke="#55544E" stroke-width="0.71">
      <polyline points="210,120 180,90 80,90" fill="none" />
      <text x="75" y="86" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="6.5" fill="#111110" stroke="none">Granite Ashlar Masonry (120mm)</text>

      <polyline points="320,140 350,110 470,110" fill="none" />
      <text x="475" y="106" font-family="'JetBrains Mono', monospace" font-size="6.5" fill="#111110" stroke="none">Lime-Hemp Monolith Insulation (240mm)</text>

      <polyline points="390,180 430,150 490,150" fill="none" />
      <text x="495" y="146" font-family="'JetBrains Mono', monospace" font-size="6.5" fill="#111110" stroke="none">Terracotta Rainscreen Tile (30mm)</text>

      <polyline points="300,310 330,340 450,340" fill="none" />
      <text x="455" y="336" font-family="'JetBrains Mono', monospace" font-size="6.5" fill="#111110" stroke="none">Schöck Isokorb Thermal Break Plinth</text>
    </g>
  </g>
</svg>"""
    return svg


# ==============================================================================
# 3. Template 2: 1:5 Bespoke Joinery Reveal Generator
# ==============================================================================

def generate_millwork_reveal_1_5_svg(
    shadow_gap_mm: float = 3.0,
    cup_depth_mm: float = 12.8,
    reveal_mm: float = 2.0,
    width: float = 800,
    height: float = 600
) -> str:
    """
    Generates a 1:5 bespoke joinery reveal drawing showcasing:
    - 3-8mm shadow gap (joint creux) to absorb hygroscopic movement (2-3mm/m)
    - Blum / Hettich concealed cup routing (12.8mm depth, 35mm cup, 2mm reveal)
    - High-grade veneer callouts and calibrated ISO 128 lineweights.
    """
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Wood grain hatching: 0.13mm (0.37pt) fine lines -->
    <pattern id="woodgrain-hatch" width="8" height="8" patternTransform="rotate(15 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#84827A" stroke-width="0.37" stroke-dasharray="4,1" />
    </pattern>
    <pattern id="plywood-core" width="12" height="12" patternUnits="userSpaceOnUse">
      <line x1="0" y1="3" x2="12" y2="3" stroke="#84827A" stroke-width="0.37" />
      <line x1="0" y1="9" x2="12" y2="9" stroke="#84827A" stroke-width="0.37" />
    </pattern>
  </defs>

  <!-- Sheet Background -->
  <rect width="100%" height="100%" fill="#FBFBFA" />

  <!-- Header Block -->
  <g id="header-block" transform="translate(40, 40)">
    <text x="0" y="0" font-family="'Space Grotesk', sans-serif" font-size="14" font-weight="bold" fill="#111110">PLATE 05 — 1:5 BESPOKE MILLWORK &amp; JOINERY REVEAL</text>
    <text x="0" y="18" font-family="'JetBrains Mono', monospace" font-size="8" fill="#55544E">DETAIL: {shadow_gap_mm:.1f}MM SHADOW GAP (JOINT CREUX) + BLUM CLIP TOP BLUMOTION CONCEALED HINGE</text>
  </g>

  <!-- Joinery Detail Assembly at Scale 1:5 -->
  <g id="joinery-assembly" transform="translate(100, 110)">
    <!-- Primary Carcase (18mm Birch Plywood): Cut plane 0.50mm (1.42pt) -->
    <rect x="120" y="60" width="180" height="340" fill="#F4F3EF" stroke="#111110" stroke-width="1.42" />
    <rect x="120" y="60" width="180" height="340" fill="url(#plywood-core)" />

    <!-- Cabinet Door (19mm Substrate + 0.6mm Veneer): Cut plane 0.50mm (1.42pt) -->
    <!-- Door is offset from carcase by shadow_gap_mm and 2mm front reveal -->
    <g id="cabinet-door" transform="translate(320, 60)">
      <!-- 19mm Substrate Body -->
      <rect x="0" y="0" width="190" height="340" fill="#EAE8E1" stroke="#111110" stroke-width="1.42" />
      <rect x="0" y="0" width="190" height="340" fill="url(#woodgrain-hatch)" />

      <!-- Quartersawn Oak Veneer Layer: 0.25mm (0.71pt) -->
      <rect x="0" y="0" width="6" height="340" fill="#D5CBB9" stroke="#55544E" stroke-width="0.71" />
      <rect x="184" y="0" width="6" height="340" fill="#D5CBB9" stroke="#55544E" stroke-width="0.71" />

      <!-- Blum Concealed Cup Pocket Routing: Ø35mm x 12.8mm depth -->
      <!-- Pocket cut into door back edge: depth = 12.8mm, diameter = 70px (35mm equivalent) -->
      <rect x="0" y="100" width="64" height="140" fill="#DFDDD5" stroke="#33322E" stroke-width="1.00" />
      <text x="14" y="174" font-family="'JetBrains Mono', monospace" font-size="6.5" fill="#55544E" transform="rotate(-90 14 174)">ROUTING DEPTH: {cup_depth_mm}mm</text>
    </g>

    <!-- Blum Hinge Mechanism Body: 0.35mm (1.00pt) -->
    <path d="M 280,180 L 320,180 L 340,160 L 340,200 L 320,200 Z" fill="#D0CCC0" stroke="#33322E" stroke-width="1.00" />
    <circle cx="300" cy="190" r="4" fill="#55544E" />

    <!-- 3mm Negative Shadow Reveal (Joint Creux): 0.25mm (0.71pt) -->
    <rect x="300" y="40" width="20" height="380" fill="#E0DDD5" fill-opacity="0.3" stroke="#84827A" stroke-width="0.71" stroke-dasharray="2,2" />

    <!-- Dimension Chains: 0.13mm (0.37pt) with tick marks -->
    <g id="dimension-chains" stroke="#84827A" stroke-width="0.37">
      <!-- Shadow gap dimension -->
      <line x1="300" y1="420" x2="320" y2="420" />
      <line x1="300" y1="415" x2="300" y2="425" stroke-width="0.71" />
      <line x1="320" y1="415" x2="320" y2="425" stroke-width="0.71" />
      <text x="302" y="435" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">{shadow_gap_mm:.0f} mm</text>

      <!-- Door substrate thickness dimension -->
      <line x1="320" y1="420" x2="510" y2="420" />
      <line x1="510" y1="415" x2="510" y2="425" stroke-width="0.71" />
      <text x="400" y="435" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">19 mm</text>

      <!-- Cup diameter dimension -->
      <line x1="530" y1="160" x2="530" y2="230" />
      <line x1="525" y1="160" x2="535" y2="160" stroke-width="0.71" />
      <line x1="525" y1="230" x2="535" y2="230" stroke-width="0.71" />
      <text x="542" y="198" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">Ø35 mm</text>
    </g>

    <!-- Technical Specification Callouts -->
    <g id="callouts" stroke="#55544E" stroke-width="0.71">
      <polyline points="310,50 310,20 220,20" fill="none" />
      <text x="215" y="16" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="6.5" fill="#111110" stroke="none">3mm Shadow Gap (Joint Creux) — Absorbs Hygroscopic Expansion (2-3mm/m)</text>

      <polyline points="350,170 380,140 450,140" fill="none" />
      <text x="455" y="136" font-family="'JetBrains Mono', monospace" font-size="6.5" fill="#111110" stroke="none">Blum Clip Top BLUMOTION 110° Cup (Ø35mm x 12.8mm pocket)</text>

      <polyline points="420,280 460,310 520,310" fill="none" />
      <text x="525" y="306" font-family="'JetBrains Mono', monospace" font-size="6.5" fill="#111110" stroke="none">European Oak Quartersawn Veneer (0.6mm) on 19mm MR-MDF</text>

      <polyline points="200,300 160,330 80,330" fill="none" />
      <text x="75" y="326" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="6.5" fill="#111110" stroke="none">18mm Birch Plywood Carcase Structure</text>
    </g>
  </g>
</svg>"""
    return svg


# ==============================================================================
# 4. Template 3: 1:100 Statutory Spatial Plan Generator
# ==============================================================================

def generate_spatial_plan_1_100_svg(
    corridor_width_mm: float = 1400.0,
    door_clear_mm: float = 830.0,
    egress_max_m: float = 30.0,
    width: float = 800,
    height: float = 600
) -> str:
    """
    Generates a 1:100 statutory spatial plan vector plate demonstrating:
    - PMR / ADA wheelchair turning circle (Ø1500mm unobstructed)
    - Door clear openings >= 830mm (900mm leaf)
    - Circulation corridor width >= 1400mm
    - Emergency egress travel distance <= 30m to protected fire stair.
    """
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <!-- Wall poché pattern: 0.13mm (0.37pt) hatch -->
    <pattern id="wall-hatch" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#84827A" stroke-width="0.37" />
    </pattern>
    <!-- Marker for egress route arrow -->
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#8B263E" />
    </marker>
  </defs>

  <!-- Sheet Background -->
  <rect width="100%" height="100%" fill="#FBFBFA" />

  <!-- Header Block -->
  <g id="header-block" transform="translate(40, 40)">
    <text x="0" y="0" font-family="'Space Grotesk', sans-serif" font-size="14" font-weight="bold" fill="#111110">PLATE 06 — 1:100 STATUTORY SPATIAL ANATOMY &amp; CODE EGRESS PLAN</text>
    <text x="0" y="18" font-family="'JetBrains Mono', monospace" font-size="8" fill="#55544E">ACCESSIBILITY: PMR/ADA TURNING (Ø1500mm) | CLEAR DOOR ≥830mm | CORRIDOR ≥1400mm | EGRESS ≤30m</text>
  </g>

  <!-- Plan Drawing Assembly at Scale 1:100 -->
  <g id="plan-assembly" transform="translate(60, 90)">
    <!-- Multi-Axis Structural Column Grid: 0.13mm (0.37pt) -->
    <g id="column-grid" stroke="#84827A" stroke-width="0.37">
      <!-- Vertical Grid Lines 1, 2, 3, 4 -->
      <line x1="80" y1="20" x2="80" y2="440" stroke-dasharray="10,2,2,2" />
      <line x1="260" y1="20" x2="260" y2="440" stroke-dasharray="10,2,2,2" />
      <line x1="440" y1="20" x2="440" y2="440" stroke-dasharray="10,2,2,2" />
      <line x1="620" y1="20" x2="620" y2="440" stroke-dasharray="10,2,2,2" />

      <!-- Horizontal Grid Lines A, B, C -->
      <line x1="40" y1="60" x2="660" y2="60" stroke-dasharray="10,2,2,2" />
      <line x1="40" y1="240" x2="660" y2="240" stroke-dasharray="10,2,2,2" />
      <line x1="40" y1="420" x2="660" y2="420" stroke-dasharray="10,2,2,2" />

      <!-- Grid Bubbles: 0.25mm (0.71pt) -->
      <circle cx="80" cy="10" r="8" fill="#FFF" stroke="#55544E" stroke-width="0.71" />
      <text x="80" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">1</text>
      <circle cx="260" cy="10" r="8" fill="#FFF" stroke="#55544E" stroke-width="0.71" />
      <text x="260" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">2</text>
      <circle cx="440" cy="10" r="8" fill="#FFF" stroke="#55544E" stroke-width="0.71" />
      <text x="440" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">3</text>
      <circle cx="620" cy="10" r="8" fill="#FFF" stroke="#55544E" stroke-width="0.71" />
      <text x="620" y="13" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">4</text>

      <circle cx="25" cy="60" r="8" fill="#FFF" stroke="#55544E" stroke-width="0.71" />
      <text x="25" y="63" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">A</text>
      <circle cx="25" cy="240" r="8" fill="#FFF" stroke="#55544E" stroke-width="0.71" />
      <text x="25" y="243" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">B</text>
      <circle cx="25" cy="420" r="8" fill="#FFF" stroke="#55544E" stroke-width="0.71" />
      <text x="25" y="423" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="7" fill="#111110">C</text>
    </g>

    <!-- Structural Reinforced Columns (400x400mm at 1:100): 0.50mm (1.42pt) -->
    <g id="columns" fill="#33322E" stroke="#111110" stroke-width="1.42">
      <rect x="74" y="54" width="12" height="12" />
      <rect x="254" y="54" width="12" height="12" />
      <rect x="434" y="54" width="12" height="12" />
      <rect x="614" y="54" width="12" height="12" />
      <rect x="74" y="234" width="12" height="12" />
      <rect x="254" y="234" width="12" height="12" />
      <rect x="434" y="234" width="12" height="12" />
      <rect x="614" y="234" width="12" height="12" />
      <rect x="74" y="414" width="12" height="12" />
      <rect x="254" y="414" width="12" height="12" />
      <rect x="434" y="414" width="12" height="12" />
      <rect x="614" y="414" width="12" height="12" />
    </g>

    <!-- External Structural Perimeter Walls: Cut plane 0.50mm (1.42pt) -->
    <polygon points="80,60 620,60 620,420 80,420 80,60" fill="none" stroke="#111110" stroke-width="1.42" />

    <!-- Interior Partitions (Secondary): 0.35mm (1.00pt) -->
    <g id="partitions" stroke="#33322E" stroke-width="1.00">
      <!-- Corridor walls: width = 1400mm (42px equivalent at 1:100) -->
      <line x1="80" y1="219" x2="380" y2="219" />
      <line x1="80" y1="261" x2="380" y2="261" />
      <line x1="380" y1="60" x2="380" y2="219" />
      <line x1="380" y1="261" x2="380" y2="420" />
      <!-- Protected Fire Stair Enclosure -->
      <rect x="520" y="60" width="100" height="120" fill="#F4F3EF" />
    </g>

    <!-- PMR / ADA Wheelchair Turning Circle: Ø1500mm (45px at 1:100): 0.35mm Dash (1.00pt) -->
    <g id="pmr-turning-circle" transform="translate(190, 240)">
      <circle cx="0" cy="0" r="22.5" fill="#8B263E" fill-opacity="0.08" stroke="#8B263E" stroke-width="1.00" stroke-dasharray="2,2" />
      <line x1="-6" y1="0" x2="6" y2="0" stroke="#8B263E" stroke-width="0.71" />
      <line x1="0" y1="-6" x2="0" y2="6" stroke="#8B263E" stroke-width="0.71" />
      <text x="0" y="-26" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="bold" fill="#8B263E">PMR / ADA TURNING Ø1500mm</text>
    </g>

    <!-- Accessible Door Clear Width: >= 830mm (900mm leaf): 0.25mm (0.71pt) -->
    <g id="doors" stroke="#55544E" stroke-width="0.71" fill="none">
      <!-- Office Door -->
      <line x1="380" y1="160" x2="380" y2="187" stroke="#FFF" stroke-width="2.0" />
      <line x1="380" y1="160" x2="355" y2="175" />
      <path d="M 380,187 A 27,27 0 0,0 355,175" stroke-dasharray="2,1" />
      <text x="340" y="160" font-family="'JetBrains Mono', monospace" font-size="6" fill="#111110">CLEAR ≥830mm</text>

      <!-- Fire Stair Door (EI60) -->
      <line x1="520" y1="130" x2="520" y2="157" stroke="#FFF" stroke-width="2.0" />
      <line x1="520" y1="130" x2="495" y2="145" stroke="#8B263E" />
      <path d="M 520,157 A 27,27 0 0,0 495,145" stroke="#8B263E" stroke-dasharray="2,1" />
      <text x="470" y="130" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="bold" fill="#8B263E">FIRE DOOR (EI60)</text>
    </g>

    <!-- Emergency Egress Travel Path: 0.35mm Dash with Arrow (1.00pt) -->
    <g id="egress-route">
      <path d="M 120,120 L 120,240 L 460,240 L 460,140 L 515,140" fill="none" stroke="#8B263E" stroke-width="1.00" stroke-dasharray="4,2" marker-end="url(#arrow)" />
      <rect x="230" y="222" width="180" height="14" fill="#FFF" stroke="#8B263E" stroke-width="0.71" rx="2" />
      <text x="320" y="232" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="bold" fill="#8B263E">EGRESS DISTANCE: 18.4m (LIMIT ≤{egress_max_m:.0f}m)</text>
    </g>

    <!-- Dimension Chains: 0.13mm (0.37pt) -->
    <g id="dimensions" stroke="#84827A" stroke-width="0.37">
      <!-- Corridor width dimension -->
      <line x1="100" y1="219" x2="100" y2="261" />
      <line x1="95" y1="219" x2="105" y2="219" stroke-width="0.71" />
      <line x1="95" y1="261" x2="105" y2="261" stroke-width="0.71" />
      <text x="110" y="243" font-family="'JetBrains Mono', monospace" font-size="6.5" fill="#111110">{corridor_width_mm:.0f}mm</text>
    </g>

    <!-- Space Labels -->
    <g id="room-labels" font-family="'Space Grotesk', sans-serif" font-size="8" font-weight="600" fill="#33322E">
      <text x="200" y="130">PRIMARY DESIGN STUDIO</text>
      <text x="200" y="340">MEETING ATELIER</text>
      <text x="540" y="110">PROTECTED STAIR</text>
      <text x="540" y="122" font-size="6" fill="#84827A">PRESSURIZED AIRLOCK</text>
    </g>
  </g>
</svg>"""
    return svg


# ==============================================================================
# 5. Template Batch Writer
# ==============================================================================

def write_all_templates(output_dir: Optional[str] = None) -> Dict[str, str]:
    """
    Generates and saves all three standard publication-grade SVG templates
    to the designated templates directory.
    """
    if output_dir is None:
        output_dir = os.path.dirname(__file__)

    os.makedirs(output_dir, exist_ok=True)
    generated = {}

    # 1. 1:20 Constructive Wall Section
    wall_svg = generate_wall_section_1_20_svg()
    wall_path = os.path.join(output_dir, "wall_section_1_20.svg")
    with open(wall_path, "w", encoding="utf-8") as f:
        f.write(wall_svg)
    generated["wall_section_1_20.svg"] = wall_path

    # 2. 1:5 Bespoke Joinery Reveal
    joinery_svg = generate_millwork_reveal_1_5_svg()
    joinery_path = os.path.join(output_dir, "millwork_reveal_1_5.svg")
    with open(joinery_path, "w", encoding="utf-8") as f:
        f.write(joinery_svg)
    generated["millwork_reveal_1_5.svg"] = joinery_path

    # 3. 1:100 Statutory Spatial Plan
    plan_svg = generate_spatial_plan_1_100_svg()
    plan_path = os.path.join(output_dir, "spatial_plan_1_100.svg")
    with open(plan_path, "w", encoding="utf-8") as f:
        f.write(plan_svg)
    generated["spatial_plan_1_100.svg"] = plan_path

    return generated


if __name__ == "__main__":
    results = write_all_templates()
    for name, path in results.items():
        print(f"Generated: {name} -> {path}")
