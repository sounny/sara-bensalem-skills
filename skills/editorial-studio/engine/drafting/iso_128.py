"""
engine/drafting/iso_128.py
ISO 128:2020 Orthographic Technical Drafting Library.
Defines calibrated metric stroke weight hierarchies, point conversions,
architectural element mappings, and scale-aware vector downsampling algorithms.

Authoritative Reference:
- ISO 128:2020 (Technical product documentation -- General principles of representation)
- ORIGINAL_REQUEST.md §R4
- personas/tectonic_detailer.md §4, §5
"""

import re
import xml.etree.ElementTree as ET
from typing import Union, List, Dict, Any, Optional

# Register default SVG namespace to prevent ns0 prefixes
ET.register_namespace("", "http://www.w3.org/2000/svg")

# ==============================================================================
# 1. Exact Metric Stroke Weight Constants (ISO 128:2020)
# ==============================================================================

# Metric widths in millimeters
STROKE_HAIRLINE: float = 0.13
STROKE_THIN: float = 0.25
STROKE_MEDIUM: float = 0.35
STROKE_WIDE: float = 0.50
STROKE_EXTRA_WIDE: float = 0.70

# Minimum physical print offset reproduction limit
MIN_STROKE_MM: float = 0.08

# Standard set of ISO 128 stroke weights
STANDARD_ISO_128_STROKES = {0.13, 0.25, 0.35, 0.50, 0.70}

# Unit conversion factors: 1 inch = 25.4 mm = 72 pt
MM_TO_PT: float = 72.0 / 25.4  # ~2.83464567 pt/mm
PT_TO_MM: float = 25.4 / 72.0  # ~0.35277778 mm/pt

# Point equivalents (rounded to standard 2 decimal places for CAD/SVG precision)
STROKE_HAIRLINE_PT: float = round(STROKE_HAIRLINE * MM_TO_PT, 2)    # 0.37 pt
STROKE_THIN_PT: float = round(STROKE_THIN * MM_TO_PT, 2)            # 0.71 pt
STROKE_MEDIUM_PT: float = round(STROKE_MEDIUM * MM_TO_PT, 2)        # 0.99 ~ 1.00 pt
STROKE_WIDE_PT: float = round(STROKE_WIDE * MM_TO_PT, 2)            # 1.42 pt
STROKE_EXTRA_WIDE_PT: float = round(STROKE_EXTRA_WIDE * MM_TO_PT, 2) # 1.98 ~ 2.00 pt

# Minimum stroke point equivalent
MIN_STROKE_PT: float = round(MIN_STROKE_MM * MM_TO_PT, 2)          # ~0.23 pt


# ==============================================================================
# 2. Architectural Element Mapping
# ==============================================================================

ARCHITECTURAL_ROLES = {
    "ground_cut": {
        "metric_mm": STROKE_EXTRA_WIDE,
        "point_pt": 1.984,
        "pt_rounded": 2.00,
        "hex_color": "#111110",
        "role": "Ground/Bedrock, Primary Mass Cut",
        "dash_array": None,
    },
    "primary_structure": {
        "metric_mm": STROKE_WIDE,
        "point_pt": 1.417,
        "pt_rounded": 1.42,
        "hex_color": "#111110",
        "role": "Structural Slabs, Columns, Shear Walls",
        "dash_array": None,
    },
    "secondary_partitions": {
        "metric_mm": STROKE_MEDIUM,
        "point_pt": 0.992,
        "pt_rounded": 1.00,
        "hex_color": "#33322E",
        "role": "Partitions, Joinery Carcase",
        "dash_array": None,
    },
    "visible_projections": {
        "metric_mm": STROKE_THIN,
        "point_pt": 0.709,
        "pt_rounded": 0.71,
        "hex_color": "#55544E",
        "role": "Uncut Edges, Dimension Chains, Door Swings",
        "dash_array": None,
    },
    "hatch_insulation": {
        "metric_mm": STROKE_HAIRLINE,
        "point_pt": 0.369,
        "pt_rounded": 0.37,
        "hex_color": "#84827A",
        "role": "Hatching, Insulation Batts, Background Grids",
        "dash_array": None,
    },
    "epdm_membrane": {
        "metric_mm": STROKE_THIN,
        "point_pt": 0.709,
        "pt_rounded": 0.71,
        "hex_color": "#111110",
        "role": "EPDM Waterproofing, Vapour Retarder",
        "dash_array": "3,1",
    },
    "pmr_egress_path": {
        "metric_mm": STROKE_MEDIUM,
        "point_pt": 0.992,
        "pt_rounded": 1.00,
        "hex_color": "#8B263E",
        "role": "PMR Accessibility Turning Circle, Egress Vector",
        "dash_array": "1,2",
    },
}

# Aliases for architectural categories
ELEMENT_STROKE_MAP: Dict[str, Dict[str, Any]] = {
    # 0.13 mm - Hatching and cavities
    "hatching": ARCHITECTURAL_ROLES["hatch_insulation"],
    "cavities": ARCHITECTURAL_ROLES["hatch_insulation"],
    "insulation": ARCHITECTURAL_ROLES["hatch_insulation"],
    "centerline": ARCHITECTURAL_ROLES["hatch_insulation"],
    # 0.25 mm - Dimensions and projections
    "dimensions": ARCHITECTURAL_ROLES["visible_projections"],
    "projections": ARCHITECTURAL_ROLES["visible_projections"],
    "uncut_edges": ARCHITECTURAL_ROLES["visible_projections"],
    "door_swings": ARCHITECTURAL_ROLES["visible_projections"],
    "epdm": ARCHITECTURAL_ROLES["epdm_membrane"],
    # 0.35 mm - Partitions and joinery
    "partitions": ARCHITECTURAL_ROLES["secondary_partitions"],
    "joinery": ARCHITECTURAL_ROLES["secondary_partitions"],
    "carcase": ARCHITECTURAL_ROLES["secondary_partitions"],
    "pmr_circle": ARCHITECTURAL_ROLES["pmr_egress_path"],
    "egress": ARCHITECTURAL_ROLES["pmr_egress_path"],
    # 0.50 mm - Structural cut planes
    "structural_cut_planes": ARCHITECTURAL_ROLES["primary_structure"],
    "structure": ARCHITECTURAL_ROLES["primary_structure"],
    "columns": ARCHITECTURAL_ROLES["primary_structure"],
    "slabs": ARCHITECTURAL_ROLES["primary_structure"],
    # 0.70 mm - Ground line and mass cut
    "ground_line": ARCHITECTURAL_ROLES["ground_cut"],
    "mass_cut": ARCHITECTURAL_ROLES["ground_cut"],
    "bedrock": ARCHITECTURAL_ROLES["ground_cut"],
}


def get_element_stroke(element_name: str) -> Dict[str, Any]:
    """Looks up calibrated stroke specification for an architectural element."""
    normalized = element_name.strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in ELEMENT_STROKE_MAP:
        return ELEMENT_STROKE_MAP[normalized]
    if normalized in ARCHITECTURAL_ROLES:
        return ARCHITECTURAL_ROLES[normalized]
    # Default to visible projections (0.25mm)
    return ARCHITECTURAL_ROLES["visible_projections"]


def mm_to_pt(mm: float) -> float:
    """Converts millimeters to typographic points."""
    return mm * MM_TO_PT


def pt_to_mm(pt: float) -> float:
    """Converts typographic points to millimeters."""
    return pt * PT_TO_MM


def validate_stroke_weight(stroke_mm: float, allow_clamped: bool = True) -> List[str]:
    """
    Validates vector stroke weight against ISO 128 standards and physical print limits.
    Returns list of error messages (empty if valid).
    """
    errors = []
    if stroke_mm <= 0.0:
        errors.append(f"Stroke weight must be positive (got {stroke_mm}mm)")
        return errors

    if stroke_mm < MIN_STROKE_MM:
        errors.append(
            f"Stroke weight {stroke_mm}mm is below the 0.08mm minimum print threshold (risk of dropped hairline)"
        )

    if stroke_mm not in STANDARD_ISO_128_STROKES:
        is_close = any(abs(stroke_mm - std) < 0.02 for std in STANDARD_ISO_128_STROKES)
        if not is_close and stroke_mm > MIN_STROKE_MM:
            errors.append(
                f"Non-standard ISO 128 stroke weight: {stroke_mm}mm (expected one of {sorted(list(STANDARD_ISO_128_STROKES))})"
            )

    if stroke_mm > 5.0:
        errors.append(
            f"Excessive stroke weight {stroke_mm}mm exceeds architectural drafting bounds"
        )

    return errors


# ==============================================================================
# 3. Scale-Aware Downsampling Core Functions
# ==============================================================================

def downsample_stroke(w_native_mm: float, scale_factor: float, min_clamp_mm: float = MIN_STROKE_MM) -> float:
    """
    Clamps effective stroke weight to prevent dropped hairline strokes in offset print.
    w_eff = max(w_native * scale_factor, min_clamp_mm)
    """
    if isinstance(scale_factor, bool) or not isinstance(scale_factor, (int, float)) or scale_factor <= 0.0:
        raise ValueError(f"scale_factor must be strictly positive (got {scale_factor})")
    scaled = w_native_mm * scale_factor
    return max(scaled, min_clamp_mm)


def downsample_hatch(native_spacing_mm: float, scale_factor: float) -> Dict[str, Any]:
    """
    Decimates or replaces dense hatch patterns when resized:
    - s >= 0.75mm: retain lines
    - 0.35mm <= s < 0.75mm: decimate by 2x (s_new = 2 * s)
    - s < 0.35mm: replace with flat 10% tint poché (#F1F1EB or #E5E5E5)
    """
    scaled_spacing = round(native_spacing_mm * scale_factor, 4)
    if scaled_spacing >= 0.75:
        return {"action": "RETAIN", "spacing_mm": scaled_spacing, "fill": "none"}
    elif scaled_spacing >= 0.35:
        return {"action": "DECIMATE_2X", "spacing_mm": scaled_spacing * 2.0, "fill": "none"}
    else:
        return {"action": "POCHE_REPLACE", "spacing_mm": None, "fill": "#F1F1EB"}


def filter_annotations(scale_factor: float) -> str:
    """
    Returns annotation level allowed at given viewport scale factor:
    - scale >= 0.75: FULL_ANNOTATIONS (all cotations, dimensions, callouts)
    - 0.40 <= scale < 0.75: MAJOR_DIMENSIONS_ONLY (structural grid, overall dimensions)
    - scale < 0.40: GRAPHIC_SCALE_BAR_ONLY (suppress internal dimensions, retain scale bar)
    """
    if scale_factor >= 0.75:
        return "FULL_ANNOTATIONS"
    elif scale_factor >= 0.40:
        return "MAJOR_DIMENSIONS_ONLY"
    else:
        return "GRAPHIC_SCALE_BAR_ONLY"


# ==============================================================================
# 4. Scale-Aware SVG / Element Downsampler
# ==============================================================================

def downsample_strokes(
    svg_or_elements: Union[str, ET.Element, ET.ElementTree, List[Dict[str, Any]], Dict[str, Any]],
    target_scale: float,
    min_stroke_mm: float = MIN_STROKE_MM,
    poche_color: str = "#E5E5E5",
    poche_opacity: float = 0.8
) -> Any:
    """
    Applies scale-aware downsampling to SVG vector graphics or element structures:
    1. Clamps scaled stroke weights to w >= min_stroke_mm (default 0.08mm).
    2. When hatch spacing drops below 0.35mm, converts hatch lines to semi-transparent
       poché fill (#E5E5E5 or tint) to prevent ink coalescence.
    3. Culls sub-millimeter annotations or dimensions when reducing plate scale.
    """
    if isinstance(target_scale, bool) or not isinstance(target_scale, (int, float)) or target_scale <= 0.0:
        raise ValueError(f"target_scale must be a strictly positive number (got {target_scale})")

    min_stroke_pt = min_stroke_mm * MM_TO_PT

    # Handle Python dictionary or list of drawing elements
    if isinstance(svg_or_elements, (list, dict)):
        return _downsample_element_data(svg_or_elements, target_scale, min_stroke_mm, poche_color)

    # Handle SVG XML string or ElementTree
    is_str_input = isinstance(svg_or_elements, str)
    if is_str_input:
        root = ET.fromstring(svg_or_elements)
    elif isinstance(svg_or_elements, ET.ElementTree):
        root = svg_or_elements.getroot()
    elif isinstance(svg_or_elements, ET.Element):
        root = svg_or_elements
    else:
        raise TypeError(f"Unsupported input type for downsample_strokes: {type(svg_or_elements)}")

    annotation_level = filter_annotations(target_scale)

    # 1. Update hatch patterns in <defs>
    patterns_to_poche = set()
    for pattern in root.findall(".//{http://www.w3.org/2000/svg}pattern") + root.findall(".//pattern"):
        p_id = pattern.get("id", "")
        w_val = pattern.get("width")
        h_val = pattern.get("height")
        try:
            native_spacing = float(w_val) if w_val else (float(h_val) if h_val else 10.0)
        except (ValueError, TypeError):
            native_spacing = 10.0

        native_spacing_mm = native_spacing * PT_TO_MM
        hatch_res = downsample_hatch(native_spacing_mm, target_scale)

        if hatch_res["action"] == "POCHE_REPLACE":
            patterns_to_poche.add(p_id)
            pattern.clear()
            pattern.set("id", p_id)
            pattern.set("width", "10")
            pattern.set("height", "10")
            pattern.set("patternUnits", "userSpaceOnUse")
            rect = ET.SubElement(pattern, "rect")
            rect.set("width", "100%")
            rect.set("height", "100%")
            rect.set("fill", poche_color)
            rect.set("fill-opacity", str(poche_opacity))
        elif hatch_res["action"] == "DECIMATE_2X":
            new_dim = str(native_spacing * 2.0)
            pattern.set("width", new_dim)
            pattern.set("height", new_dim)

    # Build parent map to check ancestor properties
    parent_map = {c: p for p in root.iter() for c in p}

    def is_protected_ancestor(node: ET.Element) -> bool:
        curr = node
        while curr is not None:
            cid = curr.get("id", "").lower()
            ccls = curr.get("class", "").lower()
            if "scale-bar" in cid or "scale_bar" in cid or "scale-bar" in ccls:
                return True
            if "header" in cid or "title" in cid:
                return True
            curr = parent_map.get(curr)
        return False

    # 2. Traverse and process elements
    for elem in list(root.iter()):
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        elem_id = elem.get("id", "").lower()
        elem_class = elem.get("class", "").lower()

        # Check for hatch fill reference
        fill_attr = elem.get("fill", "")
        for pid in patterns_to_poche:
            if f"url(#{pid})" in fill_attr:
                elem.set("fill", poche_color)
                elem.set("fill-opacity", str(poche_opacity))

        # Clamp and scale stroke-width attribute
        if "stroke-width" in elem.attrib:
            orig_sw = elem.attrib["stroke-width"]
            new_sw = _scale_stroke_attr(orig_sw, target_scale, min_stroke_mm, min_stroke_pt)
            elem.set("stroke-width", new_sw)

        # Clamp and scale style attribute if it contains stroke-width
        if "style" in elem.attrib:
            style_str = elem.attrib["style"]
            if "stroke-width" in style_str:
                elem.attrib["style"] = _scale_style_stroke(style_str, target_scale, min_stroke_mm, min_stroke_pt)

        # 3. Annotation culling
        protected = is_protected_ancestor(elem)
        if not protected:
            is_dim = (
                "dimension" in elem_id
                or "dimension" in elem_class
                or "cotation" in elem_id
                or tag == "text"
            )
            is_minor_dim = (
                "minor" in elem_id
                or "minor" in elem_class
                or "sub-layer" in elem_class
                or "witness" in elem_class
            )

            if annotation_level == "MAJOR_DIMENSIONS_ONLY":
                if is_minor_dim:
                    elem.set("display", "none")
            elif annotation_level == "GRAPHIC_SCALE_BAR_ONLY":
                if is_dim:
                    elem.set("display", "none")

    if is_str_input:
        return ET.tostring(root, encoding="utf-8").decode("utf-8")
    return root


def _scale_stroke_attr(val_str: str, scale_factor: float, min_mm: float, min_pt: float) -> str:
    """Scales and clamps stroke-width value string with unit preservation."""
    val_str = val_str.strip()
    if val_str.endswith("mm"):
        try:
            val = float(val_str[:-2])
            scaled = max(val * scale_factor, min_mm)
            return f"{scaled:.2f}mm"
        except ValueError:
            return val_str
    elif val_str.endswith("pt"):
        try:
            val = float(val_str[:-2])
            scaled = max(val * scale_factor, min_pt)
            return f"{scaled:.2f}pt"
        except ValueError:
            return val_str
    elif val_str.endswith("px"):
        try:
            val = float(val_str[:-2])
            scaled = max(val * scale_factor, min_pt)
            return f"{scaled:.2f}px"
        except ValueError:
            return val_str
    else:
        try:
            val = float(val_str)
            scaled = max(val * scale_factor, min_pt)
            return f"{scaled:.2f}"
        except ValueError:
            return val_str


def _scale_style_stroke(style_str: str, scale_factor: float, min_mm: float, min_pt: float) -> str:
    """Parses inline CSS style string and updates stroke-width property."""
    parts = style_str.split(";")
    new_parts = []
    for part in parts:
        if not part.strip():
            continue
        if ":" in part:
            k, v = part.split(":", 1)
            k_clean = k.strip()
            v_clean = v.strip()
            if k_clean == "stroke-width":
                v_scaled = _scale_stroke_attr(v_clean, scale_factor, min_mm, min_pt)
                new_parts.append(f"{k_clean}: {v_scaled}")
            else:
                new_parts.append(part)
        else:
            new_parts.append(part)
    return "; ".join(new_parts)


def _downsample_element_data(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    target_scale: float,
    min_stroke_mm: float,
    poche_color: str
) -> Any:
    """Downsamples structured primitive element dictionaries."""
    if isinstance(data, list):
        return [_downsample_element_data(item, target_scale, min_stroke_mm, poche_color) for item in data]
    elif isinstance(data, dict):
        result = dict(data)
        if "stroke_mm" in result:
            result["stroke_mm"] = downsample_stroke(result["stroke_mm"], target_scale, min_stroke_mm)
        if "stroke_pt" in result:
            min_pt = min_stroke_mm * MM_TO_PT
            result["stroke_pt"] = max(result["stroke_pt"] * target_scale, min_pt)
        if "hatch_spacing_mm" in result:
            h_res = downsample_hatch(result["hatch_spacing_mm"], target_scale)
            result["hatch_status"] = h_res
            if h_res["action"] == "POCHE_REPLACE":
                result["fill"] = poche_color
        if "annotation_type" in result:
            allowed_level = filter_annotations(target_scale)
            if allowed_level == "GRAPHIC_SCALE_BAR_ONLY" and result["annotation_type"] != "SCALE_BAR":
                result["visible"] = False
            elif allowed_level == "MAJOR_DIMENSIONS_ONLY" and result["annotation_type"] == "MINOR_DIMENSION":
                result["visible"] = False
        return result
    return data
