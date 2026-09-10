"""
engine/drafting/project_passport.py
Standardized Project Passport Generator, Validator, and Multi-Format Renderer.
Conforms to ProjectPassport Draft 2020-12 schema.

Authoritative Reference:
- ORIGINAL_REQUEST.md §R4
- personas/tectonic_detailer.md §9
- tests/tier1_features/test_project_passport.py
- tests/tier2_boundaries/test_boundary_passport_schema.py
- tests/tier5_adversarial/test_adversarial_remediation_edge_cases.py
"""

import re
import json
from typing import Dict, Any, List, Optional, Union
from jsonschema import Draft202012Validator, ValidationError

# ==============================================================================
# 1. Authoritative Draft 2020-12 Schema Definition
# ==============================================================================

PASSPORT_REQUIRED_FIELDS = [
    "title", "typology", "location", "coordinates", "year", "area_m2",
    "client", "stage", "candidate_role", "line_item_contributions",
    "software_stack", "work_authorization", "executive_premise"
]

PROJECT_PASSPORT_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ProjectPassport",
    "type": "object",
    "required": PASSPORT_REQUIRED_FIELDS,
    "properties": {
        "title": {
            "type": "string",
            "description": "Project official title or competition name"
        },
        "typology": {
            "type": "string",
            "description": "Architectural or spatial typology"
        },
        "location": {
            "type": "string",
            "description": "City, Region, and Country of project"
        },
        "coordinates": {
            "type": "string",
            "description": "Geographic DMS or decimal coordinates"
        },
        "year": {
            "type": "string",
            "description": "Completion or design year"
        },
        "area_m2": {
            "type": "number",
            "description": "Gross Internal Area (GIA) in square meters (integer or float)"
        },
        "budget_eur": {
            "type": "integer",
            "description": "Construction budget in EUR"
        },
        "client": {
            "type": "string",
            "description": "Client institution, developer, or competition authority"
        },
        "stage": {
            "type": "string",
            "description": "Professional stage reached (RIBA 0-7, AIA SD/DD/CD/CA, HOAI 1-9, Loi MOP)"
        },
        "team_size": {
            "type": "integer",
            "description": "Total number of core architectural team members"
        },
        "candidate_role": {
            "type": "string",
            "description": "Specific, non-generic role performed by candidate"
        },
        "line_item_contributions": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "description": "Detailed bulleted deliverables authored by candidate (minimum 3)"
        },
        "software_stack": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "description": "Non-empty list of BIM/CAD/computational tools employed"
        },
        "work_authorization": {
            "type": "string",
            "description": "Candidate legal residency or work authorization status"
        },
        "executive_premise": {
            "type": "string",
            "description": "Architectural thesis or technical challenge solved (minimum 8 words)"
        }
    }
}

_SCHEMA_VALIDATOR = Draft202012Validator(PROJECT_PASSPORT_SCHEMA)


# ==============================================================================
# 2. Schema Validation Engine
# ==============================================================================

def validate_passport(data: Dict[str, Any]) -> List[str]:
    """
    Validates passport data against authoritative schema and domain constraints.
    Returns list of error messages (empty list if 100% valid).
    """
    errors: List[str] = []

    # 1. Missing and null field checks
    for field in PASSPORT_REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")
        elif data[field] is None:
            errors.append(f"Field '{field}' cannot be null")

    # 2. Area M2 type checking (must be number: float/int, not bool or non-numeric)
    if "area_m2" in data and data["area_m2"] is not None:
        val = data["area_m2"]
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            errors.append(f"Field 'area_m2' must be a number (integer or float, got {type(val).__name__})")

    # 3. Coordinates formatting
    if "coordinates" in data and isinstance(data["coordinates"], str):
        if not re.search(r"\d+°|\d+\.\d+", data["coordinates"]):
            errors.append("Invalid coordinates format: must contain degree symbols or decimal coordinates")

    # 4. Line item contributions minimum items
    if "line_item_contributions" in data and data["line_item_contributions"] is not None:
        items = data["line_item_contributions"]
        if not isinstance(items, list) or len(items) < 3:
            errors.append(
                f"line_item_contributions must be a list with at least 3 items (got {len(items) if isinstance(items, list) else 'non-list'})"
            )

    # 5. Software stack non-empty list
    if "software_stack" in data and data["software_stack"] is not None:
        sw = data["software_stack"]
        if not isinstance(sw, list) or len(sw) == 0:
            errors.append("software_stack must be a non-empty list of tools")

    # 6. Executive premise minimum depth
    if "executive_premise" in data and isinstance(data["executive_premise"], str):
        words = data["executive_premise"].split()
        if len(words) < 8:
            errors.append("executive_premise must be at least 8 words defining the architectural premise")

    # 7. Cross-validate against formal Draft 2020-12 validator if basic checks passed
    if not errors:
        for err in _SCHEMA_VALIDATOR.iter_errors(data):
            errors.append(f"Draft 2020-12 Schema Error: {err.message}")

    return errors


# ==============================================================================
# 3. Multi-Format Generation Functions
# ==============================================================================

def generate_svg_badge(passport_data: Dict[str, Any], width: float = 380, height: float = 240) -> str:
    """
    Generates an orthographic SVG vector badge conforming to ISO 128 hairline standards
    and Swiss typographic discipline for project opening spreads.
    """
    title = _xml_escape(str(passport_data.get("title", "UNTITLED PROJECT")))
    typology = _xml_escape(str(passport_data.get("typology", "Architectural Case Study")))
    location = _xml_escape(str(passport_data.get("location", "")))
    coords = _xml_escape(str(passport_data.get("coordinates", "")))
    year = _xml_escape(str(passport_data.get("year", "")))
    area = passport_data.get("area_m2", 0)
    area_str = f"{area:,.1f} m²" if isinstance(area, float) else f"{area:,} m²"
    client = _xml_escape(str(passport_data.get("client", "")))
    stage = _xml_escape(str(passport_data.get("stage", "")))
    role = _xml_escape(str(passport_data.get("candidate_role", "")))
    auth = _xml_escape(str(passport_data.get("work_authorization", "")))
    premise = _xml_escape(str(passport_data.get("executive_premise", "")))

    contribs = passport_data.get("line_item_contributions", [])
    contrib_lines = []
    y_contrib = 138
    for c in contribs[:3]:
        c_esc = _xml_escape(str(c))
        contrib_lines.append(f'  <text x="24" y="{y_contrib}" font-family="\'JetBrains Mono\', monospace" font-size="6.5" fill="#33322E">• {c_esc}</text>')
        y_contrib += 11
    contrib_str = "\n".join(contrib_lines)

    tools = passport_data.get("software_stack", [])
    tools_str = _xml_escape(" · ".join([str(t) for t in tools]))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <style>
      .passport-bg {{ fill: #FBFBFA; }}
      .passport-border {{ fill: none; stroke: #55544E; stroke-width: 0.71; }}
      .passport-grid {{ stroke: #84827A; stroke-width: 0.37; }}
      .header-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: bold; fill: #111110; }}
      .badge-label {{ font-family: 'JetBrains Mono', monospace; font-size: 7px; font-weight: 600; fill: #84827A; letter-spacing: 0.5px; }}
      .meta-label {{ font-family: 'JetBrains Mono', monospace; font-size: 6px; font-weight: 600; fill: #84827A; text-transform: uppercase; }}
      .meta-val {{ font-family: 'JetBrains Mono', monospace; font-size: 7px; font-weight: 500; fill: #111110; }}
    </style>
  </defs>

  <!-- Passport Card Substrate: 0.25mm border (0.71pt) -->
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" class="passport-bg passport-border" rx="2" />

  <!-- Header Block: Project Title and Category -->
  <g transform="translate(16, 22)">
    <text x="0" y="0" class="badge-label">PROJECT PASSPORT / METADATA BLOCK</text>
    <text x="0" y="14" class="header-title">{title}</text>
    <text x="0" y="25" class="meta-val" fill="#55544E">{typology} | {year}</text>
  </g>

  <!-- Horizontal Divider: 0.13mm (0.37pt) hairline -->
  <line x1="16" y1="56" x2="{width - 16}" y2="56" class="passport-grid" />

  <!-- 4-Column Metadata Metric Row -->
  <g transform="translate(16, 68)">
    <text x="0" y="0" class="meta-label">LOCATION &amp; COORDS</text>
    <text x="0" y="10" class="meta-val">{location}</text>
    <text x="0" y="20" class="meta-val" fill="#55544E" font-size="6.5">{coords}</text>

    <text x="120" y="0" class="meta-label">GROSS AREA</text>
    <text x="120" y="10" class="meta-val">{area_str}</text>
    <text x="120" y="20" class="meta-val" fill="#55544E" font-size="6.5">Client: {client}</text>

    <text x="230" y="0" class="meta-label">STAGE &amp; STATUS</text>
    <text x="230" y="10" class="meta-val">{stage}</text>
    <text x="230" y="20" class="meta-val" fill="#55544E" font-size="6.5">{auth}</text>
  </g>

  <!-- Horizontal Divider: 0.13mm (0.37pt) hairline -->
  <line x1="16" y1="102" x2="{width - 16}" y2="102" class="passport-grid" />

  <!-- Candidate Role & Line Item Contributions -->
  <g transform="translate(16, 114)">
    <text x="0" y="0" class="meta-label">CANDIDATE ROLE: <tspan class="meta-val" font-weight="bold">{role}</tspan></text>
  </g>
{contrib_str}
  <!-- Horizontal Divider: 0.13mm (0.37pt) hairline -->
  <line x1="16" y1="178" x2="{width - 16}" y2="178" class="passport-grid" />

  <!-- Footer: Software Stack & Executive Premise -->
  <g transform="translate(16, 190)">
    <text x="0" y="0" class="meta-label">SOFTWARE STACK: <tspan class="meta-val">{tools_str}</tspan></text>
    <text x="0" y="12" class="meta-label">EXECUTIVE PREMISE:</text>
    <text x="0" y="22" font-family="'JetBrains Mono', monospace" font-size="6" fill="#33322E">{premise[:90]}...</text>
  </g>
</svg>"""


def generate_typst_block(passport_data: Dict[str, Any]) -> str:
    """
    Generates declarative Typst markup block for opening spread insertion.
    """
    title = passport_data.get("title", "Untitled Project")
    typology = passport_data.get("typology", "")
    location = passport_data.get("location", "")
    coords = passport_data.get("coordinates", "")
    year = passport_data.get("year", "")
    area = passport_data.get("area_m2", 0)
    stage = passport_data.get("stage", "")
    role = passport_data.get("candidate_role", "")
    auth = passport_data.get("work_authorization", "")
    premise = passport_data.get("executive_premise", "")
    contribs = passport_data.get("line_item_contributions", [])
    contrib_items = "\n".join([f'      [- {c}]' for c in contribs])
    tools = ", ".join(passport_data.get("software_stack", []))

    return f"""// Standardized Project Passport Block
#block(
  stroke: 0.25pt + rgb("#55544E"),
  inset: (x: 10pt, y: 8pt),
  radius: 2pt,
  fill: rgb("#FBFBFA"),
  width: 100%,
)[
  #set text(font: "JetBrains Mono", size: 6.5pt, fill: rgb("#111110"))
  #place(top + right)[
    #text(size: 6pt, fill: rgb("#84827A"))[PASSPORT 2026 // ISO 128]
  ]
  #v(2pt)
  #text(weight: "bold", size: 9pt, font: "Space Grotesk")[{title}]\\
  #text(fill: rgb("#55544E"))[{typology} | {location} | {year}]

  #line(length: 100%, stroke: 0.13pt + rgb("#84827A"))

  #grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 6pt,
    [
      #text(weight: "bold")[COORDINATES:]\\
      {coords}
    ],
    [
      #text(weight: "bold")[GROSS AREA / STAGE:]\\
      {area} m² | {stage}
    ],
    [
      #text(weight: "bold")[AUTHORIZATION:]\\
      {auth}
    ]
  )

  #line(length: 100%, stroke: 0.13pt + rgb("#84827A"))

  #text(weight: "bold")[ROLE & CONTRIBUTIONS: {role}]
  #list(
{contrib_items}
  )

  #line(length: 100%, stroke: 0.13pt + rgb("#84827A"))

  #grid(
    columns: (1fr, 2fr),
    gutter: 6pt,
    [
      #text(weight: "bold")[SOFTWARE STACK:]\\
      {tools}
    ],
    [
      #text(weight: "bold")[EXECUTIVE PREMISE:]\\
      #text(size: 5.5pt, fill: rgb("#33322E"))[{premise}]
    ]
  )
]
"""


def generate_html_component(passport_data: Dict[str, Any]) -> str:
    """
    Generates responsive, publication-grade HTML/CSS component with Swiss typography.
    """
    title = _xml_escape(str(passport_data.get("title", "")))
    typology = _xml_escape(str(passport_data.get("typology", "")))
    location = _xml_escape(str(passport_data.get("location", "")))
    coords = _xml_escape(str(passport_data.get("coordinates", "")))
    year = _xml_escape(str(passport_data.get("year", "")))
    area = passport_data.get("area_m2", 0)
    stage = _xml_escape(str(passport_data.get("stage", "")))
    role = _xml_escape(str(passport_data.get("candidate_role", "")))
    auth = _xml_escape(str(passport_data.get("work_authorization", "")))
    premise = _xml_escape(str(passport_data.get("executive_premise", "")))
    contribs = passport_data.get("line_item_contributions", [])
    contrib_html = "".join([f"      <li>{_xml_escape(str(c))}</li>\n" for c in contribs])
    tools = passport_data.get("software_stack", [])
    tools_html = "".join([f'<span class="badge">{_xml_escape(str(t))}</span>' for t in tools])

    return f"""<section class="project-passport" role="region" aria-label="Project Passport">
  <style>
    .project-passport {{
      box-sizing: border-box;
      width: 100%;
      max-width: 480px;
      padding: 14px 16px;
      background: #FBFBFA;
      border: 0.71pt solid #55544E;
      border-radius: 2px;
      font-family: 'JetBrains Mono', monospace;
      color: #111110;
      font-size: 11px;
      line-height: 1.4;
    }}
    .project-passport * {{ box-sizing: border-box; }}
    .passport-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }}
    .passport-category {{ font-size: 8px; text-transform: uppercase; color: #84827A; letter-spacing: 0.5px; }}
    .passport-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 700; margin: 2px 0; }}
    .passport-subtitle {{ font-size: 9px; color: #55544E; }}
    .passport-divider {{ height: 0.37pt; background: #84827A; margin: 8px 0; border: none; }}
    .passport-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; font-size: 9px; }}
    .passport-field-label {{ font-size: 7px; text-transform: uppercase; color: #84827A; display: block; }}
    .passport-contributions {{ margin: 6px 0; padding-left: 14px; font-size: 8.5px; color: #33322E; }}
    .passport-badges {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }}
    .passport-badges .badge {{ background: #EFEFEA; border: 0.37pt solid #D0CEC7; border-radius: 2px; padding: 2px 5px; font-size: 8px; }}
    .passport-premise {{ font-size: 8px; color: #55544E; font-style: italic; margin-top: 4px; }}
  </style>

  <header class="passport-header">
    <div>
      <span class="passport-category">Project Passport // ISO 128</span>
      <h3 class="passport-title">{title}</h3>
      <div class="passport-subtitle">{typology} — {location} ({year})</div>
    </div>
  </header>

  <hr class="passport-divider" />

  <div class="passport-grid">
    <div>
      <span class="passport-field-label">Coordinates</span>
      <span>{coords}</span>
    </div>
    <div>
      <span class="passport-field-label">Area GIA</span>
      <span>{area} m²</span>
    </div>
    <div>
      <span class="passport-field-label">Stage</span>
      <span>{stage}</span>
    </div>
  </div>

  <hr class="passport-divider" />

  <div>
    <span class="passport-field-label">Candidate Role &amp; Deliverables</span>
    <strong>{role}</strong>
    <ul class="passport-contributions">
{contrib_html}    </ul>
  </div>

  <hr class="passport-divider" />

  <div>
    <span class="passport-field-label">Software Stack</span>
    <div class="passport-badges">
      {tools_html}
    </div>
    <div class="passport-premise">"{premise}"</div>
  </div>
</section>"""


# ==============================================================================
# 4. ProjectPassport Class
# ==============================================================================

class ProjectPassport:
    """
    High-level Project Passport entity with full validation and multi-target compilation.
    """

    def __init__(self, data: Dict[str, Any]):
        self._data = dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectPassport":
        return cls(data)

    @classmethod
    def from_json(cls, json_str: str) -> "ProjectPassport":
        return cls(json.loads(json_str))

    @classmethod
    def from_json_file(cls, file_path: str) -> "ProjectPassport":
        with open(file_path, "r", encoding="utf-8") as f:
            return cls(json.load(f))

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

    def validate(self) -> List[str]:
        """Validates against authoritative schema; returns list of error messages."""
        return validate_passport(self._data)

    def is_valid(self) -> bool:
        """Returns True if passport passes all schema rules."""
        return len(self.validate()) == 0

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self._data, indent=indent)

    def to_svg(self, width: float = 380, height: float = 240) -> str:
        return generate_svg_badge(self._data, width, height)

    def to_typst(self) -> str:
        return generate_typst_block(self._data)

    def to_html(self) -> str:
        return generate_html_component(self._data)


def _xml_escape(text: str) -> str:
    """Escapes XML special characters for SVG/HTML rendering."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
