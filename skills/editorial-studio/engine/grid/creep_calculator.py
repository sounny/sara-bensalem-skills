"""
engine/grid/creep_calculator.py
Automated Gutter Creep, Shingling, and Spine Bindery Physics Calculus.

Authoritative Sources:
- ORIGINAL_REQUEST.md §R3
- personas/compositor.md §3, §5
- Bringhurst, The Elements of Typographic Style
"""

from __future__ import annotations
from typing import Dict, Any


SUPPORTED_BINDING_TYPES = frozenset({
    "SMYTH_SEWN",
    "PERFECT_BOUND",
    "LAY_FLAT",
    "SADDLE_STITCHED",
    # Aliases
    "LAYFLAT",
    "PUR_PERFECT_BOUND",
    "PUR",
    "FOLDED_SIGNATURE_PUR",
    "PERFECT_BOUND_FOLDED",
    "SINGLE_LEAF_PUR",
    "SADDLE_STITCH"
})


def calculate_gutter_creep(
    page: int,
    total_pages: int,
    binding_type: str,
    paper_caliper_mm: float = 0.15,
    signature_size: int = 16,
    gutter_draw_mm: float = 8.0,
    base_inner_margin_mm: float = 20.0,
    base_outer_margin_mm: float = 18.0,
    folded_signature: bool = False,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Computes exact gutter creep displacement, spine glue draw, shingle offset,
    and dynamically adjusted inner and outer margins for printed publications.

    Args:
        page: 1-based page number (1 <= page <= total_pages).
        total_pages: Total page count of the publication (N).
        binding_type: Binding method ("SMYTH_SEWN", "PERFECT_BOUND", "LAY_FLAT", "SADDLE_STITCHED").
        paper_caliper_mm: Single sheet thickness in millimeters (default 0.15mm).
        signature_size: Number of pages per folded signature (default 16).
        gutter_draw_mm: Spine glue clamp gutter draw in millimeters for PUR (default 8.0mm).
        base_inner_margin_mm: Nominal inner (spine) margin in millimeters (default 20.0mm).
        base_outer_margin_mm: Nominal outer (trim) margin in millimeters (default 18.0mm).
        folded_signature: Whether PUR binding uses folded signatures (Burst/PUR) vs single-leaf cut.
        **kwargs: Additional compatibility aliases (e.g. base_inner_mm, base_outer_mm).

    Returns:
        Dictionary containing:
            - inner_margin_mm (float)
            - outer_margin_mm (float)
            - shingle_mm (float)
            - creep_offset_mm (float)
            - delta_creep_mm (float, alias)
            - gutter_draw_mm (float)
            - page (int)
            - binding_type (str)
    """
    # Resolve argument aliases
    if "base_inner_mm" in kwargs:
        base_inner_margin_mm = float(kwargs["base_inner_mm"])
    if "base_outer_mm" in kwargs:
        base_outer_margin_mm = float(kwargs["base_outer_mm"])

    # Normalization & Validation
    if not isinstance(binding_type, str):
        raise ValueError(f"Binding type must be a string, got {type(binding_type).__name__}")

    b_type_raw = binding_type.upper().strip()
    if b_type_raw not in SUPPORTED_BINDING_TYPES:
        raise ValueError(
            f"Unsupported binding type: '{binding_type}'. "
            f"Valid types are: SMYTH_SEWN, PERFECT_BOUND, LAY_FLAT, SADDLE_STITCHED"
        )

    # Map aliases to canonical names
    if b_type_raw in {"LAYFLAT", "LAY_FLAT"}:
        canonical_btype = "LAY_FLAT"
    elif b_type_raw in {"SMYTH_SEWN", "SMYTHSEWN"}:
        canonical_btype = "SMYTH_SEWN"
    elif b_type_raw in {"SADDLE_STITCH", "SADDLE_STITCHED"}:
        canonical_btype = "SADDLE_STITCHED"
    else:
        canonical_btype = "PERFECT_BOUND"

    # Validate page counts
    if total_pages < 1:
        raise ValueError(f"total_pages must be >= 1, got {total_pages}")
    if page < 1 or page > total_pages:
        raise ValueError(f"page index {page} out of bounds [1, {total_pages}]")

    # Saddle stitch restriction to N <= 64
    if canonical_btype == "SADDLE_STITCHED" and total_pages > 64:
        raise ValueError(
            f"Saddle-stitched binding is strictly restricted to N <= 64 pages (got N={total_pages}). "
            "For publications exceeding 64 pages, specify SMYTH_SEWN or PERFECT_BOUND."
        )

    caliper = max(0.0, float(paper_caliper_mm))
    g_draw = 0.0
    shingle = 0.0
    creep_offset = 0.0

    if canonical_btype == "LAY_FLAT":
        # Lay-flat board-mounted duplex leaves open 180 deg flat: zero spine draw, zero creep
        g_draw = 0.0
        creep_offset = 0.0
        shingle = 0.0
        inner_margin = base_inner_margin_mm
        outer_margin = max(base_outer_margin_mm, 5.0)

    elif canonical_btype == "SMYTH_SEWN":
        # Signature-sewn in signatures of S pages.
        # Creep is cyclical and resets at every signature boundary.
        g_draw = 0.0
        sig_s = max(2, int(signature_size))
        j = (page - 1) % sig_s
        leaf = min(j // 2, (sig_s // 2) - 1 - (j // 2))
        leaf = max(0, leaf)
        creep_offset = caliper * leaf
        shingle = creep_offset
        inner_margin = base_inner_margin_mm + creep_offset
        outer_margin = max(base_outer_margin_mm - creep_offset, 5.0)

    elif canonical_btype == "PERFECT_BOUND":
        # PUR adhesive binding adds spine clamp glue consumption G_draw
        g_draw = float(gutter_draw_mm)
        is_folded = folded_signature or b_type_raw in {"FOLDED_SIGNATURE_PUR", "PERFECT_BOUND_FOLDED"}

        if is_folded:
            # Folded-Signature PUR: shingling occurs strictly within each signature
            sig_s = max(2, int(signature_size))
            j = (page - 1) % sig_s
            leaf = min(j // 2, (sig_s // 2) - 1 - (j // 2))
            leaf = max(0, leaf)
            shingle = caliper * leaf
        else:
            # Single-Leaf Cut PUR: individual milled leaves have strictly zero shingle
            shingle = 0.0

        creep_offset = shingle
        inner_margin = base_inner_margin_mm + g_draw + shingle
        outer_margin = max(base_outer_margin_mm - shingle, 5.0)

    elif canonical_btype == "SADDLE_STITCHED":
        # Folded booklet nested sheets. Imposition symmetry guarantees recto and verso
        # of the same physical leaf have identical creep displacement:
        # leaf(p) = floor((p - 1) / 2)
        # Normalized relative to outermost wrap sheet:
        # delta_creep(p) = c * min(leaf, N // 2 - 1 - leaf)
        g_draw = 0.0
        leaf = (page - 1) // 2
        half_n = total_pages // 2
        leaf_depth = min(leaf, max(0, half_n - 1 - leaf))
        creep_offset = caliper * max(0, leaf_depth)
        shingle = creep_offset
        inner_margin = base_inner_margin_mm + creep_offset
        outer_margin = max(base_outer_margin_mm - creep_offset, 5.0)

    return {
        "page": page,
        "binding_type": canonical_btype,
        "inner_margin_mm": round(inner_margin, 4),
        "outer_margin_mm": round(outer_margin, 4),
        "shingle_mm": round(shingle, 4),
        "creep_offset_mm": round(creep_offset, 4),
        "delta_creep_mm": round(creep_offset, 4),
        "gutter_draw_mm": round(g_draw, 4),
    }


# Backward-compatible alias for test suites
calculate_creep = calculate_gutter_creep
