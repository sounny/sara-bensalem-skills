#!/usr/bin/env python3
"""
Repacks web/sara-bensalem-skills.zip with the complete canonical 10 architectural skills,
mcp-server, operational CLI scripts, tests, and documentation.
"""
import os
import zipfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP_PATH = os.path.join(BASE_DIR, "web", "sara-bensalem-skills.zip")

EXCLUDED_DIRS = {"__pycache__", ".git", ".pytest_cache", "venv", ".venv", "node_modules", ".agents"}
EXCLUDED_EXTS = {".pyc", ".pyo", ".tmp", ".DS_Store"}

def repack():
    print(f"Repacking {ZIP_PATH}...")
    include_dirs = ["skills", "mcp-server", "scripts", "tests", "docs"]
    include_files = ["README.md", "gemini_manifest.json"]

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for d in include_dirs:
            dir_path = os.path.join(BASE_DIR, d)
            if not os.path.exists(dir_path):
                continue
            for root, dirs, files in os.walk(dir_path):
                # Filter out excluded directory trees in-place
                dirs[:] = [sub for sub in dirs if sub not in EXCLUDED_DIRS]
                for f in files:
                    ext = os.path.splitext(f)[1]
                    if ext in EXCLUDED_EXTS or f.startswith("."):
                        continue
                    full_path = os.path.join(root, f)
                    arcname = os.path.relpath(full_path, BASE_DIR).replace("\\", "/")
                    zf.write(full_path, arcname)

        for f_name in include_files:
            f_path = os.path.join(BASE_DIR, f_name)
            if os.path.exists(f_path):
                zf.write(f_path, f_name)

    size_kb = os.path.getsize(ZIP_PATH) / 1024
    print(f"Repacking complete. Archive size: {size_kb:.1f} KB")

if __name__ == "__main__":
    repack()
