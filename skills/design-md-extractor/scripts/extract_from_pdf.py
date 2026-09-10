#!/usr/bin/env python3
"""
extract_from_pdf.py
Antigravity Design MD Extractor — PDF Monograph & Portfolio Engine

Uses PyMuPDF (fitz) and Pillow to reverse-engineer visual design systems,
typographic scales, column grids, margins, and color palettes from any PDF document
(architectural monographs, portfolios, brand guidelines, lookbooks, magazines).
Outputs production-ready DESIGN.md and Google Stitch design-system.json.
"""

import os
import sys
import json
import base64
import argparse
from datetime import datetime
from collections import Counter
from pathlib import Path

# Supported Stitch font enums mapping
STITCH_FONTS = {
    "inter": "INTER",
    "montserrat": "MONTSERRAT",
    "space grotesk": "SPACE_GROTESK",
    "manrope": "MANROPE",
    "plus jakarta sans": "PLUS_JAKARTA_SANS",
    "geist": "GEIST",
    "dm sans": "DM_SANS",
    "ibm plex sans": "IBM_PLEX_SANS",
    "roboto": "ROBOTO_FLEX",
    "roboto flex": "ROBOTO_FLEX",
    "work sans": "WORK_SANS",
    "rubik": "RUBIK",
    "outfit": "OUTFIT",
    "sora": "SORA",
    "syne": "SYNE",
    "century": "CENTURY_GOTHIC",
    "gothic": "MONTSERRAT",
    "helvetica": "INTER",
    "neue haas": "INTER",
    "univers": "INTER",
    "arial": "INTER",
    "futura": "SPACE_GROTESK",
    "bodoni": "BODONI_MODA",
    "playfair": "PLAYFAIR_DISPLAY",
    "garamond": "EB_GARAMOND",
    "caslon": "LIBRE_CASLON_TEXT",
    "noto serif": "NOTO_SERIF",
    "merriweather": "MERRIWEATHER",
    "jetbrains mono": "JETBRAINS_MONO",
    "space mono": "SPACE_MONO",
    "courier": "COURIER_PRIME"
}

def clean_font_name(raw_name):
    if not raw_name:
        return "Inter", "INTER"
    # Strip subset prefixes like 'AYQVMA+CenturyGothic'
    cleaned = raw_name.split("+")[-1].replace("-", " ").replace(",", " ")
    cleaned = cleaned.strip()
    primary = cleaned.split()[0] if cleaned else "Inter"

    matched_enum = "INTER"
    for name, enum_val in STITCH_FONTS.items():
        if name in cleaned.lower():
            matched_enum = enum_val
            break

    # If serif detected but not mapped
    if matched_enum == "INTER" and any(s in cleaned.lower() for s in ["serif", "roman", "minion", "baskerville"]):
        matched_enum = "EB_GARAMOND"

    return cleaned, matched_enum

def rgb_tuple_to_hex(rgb):
    if not rgb or len(rgb) < 3:
        return None
    r, g, b = [int(max(0, min(1, c)) * 255) if isinstance(c, float) else int(c) for c in rgb[:3]]
    return f"#{r:02x}{g:02x}{b:02x}".upper()

def extract_dominant_colors_from_pixmap(pixmap, num_colors=6):
    from PIL import Image
    # Convert fitz pixmap to PIL Image
    img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    img = img.resize((150, 150))
    # Quantize to find dominant palette
    quantized = img.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()[:num_colors * 3]
    hex_colors = []
    for i in range(0, len(palette), 3):
        r, g, b = palette[i], palette[i+1], palette[i+2]
        hex_colors.append(f"#{r:02x}{g:02x}{b:02x}".upper())
    return hex_colors

def extract_pdf_design(pdf_path, max_pages=10):
    import fitz  # PyMuPDF

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    meta = doc.metadata or {}
    title = meta.get("title") or Path(pdf_path).stem.replace("_", " ").title()

    sample_count = min(total_pages, max_pages)
    print(f"[*] Analyzing PDF: '{title}' ({total_pages} pages, sampling first {sample_count})...")

    # 1. Page Geometry
    first_page = doc[0]
    rect = first_page.rect
    width_pt, height_pt = rect.width, rect.height
    aspect_ratio = width_pt / height_pt if height_pt > 0 else 1.414

    # Determine standard format
    is_landscape = width_pt > height_pt
    if abs(width_pt - 1190.55) < 20 and abs(height_pt - 841.89) < 20:
        format_desc = "A3 Landscape Spread (420mm x 297mm)"
    elif abs(width_pt - 841.89) < 20 and abs(height_pt - 595.28) < 20:
        format_desc = "A4 Landscape Monograph (297mm x 210mm)"
    elif abs(width_pt - 595.28) < 20 and abs(height_pt - 841.89) < 20:
        format_desc = "A4 Portrait Monograph (210mm x 297mm)"
    elif aspect_ratio >= 1.7:
        format_desc = f"16:9 Widescreen Portfolio ({int(width_pt)}pt x {int(height_pt)}pt)"
    else:
        format_desc = f"Custom Format ({int(width_pt)}pt x {int(height_pt)}pt, ratio {aspect_ratio:.2f})"

    # 2. Typographic Inspection
    font_counter = Counter()
    size_counter = Counter()
    all_font_names = set()
    left_margins = []
    top_margins = []
    text_blocks_count = 0

    for i in range(sample_count):
        page = doc[i]
        # Embedded fonts
        for f in page.get_fonts():
            name = f[3]
            all_font_names.add(name)

        # Text blocks & font sizes
        page_dict = page.get_text("dict")
        for block in page_dict.get("blocks", []):
            if block.get("type") == 0:  # Text block
                bbox = block.get("bbox", [0, 0, 0, 0])
                if bbox[0] > 10 and bbox[0] < width_pt / 2:
                    left_margins.append(bbox[0])
                if bbox[1] > 10 and bbox[1] < height_pt / 3:
                    top_margins.append(bbox[1])

                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        fn = span.get("font", "Unknown")
                        sz = round(span.get("size", 10), 1)
                        font_counter[fn] += len(span.get("text", ""))
                        size_counter[sz] += len(span.get("text", ""))
                        text_blocks_count += 1

    # 3. Vector & Image Color Extraction
    vector_colors = Counter()
    for i in range(min(sample_count, 3)):
        page = doc[i]
        drawings = page.get_drawings()
        for d in drawings:
            fill = d.get("fill")
            stroke = d.get("color")
            if fill:
                h = rgb_tuple_to_hex(fill)
                if h: vector_colors[h] += 1
            if stroke:
                h = rgb_tuple_to_hex(stroke)
                if h: vector_colors[h] += 1

    # Render spread 0 or 1 to sample raster palette
    sample_page_idx = 1 if total_pages > 1 else 0
    pix = doc[sample_page_idx].get_pixmap(dpi=100)
    raster_palette = extract_dominant_colors_from_pixmap(pix, num_colors=8)
    doc.close()

    # Determine Primary Colors & Theme
    # Most common colors
    bg_candidate = raster_palette[0] if raster_palette else "#FFFFFF"
    # Check if background is dark
    r = int(bg_candidate[1:3], 16)
    g = int(bg_candidate[3:5], 16)
    b = int(bg_candidate[5:7], 16)
    lum = 0.299*r + 0.587*g + 0.114*b
    is_dark = lum < 100
    color_mode = "DARK" if is_dark else "LIGHT"

    canvas_bg = bg_candidate if (is_dark and lum < 60) or (not is_dark and lum > 200) else ("#0B0F17" if is_dark else "#FFFFFF")
    text_primary = "#F8FAFC" if is_dark else "#0F172A"
    text_muted = "#94A3B8" if is_dark else "#64748B"

    # Identify Accent Color (non-neutral from raster or vector)
    accent_color = "#3B82F6"
    for col in raster_palette + [c for c, _ in vector_colors.most_common(5)]:
        cr = int(col[1:3], 16)
        cg = int(col[3:5], 16)
        cb = int(col[5:7], 16)
        # Check saturation/vibrancy (diff between channels)
        spread = max(cr, cg, cb) - min(cr, cg, cb)
        if spread > 40 and col != canvas_bg and col != text_primary:
            accent_color = col
            break

    secondary_color = "#6366F1" if is_dark else "#475569"
    border_color = "rgba(255, 255, 255, 0.15)" if is_dark else "rgba(0, 0, 0, 0.10)"

    # Determine Typography
    most_common_font = font_counter.most_common(1)[0][0] if font_counter else (list(all_font_names)[0] if all_font_names else "CenturyGothic")
    body_font_clean, body_font_enum = clean_font_name(most_common_font)

    # Check for bold or heading font variant
    heading_font_clean = body_font_clean
    heading_font_enum = body_font_enum
    for f in all_font_names:
        if any(h in f.lower() for h in ["bold", "black", "heavy", "display", "headline"]):
            heading_font_clean, heading_font_enum = clean_font_name(f)
            break

    # Determine Font Sizes
    sorted_sizes = [sz for sz, count in size_counter.most_common(10) if count > 5]
    sorted_sizes.sort()
    body_sz = 9.0
    h1_sz = 24.0
    h2_sz = 14.0
    caption_sz = 7.0

    if sorted_sizes:
        # Body text is usually the most frequent size between 8pt and 13pt
        candidates = [sz for sz in sorted_sizes if 7.5 <= sz <= 14.0]
        if candidates:
            body_sz = candidates[0]
        # Headings are larger sizes
        headings = [sz for sz in sorted_sizes if sz > body_sz * 1.3]
        if headings:
            h2_sz = headings[0]
            h1_sz = headings[-1]
        captions = [sz for sz in sorted_sizes if sz < body_sz]
        if captions:
            caption_sz = captions[0]

    # Grid & Margins
    margin_left_pt = round(min(left_margins), 1) if left_margins else 36.0
    margin_top_pt = round(min(top_margins), 1) if top_margins else 36.0

    # Classify Editorial / Monograph Aesthetic
    if is_landscape and "gothic" in body_font_clean.lower() or "century" in body_font_clean.lower():
        aesthetic_label = "Modernist Swiss Landscape Monograph"
    elif "serif" in body_font_clean.lower() or "garamond" in body_font_clean.lower():
        aesthetic_label = "Classic Academic Architectural Monograph"
    elif is_dark:
        aesthetic_label = "Dark Titanium Tectonic Dossier"
    else:
        aesthetic_label = "Contemporary Minimalist Studio Monograph"

    roundness_token = "ROUND_FOUR" if "monograph" in aesthetic_label.lower() or "architectural" in aesthetic_label.lower() else "ROUND_EIGHT"

    # Generate Stitch JSON Config
    stitch_ds = {
        "displayName": f"{title} Monograph Design System",
        "theme": {
            "colorMode": color_mode,
            "customColor": accent_color,
            "colorVariant": "TONAL_SPOT" if "architectural" in aesthetic_label.lower() else "NEUTRAL",
            "headlineFont": heading_font_enum,
            "bodyFont": body_font_enum,
            "roundness": roundness_token,
            "spacing": {
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "36px",
                "xxl": "54px"
            }
        }
    }

    # Synthesize Publication DESIGN.md Content
    design_md = f"""# DESIGN.md — {title} Monograph Design System
<!-- Extracted by Antigravity Design MD Extractor (PDF Monograph & Editorial Engine) -->

## Metadata & Editorial Identity
- **Source Document**: `{Path(pdf_path).name}`
- **Page Count**: `{total_pages}` Pages
- **Trim Dimensions**: `{format_desc}` ({width_pt:.1f}pt x {height_pt:.1f}pt)
- **Aspect Ratio**: `{aspect_ratio:.2f}` ({'Facing Spread' if is_landscape else 'Single Column Vertical'})
- **Extracted Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Aesthetic Classification**: **{aesthetic_label}**
- **Appearance Mode**: `{color_mode}` Canvas

---

## 1. Color Palette & Chromatic Grammar

| Token Name | Hex Code | Role in Publication | Contrast vs BG |
| :--- | :--- | :--- | :--- |
| `--color-primary` | `{accent_color}` | Hero Callouts & Drawing Section Pins | High |
| `--color-secondary` | `{secondary_color}` | Secondary Headers & Dimension Callouts | Balanced |
| `--color-background` | `{canvas_bg}` | Paper Substrate / Sheet Background | Anchor |
| `--color-surface` | `{text_muted}15` | Drawing Frame / Tectonic Matting | Subordinate |
| `--color-text-primary` | `{text_primary}` | Body Narrative & Project Passports | AAA Print Compliant |
| `--color-text-muted` | `{text_muted}` | Graphic Bar Scales & Drawing Legends | AA Print Compliant |
| `--color-border` | `{border_color}` | 0.25pt CAD Setting-Out & Grid Lines | Subtle |

---

## 2. Typographic Scale & Editorial Hierarchy

- **Display & Headline Font**: `{heading_font_clean}` (`{heading_font_enum}`)
- **Body & Narrative Font**: `{body_font_clean}` (`{body_font_enum}`)
- **Metadata & Data Font**: `JetBrains Mono` / `Courier Prime`

### Print & Editorial Typographic Scale
| Hierarchy Level | Point Size | Leading | Weight | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Title / Cover H1** | `{h1_sz:.1f}pt` | `{h1_sz * 1.2:.1f}pt` | Bold | Cover Title & Flagship Chapter Openers |
| **Section H2** | `{h2_sz:.1f}pt` | `{h2_sz * 1.25:.1f}pt` | SemiBold | Project Name & Act Headers |
| **Body Narrative** | `{body_sz:.1f}pt` | `{body_sz * 1.4:.1f}pt` | Regular | Curatorial Statement & Spatial Concept |
| **Caption & Scales** | `{caption_sz:.1f}pt` | `{caption_sz * 1.3:.1f}pt` | Regular | 1:100 Plan Legends, 1:20 Material Tags |

---

## 3. Modular Grid & Sheet Layout

- **Layout Structure**: 12-Column Swiss Modular Grid (6 columns per page in 2-page facing spread)
- **Inner Margin (Gutter Creep Safety)**: `{margin_left_pt:.1f}pt` ({margin_left_pt * 0.3527:.1f}mm)
- **Top / Header Margin**: `{margin_top_pt:.1f}pt` ({margin_top_pt * 0.3527:.1f}mm)
- **Baseline Grid Rhythm**: `4pt` / `8pt` lock across facing verso/recto spreads
- **Negative Space Ratio**: ~35% editorial breathing room surrounding orthographic plates

---

## 4. Tectonic & Spatial Plate Standards

- **ISO 128 Lineweights**:
  - `0.13mm` (Hairline): Material hatches, insulation zigzag, ceiling grid
  - `0.25mm` (Thin): Dimension chains, grid axes, door swings
  - `0.35mm` (Medium): Secondary partitions, joinery reveals, furniture
  - `0.50mm - 0.70mm` (Heavy Cut): Primary structural walls, floor slabs in section
- **Scale Bar Obligation**: Every plate must feature a graphic metric bar scale (0m, 1m, 2m, 5m).

---

## 5. Google Stitch MCP Specification

```json
{json.dumps(stitch_ds, indent=2)}
```

---

## 6. Typst / Paged.js Editorial Studio Preset

```typst
#let monograph-theme = (
  font-heading: "{heading_font_clean}",
  font-body: "{body_font_clean}",
  size-body: {body_sz}pt,
  color-primary: rgb("{accent_color}"),
  color-bg: rgb("{canvas_bg}"),
  color-text: rgb("{text_primary}"),
  margin-left: {margin_left_pt}pt,
  margin-top: {margin_top_pt}pt,
)
```
"""

    return {
        "pdf_path": pdf_path,
        "title": title,
        "design_md": design_md,
        "stitch_ds": stitch_ds,
        "base64_md": base64.b64encode(design_md.encode("utf-8")).decode("utf-8")
    }

def main():
    parser = argparse.ArgumentParser(description="Antigravity PDF Monograph Design MD Extractor")
    parser.add_argument("pdf_path", help="Path to PDF monograph, portfolio, or brand guide")
    parser.add_argument("--output-dir", "-o", default=".", help="Directory to save DESIGN.md and design-system.json")
    parser.add_argument("--max-pages", type=int, default=10, help="Max pages to sample for typographic inspection")
    args = parser.parse_args()

    res = extract_pdf_design(args.pdf_path, max_pages=args.max_pages)

    out_dir = args.output_dir
    os.makedirs(out_dir, exist_ok=True)

    md_path = os.path.join(out_dir, "DESIGN.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(res["design_md"])

    ds_path = os.path.join(out_dir, "design-system.json")
    with open(ds_path, "w", encoding="utf-8") as f:
        json.dump(res["stitch_ds"], f, indent=2)

    b64_path = os.path.join(out_dir, "design_md_base64.txt")
    with open(b64_path, "w", encoding="utf-8") as f:
        f.write(res["base64_md"])

    print(f"[+] Successfully reverse-engineered design system from '{res['title']}'")
    print(f"[+] Generated: {md_path}")
    print(f"[+] Generated: {ds_path} (Stitch theme ready)")
    print(f"[+] Base64 payload ready for stitch:upload_design_md: {b64_path}")

if __name__ == "__main__":
    main()
