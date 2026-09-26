#!/usr/bin/env python3
"""
Sara Bensalem Skills — 100-Point Portfolio Audit Engine (2026 Enhanced Edition)
Performs automated structural and spatial audit of architectural and spatial design portfolios
against the 100-Point Rubric, detecting "render traps", scalar disconnects, and layout friction.
Author: Sara Bensalem <sara@sarabensalem.com>
Strasbourg Atelier [48°35'05"N 07°45'02"E]
Website: https://skills.sarabensalem.com
"""

import sys
import os
import json
import argparse
import re

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

def audit_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        return {
            "filename": os.path.basename(pdf_path) if pdf_path else "",
            "file_size_mb": 0.0,
            "status": "error",
            "error": f"File not found: {pdf_path}",
            "verdict": "FILE_NOT_FOUND",
            "total_score": 0,
            "overall_score": 0,
            "score": 0
        }
    
    file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    filename = os.path.basename(pdf_path)

    if os.path.getsize(pdf_path) == 0:
        return {
            "filename": filename,
            "file_size_mb": 0.0,
            "status": "error",
            "error": "Empty file (0 bytes). Not a valid PDF.",
            "verdict": "INVALID_PDF",
            "total_score": 0,
            "overall_score": 0,
            "score": 0
        }
    
    if not fitz:
        return {
            "filename": filename,
            "file_size_mb": round(file_size_mb, 2),
            "status": "error",
            "error": "PyMuPDF (fitz) required for geometry extraction.",
            "message": "PyMuPDF (fitz) required for geometry extraction.",
            "verdict": "DEPENDENCY_MISSING",
            "total_score": 0,
            "overall_score": 0,
            "score": 0
        }
        
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        return {
            "filename": filename,
            "file_size_mb": round(file_size_mb, 2),
            "status": "error",
            "error": f"Corrupted or invalid PDF: {str(e)}",
            "verdict": "INVALID_OR_CORRUPT_PDF",
            "total_score": 0,
            "overall_score": 0,
            "score": 0
        }

    try:
        if doc.is_encrypted:
            auth_ok = doc.authenticate("")
            if not auth_ok and doc.needs_pass:
                return {
                    "filename": filename,
                    "file_size_mb": round(file_size_mb, 2),
                    "status": "error",
                    "error": "Password-protected PDF. Decryption required.",
                    "verdict": "PASSWORD_PROTECTED_PDF",
                    "total_score": 0,
                    "overall_score": 0,
                    "score": 0
                }

        page_count = len(doc)
        if page_count == 0:
            return {
                "filename": filename,
                "file_size_mb": round(file_size_mb, 2),
                "status": "error",
                "error": "PDF contains 0 pages.",
                "verdict": "EMPTY_DOCUMENT",
                "total_score": 0,
                "overall_score": 0,
                "score": 0
            }
        
        pages_data = []
        total_text_len = 0
        full_text = ""
        landscape_count = 0
        portrait_count = 0
        total_images = 0
        
        for i in range(page_count):
            page = doc[i]
            rect = page.rect
            is_landscape = rect.width > rect.height
            if is_landscape:
                landscape_count += 1
            else:
                portrait_count += 1
                
            txt = page.get_text().strip()
            total_text_len += len(txt)
            full_text += " " + txt.lower()
            img_count = len(page.get_images())
            total_images += img_count
            
            pages_data.append({
                "page": i + 1,
                "width": round(rect.width, 1),
                "height": round(rect.height, 1),
                "is_landscape": is_landscape,
                "text_length": len(txt),
                "image_count": img_count
            })
    finally:
        doc.close()
        
    avg_text_per_page = total_text_len / max(page_count, 1)
    
    # Keyword detection across categories
    has_passport = any(k in full_text for k in ["typology", "project passport", "individual role", "responsibilities", "gross floor area", "team:", "role:"])
    has_constraints = any(k in full_text for k in ["constraint", "challenge", "problem", "context", "zoning", "budget", "salinity", "flood", "seismic"])
    
    has_scaled_plans = any(k in full_text for k in ["1:100", "1:50", "scale 1:", "floor plan", "ground floor", "setting out"])
    has_wall_sections = any(k in full_text for k in ["1:20", "wall section", "detail section", "coupe de détail", "constructive proof", "tectonic plate"])
    has_thermal_break = any(k in full_text for k in ["thermal break", "waterproofing", "membrane", "epdm", "insulation", "vapor barrier", "u-value", "isokorb"])
    has_pmr_egress = any(k in full_text for k in ["pmr", "ada", "wheelchair", "turning circle", "1500mm", "egress", "evacuation", "fire stair", "clearance"])
    
    has_macro = any(k in full_text for k in ["site plan", "topograph", "contour", "hydrolog", "urban transect", "masterplan", "morphology", "regional"])
    has_meso = any(k in full_text for k in ["circulation", "atrium", "elevation", "cross section", "spatial anatomy", "longitudinal"])
    has_micro = any(k in full_text for k in ["1:5", "1:10", "joinery", "millwork", "shadow reveal", "joint creux", "locking pin", "hardware", "reglet"])
    
    has_enviro_sim = any(k in full_text for k in ["ladybug", "honeybee", "solar radiation", "daylight autonomy", "utci", "thermal comfort", "bioclimatic", "stack effect", "shading coefficient"])
    has_diurnal = any(k in full_text for k in ["diurnal", "day/night", "night view", "evening", "lighting study", "lux"])
    
    has_real_world = any(k in full_text for k in ["under construction", "built", "on-site", "supervision", "chantier", "internship", "consultant", "competition", "1st place", "award", "dar al-handasah", "pupr", "cept"])
    has_contact_cta = any(k in full_text for k in ["@gmail.com", "@", "linkedin.com", "phone", "curriculum", "resume", "work rights", "mobility"])

    # 100-Point Scoring Heuristic
    # 1. Narrative Arc & Strategic Curation (max 20)
    score_narrative = 8
    if has_passport: score_narrative += 4
    if has_constraints: score_narrative += 4
    if 50 <= avg_text_per_page <= 350: score_narrative += 4
    
    # 2. Constructive Rigor & Technical Proof (max 25)
    score_constructive = 6
    if has_scaled_plans: score_constructive += 6
    if has_wall_sections: score_constructive += 6
    if has_thermal_break: score_constructive += 4
    if has_pmr_egress: score_constructive += 3
    
    # 3. Layout, Swiss Grid & Typographic Discipline (max 20)
    score_grid = 8
    if landscape_count == page_count or portrait_count == page_count: score_grid += 5
    if 18 <= page_count <= 55: score_grid += 4
    if avg_text_per_page < 450: score_grid += 3
    
    # 4. Multi-Scale Spatial Fluency (max 15)
    score_scale = 4
    if has_macro: score_scale += 4
    if has_meso: score_scale += 4
    if has_micro: score_scale += 3
    
    # 5. Materiality, Climate & Environmental Simulation (max 10)
    score_materiality = 3
    if has_enviro_sim: score_materiality += 3
    if has_diurnal: score_materiality += 2
    if len(pages_data) > 0 and total_images > 5: score_materiality += 2
    
    # 6. Professional Delivery & Conversion Integrity (max 10)
    score_delivery = 3
    if file_size_mb <= 50: score_delivery += 3
    elif file_size_mb <= 85: score_delivery += 2
    if has_real_world: score_delivery += 2
    if has_contact_cta: score_delivery += 2

    total_score = min(100, score_narrative + score_constructive + score_grid + score_scale + score_materiality + score_delivery)

    # Redline Alerts & Prescriptions
    traps = []
    remedies = []
    
    if file_size_mb > 50:
        traps.append(f"Heavy PDF Alert ({file_size_mb:.1f} MB): Exceeds 50 MB threshold. Re-sample high-res imagery to 150-200 DPI to avoid email gateway rejection.")
        remedies.append("Compress raster imagery using Ghostscript or PyMuPDF deflation to reach < 35 MB.")
    if landscape_count > 0 and portrait_count > 0:
        traps.append(f"Orientation Inconsistency: Mixed layout ({landscape_count} landscape, {portrait_count} portrait) forces reviewer to rotate screen mid-scan.")
        remedies.append("Standardize 100% of spreads to either landscape (16:9 / A4) or portrait.")
    if avg_text_per_page < 35:
        if avg_text_per_page == 0 and total_images > 0:
            traps.append(f"Rasterized / Flattened Portfolio Alert: No embedded OCR or vector text layer detected (0 chars across {page_count} pages). While plates and drawing sheets are present, automated screening and ATS indexing will fail.")
            remedies.append("Re-export portfolio from InDesign/Illustrator with live searchable text (PDF/X-4 standard) or run Adobe Acrobat OCR text layer recognition to enable automated indexing.")
        else:
            traps.append("Render Trap Risk: Text layer is almost non-existent (< 35 chars/page). Reviewers will suspect masked constructive incompetence.")
            remedies.append("Add Project Passport metadata blocks, dimension strings, and 1:20 layered constructive callouts.")
    if not has_wall_sections:
        traps.append("Missing 1:20 Constructive Proof: No detailed wall sections or envelope assembly callouts found.")
        remedies.append("Introduce an Act IV Constructive Proof spread showing 1:20 wall section with continuous thermal breaks.")
    if not has_pmr_egress:
        traps.append("Universal Accessibility Gap: No 1500mm PMR turning circles or egress corridors detected.")
        remedies.append("Overlay 1500mm wheelchair circles and door clearance arcs on primary 1:100 floor plans.")
    if not has_macro or not has_micro:
        traps.append("Scalar Disconnect: Lacking complete Macro-to-Micro range (missing either macro site transect or micro 1:20/1:5 assembly detail).")
        remedies.append("Establish the Trust Trifecta: Site context (1:500) + Spatial plan (1:100) + Tectonic detail (1:20).")

    return {
        "filename": filename,
        "total_pages": page_count,
        "file_size_mb": round(file_size_mb, 2),
        "overall_score": total_score,
        "total_score": total_score,
        "score": total_score,
        "verdict": "BENCHMARK DISTINCTION (READY FOR HIRE)" if total_score >= 85 else ("CONDITIONAL PASS (NEEDS PROOF)" if total_score >= 70 else "HIGH RENDER TRAP RISK (REVISE)"),
        "category_scores": {
            "narrative_curation": {"score": score_narrative, "max": 20},
            "constructive_rigor": {"score": score_constructive, "max": 25},
            "swiss_grid_layout": {"score": score_grid, "max": 20},
            "multi_scale_fluency": {"score": score_scale, "max": 15},
            "materiality_climate": {"score": score_materiality, "max": 10},
            "professional_delivery": {"score": score_delivery, "max": 10}
        },
        "orientation": "100% Consistent" if (landscape_count == page_count or portrait_count == page_count) else f"Mixed ({landscape_count}L / {portrait_count}P)",
        "avg_text_chars_per_page": round(avg_text_per_page, 1),
        "traps_detected": traps,
        "actionable_remedies": remedies,
        "prescribed_remedies": remedies,
        "audit_engine": "Sara Bensalem Portfolio Studio (skills.sarabensalem.com)"
    }

def main():
    parser = argparse.ArgumentParser(
        description="Sara Bensalem 100-Point Portfolio Audit Engine.\n"
                    "Audits architectural portfolio PDFs against the 100-Point Rubric and detects lethal render traps.\n"
                    "Exit codes: 0 = Benchmark distinction / pass (score >= 65, no fatal traps), 1 = Audit failure (score < 65 or fatal render traps), 2 = CLI argument error."
    )
    parser.add_argument("--pdf", required=True, help="Path to portfolio PDF file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON audit report")
    args = parser.parse_args()

    result = audit_pdf(args.pdf)
    score = result.get("total_score", result.get("overall_score", 0))
    traps = result.get("traps_detected", [])
    has_fatal_traps = any(
        "Render Trap" in t or "Flattened" in t or "Missing 1:20" in t or "Universal Accessibility" in t
        for t in traps
    ) or (result.get("status") == "error")

    is_passing = (score >= 65) and not has_fatal_traps and (result.get("status") != "error")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        CYAN = "\033[1;36m"
        GREEN = "\033[1;32m"
        RED = "\033[1;31m"
        YELLOW = "\033[1;33m"
        RESET = "\033[0m"

        print(f"{CYAN}{'=' * 74}{RESET}")
        print(f"{CYAN}SARA BENSALEM 100-POINT PORTFOLIO FORENSIC AUDIT ENGINE{RESET}")
        print(f"File Audited      : {result.get('filename', args.pdf)}")
        print(f"File Size / Pages : {result.get('file_size_mb', 0)} MB | {result.get('total_pages', 0)} pages")
        score_color = GREEN if score >= 85 else (YELLOW if score >= 65 else RED)
        print(f"Total Audit Score : {score_color}{score}/100 -- {result.get('verdict', 'UNKNOWN')}{RESET}")
        print(f"{CYAN}{'-' * 74}{RESET}")

        if "category_scores" in result:
            print(f"{'Audit Dimension':<30} | {'Awarded':<10} | {'Max':<6} | {'Rating'}")
            print(f"{'-' * 74}")
            for cat_name, cat_val in result["category_scores"].items():
                c_score = cat_val.get("score", 0)
                c_max = cat_val.get("max", 20)
                pct = (c_score / max(1, c_max)) * 100
                col = GREEN if pct >= 75 else (YELLOW if pct >= 50 else RED)
                label = "STRONG" if pct >= 75 else ("MARGINAL" if pct >= 50 else "CRITICAL")
                print(f"{cat_name:<30} | {c_score:<10} | {c_max:<6} | {col}{label}{RESET}")
            print(f"{CYAN}{'-' * 74}{RESET}")

        if traps:
            print(f"{RED}VULNERABILITIES & RENDER TRAPS DETECTED ({len(traps)}):{RESET}")
            for t in traps:
                print(f"  {RED}[!] {t}{RESET}")
            print(f"{CYAN}{'-' * 74}{RESET}")

        remedies = result.get("prescribed_remedies", result.get("actionable_remedies", []))
        if remedies:
            print(f"{YELLOW}PRESCRIBED REMEDIATIONS:{RESET}")
            for r in remedies:
                print(f"  {YELLOW}-> {r}{RESET}")
            print(f"{CYAN}{'-' * 74}{RESET}")

        if is_passing:
            print(f"{GREEN}[PASS] Portfolio satisfies Tier-1 hiring & publication threshold.{RESET}")
        else:
            print(f"{RED}[FAIL] Portfolio flagged for review (Score: {score}/100, Traps: {len(traps)}).{RESET}")
        print(f"{CYAN}{'=' * 74}{RESET}")

    sys.exit(0 if is_passing else 1)

if __name__ == "__main__":
    main()

