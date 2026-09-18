#!/usr/bin/env python3
"""
portfolio_forensic_linter.py
----------------------------
Automated Forensic Portfolio Audit & Tectonic Linter for Architecture & Design Portfolios.

Audits:
1. Antipattern #18: The Flattened Raster Print Trap (detects flattened Photoshop/Canva rasters).
2. Orientation & Rotation Inversion (detects 180° inverted drawings like Page 23 errors).
3. Typographic Placeholders & Display Misspellings (detects Lorem Ipsum, ADMINSTRATIVE, VISULAIZATION).
4. Aspect Ratio & Slide Dimensions (detects vertical boards pasted sideways into widescreen).
5. Preliminary Sara Bensalem Rubric Diagnostic Score.

Usage:
  python portfolio_forensic_linter.py <path_to_portfolio.pdf>
"""

import sys
import os
import json
import argparse
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("Error: PyMuPDF (fitz) is required. Install via 'pip install pymupdf'.")

# Common red-flag placeholders and orthographic typos observed across portfolios
KNOWN_TYPOS = [
    "lorem ipsum",
    "dolor sit amet",
    "insert text here",
    "adminstrative",
    "visulaization",
    "prespective",
    "detailes",
    "resraurant",
    "weigh of decision",
    "outdoor funiture",
    "[project name]",
    "[client]"
]

def audit_portfolio_pdf(pdf_path: str) -> Dict[str, Any]:
    if not os.path.exists(pdf_path):
        return {"error": f"File not found: {pdf_path}"}

    doc = fitz.open(pdf_path)
    file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    page_count = len(doc)
    metadata = doc.metadata or {}

    total_characters = 0
    pages_with_zero_text = 0
    total_images = 0
    page_aspect_ratios = []
    typos_found = []
    rotation_anomalies = []

    for page_idx in range(page_count):
        page = doc[page_idx]
        p_num = page_idx + 1
        rect = page.rect
        w, h = rect.width, rect.height
        aspect = w / max(1.0, h)
        page_aspect_ratios.append(aspect)

        # Check page rotation
        if page.rotation != 0:
            rotation_anomalies.append({
                "page": p_num,
                "rotation_deg": page.rotation,
                "note": f"Page {p_num} has non-zero rotation metadata ({page.rotation}°)"
            })

        # Text extraction
        text = page.get_text("text") or ""
        char_count = len(text.strip())
        total_characters += char_count

        if char_count == 0:
            pages_with_zero_text += 1

        # Check for known typos in extracted text
        text_lower = text.lower()
        for typo in KNOWN_TYPOS:
            if typo in text_lower:
                typos_found.append({
                    "page": p_num,
                    "matched_pattern": typo,
                    "context": text_lower[max(0, text_lower.find(typo)-30):min(len(text_lower), text_lower.find(typo)+40)].strip()
                })

        # Count images
        img_list = page.get_images(full=True)
        total_images += len(img_list)

    # Forensic Diagnosis
    is_flattened_raster = False
    flattened_reason = ""
    creator = metadata.get("creator", "").lower()
    producer = metadata.get("producer", "").lower()

    if "photoshop" in creator or "photoshop" in producer or "image conversion" in producer:
        if pages_with_zero_text / max(1, page_count) >= 0.8:
            is_flattened_raster = True
            flattened_reason = f"Flattened via Adobe Photoshop image conversion plug-in ({pages_with_zero_text}/{page_count} pages contain 0 selectable text)."
    elif pages_with_zero_text / max(1, page_count) >= 0.9 and total_images >= page_count:
        is_flattened_raster = True
        flattened_reason = f"{pages_with_zero_text}/{page_count} pages have 0 selectable vector text; CAD drawings are rasterized."

    # Estimate score deductions
    deductions = []
    initial_score = 90.0

    if is_flattened_raster:
        deductions.append((-10.0, "Antipattern #18: The Flattened Raster Print Trap (unselectable text, blurred CAD lines)"))
        initial_score -= 10.0

    if typos_found:
        pen = min(15.0, len(typos_found) * 5.0)
        deductions.append((-pen, f"Placeholders / Display Typos found ({len(typos_found)} occurrences)"))
        initial_score -= pen

    if file_size_mb > 50.0:
        deductions.append((-5.0, f"Excessive file weight ({file_size_mb:.1f} MB > 50 MB threshold)"))
        initial_score -= 5.0

    if page_count > 60:
        deductions.append((-5.0, f"Uncurated portfolio length ({page_count} pages > 60 pages)"))
        initial_score -= 5.0
    elif page_count < 10:
        deductions.append((-10.0, f"Insufficient depth ({page_count} pages < 10 pages)"))
        initial_score -= 10.0

    avg_aspect = sum(page_aspect_ratios) / max(1, len(page_aspect_ratios))
    aspect_inconsistencies = [
        f"Page {i+1} aspect {ar:.2f} differs from avg {avg_aspect:.2f}"
        for i, ar in enumerate(page_aspect_ratios)
        if abs(ar - avg_aspect) > 0.25
    ]

    return {
        "pdf_path": pdf_path,
        "page_count": page_count,
        "file_size_mb": round(file_size_mb, 2),
        "creator": metadata.get("creator", "Unknown"),
        "producer": metadata.get("producer", "Unknown"),
        "total_extracted_characters": total_characters,
        "pages_with_zero_text": pages_with_zero_text,
        "total_raster_images": total_images,
        "is_flattened_raster_trap": is_flattened_raster,
        "flattened_reason": flattened_reason,
        "typos_detected": typos_found,
        "rotation_anomalies": rotation_anomalies,
        "aspect_ratio_inconsistencies": aspect_inconsistencies[:5],
        "estimated_base_score": max(30.0, round(initial_score, 1)),
        "deductions": deductions,
        "verdict": "FLAGGED_FOR_RESCUE" if (is_flattened_raster or typos_found or initial_score < 75) else "CLEAN"
    }

def print_audit_report(result: Dict[str, Any]):
    print("=" * 76)
    print("ANTIGRAVITY AUTONOMOUS PORTFOLIO FORENSIC LINTER REPORT")
    print("=" * 76)
    print(f"File: {os.path.basename(result.get('pdf_path', ''))}")
    print(f"Pages: {result.get('page_count')} | Size: {result.get('file_size_mb')} MB")
    print(f"Creator: {result.get('creator')} | Producer: {result.get('producer')}")
    print("-" * 76)

    if result.get("is_flattened_raster_trap"):
        print("[CRITICAL RED FLAG] ANTIPATTERN #18 DETECTED: The Flattened Raster Print Trap")
        print(f"  -> {result.get('flattened_reason')}")
        print("  -> Impact: Zero selectable vector text, CAD lines pixelated, fails automated ATS.")
    else:
        print("[OK] Vector text layer detected.")

    if result.get("typos_detected"):
        print(f"\n[TYPOS & PLACEHOLDERS] {len(result.get('typos_detected'))} Found:")
        for t in result["typos_detected"]:
            print(f"  * Page {t['page']}: '{t['matched_pattern']}' (Context: ...{t['context']}...)")

    if result.get("rotation_anomalies"):
        print(f"\n[ROTATION ANOMALIES]:")
        for r in result["rotation_anomalies"]:
            print(f"  * Page {r['page']}: {r['note']}")

    if result.get("aspect_ratio_inconsistencies"):
        print(f"\n[ASPECT RATIO INCONSISTENCIES]:")
        for a in result["aspect_ratio_inconsistencies"]:
            print(f"  * {a}")

    print("-" * 76)
    print(f"Estimated Base Score: {result.get('estimated_base_score')} / 100")
    print(f"Deductions:")
    for pts, reason in result.get("deductions", []):
        print(f"  {pts:+4.1f} pts : {reason}")
    print(f"Final Forensic Verdict: {result.get('verdict')}")
    print("=" * 76)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Portfolio Forensic Linter")
    parser.add_argument("pdf", help="Path to portfolio PDF")
    args = parser.parse_args()

    res = audit_portfolio_pdf(args.pdf)
    print_audit_report(res)
