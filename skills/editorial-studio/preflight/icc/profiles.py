"""
preflight/icc/profiles.py
ICC Color Profile Metadata Definitions for FOGRA51 and FOGRA52.
ISO 12647-2:2013 Characterization standards for prepress publication auditing.
"""

import os
import json
from typing import Dict, Any, Optional

ICC_DIR = os.path.dirname(os.path.abspath(__file__))

def load_profile_metadata(profile_name: str) -> Dict[str, Any]:
    """
    Loads JSON metadata for standard ICC profiles (FOGRA51, FOGRA52).
    """
    canonical_name = profile_name.strip().lower()
    if "51" in canonical_name or "coated" in canonical_name:
        filename = "fogra51.json"
    elif "52" in canonical_name or "uncoated" in canonical_name:
        filename = "fogra52.json"
    else:
        filename = "fogra51.json"

    filepath = os.path.join(ICC_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

FOGRA51_METADATA = load_profile_metadata("FOGRA51")
FOGRA52_METADATA = load_profile_metadata("FOGRA52")

def get_tac_limit(profile_name: str, fallback: float = 320.0) -> float:
    """Returns the absolute maximum TAC allowed for the profile."""
    meta = load_profile_metadata(profile_name)
    return meta.get("tac_limits", {}).get("absolute_max_percent", fallback)
