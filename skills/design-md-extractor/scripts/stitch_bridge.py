#!/usr/bin/env python3
"""
stitch_bridge.py
Antigravity Stitch MCP Integration Bridge

Loads an extracted DESIGN.md file, generates the base64 payload required by
Stitch MCP (upload_design_md), and prepares the RPC request payloads for:
1. upload_design_md
2. create_design_system_from_design_md
3. create_design_system
"""

import os
import sys
import json
import base64
import argparse
from pathlib import Path

def prepare_stitch_payloads(design_md_path, project_id=None, ds_json_path=None):
    if not os.path.exists(design_md_path):
        raise FileNotFoundError(f"DESIGN.md not found: {design_md_path}")

    with open(design_md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Encode to UTF-8 base64
    b64_encoded = base64.b64encode(md_content.encode("utf-8")).decode("utf-8")

    # Load design-system.json if available
    ds_data = None
    if ds_json_path and os.path.exists(ds_json_path):
        with open(ds_json_path, "r", encoding="utf-8") as f:
            ds_data = json.load(f)
    else:
        # Check sibling directory
        sibling_ds = Path(design_md_path).parent / "design-system.json"
        if sibling_ds.exists():
            with open(sibling_ds, "r", encoding="utf-8") as f:
                ds_data = json.load(f)

    # Payload 1: upload_design_md
    upload_payload = {
        "projectId": project_id or "TARGET_PROJECT_ID",
        "designMdBase64": b64_encoded
    }

    # Payload 2: create_design_system (alternative direct API)
    create_ds_payload = None
    if ds_data:
        create_ds_payload = {
            "projectId": project_id or "TARGET_PROJECT_ID",
            "designSystem": {
                "displayName": ds_data.get("displayName", "Extracted Design System"),
                "theme": ds_data.get("theme", {})
            }
        }
        # Embed raw designMd markdown in theme
        create_ds_payload["designSystem"]["theme"]["designMd"] = md_content

    return {
        "upload_design_md": upload_payload,
        "create_design_system": create_ds_payload,
        "design_md_length_bytes": len(md_content.encode("utf-8")),
        "base64_length_chars": len(b64_encoded)
    }

def main():
    parser = argparse.ArgumentParser(description="Antigravity Stitch MCP Payload Bridge")
    parser.add_argument("design_md", help="Path to DESIGN.md file")
    parser.add_argument("--project-id", "-p", default=None, help="Google Stitch Project ID")
    parser.add_argument("--json", action="store_true", help="Output full JSON payloads")
    args = parser.parse_args()

    payloads = prepare_stitch_payloads(args.design_md, project_id=args.project_id)

    if args.json:
        print(json.dumps(payloads, indent=2))
    else:
        print("=" * 72)
        print(" ANTIGRAVITY GOOGLE STITCH BRIDGE")
        print("=" * 72)
        print(f"DESIGN.md Size:   {payloads['design_md_length_bytes']} bytes")
        print(f"Base64 Char Len:  {payloads['base64_length_chars']} chars")
        print("-" * 72)
        print("Step 1: Upload to Google Stitch MCP:")
        print("Call MCP Tool: stitch:upload_design_md")
        print(f"Arguments: {{ 'projectId': '{args.project_id or '<PROJECT_ID>'}', 'designMdBase64': '<BASE64_STRING>' }}")
        print("-" * 72)
        print("Step 2: Generate Design System in Stitch:")
        print("Call MCP Tool: stitch:create_design_system_from_design_md")
        print("=" * 72)

if __name__ == "__main__":
    main()
