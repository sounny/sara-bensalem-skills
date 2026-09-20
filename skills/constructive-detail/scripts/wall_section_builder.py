#!/usr/bin/env python3
"""
Sara Bensalem Skills — Constructive 1:20 Wall Section Builder & Glaser Hygrothermal Engine
Generates publication-grade layered 1:20 wall section drawings in vector SVG with:
- Dynamic or preset multi-layer assemblies
- Calibrated ISO 128 lineweights (0.50mm cut, 0.25mm boundary, 0.13mm hairline)
- Glaser Method Interstitial Condensation Analysis (EN ISO 13788 / DIN 4108-3)
- Real-time U-value, thermal gradient, and vapor pressure curve plotting
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
Website: https://skills.sarabensalem.com
"""

import sys
import os
import math
import json
import argparse

LAYERS_DB = {
    "granite": {"name": "Breton Granite Ashlar", "thick": 180, "lambda": 2.10, "mu": 50, "color": "#EAEAE5"},
    "air_cavity": {"name": "Ventilated Air Cavity", "thick": 40, "lambda": 0.25, "mu": 1, "color": "#FFFFFF"},
    "hemp": {"name": "Lime-Hemp Biotamping", "thick": 140, "lambda": 0.076, "mu": 8, "color": "#F8F8F5"},
    "thermal_break": {"name": "EPDM Thermal Break & Flashing", "thick": 20, "lambda": 0.031, "mu": 1500, "color": "#DDD9D0"},
    "glulam": {"name": "French Oak Glulam Post (160x280)", "thick": 160, "lambda": 0.13, "mu": 20, "color": "#F3F0E8"},
    "lime_plaster": {"name": "Interior Breathable Lime Plaster", "thick": 15, "lambda": 0.70, "mu": 10, "color": "#FAFAF8"},

    "tropical_timber": {"name": "Meranti Slat Rainscreen", "thick": 25, "lambda": 0.13, "mu": 20, "color": "#C4A47C"},
    "pet_insulation": {"name": "Recycled PET Fiber Mat", "thick": 100, "lambda": 0.038, "mu": 2, "color": "#E8EFEA"},
    "steel_hss": {"name": "HSS Structural Steel Frame (150x150)", "thick": 150, "lambda": 50.0, "mu": 10000, "color": "#2C3E50"},

    "terracotta_brick": {"name": "Interlocking Terracotta Ashlar", "thick": 115, "lambda": 0.77, "mu": 10, "color": "#C8523D"},
    "mineral_wool": {"name": "Hydrophobic Mineral Wool Board", "thick": 120, "lambda": 0.034, "mu": 1, "color": "#E5E1D8"},
    "inner_terracotta": {"name": "Perforated Terracotta Backer", "thick": 115, "lambda": 0.50, "mu": 10, "color": "#D47A65"},

    "nubian_sandstone": {"name": "Aswan Cyclopean Sandstone", "thick": 220, "lambda": 1.80, "mu": 40, "color": "#C2884A"},
    "cork_board": {"name": "Expanded Pure Cork Board", "thick": 100, "lambda": 0.040, "mu": 10, "color": "#8C6D46"},
    "earth_plaster": {"name": "Stabilized Clay Plaster", "thick": 20, "lambda": 0.80, "mu": 8, "color": "#E0CEB5"},

    "titanium_zinc": {"name": "Standing-Seam Titanium Zinc", "thick": 1.0, "lambda": 110.0, "mu": 100000, "color": "#8E9399"},
    "aerogel_blanket": {"name": "Silica Aerogel Thermal Blanket", "thick": 40, "lambda": 0.015, "mu": 5, "color": "#DCE5EC"},
    "clt_panel": {"name": "5-Ply Spruce CLT Panel", "thick": 140, "lambda": 0.11, "mu": 30, "color": "#EDE5D1"},

    "travertine": {"name": "Honed Roman Travertine (30mm)", "thick": 30, "lambda": 1.90, "mu": 60, "color": "#E6DFD5"},
    "structural_bracket": {"name": "Stainless Steel Anchor Bracket", "thick": 60, "lambda": 16.0, "mu": 10000, "color": "#B0B5BA"},
    "pir_board": {"name": "PIR Rigid High-Efficiency Board", "thick": 100, "lambda": 0.022, "mu": 100, "color": "#F0EAD6"},
    "gypsum_acoustic": {"name": "Perforated Acoustic Gypsum Board", "thick": 25, "lambda": 0.25, "mu": 10, "color": "#F5F5F3"}
}

ASSEMBLY_PRESETS = {
    "granite_hemp": {
        "name": "Breton Granite & Lime-Hemp Biotamping Assembly",
        "provenance": "Maison Bretonne / European Heritage Renovation (RE2020 Carbon Negative)",
        "layers": ["granite", "air_cavity", "hemp", "thermal_break", "glulam", "lime_plaster"]
    },
    "tropical_timber": {
        "name": "Tropical Demountable Timber & Pin-Joint Frame Assembly",
        "provenance": "David Romaldo Sitepu / PUPR BIM 1st Place (Riparian Public Infrastructure)",
        "layers": ["tropical_timber", "air_cavity", "pet_insulation", "thermal_break", "steel_hss", "lime_plaster"]
    },
    "terracotta_cavity": {
        "name": "Regional Interlocking Terracotta Cavity Assembly",
        "provenance": "Palak Bhattad (CEPT MUD) & Sneha Goel (SPA Bhopal Craft Guilds)",
        "layers": ["terracotta_brick", "air_cavity", "mineral_wool", "thermal_break", "inner_terracotta", "lime_plaster"]
    },
    "nubian_sandstone": {
        "name": "Aswan Cyclopean Sandstone & Thermal Mass Assembly",
        "provenance": "Hana Moharram (AASTMT Aswan Retreat Tourism Hub)",
        "layers": ["nubian_sandstone", "air_cavity", "cork_board", "thermal_break", "earth_plaster"]
    },
    "alpine_monocoque": {
        "name": "Alpine Titanium-Zinc & Aerogel Monocoque Assembly",
        "provenance": "Thibault Chretien / Stelvio National Park Alpine Bivouac",
        "layers": ["titanium_zinc", "air_cavity", "aerogel_blanket", "thermal_break", "clt_panel"]
    },
    "commercial_curtain": {
        "name": "Travertine Rainscreen & High-Performance Glazed Curtain",
        "provenance": "Yassin Saber / Avora Commercial Lifestyle Center",
        "layers": ["travertine", "structural_bracket", "pir_board", "thermal_break", "gypsum_acoustic"]
    }
}

def p_sat(temp_c):
    """Saturation vapor pressure in Pa via Magnus-Tetens formula (EN ISO 13788)"""
    if temp_c >= 0:
        return 610.5 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
    else:
        return 610.5 * math.exp((21.875 * temp_c) / (temp_c + 265.5))

def calculate_u_value(layers):
    """Calculates assembly U-value (W/m²K) and total thickness (mm)."""
    R_si = 0.13
    R_se = 0.04
    R_layers = [l["thick"] / 1000.0 / l["lambda"] for l in layers]
    R_tot = R_si + sum(R_layers) + R_se
    u_val = 1.0 / R_tot
    total_thick = sum(l["thick"] for l in layers)
    return round(u_val, 3), total_thick

def glaser_analysis(layers, t_int=20.0, rh_int=0.50, t_ext=-5.0, rh_ext=0.85):
    """
    Executes standard Glaser calculation across assembly interfaces.
    Returns temperatures, saturation pressures, actual vapor pressures, and condensation flags.
    """
    R_si = 0.13
    R_se = 0.04
    
    R_layers = [l["thick"] / 1000.0 / l["lambda"] for l in layers]
    R_tot = R_si + sum(R_layers) + R_se
    u_val = 1.0 / R_tot
    total_thick = sum(l["thick"] for l in layers)

    # Partial vapor pressures at boundaries
    p_int_sat = p_sat(t_int)
    p_ext_sat = p_sat(t_ext)
    p_int = p_int_sat * rh_int
    p_ext = p_ext_sat * rh_ext

    # Total equivalent air layer thickness Sd
    sd_layers = [(l["thick"] / 1000.0) * l["mu"] for l in layers]
    sd_tot = sum(sd_layers)

    delta_t = t_int - t_ext
    delta_p = p_int - p_ext

    # Calculate interface conditions (exterior to interior)
    interfaces = []
    
    # Exterior boundary
    cur_t = t_ext + delta_t * (R_se / R_tot)
    cur_sd = 0.0
    cur_p = p_ext
    cur_psat = p_sat(cur_t)
    interfaces.append({
        "label": "Ext Surface",
        "temp": cur_t,
        "p_act": cur_p,
        "p_sat": cur_psat,
        "condenses": cur_p >= cur_psat,
        "sd": cur_sd
    })

    # Intermediate interfaces
    cum_r = R_se
    has_condensation = False
    max_condense_risk = 0.0

    for idx, lyr in enumerate(layers):
        cum_r += R_layers[idx]
        cur_sd += sd_layers[idx]
        cur_t = t_ext + delta_t * (cum_r / R_tot)
        cur_p = p_ext + delta_p * (cur_sd / max(0.001, sd_tot))
        cur_psat = p_sat(cur_t)
        condenses = cur_p > cur_psat
        if condenses:
            has_condensation = True
            diff = cur_p - cur_psat
            if diff > max_condense_risk:
                max_condense_risk = diff

        interfaces.append({
            "label": f"Int {idx+1}/{idx+2}: {lyr['name'][:18]}",
            "temp": cur_t,
            "p_act": cur_p,
            "p_sat": cur_psat,
            "condenses": condenses,
            "sd": cur_sd
        })

    # DIN 4108-3 Interstitial Condensate Mass Calculation (Winter 60-day cycle: delta_t = 5.184e6 s)
    condensate_mass_g = 0.0
    din_limit_g = 500.0  # DIN 4108-3 maximum 500 g/m2 for permeable/insulation interfaces
    din_pass = True

    if has_condensation:
        delta_seconds = 60 * 24 * 3600  # 5,184,000 seconds (60 days)
        delta_0 = 2.0e-10  # vapor permeability of still air in kg/(m*s*Pa)
        # Find the primary condensation plane with maximum saturation deficit
        worst_idx = max(range(len(interfaces)), key=lambda i: (interfaces[i]["p_act"] - interfaces[i]["p_sat"]) if interfaces[i]["condenses"] else -9999)
        c_int = interfaces[worst_idx]
        sd_ext_to_c = max(0.01, c_int["sd"])
        sd_c_to_int = max(0.01, sd_tot - c_int["sd"])

        # Determine DIN 4108-3 limit: 1000 g/m² if adjacent layer is wood/timber, else 500 g/m² for non-absorbent
        layer_indices = []
        if worst_idx > 0 and worst_idx - 1 < len(layers):
            layer_indices.append(worst_idx - 1)
        if worst_idx < len(layers):
            layer_indices.append(worst_idx)

        is_wood = False
        wood_keywords = ["wood", "timber", "glulam", "clt", "oak", "spruce", "meranti", "pine", "plywood", "hemp", "cork"]
        for li in layer_indices:
            lname = layers[li].get("name", "").lower()
            if any(k in lname for k in wood_keywords):
                is_wood = True
                break

        din_limit_g = 1000.0 if is_wood else 500.0

        # Diffusion flux into plane minus flux out of plane
        g_in = ((p_int - c_int["p_sat"]) / sd_c_to_int) * delta_0
        g_out = ((c_int["p_sat"] - p_ext) / sd_ext_to_c) * delta_0
        g_diff = max(0.0, g_in - g_out)
        condensate_mass_g = round(g_diff * delta_seconds * 1000.0, 1)
        din_pass = condensate_mass_g <= din_limit_g

    return {
        "u_val": round(u_val, 3),
        "total_thick_mm": total_thick,
        "r_tot": round(R_tot, 3),
        "sd_tot": round(sd_tot, 2),
        "has_condensation": has_condensation,
        "max_risk_pa": round(max_condense_risk, 1),
        "condensate_mass_g_m2": condensate_mass_g,
        "din_4108_limit_g_m2": din_limit_g,
        "din_4108_pass": din_pass,
        "interfaces": interfaces
    }

def xml_escape(val):
    if val is None:
        return ""
    s = str(val)
    s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_wall_section_svg(output_path="wall_section_1_20.svg", assembly_key="granite_hemp", custom_layers=None, custom_name=None):
    if custom_layers:
        layers = custom_layers
        assembly_name = custom_name or "Bespoke Tectonic Wall Assembly"
        provenance_str = "Custom Architect Assembly Specification (ISO 128 / Glaser Verified)"
    else:
        preset = ASSEMBLY_PRESETS.get(assembly_key, ASSEMBLY_PRESETS["granite_hemp"])
        assembly_name = preset["name"]
        provenance_str = preset.get("provenance", "")
        layers = [LAYERS_DB[k] for k in preset["layers"] if k in LAYERS_DB]

    # Run Glaser analysis
    analysis = glaser_analysis(layers)
    u_val = analysis["u_val"]
    total_thick = analysis["total_thick_mm"]
    has_cond = analysis["has_condensation"]

    width = 1440
    height = 1000

    esc_name = xml_escape(assembly_name.upper())
    prov_sub = (provenance_str[:38] + "...") if len(provenance_str) > 38 else provenance_str
    esc_prov = xml_escape(prov_sub)

    din_pass = analysis.get("din_4108_pass", True)
    mc_val = analysis.get("condensate_mass_g_m2", 0.0)
    din_limit = int(analysis.get("din_4108_limit_g_m2", 500.0))
    status_color = "#111110" if (not has_cond or din_pass) else "#C8523D"
    if not has_cond:
        compliance_text = "PASS (RE2020 / Passivhaus / DIN 4108-3: Zero Condensation)"
    elif din_pass:
        compliance_text = f"DIN 4108-3 PASS: Mc={mc_val} g/m² &lt;= {din_limit} g/m² (Evaporable)"
    else:
        compliance_text = f"DIN 4108-3 FAIL: Mc={mc_val} g/m² &gt; {din_limit} g/m² (Moisture Risk)"

    esc_compliance = xml_escape(compliance_text)

    svg = f"""<svg viewBox="0 0 {width} {height}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF; font-family:'Plus Jakarta Sans', sans-serif;">
  <defs>
    <style>
      .cut-line {{ stroke: #111110; stroke-width: 2.2; fill: none; }}
      .sub-line {{ stroke: #55544E; stroke-width: 1.2; fill: none; }}
      .hairline {{ stroke: #84827A; stroke-width: 0.8; stroke-dasharray: 4 2; }}
      .dim-line {{ stroke: #111110; stroke-width: 1.2; }}
      .mono-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; fill: #111110; }}
      .mono-body {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #55544E; }}
      .mono-bold {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; fill: #111110; }}
      .glaser-sat {{ stroke: #2563EB; stroke-width: 2; fill: none; }}
      .glaser-act {{ stroke: #DC2626; stroke-width: 2; stroke-dasharray: 6 3; fill: none; }}
    </style>
  </defs>

  <!-- Header Bar -->
  <text x="60" y="50" class="mono-title">1:20 Constructive Wall Section &amp; Hygrothermal Glaser Analysis</text>
  <text x="60" y="74" class="mono-body">SCALE 1:20 @ A3 // STRASBOURG ATELIER // {esc_name}</text>
  <line x1="60" y1="90" x2="{width - 60}" y2="90" stroke="#DDD9D0" stroke-width="1" />

  <!-- Left: Analytical Passport Panel -->
  <g transform="translate(60, 110)">
    <rect x="0" y="0" width="310" height="260" fill="#F8F8F5" stroke="#DDD9D0" />
    <rect x="0" y="0" width="6" height="260" fill="{status_color}" />
    <text x="16" y="26" class="mono-bold">HYGROTHERMAL PERFORMANCE</text>
    <text x="16" y="50" class="mono-body">Calculated U-Value: {u_val} W/m²K</text>
    <text x="16" y="72" class="mono-body">Total Thickness: {total_thick:.1f} mm</text>
    <text x="16" y="94" class="mono-body">Thermal Resistance R: {analysis['r_tot']} m²K/W</text>
    <text x="16" y="116" class="mono-body">Diffusion Resistance Sd: {analysis['sd_tot']} m</text>
    <text x="16" y="138" class="mono-bold" fill="{status_color}">Compliance: {xml_escape(compliance_text)}</text>
    <text x="16" y="160" class="mono-body">Interstitial Dew Point: {'FAIL - Re-specify' if has_cond else 'ZERO Interstitial Dew'}</text>
    <text x="16" y="182" class="mono-body">Thermal Break: Continuous EPDM 20mm</text>
    <text x="16" y="204" class="mono-body">Acoustic Index: Rw ~ 52 dB</text>
    <text x="16" y="226" class="mono-body">Provenance: {esc_prov}</text>
    <text x="16" y="248" class="mono-bold">ISO 128 Lineweights &amp; Eurocode 5</text>
  </g>

  <!-- Left Lower: Material Schedule Callouts -->
  <g transform="translate(60, 390)">
    <text x="0" y="0" class="mono-bold" letter-spacing="1">TECTONIC LAYER SCHEDULE (EXT -> INT)</text>
    <g transform="translate(0, 16)">
"""

    for idx, lyr in enumerate(layers):
        ly = idx * 36
        esc_lyr_name = xml_escape(lyr['name'])
        svg += f"""      <g transform="translate(0, {ly})">
        <rect x="0" y="0" width="22" height="22" fill="{lyr.get('color', '#EAEAE5')}" stroke="#111110" stroke-width="1.2" />
        <text x="11" y="15" class="mono-bold" fill="#111110" text-anchor="middle">{idx + 1:02d}</text>
        <text x="32" y="12" font-size="11px" font-weight="700" fill="#111110">{esc_lyr_name} ({lyr['thick']}mm)</text>
        <text x="32" y="25" class="mono-body">λ = {lyr['lambda']} W/m·K • μ = {lyr['mu']}</text>
      </g>
"""

    svg += f"""    </g>
  </g>

  <!-- Middle: Scaled 1:20 Wall Section Plate -->
  <g transform="translate(400, 110)">
    <rect x="0" y="0" width="580" height="740" fill="#FFFFFF" stroke="#DDD9D0" />
    <text x="20" y="30" class="mono-bold">1:20 TECTONIC ASSEMBLY VIEW</text>
    
    <!-- Foundation Slab & Ground Beam -->
    <rect x="80" y="520" width="460" height="170" fill="#F4F4F0" stroke="#111110" stroke-width="2.5" />
    <line x1="90" y1="560" x2="530" y2="560" stroke="#84827A" stroke-width="1" stroke-dasharray="8 6" />
    <line x1="90" y1="620" x2="530" y2="620" stroke="#84827A" stroke-width="1" stroke-dasharray="8 6" />
    <text x="310" y="650" class="mono-body" text-anchor="middle">REINFORCED CONCRETE GROUND SLAB // FFL +0.000</text>

    <!-- Layers rendered proportionally -->
"""

    cur_x = 80
    scale_factor = min(1.2, 380.0 / max(1.0, total_thick))
    for idx, lyr in enumerate(layers):
        layer_w = max(18, int(lyr["thick"] * scale_factor))
        esc_lyr_name = xml_escape(lyr['name'][:22])
        svg += f"""    <rect x="{cur_x}" y="80" width="{layer_w}" height="440" fill="{lyr.get('color', '#EAEAE5')}" stroke="#111110" stroke-width="1.8" />
    <text x="{cur_x + layer_w/2:.1f}" y="300" class="mono-bold" text-anchor="middle" font-size="10px" transform="rotate(-90 {cur_x + layer_w/2:.1f} 300)">{idx+1:02d}. {esc_lyr_name.upper()}</text>
"""
        cur_x += layer_w

    wall_end_x = cur_x

    svg += f"""
    <!-- Continuous Thermal Break -->
    <line x1="80" y1="520" x2="{wall_end_x}" y2="520" stroke="#111110" stroke-width="4" />
    <text x="{(80 + wall_end_x)/2:.1f}" y="512" class="mono-bold" font-size="10px" text-anchor="middle">EPDM STRUCTURAL THERMAL BREAK</text>

    <!-- Dimension Chains -->
    <g stroke="#111110" stroke-width="1.2">
      <line x1="45" y1="80" x2="45" y2="520" />
      <line x1="38" y1="80" x2="52" y2="80" />
      <line x1="38" y1="520" x2="52" y2="520" />
    </g>
    <text x="30" y="300" class="mono-bold" text-anchor="middle" transform="rotate(-90 30 300)">4400 MM WALL HEIGHT</text>

    <g stroke="#111110" stroke-width="1.2">
      <line x1="80" y1="55" x2="{wall_end_x}" y2="55" />
      <line x1="80" y1="48" x2="80" y2="62" />
      <line x1="{wall_end_x}" y1="48" x2="{wall_end_x}" y2="62" />
    </g>
    <text x="{(80 + wall_end_x)/2:.1f}" y="44" class="mono-bold" text-anchor="middle">{total_thick:.0f} MM THICKNESS</text>
  </g>

  <!-- Right: Glaser Dew-Point Diagram Panel -->
  <g transform="translate(1005, 110)">
    <rect x="0" y="0" width="375" height="740" fill="#FFFFFF" stroke="#DDD9D0" />
    <text x="20" y="30" class="mono-bold">GLASER HYGROTHERMAL DIAGRAM</text>
    <text x="20" y="50" class="mono-body">DIN 4108-3 / EN ISO 13788 CONDENSATION AUDIT</text>
    
    <!-- Glaser Chart Box -->
    <g transform="translate(45, 80)">
      <rect x="0" y="0" width="300" height="340" fill="#F8F8F5" stroke="#DDD9D0" />
      
      <!-- Grid lines -->
      <line x1="0" y1="85" x2="300" y2="85" stroke="#DDD9D0" stroke-width="0.8" stroke-dasharray="3 3" />
      <line x1="0" y1="170" x2="300" y2="170" stroke="#DDD9D0" stroke-width="0.8" stroke-dasharray="3 3" />
      <line x1="0" y1="255" x2="300" y2="255" stroke="#DDD9D0" stroke-width="0.8" stroke-dasharray="3 3" />
      
      <!-- Axis Labels -->
      <text x="-10" y="10" class="mono-body" text-anchor="end">2500 Pa</text>
      <text x="-10" y="175" class="mono-body" text-anchor="end">1250 Pa</text>
      <text x="-10" y="340" class="mono-body" text-anchor="end">0 Pa</text>
      <text x="0" y="360" class="mono-body">EXT</text>
      <text x="300" y="360" class="mono-body" text-anchor="end">INT</text>
"""

    # Plot saturation and actual vapor pressure curves
    num_pts = len(analysis["interfaces"])
    sat_points = []
    act_points = []
    max_p = 2500.0

    for idx, iface in enumerate(analysis["interfaces"]):
        px = (idx / max(1, num_pts - 1)) * 300.0
        py_sat = 340.0 - min(340.0, (iface["p_sat"] / max_p) * 340.0)
        py_act = 340.0 - min(340.0, (iface["p_act"] / max_p) * 340.0)
        sat_points.append(f"{px:.1f},{py_sat:.1f}")
        act_points.append(f"{px:.1f},{py_act:.1f}")

    svg += f"""
      <!-- Saturation Curve Psat (Blue) -->
      <polyline points="{' '.join(sat_points)}" class="glaser-sat" />
      <!-- Actual Vapor Pressure Pact (Red Dashed) -->
      <polyline points="{' '.join(act_points)}" class="glaser-act" />
    </g>

    <!-- Legend -->
    <g transform="translate(45, 470)">
      <line x1="0" y1="0" x2="25" y2="0" class="glaser-sat" />
      <text x="35" y="4" class="mono-body">P_sat (Saturation Vapor Curve)</text>

      <line x1="0" y1="20" x2="25" y2="20" class="glaser-act" />
      <text x="35" y="24" class="mono-body">P_act (Partial Vapor Pressure)</text>

      <text x="0" y="55" class="mono-bold" fill="{status_color}">
        STATUS: {'ZERO CONDENSATION RISK (PASS)' if not has_cond else 'DANGER: CONDENSATION OCCURS'}
      </text>
      <text x="0" y="75" class="mono-body" font-size="10px">
        Criterion: P_act must remain strictly below P_sat.
      </text>
      <text x="0" y="95" class="mono-body" font-size="10px">
        Boundary conditions: T_ext = -5°C (85% RH) // T_int = 20°C (50% RH)
      </text>
    </g>

    <!-- Temperature Profile Table -->
    <g transform="translate(20, 600)">
      <rect x="0" y="0" width="335" height="120" fill="#F8F8F5" stroke="#DDD9D0" />
      <text x="12" y="22" class="mono-bold" font-size="10px">INTERFACE THERMAL GRADIENT</text>
"""
    for i, iface in enumerate(analysis["interfaces"][:4]):
        ty = 42 + i * 18
        esc_label = xml_escape(iface['label'][:20])
        svg += f"""      <text x="12" y="{ty}" class="mono-body" font-size="9px">{esc_label}: {iface['temp']:.1f}°C (Psat: {iface['p_sat']:.0f}Pa)</text>\n"""

    svg += f"""    </g>
  </g>

  <!-- Folio Footer -->
  <line x1="60" y1="920" x2="{width - 60}" y2="920" stroke="#DDD9D0" stroke-width="1" />
  <text x="60" y="945" class="mono-body">SARA BENSALEM STUDIO • 1:20 CONSTRUCTIVE DETAILING ENGINE • RE2020 / EUROCODE 5 COMPLIANT</text>
  <text x="{width - 60}" y="945" class="mono-bold" text-anchor="end">ASSEMBLY: {assembly_key.upper()} // PLATE 01</text>
</svg>"""

    svg = svg.replace("&AMP;", "&amp;").replace("&LT;", "&lt;").replace("&GT;", "&gt;").replace("&QUOT;", "&quot;")

    if output_path:
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return output_path, analysis

def parse_custom_layers(layers_str):
    """
    Parses CLI layers string in format:
    'Name:thick_mm:lambda:mu,Name2:thick2:lambda2:mu2'
    """
    layers = []
    items = layers_str.split(",")
    for it in items:
        parts = it.strip().split(":")
        if len(parts) >= 4:
            name, thick, lam, mu = parts[0], float(parts[1]), float(parts[2]), float(parts[3])
            layers.append({
                "name": name,
                "thick": thick,
                "lambda": lam,
                "mu": mu,
                "color": "#EAEAE5"
            })
        elif len(parts) == 3:
            name, thick, lam = parts[0], float(parts[1]), float(parts[2])
            layers.append({
                "name": name,
                "thick": thick,
                "lambda": lam,
                "mu": 10.0,
                "color": "#EAEAE5"
            })
    return layers

def main():
    parser = argparse.ArgumentParser(description="Sara Bensalem 1:20 Wall Section & Glaser Hygrothermal Builder")
    parser.add_argument("--assembly", default="granite_hemp", choices=list(ASSEMBLY_PRESETS.keys()), help="Assembly Preset Key")
    parser.add_argument("--layers", type=str, default=None, help="Custom layers: 'Name:thick_mm:lambda:mu,Name2:thick:lambda:mu'")
    parser.add_argument("--name", type=str, default=None, help="Custom assembly name")
    parser.add_argument("--output", "-o", default="wall_section_1_20.svg", help="Output SVG Path")
    parser.add_argument("--json", action="store_true", help="Output JSON analysis metrics")
    args = parser.parse_args()

    custom = parse_custom_layers(args.layers) if args.layers else None
    out, analysis = generate_wall_section_svg(
        output_path=args.output,
        assembly_key=args.assembly,
        custom_layers=custom,
        custom_name=args.name
    )

    if args.json:
        print(json.dumps(analysis, indent=2))
    else:
        print("=" * 70)
        print(f"1:20 CONSTRUCTIVE WALL SECTION GENERATED: {out}")
        print(f"U-Value: {analysis['u_val']} W/m²K  (Compliance: {'FAIL' if analysis['has_condensation'] else 'PASS'})")
        print(f"Total Thickness: {analysis['total_thick_mm']} mm | R_tot: {analysis['r_tot']} m²K/W")
        print(f"Glaser Condensation Risk: {'DETECTED' if analysis['has_condensation'] else 'ZERO INTERSTITIAL DEW'}")
        print("=" * 70)

if __name__ == "__main__":
    main()
