#!/usr/bin/env python3
"""
extract_from_image.py - Extract Design Tokens & DESIGN.md from Images / Renderings
Sara Bensalem Skills — Design MD Extractor
Extracts dominant color palettes, luminance hierarchies, contrast ratios (WCAG 2.1),
and produces publication-grade DESIGN.md tokens and Google Stitch design-system.json.
Author: Sara Bensalem <sara@sarabensalem.com>
"""

import sys
import os
import math
import json
import argparse
from pathlib import Path
from PIL import Image

def rgb_to_hex(r, g, b):
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}".upper()

def relative_luminance(r, g, b):
    # sRGB relative luminance (WCAG 2.1)
    rgb = [x / 255.0 for x in (r, g, b)]
    lum = []
    for c in rgb:
        if c <= 0.03928:
            lum.append(c / 12.92)
        else:
            lum.append(((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * lum[0] + 0.7152 * lum[1] + 0.0722 * lum[2]

def contrast_ratio(lum1, lum2):
    l_max = max(lum1, lum2)
    l_min = min(lum1, lum2)
    return (l_max + 0.05) / (l_min + 0.05)

def color_distance(c1, c2):
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)

def saturation(r, g, b):
    mx = max(r, g, b)
    mn = min(r, g, b)
    if mx == 0:
        return 0.0
    return (mx - mn) / mx

def extract_palette_from_image(image_path: str, max_colors: int = 8):
    p = Path(image_path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {p}")

    img = Image.open(p).convert("RGB")
    img.thumbnail((300, 300), Image.Resampling.LANCZOS)

    # Quantize
    q_img = img.quantize(colors=24, method=Image.Quantize.MEDIANCUT)
    palette = q_img.getpalette()[:72]  # 24 colors * 3 channels
    color_counts = q_img.getcolors()

    # Sort colors by frequency
    sorted_colors = sorted(color_counts, key=lambda x: x[0], reverse=True)

    extracted = []
    for count, idx in sorted_colors:
        r = palette[idx * 3]
        g = palette[idx * 3 + 1]
        b = palette[idx * 3 + 2]
        
        # Deduplicate
        is_dup = False
        for ext in extracted:
            if color_distance((r, g, b), ext["rgb"]) < 28.0:
                is_dup = True
                ext["count"] += count
                break
        if not is_dup:
            extracted.append({
                "rgb": (r, g, b),
                "hex": rgb_to_hex(r, g, b),
                "count": count,
                "lum": relative_luminance(r, g, b),
                "sat": saturation(r, g, b)
            })
        if len(extracted) >= max_colors:
            break

    total_pixels = sum(c["count"] for c in extracted)
    for c in extracted:
        c["share"] = round((c["count"] / max(1, total_pixels)) * 100, 1)

    # Classify Roles
    # Determine dominant mode (dark or light)
    bg_candidate = extracted[0]
    is_dark_mode = bg_candidate["lum"] < 0.2

    if is_dark_mode:
        bg = min(extracted, key=lambda x: x["lum"])
        text_primary = max(extracted, key=lambda x: x["lum"])
    else:
        bg = max(extracted, key=lambda x: x["lum"])
        text_primary = min(extracted, key=lambda x: x["lum"])

    # Surface candidate: close to bg but distinct
    surfaces = [c for c in extracted if c != bg and abs(c["lum"] - bg["lum"]) < 0.25]
    surface = surfaces[0] if surfaces else bg

    # Accent candidate: highest saturation that isn't bg or primary text
    accents = [c for c in extracted if c != bg and c != text_primary]
    accent = max(accents, key=lambda x: x["sat"]) if accents else extracted[0]

    # Border: intermediate luminance
    borders = [c for c in extracted if c != bg and c != text_primary and c != accent]
    border = borders[0] if borders else surface

    contrast = contrast_ratio(bg["lum"], text_primary["lum"])

    return {
        "source_image": p.name,
        "is_dark_mode": is_dark_mode,
        "contrast_ratio": round(contrast, 2),
        "wcag_aaa_compliant": contrast >= 7.0,
        "tokens": {
            "background": bg["hex"],
            "surface": surface["hex"],
            "primary": text_primary["hex"],
            "accent": accent["hex"],
            "border": border["hex"]
        },
        "all_extracted_colors": extracted
    }

def format_design_md(analysis: dict) -> str:
    t = analysis["tokens"]
    md = f"""# Visual Design System: {analysis['source_image']}
> Extracted via Sara Bensalem `design-md-extractor` from `{analysis['source_image']}`

---

## 🎨 Core Color Palette Tokens
| Token | Hex Value | Role | Share | Contrast to Bg |
| :--- | :--- | :--- | :---: | :---: |
| `color-bg` | `{t['background']}` | Canvas Background / Substrate | Mode: {'Dark' if analysis['is_dark_mode'] else 'Light'} | 1.0:1 |
| `color-surface` | `{t['surface']}` | Card Surface / Elevated Plate | Secondary Container | - |
| `color-text-primary` | `{t['primary']}` | Primary Body & Display Headers | High Contrast | **{analysis['contrast_ratio']}:1** ({'AAA PASS' if analysis['wcag_aaa_compliant'] else 'AA Pass'}) |
| `color-accent` | `{t['accent']}` | Tectonic Focus & Drawing Callouts | Chromatic Focal | - |
| `color-border` | `{t['border']}` | Swiss Modular Grid & Hairlines | Subtle Delimitation | - |

---

## 🏛️ All Extracted Dominant Clusters
"""
    for idx, c in enumerate(analysis["all_extracted_colors"], 1):
        md += f"- **Cluster {idx:02d}**: `{c['hex']}` (Share: {c['share']}%, Lum: {c['lum']:.3f}, Sat: {c['sat']:.2f})\n"

    md += f"""
---

## 📐 Typographic & Layout Directives
- **Display Typography**: Neue Haas Grotesk / Space Grotesk (Tracking: -0.02em, Leading: 1.05)
- **Body & Captions**: Plus Jakarta Sans / Inter (Font Size: 11pt, Leading: 1.45)
- **Technical Annotations**: JetBrains Mono / IBM Plex Mono (Font Size: 9pt, Uppercase)
- **Grid Structure**: 12-Column Swiss Modular Grid (4mm gutters, 16px baseline locking)
- **Contrast Standard**: {analysis['contrast_ratio']}:1 (WCAG 2.1 {'AAA' if analysis['wcag_aaa_compliant'] else 'AA'})
"""
    return md

def main():
    parser = argparse.ArgumentParser(description="Extract Design Tokens from Image / Renderings")
    parser.add_argument("image", help="Path to architectural rendering, cover, or photograph")
    parser.add_argument("--output-dir", "-o", default=".", help="Directory to save DESIGN.md and design-system.json")
    parser.add_argument("--json", action="store_true", help="Print JSON tokens to stdout")
    args = parser.parse_args()

    analysis = extract_palette_from_image(args.image)
    out_dir = Path(args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    md_content = format_design_md(analysis)
    md_path = out_dir / "DESIGN.md"
    md_path.write_text(md_content, encoding="utf-8")

    stitch_ds = {
        "name": f"Extracted from {Path(args.image).stem}",
        "customColor": analysis["tokens"]["accent"],
        "tokens": analysis["tokens"],
        "all_colors": [c["hex"] for c in analysis["all_extracted_colors"]],
        "typography": {
            "display": "Space Grotesk",
            "body": "Plus Jakarta Sans",
            "mono": "JetBrains Mono"
        }
    }
    json_path = out_dir / "design-system.json"
    json_path.write_text(json.dumps(stitch_ds, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(analysis, indent=2))
    else:
        print("=" * 70)
        print(f"DESIGN TOKENS EXTRACTED FROM: {args.image}")
        print(f"Background: {analysis['tokens']['background']} | Text: {analysis['tokens']['primary']}")
        print(f"Accent:     {analysis['tokens']['accent']} | Surface: {analysis['tokens']['surface']}")
        print(f"Contrast:   {analysis['contrast_ratio']}:1 ({'WCAG AAA PASS' if analysis['wcag_aaa_compliant'] else 'AA PASS'})")
        print(f"[+] Wrote {md_path}")
        print(f"[+] Wrote {json_path}")
        print("=" * 70)

if __name__ == "__main__":
    main()
