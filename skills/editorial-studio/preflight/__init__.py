"""
preflight package - Automated Preflight Validation & Vision-in-the-Loop Engine
Editorial Studio Publishing System (Milestone 5)

Exports:
- PublicationAuditor: Master engine class
- StandalonePreflightAuditor: Alias for engine
- audit_pdf: High-level auditing function
- main: CLI entry point
- Preflight calculation helpers
"""

from .audit_publication import (
    PublicationAuditor,
    StandalonePreflightAuditor,
    audit_pdf,
    main,
    check_aabb_intersection,
    compute_contrast_ratio,
    evaluate_text_image_collision,
    calculate_tac_for_image_bytes,
    evaluate_image_resolution,
    MM_TO_PT,
    SUBSET_REGEX
)

from .icc import (
    load_profile_metadata,
    get_tac_limit,
    FOGRA51_METADATA,
    FOGRA52_METADATA
)

__all__ = [
    "PublicationAuditor",
    "StandalonePreflightAuditor",
    "audit_pdf",
    "main",
    "check_aabb_intersection",
    "compute_contrast_ratio",
    "evaluate_text_image_collision",
    "calculate_tac_for_image_bytes",
    "evaluate_image_resolution",
    "MM_TO_PT",
    "SUBSET_REGEX",
    "load_profile_metadata",
    "get_tac_limit",
    "FOGRA51_METADATA",
    "FOGRA52_METADATA"
]
