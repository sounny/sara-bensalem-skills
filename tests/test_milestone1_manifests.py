#!/usr/bin/env python3
"""
Test Suite for Milestone 1 Manifest Verification and Stress-Testing
Validates:
1. gemini_manifest.json syntax, duplicate keys, trailing commas, and full schema conformance
2. skills/*/manifest.json syntax, duplicate keys, trailing commas, and schema conformance
3. File and directory resolution for all 10 canonical skills and their SKILL.md
4. Resolution of all CLI commands and script paths referenced across manifests
5. Absence of obsolete duplicate directories (skills/portfolio-design)
6. Mutation stress testing (negative test oracle)
"""

import os
import re
import json
import unittest

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
    """
    Scans raw JSON string for trailing commas before } or ] outside of quoted strings.
    Raises ValueError if a trailing comma is found.
    """
    # Replace all string literals with a dummy token '"x"' to preserve value presence without string commas
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
                # closing quote: output dummy token
                chars.append('"x"')
                in_string = False
            else:
                # opening quote
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
    """
    Loads JSON file verifying:
    - Strict UTF-8 decoding
    - No trailing commas
    - No duplicate keys in objects
    """
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


class TestManifestSyntaxAndSchemas(unittest.TestCase):
    """Rigorous schema and syntax testing of gemini_manifest.json and skills/*/manifest.json."""

    def test_gemini_manifest_exists_and_syntax(self):
        """Verify gemini_manifest.json exists, parses cleanly, and has no trailing commas."""
        self.assertTrue(os.path.isfile(GEMINI_MANIFEST_PATH), "gemini_manifest.json must exist")
        data = load_json_strict(GEMINI_MANIFEST_PATH)
        self.assertIsInstance(data, list, "Root of gemini_manifest.json must be a list")

    def test_gemini_manifest_research_entry(self):
        """Verify the legacy research entry at index 0."""
        data = load_json_strict(GEMINI_MANIFEST_PATH)
        first = data[0]
        self.assertEqual(first.get("task"), "deep_research_Comprehensive Taxonomy of Arch")
        self.assertEqual(first.get("artifact_type"), "deep_research")
        self.assertIn("files", first)
        self.assertIsInstance(first["files"], list)
        for f in first["files"]:
            fpath = f.get("path")
            # In CI or local test environments, the absolute path might not match the original absolute path
            # But the file is in the repo under docs/
            filename = fpath.split("\\")[-1]
            local_path = os.path.join(os.path.dirname(__file__), "..", "docs", filename)
            self.assertTrue(os.path.exists(local_path), f"Referenced research file does not exist locally: {local_path}")

    def test_gemini_manifest_contains_all_10_skills(self):
        """Verify gemini_manifest.json registers all 10 canonical architectural skills."""
        data = load_json_strict(GEMINI_MANIFEST_PATH)
        skill_entries = [item for item in data if item.get("artifact_type") == "architectural_skill"]
        self.assertEqual(len(skill_entries), 10, f"Expected 10 architectural skills, found {len(skill_entries)}")

        registered_ids = [s.get("skill_id") for s in skill_entries]
        registered_names = [s.get("name") for s in skill_entries]

        self.assertEqual(sorted(registered_ids), sorted(CANONICAL_SKILLS))
        self.assertEqual(sorted(registered_names), sorted(CANONICAL_SKILLS))

    def test_gemini_manifest_skill_schema_fields(self):
        """Verify all required schema fields for each architectural skill in gemini_manifest.json."""
        data = load_json_strict(GEMINI_MANIFEST_PATH)
        skill_entries = [item for item in data if item.get("artifact_type") == "architectural_skill"]

        required_keys = {
            "skill_id", "artifact_type", "name", "display_name",
            "version", "scale_continuum", "path", "description",
            "author", "mcp_tools", "cli_commands", "files"
        }

        for skill in skill_entries:
            skill_name = skill.get("name", "UNKNOWN")
            missing = required_keys - set(skill.keys())
            self.assertEqual(len(missing), 0, f"Skill '{skill_name}' is missing keys: {missing}")

            # Validate types and non-empty values
            self.assertTrue(isinstance(skill["skill_id"], str) and skill["skill_id"].strip())
            self.assertTrue(isinstance(skill["display_name"], str) and skill["display_name"].strip())
            self.assertTrue(isinstance(skill["version"], str) and skill["version"].strip())
            self.assertTrue(isinstance(skill["scale_continuum"], str) and skill["scale_continuum"].strip())
            self.assertTrue(isinstance(skill["description"], str) and len(skill["description"].strip()) > 30)
            self.assertTrue(isinstance(skill["author"], str) and skill["author"].strip())
            self.assertIsInstance(skill["mcp_tools"], list)
            self.assertGreater(len(skill["mcp_tools"]), 0, f"Skill '{skill_name}' has empty mcp_tools")
            self.assertIsInstance(skill["cli_commands"], list)
            self.assertGreater(len(skill["cli_commands"]), 0, f"Skill '{skill_name}' has empty cli_commands")
            self.assertIsInstance(skill["files"], list)
            self.assertGreater(len(skill["files"]), 0, f"Skill '{skill_name}' has empty files")

    def test_gemini_manifest_paths_and_files_exist_on_disk(self):
        """Verify every directory, script, and file referenced in gemini_manifest.json exists."""
        data = load_json_strict(GEMINI_MANIFEST_PATH)
        skill_entries = [item for item in data if item.get("artifact_type") == "architectural_skill"]

        for skill in skill_entries:
            skill_name = skill["name"]
            # Check skill path
            skill_path = os.path.join(PROJECT_ROOT, skill["path"])
            self.assertTrue(os.path.isdir(skill_path), f"Skill dir '{skill_path}' does not exist for {skill_name}")

            # Check files array
            for f in skill["files"]:
                fpath = os.path.join(PROJECT_ROOT, f["path"])
                self.assertTrue(os.path.isfile(fpath), f"File referenced in gemini_manifest does not exist: {fpath}")

            # Check cli_commands scripts
            for cmd_obj in skill["cli_commands"]:
                cmd_str = cmd_obj.get("command", "")
                # Pattern: python <script_path> ...
                parts = cmd_str.split()
                if len(parts) >= 2 and parts[0] == "python":
                    script_rel = parts[1]
                    script_abs = os.path.join(PROJECT_ROOT, script_rel)
                    self.assertTrue(
                        os.path.isfile(script_abs),
                        f"CLI script does not exist on disk: {script_abs} (from '{cmd_str}')"
                    )

    def test_all_10_skill_manifests_exist_and_validate(self):
        """Verify every canonical skill has a valid manifest.json without trailing commas or duplicate keys."""
        for skill_name in CANONICAL_SKILLS:
            mpath = os.path.join(SKILLS_DIR, skill_name, "manifest.json")
            self.assertTrue(os.path.isfile(mpath), f"Missing manifest.json for skill '{skill_name}' at {mpath}")
            data = load_json_strict(mpath)
            self.assertIsInstance(data, dict, f"manifest.json for '{skill_name}' must be a JSON object")

            # Validate mandatory keys
            self.assertIn("name", data, f"Skill '{skill_name}' manifest missing 'name'")
            self.assertEqual(data["name"], skill_name, f"Manifest 'name' mismatch: {data['name']} vs {skill_name}")
            self.assertIn("description", data, f"Skill '{skill_name}' manifest missing 'description'")
            self.assertTrue(len(data["description"].strip()) > 15)

            # Check entrypoint if declared
            if "entrypoint" in data:
                ep = data["entrypoint"]
                ep_abs = os.path.join(SKILLS_DIR, skill_name, ep)
                self.assertTrue(os.path.isfile(ep_abs), f"Entrypoint {ep_abs} declared in {skill_name} not found")

            # Check commands if declared
            if "commands" in data and isinstance(data["commands"], list):
                for cmd in data["commands"]:
                    if isinstance(cmd, str) and cmd.startswith("python "):
                        parts = cmd.split()
                        script_rel = parts[1]
                        script_abs = os.path.join(PROJECT_ROOT, script_rel)
                        self.assertTrue(os.path.isfile(script_abs), f"Command script {script_abs} not found on disk")

    def test_all_10_skills_have_valid_skill_md(self):
        """Verify all 10 canonical skills have non-empty, well-formed SKILL.md files."""
        for skill_name in CANONICAL_SKILLS:
            skill_md_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
            self.assertTrue(os.path.isfile(skill_md_path), f"Missing SKILL.md for '{skill_name}' at {skill_md_path}")
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertGreaterEqual(len(content.strip()), 200, f"SKILL.md for '{skill_name}' is too short")
            # Ensure it contains either frontmatter or level 1 heading
            has_heading = content.startswith("#") or "---" in content[:20]
            self.assertTrue(has_heading, f"SKILL.md for '{skill_name}' missing markdown header or frontmatter")

    def test_obsolete_duplicate_directories_removed(self):
        """Verify that skills/portfolio-design was cleanly removed and skills/ has exactly 10 directories."""
        obsolete_path = os.path.join(SKILLS_DIR, "portfolio-design")
        self.assertFalse(os.path.exists(obsolete_path), "skills/portfolio-design duplicate directory must not exist")

        actual_dirs = sorted([d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))])
        self.assertEqual(actual_dirs, CANONICAL_SKILLS, "skills/ directory contents do not match canonical 10 skills")

    def test_stress_trailing_comma_oracle(self):
        """Negative test oracle: verify that check_no_trailing_commas detects mutations."""
        valid_json = '{"name": "test", "items": [1, 2, 3]}'
        # Should pass
        check_no_trailing_commas(valid_json)

        # Trailing comma in array
        bad_arr = '{"name": "test", "items": [1, 2, 3, ]}'
        with self.assertRaises(ValueError):
            check_no_trailing_commas(bad_arr)

        # Trailing comma in object
        bad_obj = '{"name": "test", "items": [1, 2, 3], }'
        with self.assertRaises(ValueError):
            check_no_trailing_commas(bad_obj)

        # Comma inside string should NOT trigger
        str_with_comma = '{"name": "test, not trailing, ", "items": [1, 2]}'
        check_no_trailing_commas(str_with_comma)


if __name__ == "__main__":
    unittest.main(verbosity=2)
