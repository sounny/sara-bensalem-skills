# DESIGN.md — Canonical Design System Specification
<!-- Template & Schema for Antigravity Design MD Extractor -->

## Metadata & Aesthetic Identity
- **Source**: {SOURCE_NAME} ({SOURCE_TYPE}: `{SOURCE_URI_OR_PATH}`)
- **Extracted**: {EXTRACTION_TIMESTAMP}
- **Aesthetic Classification**: {AESTHETIC_TAG} (e.g. *Dark Titanium Glassmorphism*, *Swiss Editorial Monograph*, *Neo-Brutalist High-Contrast*, *Minimalist Studio*, *Warm Organic Editorial*)
- **Design Intent**: {DESIGN_SUMMARY}

---

## 1. Color Palette & Semantic Tokens

### Core Color Spectrum
| Token Name | Hex Code | RGB | OKLCH / HSL | Semantic Role | WCAG AAA Contrast |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `--color-primary` | `{HEX_PRIMARY}` | `{RGB_PRIMARY}` | `{HSL_PRIMARY}` | Primary Brand / Action Anchor | `{CONTRAST_PRIMARY}` |
| `--color-secondary` | `{HEX_SECONDARY}` | `{RGB_SECONDARY}` | `{HSL_SECONDARY}` | Supporting Accent / Subheadings | `{CONTRAST_SECONDARY}` |
| `--color-accent` | `{HEX_ACCENT}` | `{RGB_ACCENT}` | `{HSL_ACCENT}` | Interactive Highlights & Focus | `{CONTRAST_ACCENT}` |
| `--color-background` | `{HEX_BG}` | `{RGB_BG}` | `{HSL_BG}` | Canvas & Page Background | `{CONTRAST_BG}` |
| `--color-surface` | `{HEX_SURFACE}` | `{RGB_SURFACE}` | `{HSL_SURFACE}` | Card / Container Substrate | `{CONTRAST_SURFACE}` |
| `--color-surface-hover` | `{HEX_SURFACE_HOVER}` | `{RGB_SURFACE_HOVER}` | `{HSL_SURFACE_HOVER}` | Active / Hover Substrate | `{CONTRAST_SURFACE_HOVER}` |
| `--color-text-primary` | `{HEX_TEXT}` | `{RGB_TEXT}` | `{HSL_TEXT}` | High-Emphasis Body & Headlines | `{CONTRAST_TEXT}` |
| `--color-text-muted` | `{HEX_MUTED}` | `{RGB_MUTED}` | `{HSL_MUTED}` | Captions, Metadata & Folios | `{CONTRAST_MUTED}` |
| `--color-border` | `{HEX_BORDER}` | `{RGB_BORDER}` | `{HSL_BORDER}` | Structural Dividers & Outlines | `{CONTRAST_BORDER}` |

### Color Mode & Dynamic Variant
- **Appearance Mode**: `{COLOR_MODE}` (LIGHT | DARK)
- **Stitch Color Variant**: `{STITCH_COLOR_VARIANT}` (MONOCHROME | NEUTRAL | TONAL_SPOT | VIBRANT | EXPRESSIVE | FIDELITY)

---

## 2. Typography & Scalar Rhythm

### Typeface Hierarchy
- **Display & Headline Font**: `{FONT_HEADLINE}` (Fallback: `{FONT_HEADLINE_FALLBACK}`)
- **Body & Narrative Font**: `{FONT_BODY}` (Fallback: `{FONT_BODY_FALLBACK}`)
- **Metadata & Monospace Font**: `{FONT_MONO}` (Fallback: `{FONT_MONO_FALLBACK}`)
- **Baseline Grid Interval**: `{BASELINE_INTERVAL}` (e.g. `4pt` / `8pt` / `0.25rem`)

### Modular Type Scale
| Level | Font Size | Line Height | Weight | Letter Spacing | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `display-lg` | `{SIZE_DISPLAY}` | `{LH_DISPLAY}` | `{WEIGHT_DISPLAY}` | `{TRACKING_DISPLAY}` | Hero Openers & Monumental Headers |
| `headline-h1` | `{SIZE_H1}` | `{LH_H1}` | `{WEIGHT_H1}` | `{TRACKING_H1}` | Page Titles & Project Names |
| `headline-h2` | `{SIZE_H2}` | `{LH_H2}` | `{WEIGHT_H2}` | `{TRACKING_H2}` | Major Section Headers |
| `headline-h3` | `{SIZE_H3}` | `{LH_H3}` | `{WEIGHT_H3}` | `{TRACKING_H3}` | Subsection Headers |
| `body-lg` | `{SIZE_BODY_LG}` | `{LH_BODY_LG}` | `{WEIGHT_BODY_LG}` | `{TRACKING_BODY_LG}` | Lead Paragraphs & Abstract |
| `body-md` | `{SIZE_BODY_MD}` | `{LH_BODY_MD}` | `{WEIGHT_BODY_MD}` | `{TRACKING_BODY_MD}` | Standard Running Text |
| `caption` | `{SIZE_CAPTION}` | `{LH_CAPTION}` | `{WEIGHT_CAPTION}` | `{TRACKING_CAPTION}` | Drawing Annotations & Legends |
| `mono-data` | `{SIZE_MONO}` | `{LH_MONO}` | `{WEIGHT_MONO}` | `{TRACKING_MONO}` | Project Passports, Scales, Coords |

---

## 3. Spatial Layout & Grid System

### Columnar & Margin Geometry
- **Grid Structure**: `{GRID_COLUMNS}` (e.g. 12-Column Swiss Modular | 8-Column Editorial | 4-Column Mobile)
- **Gutter Width**: `{GRID_GUTTER}` (e.g. `16px` / `5mm`)
- **Page / Canvas Margins**:
  - Top: `{MARGIN_TOP}`
  - Bottom: `{MARGIN_BOTTOM}`
  - Left / Inner (Gutter Creep): `{MARGIN_LEFT}`
  - Right / Outer: `{MARGIN_RIGHT}`
- **Max Content Width**: `{CONTAINER_MAX_WIDTH}` (e.g. `1280px` / `A3 Spread 420mm`)

### Spacing Scale
```css
--space-1: 4px;   /* 0.25rem */
--space-2: 8px;   /* 0.50rem */
--space-3: 12px;  /* 0.75rem */
--space-4: 16px;  /* 1.00rem */
--space-6: 24px;  /* 1.50rem */
--space-8: 32px;  /* 2.00rem */
--space-12: 48px; /* 3.00rem */
--space-16: 64px; /* 4.00rem */
```

---

## 4. Shape, Elevation & Surface Materiality

- **Corner Roundness (Stitch Token)**: `{ROUNDNESS_TOKEN}` (`ROUND_FOUR` | `ROUND_EIGHT` | `ROUND_TWELVE` | `ROUND_FULL`)
- **Border Radius Scale**:
  - `sm`: `{RADIUS_SM}`
  - `md`: `{RADIUS_MD}`
  - `lg`: `{RADIUS_LG}`
  - `full`: `9999px`
- **Surface Elevation & Shadows**:
  - `shadow-sm`: `{SHADOW_SM}`
  - `shadow-md`: `{SHADOW_MD}`
  - `shadow-lg`: `{SHADOW_LG}`
- **Glassmorphism & Optical Filters**:
  - Backdrop Blur: `{GLASS_BLUR}`
  - Surface Saturation: `{GLASS_SATURATION}`
  - Specular Stroke: `{SPECULAR_STROKE}`

---

## 5. UI Component Archetypes

### Buttons & Interactive Controls
- **Primary Action**: `{BUTTON_PRIMARY_STYLE}`
- **Secondary / Subtle**: `{BUTTON_SECONDARY_STYLE}`
- **Ghost / Text**: `{BUTTON_GHOST_STYLE}`
- **Pill / Badge**: `{BADGE_STYLE}`

### Cards & Viewport Panels
- Substrate treatment, padding, and hover elevation transitions.

### Data Tables & Project Passports
- Swiss typographic data blocks with monospace labels and bold tabular values.

---

## 6. Google Stitch Theme JSON Bridge

```json
{
  "displayName": "{STITCH_DISPLAY_NAME}",
  "theme": {
    "colorMode": "{STITCH_COLOR_MODE}",
    "customColor": "{HEX_PRIMARY}",
    "colorVariant": "{STITCH_COLOR_VARIANT}",
    "headlineFont": "{STITCH_HEADLINE_FONT}",
    "bodyFont": "{STITCH_BODY_FONT}",
    "roundness": "{ROUNDNESS_TOKEN}"
  }
}
```

---

## 7. CSS Custom Properties Export

```css
:root {
  /* Colors */
  --color-primary: {HEX_PRIMARY};
  --color-secondary: {HEX_SECONDARY};
  --color-accent: {HEX_ACCENT};
  --color-background: {HEX_BG};
  --color-surface: {HEX_SURFACE};
  --color-text-primary: {HEX_TEXT};
  --color-text-muted: {HEX_MUTED};
  --color-border: {HEX_BORDER};

  /* Typography */
  --font-family-headline: '{FONT_HEADLINE}', system-ui, sans-serif;
  --font-family-body: '{FONT_BODY}', system-ui, sans-serif;
  --font-family-mono: '{FONT_MONO}', monospace;

  /* Shape & Elevation */
  --border-radius: {RADIUS_MD};
  --shadow-card: {SHADOW_MD};
  --glass-blur: {GLASS_BLUR};
}
```
