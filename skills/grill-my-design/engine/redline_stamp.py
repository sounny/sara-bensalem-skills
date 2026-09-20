"""
Visual Socratic Crit Sheet & Redline Stamp SVG Generator
Sara Bensalem Studio • Strasbourg Atelier [48°35'05"N 07°45'02"E]
Generates publication-grade 16:9 vector SVG crit plates with tribunal stamps.
"""

import os
import xml.sax.saxutils as saxutils
from typing import Optional
try:
    from .models import GrillReport, Severity
except ImportError:
    from models import GrillReport, Severity

def esc(text: str) -> str:
    """Escapes XML entities safely."""
    if text is None:
        return ""
    return saxutils.escape(str(text))

def generate_crit_stamp_svg(
    report: GrillReport,
    output_path: Optional[str] = None,
    project_title: str = "ARCHITECTURAL DESIGN SUBMISSION",
    typology_str: Optional[str] = None
) -> str:
    """
    Generates a 1920x1080 vector SVG Socratic Crit Sheet with:
    - Official Strasbourg Atelier Tribunal Seal (PASSED / CONDITIONAL / REWORK)
    - 5-Dimension Score Progression HUD
    - Itemized Redline Callouts with calibrated lineweights
    - Direct Tectonic Rescue CLI command blocks
    """
    width = 1920
    height = 1080

    typology_name = typology_str or report.typology or "GENERAL COMMERCIAL / RESIDENTIAL"
    typology_name = typology_name.replace("_", " ").upper()

    # Verdict styling
    overall = report.overall_score
    pre_score = report.pre_defense_score if report.pre_defense_score is not None else max(30, overall - 25)
    
    if overall >= 85:
        verdict_color = "#1B4332"     # Emerald Green
        verdict_bg = "#E8F5E9"
        verdict_badge = "STRONG HIRE // DEFENSE ACCEPTED"
        seal_status = "PASSED TRIBUNAL"
    elif overall >= 70:
        verdict_color = "#92400E"     # Amber Ochre
        verdict_bg = "#FEF3C7"
        verdict_badge = "CONDITIONAL PASS // REDLINES REQUIRED"
        seal_status = "CONDITIONAL"
    else:
        verdict_color = "#991B1B"     # Crimson Terre-Cuite
        verdict_bg = "#FEE2E2"
        verdict_badge = "RENDER TRAP ALERT // REWORK REQUIRED"
        seal_status = "REWORK REQUIRED"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&amp;family=JetBrains+Mono:wght@400;500;700&amp;display=swap');
      .swiss-title {{ font-family: 'Inter', -apple-system, sans-serif; font-size: 32px; font-weight: 700; fill: #111110; letter-spacing: -0.8px; }}
      .swiss-subtitle {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 500; fill: #84827A; letter-spacing: 1.5px; text-transform: uppercase; }}
      .swiss-h2 {{ font-family: 'Inter', -apple-system, sans-serif; font-size: 16px; font-weight: 700; fill: #111110; letter-spacing: 0.5px; }}
      .swiss-body {{ font-family: 'Inter', -apple-system, sans-serif; font-size: 13px; font-weight: 400; fill: #333330; line-height: 1.5; }}
      .mono-body {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 400; fill: #555550; }}
      .mono-bold {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; fill: #111110; letter-spacing: 0.5px; }}
      .mono-tag {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }}
      .code-box {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px; font-weight: 500; fill: #1E293B; }}
      .dimension-score {{ font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; }}
    </style>
    <!-- Grid Pattern -->
    <pattern id="archGrid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#ECEBE6" stroke-width="0.75" />
    </pattern>
  </defs>

  <!-- Background Base -->
  <rect width="{width}" height="{height}" fill="#FAF9F5" />
  <rect width="{width}" height="{height}" fill="url(#archGrid)" opacity="0.65" />

  <!-- Outer Margin Border (Swiss 60mm offset) -->
  <rect x="50" y="45" width="{width - 100}" height="{height - 90}" fill="none" stroke="#DDD9D0" stroke-width="1.5" />
  <rect x="54" y="49" width="{width - 108}" height="{height - 98}" fill="none" stroke="#EAE8E0" stroke-width="0.75" />

  <!-- TOP HEADER BLOCK -->
  <g transform="translate(80, 75)">
    <text x="0" y="24" class="swiss-subtitle">SARA BENSALEM STUDIO • STRASBOURG ATELIER [48°35'05"N 07°45'02"E] • PLATE 07</text>
    <text x="0" y="62" class="swiss-title">SOCRATIC DESIGN REVIEW TRIBUNAL &amp; REDLINE AUDIT</text>
    <text x="0" y="86" class="mono-body">PROJECT: <tspan class="mono-bold">{esc(project_title)}</tspan> | TYPOLOGY: <tspan class="mono-bold">{esc(typology_name)}</tspan> | STATUS: <tspan class="mono-bold">ROUND {report.current_round} DEFENSE</tspan></text>
  </g>

  <!-- OFFICIAL TRIBUNAL VERDICT SEAL (Top-Right Stamp) -->
  <g transform="translate(1560, 70)">
    <!-- Outer Octagonal / Circular Seal -->
    <circle cx="120" cy="65" r="58" fill="#FFFFFF" stroke="{verdict_color}" stroke-width="3" stroke-dasharray="8 3" />
    <circle cx="120" cy="65" r="50" fill="{verdict_bg}" stroke="{verdict_color}" stroke-width="1.5" />
    <text x="120" y="48" class="mono-tag" fill="{verdict_color}" font-size="8.5px" text-anchor="middle">SARA BENSALEM</text>
    <text x="120" y="65" class="mono-tag" fill="{verdict_color}" font-size="11px" font-weight="900" text-anchor="middle">{esc(seal_status)}</text>
    <text x="120" y="80" class="mono-tag" fill="{verdict_color}" font-size="8px" text-anchor="middle">STRASBOURG ATELIER</text>
    <text x="120" y="93" class="mono-body" fill="{verdict_color}" font-size="7.5px" text-anchor="middle">★ VERIFIED TECTONICS ★</text>
  </g>

  <!-- HORIZONTAL DIVIDER -->
  <line x1="80" y1="190" x2="1840" y2="190" stroke="#111110" stroke-width="1.5" />

  <!-- ================= LEFT COLUMN: SCORECARD & HUD (Width 540px) ================= -->
  <g transform="translate(80, 215)">
    <!-- Big Verdict Card -->
    <rect x="0" y="0" width="530" height="150" fill="{verdict_bg}" stroke="{verdict_color}" stroke-width="2" rx="4" />
    <text x="24" y="32" class="mono-tag" fill="{verdict_color}">TRIBUNAL DECISION // SARA BENSALEM 100-PT RUBRIC</text>
    <text x="24" y="68" class="swiss-h2" fill="{verdict_color}" font-size="18px">{esc(verdict_badge)}</text>
    
    <!-- Score Progress Display -->
    <g transform="translate(24, 85)">
      <text x="0" y="38" font-family="'Inter', sans-serif" font-size="44px" font-weight="900" fill="{verdict_color}">{overall}</text>
      <text x="65" y="34" class="mono-body" font-size="18px" fill="{verdict_color}">/ 100</text>
      
      <!-- Mini Progress Bar -->
      <g transform="translate(130, 10)">
        <text x="0" y="10" class="mono-body" font-size="9.5px">Pre-Defense: {pre_score} pts</text>
        <rect x="0" y="15" width="340" height="10" fill="#E2E8F0" rx="5" />
        <rect x="0" y="15" width="{int(pre_score * 3.4)}" height="10" fill="#94A3B8" rx="5" />
        <text x="0" y="40" class="mono-bold" font-size="10px">Post-Defense: {overall} pts ({'+' if overall >= pre_score else ''}{overall - pre_score} pts gained)</text>
        <rect x="0" y="45" width="340" height="10" fill="#E2E8F0" rx="5" />
        <rect x="0" y="45" width="{int(overall * 3.4)}" height="10" fill="{verdict_color}" rx="5" />
      </g>
    </g>

    <!-- 5-Dimension Radar / Bar Gauge HUD -->
    <g transform="translate(0, 175)">
      <rect x="0" y="0" width="530" height="375" fill="#FFFFFF" stroke="#DDD9D0" stroke-width="1.2" rx="4" />
      <text x="24" y="32" class="swiss-h2">5 DIAGNOSTIC CRITIQUE LENSES</text>
      <text x="24" y="50" class="mono-body" font-size="10px">Weighted against international building codes &amp; recruiter benchmarks</text>
      <line x1="24" y1="62" x2="506" y2="62" stroke="#EAE8E0" stroke-width="1" />
"""

    dim_y = 80
    for dim in report.dimension_scores:
        score_val = dim.score
        d_color = "#1B4332" if score_val >= 80 else ("#92400E" if score_val >= 65 else "#991B1B")
        svg += f"""
      <g transform="translate(24, {dim_y})">
        <text x="0" y="12" class="mono-bold" font-size="11px">{esc(dim.name[:32])}</text>
        <text x="482" y="12" class="dimension-score" fill="{d_color}" text-anchor="end">{score_val}%</text>
        <rect x="0" y="20" width="482" height="8" fill="#F1F0EC" rx="4" />
        <rect x="0" y="20" width="{int(score_val * 4.82)}" height="8" fill="{d_color}" rx="4" />
        <text x="0" y="44" class="mono-body" font-size="9.5px" fill="#666660">{esc(dim.critique[:68])}...</text>
      </g>
"""
        dim_y += 58

    svg += f"""
    </g>

    <!-- Recruiter 15-Second Takeaway Box -->
    <g transform="translate(0, 570)">
      <rect x="0" y="0" width="530" height="155" fill="#FFFFFF" stroke="#111110" stroke-width="1.2" rx="4" />
      <text x="20" y="28" class="mono-tag" fill="#111110">15-SECOND RECRUITER VERDICT &amp; EYE-TRACKING</text>
      <line x1="20" y1="38" x2="510" y2="38" stroke="#DDD9D0" stroke-width="1" />
      <text x="20" y="64" class="swiss-body" font-size="12.5px">{esc(report.recruiter_15s_takeaway[:220])}</text>
      <rect x="20" y="105" width="490" height="34" fill="#F4F4F0" rx="3" />
      <text x="32" y="126" class="mono-body" font-size="10px">PASS MARK: >= 85 Tier-1 Studio (Foster/BIG/ZHA) | REJECT: &lt; 65</text>
    </g>
  </g>

  <!-- ================= RIGHT COLUMN: REDLINE MARKUPS & PROBES (Width 1180px) ================= -->
  <g transform="translate(645, 215)">
    <!-- Section Title -->
    <text x="0" y="24" class="swiss-h2" font-size="18px">TOP TECTONIC VULNERABILITIES &amp; REDLINE MARKUPS</text>
    <text x="0" y="44" class="mono-body" font-size="10.5px">Identified by the 5-Persona Tribunal. Every vulnerability requires a tangible drawing amendment.</text>
    <line x1="0" y1="56" x2="1195" y2="56" stroke="#DDD9D0" stroke-width="1.2" />

    <!-- List of Vulnerability Probes -->
"""

    card_y = 70
    displayed_probes = report.top_vulnerabilities[:3] if report.top_vulnerabilities else []
    
    for idx, probe in enumerate(displayed_probes):
        sev_color = "#991B1B" if probe.severity == Severity.FATAL else ("#C2410C" if probe.severity == Severity.CRITICAL else "#D97706")
        sev_bg = "#FEF2F2" if probe.severity == Severity.FATAL else ("#FFF7ED" if probe.severity == Severity.CRITICAL else "#FFFBEB")
        persona_str = probe.persona.value.replace("_", " ").upper() if hasattr(probe.persona, "value") else str(probe.persona).upper()
        trap_label = f" // TRAP #{probe.trap_id}" if probe.trap_id else ""

        svg += f"""
    <!-- Redline Card {idx+1} -->
    <g transform="translate(0, {card_y})">
      <rect x="0" y="0" width="1195" height="155" fill="#FFFFFF" stroke="#DDD9D0" stroke-width="1.2" rx="4" />
      <rect x="0" y="0" width="10" height="155" fill="{sev_color}" rx="2" />
      
      <!-- Header Row -->
      <g transform="translate(25, 24)">
        <rect x="0" y="-14" width="75" height="20" fill="{sev_bg}" rx="3" />
        <text x="8" y="0" class="mono-tag" fill="{sev_color}">{probe.severity.value}</text>
        <text x="90" y="0" class="mono-bold" font-size="11.5px">REDLINE #{idx+1:02d}: {esc(probe.dimension.upper())}{trap_label} • [{esc(persona_str)}]</text>
      </g>
      
      <!-- Interrogation Probe -->
      <text x="25" y="58" class="mono-body" font-size="11.5px" fill="#111110" font-weight="600">Q: "{esc(probe.interrogation_question[:150])}"</text>
      
      <!-- Vulnerability & CAD Fix -->
      <g transform="translate(25, 80)">
        <text x="0" y="0" class="mono-body" font-size="10.5px" fill="#777770">DEFECT:</text>
        <text x="60" y="0" class="swiss-body" font-size="12px" fill="#B91C1C">{esc(probe.vulnerability_detected[:130])}</text>
        
        <text x="0" y="24" class="mono-body" font-size="10.5px" fill="#15803D">REMEDY:</text>
        <text x="60" y="24" class="swiss-body" font-size="12px" fill="#15803D" font-weight="600">{esc(probe.redline_fix[:130])}</text>
      </g>

      <!-- Remediation Command -->
      <g transform="translate(25, 128)">
        <rect x="0" y="-12" width="1145" height="22" fill="#F8F8F5" rx="3" stroke="#E5E4DE" stroke-width="0.75" />
        <text x="12" y="3" class="code-box" font-size="9.5px">{esc(probe.remediation_command or 'python .../wall_section_builder.py --assembly granite_hemp')}</text>
      </g>
    </g>
"""
        card_y += 168

    svg += f"""
    <!-- TECTONIC RESCUE PACKAGE BOX -->
    <g transform="translate(0, 595)">
      <rect x="0" y="0" width="1195" height="130" fill="#F3F4F6" stroke="#1E293B" stroke-width="1.5" rx="4" />
      <g transform="translate(25, 28)">
        <text x="0" y="0" class="mono-tag" fill="#0F172A" font-size="11px">★ TECTONIC RESCUE SUITE: 1-CLICK DRAWING REMEDIATION</text>
        <text x="0" y="20" class="mono-body" font-size="10px">Execute these terminal commands to automatically generate publication-grade vector plates replacing flawed renders:</text>
      </g>
      <g transform="translate(25, 65)">
        <rect x="0" y="0" width="560" height="24" fill="#FFFFFF" stroke="#CBD5E1" rx="3" />
        <text x="10" y="16" class="code-box" font-size="9.5px">python .../wall_section_builder.py --assembly granite_hemp --output 01_wall_section.svg</text>

        <rect x="585" y="0" width="560" height="24" fill="#FFFFFF" stroke="#CBD5E1" rx="3" />
        <text x="595" y="16" class="code-box" font-size="9.5px">python .../plan_compliance_engine.py --door 930 --vestibule 1500 --output 02_pmr_plan.svg</text>
      </g>
      <g transform="translate(25, 95)">
        <rect x="0" y="0" width="560" height="24" fill="#FFFFFF" stroke="#CBD5E1" rx="3" />
        <text x="10" y="16" class="code-box" font-size="9.5px">python .../bioclimatic_calculator.py --zone temperate_strasbourg --output 03_solar_flow.svg</text>

        <rect x="585" y="0" width="560" height="24" fill="#FFFFFF" stroke="#CBD5E1" rx="3" />
        <text x="595" y="16" class="code-box" font-size="9.5px">python .../spatial_stitch.py generate --archetype THE_CONSTRUCTIVE_PROOF --output 04_spread.svg</text>
      </g>
    </g>
  </g>

  <!-- ================= FOLIO FOOTER (Calibrated Lineweights) ================= -->
  <g transform="translate(80, 1025)">
    <line x1="0" y1="0" x2="1760" y2="0" stroke="#111110" stroke-width="1.2" />
    <text x="0" y="22" class="mono-body" font-size="9.5px">SARA BENSALEM STUDIO • HIGH-STAKES ARCHITECTURAL JURY TRIBUNAL • RE2020 / EUROCODE / IBC STANDARDS</text>
    
    <!-- ISO 128 Lineweight Calibration Block -->
    <g transform="translate(1150, 6)">
      <text x="0" y="14" class="mono-body" font-size="8.5px">ISO 128 LINEWEIGHTS:</text>
      <line x1="120" y1="10" x2="160" y2="10" stroke="#111110" stroke-width="3" />
      <text x="165" y="13" class="mono-body" font-size="8px">0.50 CUT</text>
      <line x1="220" y1="10" x2="260" y2="10" stroke="#111110" stroke-width="1.5" />
      <text x="265" y="13" class="mono-body" font-size="8px">0.25 BOUNDARY</text>
      <line x1="345" y1="10" x2="385" y2="10" stroke="#111110" stroke-width="0.8" />
      <text x="390" y="13" class="mono-body" font-size="8px">0.13 HAIRLINE</text>
    </g>

    <text x="1760" y="22" class="mono-bold" font-size="9.5px" text-anchor="end">PLATE 07 // CONFIDENTIAL AUDIT REPORT</text>
  </g>
</svg>"""

    if output_path:
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg)

    return svg
