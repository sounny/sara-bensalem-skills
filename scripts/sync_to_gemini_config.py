#!/usr/bin/env python3
"""
Syncs updated skills from g:/My Drive/Projects/sara-bensalem-skills/skills
to C:/Users/sounn/.gemini/config/skills.
"""
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_SKILLS = os.path.join(BASE_DIR, "skills")
TARGET_SKILLS = os.path.normpath(r"C:\Users\sounn\.gemini\config\skills")

SKILL_MAPPINGS = {
    "portfolio-monograph": "portfolio-monograph",
    "portfolio-design": "sara-bensalem-portfolio-design",
    "constructive-detail": "constructive-detail",
    "spatial-anatomy": "spatial-anatomy",
    "bioclimatic-flows": "bioclimatic-flows",
    "interior-joinery": "interior-joinery",
    "grill-my-design": "grill-my-design",
    "spatial-stitch": "spatial-stitch"
}

def sync_skills():
    print(f"Syncing skills from {PROJECT_SKILLS} to {TARGET_SKILLS}...")
    for src_name, dst_name in SKILL_MAPPINGS.items():
        src_path = os.path.join(PROJECT_SKILLS, src_name)
        dst_path = os.path.join(TARGET_SKILLS, dst_name)
        if not os.path.exists(src_path):
            print(f"Warning: Source skill {src_path} does not exist. Skipping.")
            continue
        
        # Ensure destination dir exists
        os.makedirs(dst_path, exist_ok=True)
        
        # Walk and copy files, ignoring __pycache__ and git
        for root, dirs, files in os.walk(src_path):
            if "__pycache__" in root or ".git" in root:
                continue
            rel_path = os.path.relpath(root, src_path)
            target_subdir = os.path.join(dst_path, rel_path)
            os.makedirs(target_subdir, exist_ok=True)
            for f in files:
                if f.endswith(".pyc") or f.endswith(".tmp"):
                    continue
                src_file = os.path.join(root, f)
                dst_file = os.path.join(target_subdir, f)
                shutil.copy2(src_file, dst_file)
        print(f"Synchronized: {src_name} -> {dst_name}")

    print("All skills successfully synchronized to Gemini config.")

if __name__ == "__main__":
    sync_skills()
