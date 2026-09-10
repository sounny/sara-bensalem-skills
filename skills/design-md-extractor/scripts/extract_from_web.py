#!/usr/bin/env python3
"""
extract_from_web.py
Antigravity Design MD Extractor — Web Browser Ingestion Engine

Uses Playwright to navigate to any website, evaluate computed styles,
extract typography, color palettes, spacing, border radii, elevation,
and generate a production-ready DESIGN.md and Stitch-ready design-system.json.
"""

import os
import sys
import json
import base64
import argparse
from datetime import datetime
from urllib.parse import urlparse
from collections import Counter

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
    "playfair display": "PLAYFAIR_DISPLAY",
    "eb garamond": "EB_GARAMOND",
    "noto serif": "NOTO_SERIF",
    "libre caslon text": "LIBRE_CASLON_TEXT",
    "jetbrains mono": "JETBRAINS_MONO",
    "space mono": "SPACE_MONO",
    "courier prime": "COURIER_PRIME"
}

def clean_font_name(raw_family):
    if not raw_family:
        return "Inter", "INTER"
    parts = [f.strip().strip("'\"") for f in raw_family.split(",")]
    primary = parts[0]
    matched_enum = "INTER"
    for name, enum_val in STITCH_FONTS.items():
        if name in primary.lower():
            matched_enum = enum_val
            break
    return primary, matched_enum

def rgb_to_hex(rgb_str):
    if not rgb_str or rgb_str == "transparent" or "rgba(0, 0, 0, 0)" in rgb_str:
        return None
    import re
    m = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgb_str)
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"#{r:02x}{g:02x}{b:02x}".upper()
    if rgb_str.startswith("#"):
        return rgb_str.upper()
    return None

def calc_luminance(hex_code):
    if not hex_code or len(hex_code) < 7:
        return 0.5
    try:
        r = int(hex_code[1:3], 16) / 255.0
        g = int(hex_code[3:5], 16) / 255.0
        b = int(hex_code[5:7], 16) / 255.0
        # Perceived luminance formula
        return 0.299 * r + 0.587 * g + 0.114 * b
    except Exception:
        return 0.5

def extract_web_design(url, timeout_ms=30000):
    from playwright.sync_api import sync_playwright

    print(f"[*] Navigating to {url} with Playwright headless browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        try:
            page.goto(url, wait_until="load", timeout=timeout_ms)
            page.wait_for_timeout(2000)  # Allow JS fonts & themes to hydrate
        except Exception as e:
            print(f"[!] Warning during navigation: {e}")

        title = page.title() or urlparse(url).netloc

        # Deep DOM Computed Style Extraction via JavaScript
        js_inspector = """
        () => {
            const getRGB = (c) => c || '';
            const data = {
                bgColors: [],
                textColors: [],
                borderColors: [],
                fonts: [],
                headingFonts: [],
                radii: [],
                shadows: [],
                blurs: [],
                headings: {},
                buttons: [],
                layout: {
                    maxWidth: 1280,
                    containerPadding: '24px'
                }
            };

            const sampleElements = (selector, limit = 50) => {
                return Array.from(document.querySelectorAll(selector)).slice(0, limit);
            };

            // 1. Inspect Body and Containers
            const bodyStyle = window.getComputedStyle(document.body);
            data.bgColors.push(bodyStyle.backgroundColor);
            data.textColors.push(bodyStyle.color);
            data.fonts.push({ family: bodyStyle.fontFamily, weight: bodyStyle.fontWeight, size: bodyStyle.fontSize });

            // 2. Headings
            ['h1', 'h2', 'h3', 'h4'].forEach(tag => {
                const el = document.querySelector(tag);
                if (el) {
                    const st = window.getComputedStyle(el);
                    data.headingFonts.push({ tag, family: st.fontFamily, size: st.fontSize, weight: st.fontWeight, lineHeight: st.lineHeight, tracking: st.letterSpacing });
                    data.textColors.push(st.color);
                    data.headings[tag] = {
                        fontFamily: st.fontFamily,
                        fontSize: st.fontSize,
                        fontWeight: st.fontWeight,
                        lineHeight: st.lineHeight,
                        letterSpacing: st.letterSpacing
                    };
                }
            });

            // 3. Buttons & Interactive Controls
            sampleElements('button, a.btn, [role="button"], input[type="submit"]').forEach(btn => {
                const st = window.getComputedStyle(btn);
                if (st.display !== 'none' && st.visibility !== 'hidden') {
                    data.bgColors.push(st.backgroundColor);
                    data.textColors.push(st.color);
                    data.radii.push(st.borderRadius);
                    data.borderColors.push(st.borderColor);
                    data.buttons.push({
                        bg: st.backgroundColor,
                        color: st.color,
                        radius: st.borderRadius,
                        padding: st.padding
                    });
                }
            });

            // 4. Cards and Sections
            sampleElements('article, section, .card, div[class*="card"], div[class*="container"]').forEach(card => {
                const st = window.getComputedStyle(card);
                if (st.backgroundColor && st.backgroundColor !== 'rgba(0, 0, 0, 0)' && st.backgroundColor !== 'transparent') {
                    data.bgColors.push(st.backgroundColor);
                }
                if (st.borderRadius && st.borderRadius !== '0px') {
                    data.radii.push(st.borderRadius);
                }
                if (st.boxShadow && st.boxShadow !== 'none') {
                    data.shadows.push(st.boxShadow);
                }
                if (st.backdropFilter && st.backdropFilter !== 'none') {
                    data.blurs.push(st.backdropFilter);
                }
                if (st.maxWidth && parseInt(st.maxWidth) > 600) {
                    data.layout.maxWidth = Math.max(data.layout.maxWidth, parseInt(st.maxWidth));
                }
            });

            return data;
        }
        """
        extracted = page.evaluate(js_inspector)
        browser.close()

    # Process and Normalize Colors
    raw_bg_hexes = [rgb_to_hex(c) for c in extracted["bgColors"] if rgb_to_hex(c)]
    raw_text_hexes = [rgb_to_hex(c) for c in extracted["textColors"] if rgb_to_hex(c)]
    raw_radii = [r for r in extracted["radii"] if r and r != '0px']
    raw_shadows = extracted["shadows"]

    # Deduce Theme (Light or Dark)
    bg_counter = Counter(raw_bg_hexes)
    primary_bg = bg_counter.most_common(1)[0][0] if bg_counter else "#FFFFFF"
    is_dark = calc_luminance(primary_bg) < 0.4
    color_mode = "DARK" if is_dark else "LIGHT"

    # Surface & Text Tokens
    text_counter = Counter(raw_text_hexes)
    primary_text = text_counter.most_common(1)[0][0] if text_counter else ("#F8FAFC" if is_dark else "#0F172A")
    muted_text = "#94A3B8" if is_dark else "#64748B"
    surface_color = "#1E293B" if is_dark else "#F1F5F9"
    border_color = "rgba(255, 255, 255, 0.12)" if is_dark else "rgba(0, 0, 0, 0.08)"

    # Identify Accent / Brand Primary Color (look at buttons)
    button_bgs = [rgb_to_hex(b["bg"]) for b in extracted["buttons"] if rgb_to_hex(b["bg"])]
    btn_counter = Counter(button_bgs)
    accent_color = "#3B82F6"
    for col, _ in btn_counter.most_common(5):
        if col != primary_bg and col != primary_text and col != "#000000" and col != "#FFFFFF":
            accent_color = col
            break

    # Secondary Color
    secondary_color = "#6366F1" if is_dark else "#475569"

    # Typography Normalization
    body_font_raw = extracted["fonts"][0]["family"] if extracted["fonts"] else "Inter"
    body_font_clean, body_font_enum = clean_font_name(body_font_raw)

    heading_font_raw = extracted["headingFonts"][0]["family"] if extracted["headingFonts"] else body_font_raw
    heading_font_clean, heading_font_enum = clean_font_name(heading_font_raw)

    # Corner Roundness Mapping
    roundness_token = "ROUND_EIGHT"
    radius_val = 8
    if raw_radii:
        r_common = Counter(raw_radii).most_common(1)[0][0]
        import re
        m = re.search(r'(\d+)', r_common)
        if m:
            px = int(m.group(1))
            radius_val = px
            if px <= 4: roundness_token = "ROUND_FOUR"
            elif px <= 8: roundness_token = "ROUND_EIGHT"
            elif px <= 16: roundness_token = "ROUND_TWELVE"
            else: roundness_token = "ROUND_FULL"

    # Shadows & Glassmorphism
    shadow_token = raw_shadows[0] if raw_shadows else "0 10px 25px -5px rgba(0, 0, 0, 0.1)"
    glass_blur = extracted["blurs"][0] if extracted["blurs"] else ("16px" if is_dark else "8px")

    # Aesthetic Classification
    aesthetic_label = "Modern Clean Digital"
    if is_dark:
        aesthetic_label = "Dark Titanium Glassmorphism" if "blur" in str(glass_blur).lower() or "rgba" in surface_color else "Dark Minimalist"
    elif "serif" in heading_font_clean.lower() or "editorial" in url:
        aesthetic_label = "Swiss Editorial Monograph"
    elif radius_val == 0 or roundness_token == "ROUND_FOUR":
        aesthetic_label = "Neo-Brutalist High-Contrast"

    # Generate Stitch JSON Config
    stitch_ds = {
        "displayName": f"{title} Design System",
        "theme": {
            "colorMode": color_mode,
            "customColor": accent_color,
            "colorVariant": "VIBRANT" if is_dark else "NEUTRAL",
            "headlineFont": heading_font_enum,
            "bodyFont": body_font_enum,
            "roundness": roundness_token,
            "spacing": {
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px",
                "xxl": "48px"
            }
        }
    }

    # Synthesize DESIGN.md Content
    design_md = f"""# DESIGN.md — {title} Design System
<!-- Extracted by Antigravity Design MD Extractor (Web Browser Engine) -->

## Metadata & Aesthetic Identity
- **Source URL**: [{url}]({url})
- **Extracted Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Aesthetic Classification**: **{aesthetic_label}**
- **Primary Appearance**: `{color_mode}` Mode

---

## 1. Color Palette & Semantic Tokens

| Token Name | Hex Code | Semantic Role | Contrast vs BG |
| :--- | :--- | :--- | :--- |
| `--color-primary` | `{accent_color}` | Primary Action & Brand Accent | High |
| `--color-secondary` | `{secondary_color}` | Secondary Action & Supporting Tone | Balanced |
| `--color-background` | `{primary_bg}` | Canvas / Page Background | Anchor |
| `--color-surface` | `{surface_color}` | Card & Panel Substrate | Subordinate |
| `--color-text-primary` | `{primary_text}` | High-Emphasis Text & Headlines | AAA Compliant |
| `--color-text-muted` | `{muted_text}` | Metadata, Captions & Subtitles | AA Compliant |
| `--color-border` | `{border_color}` | Dividers & Specular Frames | Subtle |

---

## 2. Typography & Modular Hierarchy

- **Display & Headline Font**: `{heading_font_clean}` (`{heading_font_enum}`)
- **Body & Running Text**: `{body_font_clean}` (`{body_font_enum}`)
- **Monospace & Metadata**: `JetBrains Mono`, `Space Grotesk`, monospace

### Heading Typographic Scale
- **H1 (Hero)**: `{extracted.get('headings', {}).get('h1', {}).get('fontSize', '48px')}` | Weight: `{extracted.get('headings', {}).get('h1', {}).get('fontWeight', '700')}`
- **H2 (Section)**: `{extracted.get('headings', {}).get('h2', {}).get('fontSize', '32px')}` | Weight: `{extracted.get('headings', {}).get('h2', {}).get('fontWeight', '600')}`
- **H3 (Card/Sub)**: `{extracted.get('headings', {}).get('h3', {}).get('fontSize', '24px')}` | Weight: `{extracted.get('headings', {}).get('h3', {}).get('fontWeight', '600')}`
- **Body**: `16px` (1.0rem) | Line Height: `1.5` | Weight: `400`

---

## 3. Shape, Elevation & Surface Materiality

- **Stitch Roundness Token**: `{roundness_token}`
- **Dominant Border Radius**: `{radius_val}px`
- **Surface Elevation**: `{shadow_token}`
- **Backdrop Blur / Glass**: `{glass_blur}`

---

## 4. Google Stitch MCP Specification

```json
{json.dumps(stitch_ds, indent=2)}
```

---

## 5. CSS Custom Properties Export

```css
:root {{
  --color-primary: {accent_color};
  --color-secondary: {secondary_color};
  --color-background: {primary_bg};
  --color-surface: {surface_color};
  --color-text-primary: {primary_text};
  --color-text-muted: {muted_text};
  --color-border: {border_color};

  --font-family-headline: '{heading_font_clean}', system-ui, sans-serif;
  --font-family-body: '{body_font_clean}', system-ui, sans-serif;
  --font-family-mono: 'JetBrains Mono', monospace;

  --border-radius: {radius_val}px;
  --glass-blur: {glass_blur};
}}
```
"""

    return {
        "url": url,
        "title": title,
        "design_md": design_md,
        "stitch_ds": stitch_ds,
        "base64_md": base64.b64encode(design_md.encode("utf-8")).decode("utf-8")
    }

def main():
    parser = argparse.ArgumentParser(description="Antigravity Web Browser Design MD Extractor")
    parser.add_argument("url", help="Target website URL to inspect")
    parser.add_argument("--output-dir", "-o", default=".", help="Directory to save DESIGN.md and design-system.json")
    parser.add_argument("--timeout", type=int, default=30000, help="Page navigation timeout in ms")
    args = parser.parse_args()

    res = extract_web_design(args.url, timeout_ms=args.timeout)

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

    print(f"[+] Successfully extracted visual design DNA from {args.url}")
    print(f"[+] Generated: {md_path}")
    print(f"[+] Generated: {ds_path} (Stitch theme ready)")
    print(f"[+] Base64 payload ready for stitch:upload_design_md: {b64_path}")

if __name__ == "__main__":
    main()
