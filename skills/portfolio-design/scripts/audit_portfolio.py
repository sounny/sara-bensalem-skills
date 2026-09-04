"""
Sara Bensalem Portfolio Audit Engine CLI
Analyzes any architectural or interior portfolio PDF against the 100-Point Rubric.
"""
import sys
import os
import json
import argparse

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

def audit_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        return {"error": f"File not found: {pdf_path}"}
    
    file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    
    if not fitz:
        return {
            "file": os.path.basename(pdf_path),
            "file_size_mb": round(file_size_mb, 2),
            "note": "PyMuPDF not available for deep geometry extraction"
        }
        
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    
    pages_data = []
    total_text_len = 0
    landscape_count = 0
    portrait_count = 0
    
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
        pages_data.append({
            "page": i + 1,
            "width": round(rect.width, 1),
            "height": round(rect.height, 1),
            "is_landscape": is_landscape,
            "text_length": len(txt),
            "image_count": len(page.get_images())
        })
        
    avg_text_per_page = total_text_len / max(page_count, 1)
    
    # Heuristic scoring
    scores = {
        "file_optimization": 3 if file_size_mb <= 50 else (2 if file_size_mb <= 90 else 1),
        "aspect_consistency": 5 if (landscape_count == page_count or portrait_count == page_count) else 2,
        "spread_budget": 5 if 18 <= page_count <= 55 else (3 if page_count < 18 else 2),
        "text_density_health": 5 if 50 <= avg_text_per_page <= 350 else (3 if avg_text_per_page < 50 else 2),
    }
    
    traps_detected = []
    if file_size_mb > 50:
        traps_detected.append("Heavy PDF Alert: File size exceeds 50 MB; compress raster assets to prevent email bounce.")
    if avg_text_per_page > 450:
        traps_detected.append("Wall of Text Alert: Average text exceeds 450 chars/page; reviewers scan in 30 seconds.")
    if avg_text_per_page < 30:
        traps_detected.append("Render Trap Risk: Very low text layer; ensure drawings have legible callouts and project passports.")
        
    return {
        "filename": os.path.basename(pdf_path),
        "total_pages": page_count,
        "file_size_mb": round(file_size_mb, 2),
        "orientation": "Landscape Dominant" if landscape_count >= portrait_count else "Portrait Dominant",
        "avg_text_per_page": round(avg_text_per_page, 1),
        "preliminary_heuristics": scores,
        "traps_detected": traps_detected,
        "engine": "Sara Bensalem Portfolio Studio (skills.sarabensalem.com)"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit an architectural portfolio PDF")
    parser.add_argument("--pdf", required=True, help="Path to PDF file")
    args = parser.parse_args()
    
    result = audit_pdf(args.pdf)
    print(json.dumps(result, indent=2))
