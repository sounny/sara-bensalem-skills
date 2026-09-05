#!/usr/bin/env python3
"""
Repacks web/sara-bensalem-skills.zip with the latest updated skills and mcp-server.
"""
import os
import zipfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP_PATH = os.path.join(BASE_DIR, "web", "sara-bensalem-skills.zip")

def repack():
    print(f"Repacking {ZIP_PATH}...")
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # Add skills
        skills_dir = os.path.join(BASE_DIR, "skills")
        for root, dirs, files in os.walk(skills_dir):
            if "__pycache__" in root or ".git" in root:
                continue
            for f in files:
                if f.endswith(".pyc") or f.endswith(".tmp"):
                    continue
                full_path = os.path.join(root, f)
                arcname = os.path.relpath(full_path, BASE_DIR).replace("\\", "/")
                zf.write(full_path, arcname)
                
        # Add mcp-server
        mcp_dir = os.path.join(BASE_DIR, "mcp-server")
        for root, dirs, files in os.walk(mcp_dir):
            if "__pycache__" in root or ".git" in root:
                continue
            for f in files:
                if f.endswith(".pyc") or f.endswith(".tmp"):
                    continue
                full_path = os.path.join(root, f)
                arcname = os.path.relpath(full_path, BASE_DIR).replace("\\", "/")
                zf.write(full_path, arcname)

        # Add README.md
        readme_path = os.path.join(BASE_DIR, "README.md")
        if os.path.exists(readme_path):
            zf.write(readme_path, "README.md")

    size_kb = os.path.getsize(ZIP_PATH) / 1024
    print(f"Repacking complete. Archive size: {size_kb:.1f} KB")

if __name__ == "__main__":
    repack()
