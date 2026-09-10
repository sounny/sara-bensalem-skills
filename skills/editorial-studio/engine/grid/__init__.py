"""
engine/grid package.
Swiss Modular Grid & Micro-Typography Engine.
"""

from .baseline import (
    snap_to_baseline,
    snap_container_height,
    compute_leading,
    validate_cross_spine_alignment,
    get_hanging_punctuation_offset,
    get_hanging_punctuation_ratio,
    detect_orphan_words,
    fix_orphan_line,
    validate_paragraph_split,
    sanitize_text_widows_orphans,
)
from .creep_calculator import (
    calculate_gutter_creep,
    calculate_creep,
    SUPPORTED_BINDING_TYPES,
)

import json
from pathlib import Path

def load_font_mapping() -> dict:
    """Loads and returns the authoritative font_mapping.json configuration."""
    font_mapping_path = Path(__file__).parent / "font_mapping.json"
    with open(font_mapping_path, "r", encoding="utf-8") as f:
        return json.load(f)

__all__ = [
    "snap_to_baseline",
    "snap_container_height",
    "compute_leading",
    "validate_cross_spine_alignment",
    "get_hanging_punctuation_offset",
    "get_hanging_punctuation_ratio",
    "detect_orphan_words",
    "fix_orphan_line",
    "validate_paragraph_split",
    "sanitize_text_widows_orphans",
    "calculate_gutter_creep",
    "calculate_creep",
    "SUPPORTED_BINDING_TYPES",
    "load_font_mapping",
]
