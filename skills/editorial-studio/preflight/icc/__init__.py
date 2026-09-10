"""
preflight/icc package
Provides ICC color profile definitions and metadata for FOGRA51 / PSO Coated v3
and FOGRA52 / PSO Uncoated v3.
"""

from .profiles import (
    load_profile_metadata,
    get_tac_limit,
    FOGRA51_METADATA,
    FOGRA52_METADATA,
    ICC_DIR
)

__all__ = [
    "load_profile_metadata",
    "get_tac_limit",
    "FOGRA51_METADATA",
    "FOGRA52_METADATA",
    "ICC_DIR"
]
