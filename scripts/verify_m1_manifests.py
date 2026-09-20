#!/usr/bin/env python3
"""
Stand-alone Forensic Verification Script for Milestone 1:
Validates and stress-tests:
1. gemini_manifest.json schema, duplicate keys, trailing commas, path resolution, and file existence.
2. skills/*/manifest.json schema, duplicate keys, trailing commas, commands, and entrypoint existence.
3. Existence and integrity of all 10 SKILL.md files.
4. Total eradication of obsolete duplicate directories (skills/portfolio-design).
"""

import sys
import os
import re
import json
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(PROJECT_ROOT, "skills")
GEMINI_MANIFEST_PATH = os.path.join(PROJECT_ROOT, "gemini_manifest.json")

CANONICAL_SKILLS = [
    "bioclimatic-flows",
    "constructive-detail",
    "design-md-extractor",
    "editorial-studio",
    "grill-my-design",
    "interior-joinery",
    "portfolio-monograph",
    "spatial-anatomy",
    "spatial-choreography",
    "spatial-stitch",
]


def check_no_trailing_commas(raw_json_str: str) -> None:
    chars = []
    in_string = False
    escape = False
    for ch in raw_json_str:
        if escape:
            escape = False
            continue
        if ch == '\\' and in_string:
            escape = True
            continue
        if ch == '"':
            if in_string:
                chars.append('"x"')
                in_string = False
            else:
                in_string = True
            continue
        if not in_string:
            chars.append(ch)

    stripped = "".join(chars)
    match = re.search(r',(\s*[}\]])', stripped)
    if match:
        idx = match.start()
        line_no = raw_json_str[:idx].count('\n') + 1
        col_no = idx - raw_json_str[:idx].rfind('\n')
        target_char = match.group(1).strip()
        raise ValueError(f"Trailing comma detected at line {line_no}, col {col_no} before '{target_char}'")


def load_json_strict(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()

    check_no_trailing_commas(raw)

    def detect_duplicate_keys(pairs):
        res = {}
        for k, v in pairs:
            if k in res:
                raise ValueError(f"Duplicate key '{k}' found in {file_path}")
            res[k] = v
        return res

    return json.loads(raw, object_pairs_hook=detect_duplicate_keys)


def verify_gemini_manifest() -> List[str]:
    errors = []
    print(f"[*] Checking gemini_manifest.json at: {GEMINI_MANIFEST_PATH}")
    if not os.path.isfile(GEMINI_MANIFEST_PATH):
        return [f"gemini_manifest.json missing at {GEMINI_MANIFEST_PATH}"]

    try:
        data = load_json_strict(GEMINI_MANIFEST_PATH)
    except Exception as e:
        return [f"gemini_manifest.json strict load failed: {e}"]

    if not isinstance(data, list):
        return ["gemini_manifest.json root must be a list"]

    if len(data) != 11:
        errors.append(f"Expected exactly 11 entries in gemini_manifest.json (1 research + 10 skills), found {len(data)}")

    # Index 0: research
    if data:
        r0 = data[0]
        if r0.get("artifact_type") != "deep_research":
            errors.append(f"Entry 0 artifact_type is '{r0.get('artifact_type')}', expected 'deep_research'")
        for f in r0.get("files", []):
            if not os.path.exists(f.get("path", "")):
                errors.append(f"Research file not found on disk: {f.get('path')}")

    # Index 1..10: skills
    skill_entries = [d for d in data if d.get("artifact_type") == "architectural_skill"]
    if len(skill_entries) != 10:
        errors.append(f"Expected 10 architectural skills, found {len(skill_entries)}")

    found_skills = [s.get("name") for s in skill_entries]
    if sorted(found_skills) != sorted(CANONICAL_SKILLS):
        errors.append(f"Skill name set mismatch: {sorted(found_skills)} != {sorted(CANONICAL_SKILLS)}")

    required_keys = {
        "skill_id", "artifact_type", "name", "display_name",
        "version", "scale_continuum", "path", "description",
        "author", "mcp_tools", "cli_commands", "files"
    }

    for s in skill_entries:
        sname = s.get("name", "UNKNOWN")
        missing = required_keys - set(s.keys())
        if missing:
            errors.append(f"Skill '{sname}' missing keys: {missing}")

        spath = os.path.join(PROJECT_ROOT, s.get("path", ""))
        if not os.path.isdir(spath):
            errors.append(f"Skill '{sname}' path does not exist: {spath}")

        for f in s.get("files", []):
            fpath = os.path.join(PROJECT_ROOT, f.get("path", ""))
            if not os.path.isfile(fpath):
                errors.append(f"Skill '{sname}' file not found: {fpath}")

        for cmd in s.get("cli_commands", []):
            cmd_str = cmd.get("command", "")
            parts = cmd_str.split()
            if len(parts) >= 2 and parts[0] == "python":
                sc_abs = os.path.join(PROJECT_ROOT, parts[1])
                if not os.path.isfile(sc_abs):
                    errors.append(f"Skill '{sname}' CLI script missing: {sc_abs}")

    return errors


def verify_skill_manifests() -> List[str]:
    errors = []
    print(f"[*] Checking 10 individual skill manifests in: {SKILLS_DIR}")

    for s in CANONICAL_SKILLS:
        mpath = os.path.join(SKILLS_DIR, s, "manifest.json")
        if not os.path.isfile(mpath):
            errors.append(f"Missing manifest.json for skill '{s}'")
            continue
        try:
            mdata = load_json_strict(mpath)
        except Exception as e:
            errors.append(f"Skill '{s}' manifest parse failure: {e}")
            continue

        if not isinstance(mdata, dict):
            errors.append(f"Skill '{s}' manifest is not a JSON object")
            continue

        if mdata.get("name") != s:
            errors.append(f"Skill '{s}' manifest name mismatch: '{mdata.get('name')}' != '{s}'")

        if not mdata.get("description"):
            errors.append(f"Skill '{s}' manifest missing non-empty description")

        if "entrypoint" in mdata:
            ep_path = os.path.join(SKILLS_DIR, s, mdata["entrypoint"])
            if not os.path.isfile(ep_path):
                errors.append(f"Skill '{s}' entrypoint missing on disk: {ep_path}")

        if "commands" in mdata and isinstance(mdata["commands"], list):
            for cmd in mdata["commands"]:
                if isinstance(cmd, str) and cmd.startswith("python "):
                    parts = cmd.split()
                    sc_path = os.path.join(PROJECT_ROOT, parts[1])
                    if not os.path.isfile(sc_path):
                        errors.append(f"Skill '{s}' manifest command script missing: {sc_path}")

    return errors


def verify_skills_markdown() -> List[str]:
    errors = []
    print(f"[*] Verifying SKILL.md for all 10 skills...")

    for s in CANONICAL_SKILLS:
        smd = os.path.join(SKILLS_DIR, s, "SKILL.md")
        if not os.path.isfile(smd):
            errors.append(f"Missing SKILL.md for skill '{s}'")
            continue
        with open(smd, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if len(content) < 200:
            errors.append(f"SKILL.md for '{s}' too short ({len(content)} chars)")
        if not (content.startswith("#") or content.startswith("---")):
            errors.append(f"SKILL.md for '{s}' does not start with heading or YAML frontmatter")

    return errors


def verify_no_obsolete_duplicates() -> List[str]:
    errors = []
    print(f"[*] Verifying absence of obsolete directories...")
    dup = os.path.join(SKILLS_DIR, "portfolio-design")
    if os.path.exists(dup):
        errors.append(f"Duplicate directory '{dup}' still exists")

    actual = sorted([d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))])
    if actual != CANONICAL_SKILLS:
        errors.append(f"skills/ contents mismatch: {actual} vs {CANONICAL_SKILLS}")

    return errors


def main():
    print("=" * 70)
    print("Milestone 1 Manifest & Skill Integrity Verification Harness")
    print("=" * 70)

    all_errors = []
    all_errors.extend(verify_gemini_manifest())
    all_errors.extend(verify_skill_manifests())
    all_errors.extend(verify_skills_markdown())
    all_errors.extend(verify_no_obsolete_duplicates())

    print("-" * 70)
    if all_errors:
        print(f"VERIFICATION FAILED: {len(all_errors)} error(s) detected:")
        for err in all_errors:
            print(f"  [!] {err}")
        sys.exit(1)
    else:
        print("ALL VERIFICATIONS PASSED: 100% compliant with M1 specifications.")
        print(f"  - gemini_manifest.json: VALID (10/10 skills + research entry, strict RFC 8259)")
        print(f"  - individual manifests: 10/10 present and valid")
        print(f"  - SKILL.md documents:   10/10 present and validated")
        print(f"  - File references:      All resolved on disk")
        print(f"  - Duplicate cleanup:    skills/portfolio-design verified eradicated")
        sys.exit(0)


if __name__ == "__main__":
    main()
