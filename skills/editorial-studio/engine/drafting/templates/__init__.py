"""
engine/drafting/templates/__init__.py
Exposes SVG template file paths and parametric vector generators.
"""

import os
from .generators import (
    compute_wall_assembly_u_value,
    generate_wall_section_1_20_svg,
    generate_millwork_reveal_1_5_svg,
    generate_spatial_plan_1_100_svg,
    write_all_templates,
    DEFAULT_WALL_LAYERS,
)

TEMPLATES_DIR = os.path.dirname(__file__)

WALL_SECTION_1_20_PATH = os.path.join(TEMPLATES_DIR, "wall_section_1_20.svg")
MILLWORK_REVEAL_1_5_PATH = os.path.join(TEMPLATES_DIR, "millwork_reveal_1_5.svg")
SPATIAL_PLAN_1_100_PATH = os.path.join(TEMPLATES_DIR, "spatial_plan_1_100.svg")


def get_template_svg(template_name: str) -> str:
    """Reads and returns raw SVG content for a given template name."""
    path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template not found: {template_name} (looked at {path})")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


__all__ = [
    "TEMPLATES_DIR",
    "WALL_SECTION_1_20_PATH",
    "MILLWORK_REVEAL_1_5_PATH",
    "SPATIAL_PLAN_1_100_PATH",
    "compute_wall_assembly_u_value",
    "generate_wall_section_1_20_svg",
    "generate_millwork_reveal_1_5_svg",
    "generate_spatial_plan_1_100_svg",
    "write_all_templates",
    "get_template_svg",
    "DEFAULT_WALL_LAYERS",
]
