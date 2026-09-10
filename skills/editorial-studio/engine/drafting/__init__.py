"""
engine/drafting
ISO 128 Orthographic Technical Drafting Library for editorial-studio publishing system.
Provides metric lineweight hierarchies, scale-aware downsampling, standardized
Project Passport blocks, and publication-grade constructive vector templates.
"""

from .iso_128 import (
    STROKE_HAIRLINE,
    STROKE_THIN,
    STROKE_MEDIUM,
    STROKE_WIDE,
    STROKE_EXTRA_WIDE,
    STROKE_HAIRLINE_PT,
    STROKE_THIN_PT,
    STROKE_MEDIUM_PT,
    STROKE_WIDE_PT,
    STROKE_EXTRA_WIDE_PT,
    MIN_STROKE_MM,
    MIN_STROKE_PT,
    STANDARD_ISO_128_STROKES,
    MM_TO_PT,
    PT_TO_MM,
    ARCHITECTURAL_ROLES,
    ELEMENT_STROKE_MAP,
    get_element_stroke,
    mm_to_pt,
    pt_to_mm,
    validate_stroke_weight,
    downsample_stroke,
    downsample_hatch,
    filter_annotations,
    downsample_strokes,
)

from .project_passport import (
    PASSPORT_REQUIRED_FIELDS,
    PROJECT_PASSPORT_SCHEMA,
    validate_passport,
    generate_svg_badge,
    generate_typst_block,
    generate_html_component,
    ProjectPassport,
)

from .templates import (
    compute_wall_assembly_u_value,
    generate_wall_section_1_20_svg,
    generate_millwork_reveal_1_5_svg,
    generate_spatial_plan_1_100_svg,
    write_all_templates,
    get_template_svg,
    WALL_SECTION_1_20_PATH,
    MILLWORK_REVEAL_1_5_PATH,
    SPATIAL_PLAN_1_100_PATH,
    DEFAULT_WALL_LAYERS,
)

__all__ = [
    # Stroke weight constants
    "STROKE_HAIRLINE",
    "STROKE_THIN",
    "STROKE_MEDIUM",
    "STROKE_WIDE",
    "STROKE_EXTRA_WIDE",
    "STROKE_HAIRLINE_PT",
    "STROKE_THIN_PT",
    "STROKE_MEDIUM_PT",
    "STROKE_WIDE_PT",
    "STROKE_EXTRA_WIDE_PT",
    "MIN_STROKE_MM",
    "MIN_STROKE_PT",
    "STANDARD_ISO_128_STROKES",
    "MM_TO_PT",
    "PT_TO_MM",
    "ARCHITECTURAL_ROLES",
    "ELEMENT_STROKE_MAP",
    "get_element_stroke",
    "mm_to_pt",
    "pt_to_mm",
    "validate_stroke_weight",
    # Scale-aware downsampling
    "downsample_stroke",
    "downsample_hatch",
    "filter_annotations",
    "downsample_strokes",
    # Project Passport
    "PASSPORT_REQUIRED_FIELDS",
    "PROJECT_PASSPORT_SCHEMA",
    "validate_passport",
    "generate_svg_badge",
    "generate_typst_block",
    "generate_html_component",
    "ProjectPassport",
    # Templates & Physics
    "compute_wall_assembly_u_value",
    "generate_wall_section_1_20_svg",
    "generate_millwork_reveal_1_5_svg",
    "generate_spatial_plan_1_100_svg",
    "write_all_templates",
    "get_template_svg",
    "WALL_SECTION_1_20_PATH",
    "MILLWORK_REVEAL_1_5_PATH",
    "SPATIAL_PLAN_1_100_PATH",
    "DEFAULT_WALL_LAYERS",
]
