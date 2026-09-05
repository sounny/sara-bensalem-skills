#!/usr/bin/env python3
"""
Sara Bensalem Skills — Bioclimatic Flows & Solar Vector Engine (2026 Enhanced Edition)
Calculates seasonal solar altitude angles, optimal shading overhang depths,
natural thermal stack cross-ventilation buoyancy loops, and diurnal thermal mass damping.
Supports 5 empirical bioclimatic zones from premier international architectural practices.
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
Website: https://skills.sarabensalem.com
"""

import sys
import os
import math
import argparse
import json

CLIMATE_PRESETS = {
    "temperate_strasbourg": {
        "name": "Temperate Continental (Strasbourg / Paris)",
        "latitude": 48.58,
        "delta_t": 6.8,
        "chimney_height": 12.0,
        "thermal_diffusivity": 0.00000035,  # Hemp-lime
        "wall_thickness_m": 0.30,
        "summer_design_temp": 32.0,
        "comfort_zone": "Passive solar heating in winter; night purge ventilation in summer."
    },
    "mediterranean_alexandria": {
        "name": "Mediterranean Coastal (Alexandria / Avora Mall)",
        "latitude": 31.20,
        "delta_t": 7.5,
        "chimney_height": 14.0,
        "thermal_diffusivity": 0.00000045,  # Travertine / concrete
        "wall_thickness_m": 0.35,
        "summer_design_temp": 34.0,
        "comfort_zone": "Self-shading courtyards; sea breeze Venturi funneling; evaporative cooling."
    },
    "hot_arid_aswan": {
        "name": "Hot-Arid Nilotic / Desert (Aswan / Al-'Ula)",
        "latitude": 24.09,
        "delta_t": 11.5,
        "chimney_height": 16.0,
        "thermal_diffusivity": 0.00000060,  # Cyclopean sandstone
        "wall_thickness_m": 0.45,
        "summer_design_temp": 44.0,
        "comfort_zone": "High-inertia stone thermal mass; subterranean air ducts; deep recessed window reveals."
    },
    "composite_bhopal": {
        "name": "Composite Subtropical / Semi-Arid (Bhopal / Ahmedabad)",
        "latitude": 23.25,
        "delta_t": 9.2,
        "chimney_height": 10.0,
        "thermal_diffusivity": 0.00000040,  # Terracotta / brick
        "wall_thickness_m": 0.30,
        "summer_design_temp": 42.0,
        "comfort_zone": "Inverted vaulted roofs; Ladybug solar radiation tuning; porous terracotta jali screens."
    },
    "tropical_bandung": {
        "name": "Tropical Monsoonal High-Humidity (Bandung / Sumatra)",
        "latitude": -6.91,
        "delta_t": 4.5,
        "chimney_height": 9.0,
        "thermal_diffusivity": 0.00000025,  # Timber / bamboo
        "wall_thickness_m": 0.15,
        "summer_design_temp": 31.0,
        "comfort_zone": "Maximum open cross-ventilation; lightweight low-inertia envelope; stilt riparian elevation."
    }
}

def calculate_solar_altitude(latitude=48.58):
    """
    Calculates the solar altitude at solar noon for summer solstice, winter solstice, and equinox.
    Uses exact astronomical solar declination:
    - Summer Solstice: declination +23.45° for Northern Hemisphere, -23.45° for Southern Hemisphere.
    - Winter Solstice: declination -23.45° for Northern Hemisphere, +23.45° for Southern Hemisphere.
    - Equinox: declination 0.0°.
    Solar altitude at solar noon: altitude = 90.0° - |latitude - declination|.
    """
    if latitude >= 0:
        summer_dec = 23.45
        winter_dec = -23.45
    else:
        summer_dec = -23.45
        winter_dec = 23.45

    summer_alt = max(0.0, min(90.0, 90.0 - abs(latitude - summer_dec)))
    winter_alt = max(0.0, min(90.0, 90.0 - abs(latitude - winter_dec)))
    equinox_alt = max(0.0, min(90.0, 90.0 - abs(latitude)))
    return round(summer_alt, 1), round(winter_alt, 1), round(equinox_alt, 1)

def calculate_overhang_depth(window_height_m=2.4, summer_alt_deg=65.0):
    # Overhang depth D = H / tan(altitude)
    # When altitude approaches 90° (overhead tropical zenith sun), tan(alt) -> inf, D -> 0
    # For tropical/overhead sun (alt >= 80°), an overhang requires a minimum structural projection (0.8m - 1.5m)
    # to protect against direct vertical zenith and high-angle diffuse sky radiation.
    if summer_alt_deg >= 82.0:
        return 1.20
    rad = math.radians(summer_alt_deg)
    if math.tan(rad) > 0.05:
        d = window_height_m / math.tan(rad)
        return round(min(3.5, max(0.6, d)), 2)
    return 1.20

def calculate_stack_ventilation(chimney_height_m=12.0, delta_t_k=6.8, t_ambient_c=30.0):
    # v = Cd * sqrt(2 * g * H * (dT / Tavg))
    # Cd discharge coefficient typically 0.60
    g = 9.81
    c_d = 0.60
    t_avg_k = (t_ambient_c + 273.15) + (delta_t_k / 2.0)
    v = c_d * math.sqrt(2 * g * chimney_height_m * (delta_t_k / t_avg_k))
    # Airflow Q for 1.5 m² stack flue
    area = 1.5
    q = v * area
    return round(v, 2), round(q, 2)

def calculate_diurnal_thermal_lag(thickness_m=0.30, thermal_diffusivity=0.00000035):
    # Approximated diurnal phase lag in hours: phi = 1.38 * x * sqrt(Period / (pi * alpha))
    # Period = 86400 s
    period = 86400.0
    phi = 1.38 * thickness_m * math.sqrt(period / (math.pi * thermal_diffusivity)) / 3600.0
    return round(min(18.0, max(4.0, phi)), 1)

def xml_escape(val):
    if val is None:
        return ""
    return str(val).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_bioclimatic_svg(output_path="bioclimatic_flow_plate.svg", climate_key="temperate_strasbourg", custom_lat=None):
    preset = CLIMATE_PRESETS.get(climate_key, CLIMATE_PRESETS["temperate_strasbourg"])
    lat = custom_lat if custom_lat is not None else preset["latitude"]
    
    summer_alt, winter_alt, eq_alt = calculate_solar_altitude(lat)
    overhang = calculate_overhang_depth(2.4, summer_alt)
    stack_v, stack_q = calculate_stack_ventilation(preset["chimney_height"], preset["delta_t"])
    lag_hours = calculate_diurnal_thermal_lag(preset["wall_thickness_m"], preset["thermal_diffusivity"])

    # Geometry & Solar Vectors
    overhang_px = max(25, min(80, int(overhang * 32)))
    tip_x = 120 - overhang_px
    tip_y = 240

    # Summer ray (strikes overhang tip at summer_alt)
    rad_s = math.radians(max(15.0, min(85.0, summer_alt)))
    tan_s = math.tan(rad_s)
    x_s_sky = 20.0
    y_s_sky = tip_y - (tip_x - x_s_sky) * tan_s
    if y_s_sky < 30.0:
        y_s_sky = 30.0
        x_s_sky = tip_x - (tip_y - y_s_sky) / tan_s
    x_s_end = tip_x + 35.0
    y_s_end = tip_y + 35.0 * tan_s

    # Winter ray (low angle penetrates deep into interior floor at winter_alt)
    rad_w = math.radians(max(10.0, min(75.0, winter_alt)))
    tan_w = math.tan(rad_w)
    x_w_sky = 20.0
    y_w_sky = max(40.0, 340.0 - (120.0 - x_w_sky) * tan_w)
    y_w_floor = 570.0
    x_w_floor = min(500.0, 120.0 + (y_w_floor - 340.0) / tan_w)

    width = 1200
    height = 1000

    esc_zone_name = xml_escape(preset['name'].upper())
    esc_zone_short = xml_escape(preset['name'].split()[0])
    esc_comfort = xml_escape(preset['comfort_zone'][:42])
    lat_dir = "° N" if lat >= 0 else "° S"

    svg = f"""<svg viewBox="0 0 {width} {height}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="background:#FFFFFF; font-family:'Plus Jakarta Sans', sans-serif;">
  <defs>
    <style>
      .building-shell {{ fill: #F8F8F5; stroke: #111110; stroke-width: 2.5; }}
      .glazing-cut {{ stroke: #111110; stroke-width: 3; }}
      .solar-summer {{ stroke: #C8523D; stroke-width: 2.2; stroke-dasharray: 6 3; marker-end: url(#arrow-red); }}
      .solar-winter {{ stroke: #2B4C7E; stroke-width: 2.2; stroke-dasharray: 4 2; marker-end: url(#arrow-blue); }}
      .airflow-cool {{ stroke: #5A7D7C; stroke-width: 2.5; fill: none; stroke-linecap: round; marker-end: url(#arrow-green); }}
      .airflow-warm {{ stroke: #C8523D; stroke-width: 2.8; fill: none; stroke-linecap: round; marker-end: url(#arrow-red); }}
      .mono-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; fill: #111110; }}
      .mono-label {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; fill: #55544E; }}
      .mono-bold {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; fill: #111110; }}
    </style>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#C8523D" />
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2B4C7E" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#5A7D7C" />
    </marker>
  </defs>

  <!-- Header -->
  <text x="60" y="50" class="mono-title">Bioclimatic Vectors &amp; Thermodynamic Airflow Dynamics</text>
  <text x="60" y="74" class="mono-label">ZONE: {esc_zone_name} // LAT: {abs(lat):.2f}{lat_dir} // PASSIVE SOLAR GEOMETRY</text>
  <line x1="60" y1="90" x2="1140" y2="90" stroke="#DDD9D0" stroke-width="1" />

  <!-- Data Panel (Ladybug-Style Scientific Breakdown) -->
  <g transform="translate(60, 110)">
    <rect x="0" y="0" width="340" height="280" fill="#F8F8F5" stroke="#DDD9D0" />
    <rect x="0" y="0" width="6" height="280" fill="#111110" />
    <text x="16" y="24" class="mono-bold">SOLAR &amp; THERMODYNAMIC METRICS</text>
    <text x="16" y="48" class="mono-label">Latitude: {abs(lat):.2f}{lat_dir} ({esc_zone_short})</text>
    <text x="16" y="70" class="mono-bold">Summer Solstice Noon: {summer_alt}° Alt (Shaded)</text>
    <text x="16" y="92" class="mono-bold">Winter Solstice Noon: {winter_alt}° Alt (Penetrating)</text>
    <text x="16" y="114" class="mono-label">Equinox Noon Altitude: {eq_alt}° Alt</text>
    <text x="16" y="136" class="mono-bold">Optimal Brise-Soleil Overhang: {overhang} m</text>
    <text x="16" y="158" class="mono-label">Stack Flue Height: {preset['chimney_height']:.1f} m (ΔT: {preset['delta_t']} K)</text>
    <text x="16" y="180" class="mono-bold">Stack Velocity: {stack_v} m/s (Q: {stack_q} m³/s)</text>
    <text x="16" y="202" class="mono-bold">Thermal Mass Diurnal Lag: {lag_hours} Hours</text>
    <text x="16" y="224" class="mono-label">Summer Design Temp: {preset['summer_design_temp']}°C</text>
    <text x="16" y="246" font-size="10px" fill="#55544E">{esc_comfort}...</text>
  </g>

  <!-- Building Cross Section Viewport -->
  <g transform="translate(440, 110)">
    <rect x="0" y="0" width="700" height="740" fill="#FFFFFF" stroke="#DDD9D0" />

    <!-- Ground Line -->
    <line x1="40" y1="580" x2="660" y2="580" stroke="#111110" stroke-width="3" />
    <text x="50" y="605" class="mono-label">NATURAL GRADE LEVEL // GROUND PLANE</text>
    
    <!-- Building Mass Section -->
    <polygon points="120,580 120,240 320,160 320,80 380,80 380,160 560,160 560,580" class="building-shell" />
    
    <!-- Overhang Brise-Soleil at Glazing Edge -->
    <rect x="{tip_x}" y="240" width="{overhang_px}" height="12" fill="#111110" />
    <text x="{tip_x - 5}" y="232" class="mono-bold" text-anchor="end">D = {overhang}M OVERHANG</text>

    <!-- South Glazing Opening -->
    <line x1="120" y1="280" x2="120" y2="540" class="glazing-cut" />
    
    <!-- North High-Level Clerestory / Ventilation Louvers -->
    <line x1="560" y1="200" x2="560" y2="280" class="glazing-cut" />
    
    <!-- Solar Vector: Summer Solstice (High Angle - Cut by Overhang) -->
    <line x1="{x_s_sky:.1f}" y1="{y_s_sky:.1f}" x2="{x_s_end:.1f}" y2="{y_s_end:.1f}" class="solar-summer" />
    <text x="{max(30.0, (x_s_sky + tip_x)/2 - 10):.1f}" y="{max(40.0, (y_s_sky + tip_y)/2 - 8):.1f}" class="mono-bold" fill="#C8523D">SUMMER {summer_alt}° (BLOCKED)</text>

    <!-- Solar Vector: Winter Solstice (Low Angle - Enters Deep Interior) -->
    <line x1="{x_w_sky:.1f}" y1="{y_w_sky:.1f}" x2="{x_w_floor:.1f}" y2="{y_w_floor:.1f}" class="solar-winter" />
    <text x="{(x_w_sky + x_w_floor)/2 - 40:.1f}" y="{(y_w_sky + y_w_floor)/2 - 15:.1f}" class="mono-bold" fill="#2B4C7E">WINTER {winter_alt}° (PASSIVE HEATING)</text>

    <!-- Airflow Dynamics: Low Intake Cool Air -->
    <path d="M 60,560 C 140,560 180,520 240,500" class="airflow-cool" />
    <text x="180" y="525" class="mono-bold" fill="#5A7D7C">COOL INTAKE AIR</text>

    <!-- Airflow Dynamics: Buoyant Warm Air Rising up Thermal Stack -->
    <path d="M 280,460 C 350,380 350,220 350,95" class="airflow-warm" />
    <text x="365" y="130" class="mono-bold" fill="#C8523D">NATURAL STACK EXHAUST ({stack_v} M/S)</text>

    <!-- High Thermal Mass Slab Callout -->
    <rect x="180" y="570" width="320" height="18" fill="#DDD9D0" stroke="#111110" stroke-width="1.2" />
    <text x="340" y="584" class="mono-bold" text-anchor="middle">THERMAL MASS SLAB // {lag_hours}H DIURNAL LAG</text>
  </g>

  <!-- Folio Footer -->
  <line x1="60" y1="920" x2="1140" y2="920" stroke="#DDD9D0" stroke-width="1" />
  <text x="60" y="945" class="mono-label">SARA BENSALEM STUDIO • BIOCLIMATIC THERMODYNAMICS &amp; SOLAR SIMULATION ENGINE</text>
  <text x="1140" y="945" class="mono-bold" text-anchor="end">ZONE: {climate_key.upper()} // PLATE 01</text>
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
    parser = argparse.ArgumentParser(description="Sara Bensalem Bioclimatic Vector & Thermodynamic Calculator")
    parser.add_argument("--zone", default="temperate_strasbourg", choices=list(CLIMATE_PRESETS.keys()), help="Climate Zone Preset")
    parser.add_argument("--lat", type=float, default=None, help="Custom Latitude (overrides preset)")
    parser.add_argument("--output", "-o", default="bioclimatic_flow_plate.svg", help="Output SVG Path")
    args = parser.parse_args()

    out = generate_bioclimatic_svg(args.output, args.zone, args.lat)
    print(f"Bioclimatic flow plate successfully generated: {out}")

if __name__ == "__main__":
    main()
