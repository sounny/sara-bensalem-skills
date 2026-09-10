---
name: editorial-studio
description: Production-grade Antigravity publishing and visual product design system for books, magazines, architectural monographs, and portfolios. Enforces Swiss typographic discipline, multi-spread narrative pacing, ISO 128 vector drafting, dual-engine compilation (Typst + Paged.js), and automated preflight print compliance.
---

# Editorial Studio (`editorial-studio`)
### *Frontier Publishing, Architectural Monograph Engineering & Print Production System*

`editorial-studio` is a production-grade Antigravity publishing and visual engineering skillset. It empowers AI agents and design engineers to author publication-grade books, magazines, architectural monographs, and portfolios that withstand forensic examination by senior design directors, technical partners, jury chairs, and prepress printers.

The engine replaces superficial 3D renders with undeniable constructive proof, eliminates typographic disorder through Swiss modular grids and baseline locking, and guarantees physical press compliance via automated prepress audits.

---

## 1. System Architecture & 5-Persona Agent Assembly

`editorial-studio` operates through a decoupled, multi-agent assembly of 5 specialized editorial personas. Each persona has typed input/output contracts, mathematical formulas, and domain constraints:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        EDITORIAL STUDIO MULTI-AGENT ARCHITECTURE                       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   ┌───────────────────────────────┐              ┌─────────────────────────────────┐   │
│   │      ART DIRECTOR AGENT       │              │        TYPOGRAPHER AGENT        │   │
│   │  • 5-Act Narrative Curation   │              │  • Tripartite Font Mapping      │   │
│   │  • 12-Column Swiss Geometry   │              │  • 4pt/6pt Baseline Locking     │   │
│   │  • Physical Palette Tokens    │              │  • Knuth-Plass & Hanging Punct. │   │
│   │  • Whitespace Discipline      │              │  • Zero 1-Word Orphans / Widows │   │
│   └───────────────┬───────────────┘              └────────────────┬────────────────┘   │
│                   │                                               │                    │
│                   ▼                                               ▼                    │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               COMPOSITOR AGENT                                 │   │
│   │   • Asymmetric Facing Spreads (Recto/Verso Dynamic Tension)                    │   │
│   │   • Binding Mechanics & Automated Gutter Creep Calculus                        │   │
│   │   • Running Folios, Section Headers, Image Framing & Bleeds                    │   │
│   └───────────────┬───────────────────────────────────────────────┬────────────────┘   │
│                   │                                               │                    │
│                   ▼                                               ▼                    │
│   ┌───────────────────────────────┐              ┌─────────────────────────────────┐   │
│   │   TECTONIC VECTOR DETAILER    │              │      PRE-FLIGHT AUDITOR         │   │
│   │  • ISO 128 Stroke Hierarchy   │              │  • PDF/X-4 Standards Conformance│   │
│   │  • 1:20 Wall Section & Glaser │              │  • FOGRA51/52 CMYK & TAC ≤ 320% │   │
│   │  • 1:5 Joinery & Reveals      │              │  • 3.0mm Bleeds & 5mm Safety    │   │
│   │  • Scale-Aware Downsampling   │              │  • 100% Subsetting & DPI ≥ 300  │   │
│   │  • Standardized Passports     │              │  • Vision Collision Linting     │   │
│   └───────────────────────────────┘              └─────────────────────────────────┘   │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### The 5 Editorial Personas

1. **Art Director (`personas/art_director.md`)**:
   - Formulates the 5-act dramaturgical narrative arc (*Hook → Context → Anatomy → Tectonic Proof → Lived Climax*).
   - Establishes the 12-column modular grid structure and negative space budget ($\ge 30\text{--}35\%$).
   - Configures the archival physical palette tokens (Bone `#F8F8F5`, Graphite `#111110`, Hairline `#DDD9D0`, Warm Greige `#C2BEB4`, Terracotta `#7A4D3B`).
   - Assigns layout archetypes to facing spreads, maintaining recto/verso visual tension.

2. **Typographer (`personas/typographer.md`)**:
   - Implements the tripartite font architecture: Structural Grotesque (display/headers), Rationalist Serif (curatorial body), and Technical Monospace (metadata, scale bars, project passports).
   - Calibrates the modular type scale (64pt, 24pt, 12pt, 9.5pt, 7.5pt, 6.5pt).
   - Locks all elements to a $4\,\text{pt}$ or $6\,\text{pt}$ baseline grid ($y_{\text{snapped}} = \text{round}(y/B) \cdot B$) ensuring zero vertical offset variance across the spine ($\Delta y < 0.25\,\text{pt}$).
   - Enforces optical hanging punctuation, Knuth-Plass global line breaks, non-breaking space insertion to eliminate 1-word orphans, and widow penalties $\ge 2$ lines.

3. **Compositor (`personas/compositor.md`)**:
   - Translates blueprints and typographic rules into balanced 2-page facing spreads.
   - Enforces cognitive anchoring on the verso (analytical density, tables, structured text) and visual projection on the recto (hero drawings, expansive plates).
   - Computes mechanical gutter creep based on page count ($N$), leaf caliper ($c$), signature size ($S$), and binding style (Smyth-sewn, PUR perfect bound, lay-flat).
   - Adjusts running folios, margins, and crossover image splits.

4. **Tectonic Vector Detailer (`personas/tectonic_detailer.md`)**:
   - Eliminates the 12 lethal "3D render traps" by providing undeniable constructive proof.
   - Drafts dimensioned $1:20$ constructive wall sections with Glaser hygrothermal $U$-value calculation ($U \le 0.15\,\text{W/m}^2\cdot\text{K}$ Passivhaus) and continuous thermal breaks.
   - Details $1:5$ bespoke interior joinery with $3\text{--}8\,\text{mm}$ shadow line reveals (*joint creux*) and hardware clearance pockets.
   - Drafts $1:100$ plans verifying PMR/ADA compliance ($\varnothing 1500\,\text{mm}$ turning circles, $\ge 830\,\text{mm}$ door openings, $\le 30\,\text{m}$ egress paths).
   - Applies scale-aware vector downsampling with stroke clamping ($w_{\min} \ge 0.08\,\text{mm}$) and hatch decimation.
   - Generates standardized Project Passport metadata blocks.

5. **Pre-flight Auditor (`personas/preflight_auditor.md`)**:
   - Validates compiled PDF artifacts against PDF/X-4 (ISO 15930-7) standards.
   - Audits FOGRA51/52 CMYK color spaces and enforces Total Area Coverage ($\text{TAC} \le 320\%$).
   - Verifies $3.0\,\text{mm}$ bleed boundaries, MediaBox/TrimBox deltas, and $5.0\,\text{mm}$ safety margins.
   - Inspects font embedding (100% embedded subsets with `^[A-Z]{6}\+` prefix) and effective image resolution ($\ge 300\,\text{DPI}$).
   - Runs vision-in-the-loop rasterization and polygon bounding-box collision detection to flag text/image overlap.
   - Computes the 100-point Sara Bensalem audit score across 5 categories.

---

## 2. The 5-Act Architectural Narrative Monograph Structure

Every architectural monograph or portfolio case study must be structured across 2 to 4 consecutive 2-page facing spreads (4 to 8 pages) adhering to the 5-Act Dramaturgical Arc:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 5-ACT ARCHITECTURAL NARRATIVE ARC                           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  SPREAD 1 (ACT 1 & ACT 2): THE HOOK, PASSPORT & TERRITORIAL CONTEXT                    │
│  ┌─────────────────────────────┬─────────────────────────────┐                         │
│  │ VERSO (Left): Act 1         │ RECTO (Right): Act 2        │                         │
│  │ • Standardized Passport     │ • Territorial Morphology    │                         │
│  │ • Executive Premise         │ • Solar Azimuth Vectors     │                         │
│  │ • Work Rights & Role Specs  │ • Prevailing Wind Loops     │                         │
│  │ • Software Toolchain        │ • Large Muted Chapter "01"  │                         │
│  └─────────────────────────────┴─────────────────────────────┘                         │
│                                                                                        │
│  SPREAD 2 (ACT 3): SPATIAL ANATOMY (1:100 PLAN)                                        │
│  ┌─────────────────────────────┬─────────────────────────────┐                         │
│  │ VERSO (Left): Massing Logic │ RECTO (Right): 1:100 Plan   │                         │
│  │ • 3-Step Volumetric Axon    │ • Dimensioned Column Grid   │                         │
│  │ • Structural Load Transfer  │ • PMR 1500mm Turning Arc    │                         │
│  │ • Circulation Hierarchy     │ • Door Clear Openings       │                         │
│  │ • Egress Distance Vectors   │ • Threshold Transition Cuts │                         │
│  └─────────────────────────────┴─────────────────────────────┘                         │
│                                                                                        │
│  SPREAD 3 (ACT 4): TECTONIC PROOF (HERO 1:20 WALL SECTION)                             │
│  ┌─────────────────────────────┬─────────────────────────────┐                         │
│  │ VERSO (Left): Physics Table │ RECTO (Right): 1:20 Section │                         │
│  │ • Layered Material Schedule │ • Full-Height Cut Vector    │                         │
│  │ • Glaser U-Value & Dew Pt   │ • ISO 128 Calibrated Strokes│                         │
│  │ • Embodied CO2 Metrics      │ • Continuous Thermal Breaks │                         │
│  │ • Cavity Ventilation Notes  │ • Millimeter Cotations      │                         │
│  └─────────────────────────────┴─────────────────────────────┘                         │
│                                                                                        │
│  SPREAD 4 (ACT 5): LIVED CLIMAX & TACTILE SCENOGRAPHY                                  │
│  ┌─────────────────────────────┬─────────────────────────────┐                         │
│  │ VERSO (Left): 1:5 Millwork  │ RECTO (Right): Scenography  │                         │
│  │ • 3mm Shadow Line Reveal    │ • Atmospheric Light Plate   │                         │
│  │ • Concealed Hinge Clearance │ • Tactile Material Triptych │                         │
│  │ • Tactile Hardware Spec     │ • Project Colophon & Notes  │                         │
│  └─────────────────────────────┴─────────────────────────────┘                         │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### The 10 Layout Archetypes
1. **The Project Passport**: Verso anchor with metadata card, thesis statement, candidate role, and work rights.
2. **The Constructive Proof (1:20 Section)**: Technical hero plate with multi-layered envelope callouts, thermal breaks, and dimension chains.
3. **The Spatial Anatomy (1:100 Plan)**: Uncropped floor plan with multi-axis column grid (1–17, A–L), PMR turning circles, and egress paths.
4. **The Cartographic Context**: Scaled regional morphology ($1:2000$), topography contours, solar vectors, and water flows.
5. **The Environmental Engine**: Thermodynamic bioclimatic diagrams, stack ventilation loops, and diurnal thermal mass damping.
6. **The Tectonic Triptych (1:5 Joinery)**: Custom cabinetry details, shadow reveals, concealed hinge pockets, and material swatches.
7. **The Process Matrix**: Massing transformations, structural calculation sketches, and study model iterations.
8. **The Scenographic Spread**: Single high-contrast raking light photograph or perspective rendering grounded by technical micro-captions.
9. **The Urban Territory**: CPTED sightline analysis, public/private threshold zoning, active ground floor transparency.
10. **The Typographic Index**: Comprehensive project catalog, drawing register, engineering team credits, and colophon.

---

## 3. Swiss Modular Grid & Micro-Typography Engine

### Tripartite Font Mapping Architecture

Typography is strictly decoupled into three distinct functional voices:

| Family Classification | Recommended Font Families | Hierarchy Roles | Typographic Parameters |
|:---|:---|:---|:---|
| **Structural Grotesque** | Space Grotesk, Inter, Neue Haas Grotesk, Univers, Plus Jakarta Sans | Spread titles, chapter indices, act badges, section subheads | Weight: 600–700; Tracking: $-0.02\,\text{em}$ (Display), $+0.08\,\text{em}$ (All-Caps Subheads) |
| **Rationalist Serif** | Adobe Garamond Pro, Minion Pro, Source Serif 4, EB Garamond, Tiempos | Curatorial essays, executive premises, historical narratives | Weight: 400; Size: 8.5–10pt; Leading: 12–14pt; Measure: 45–65 characters per line |
| **Technical Monospace** | JetBrains Mono, IBM Plex Mono, Fira Code | Project Passports, dimension strings, scale bars, callouts, folios | Weight: 500; Size: 7–8pt; Leading: 10pt; Tracking: $+0.04\,\text{em}$; Tabular lining figures |

### Baseline Grid Locking Mathematics
- **Grid Increment ($B$):** Standardized at **$4\,\text{pt}$ or $6\,\text{pt}$** (with $12\,\text{pt}$ macro increments).
- **Universal Snapping Formula:**
  $$y_{\text{snapped}} = \text{round}\left(\frac{y}{B}\right) \times B$$
  $$h_{\text{snapped}} = \text{ceil}\left(\frac{h}{B}\right) \times B$$
- **Cross-Spine Alignment Requirement:**
  Body text baselines on the left page (verso) must register horizontally across the binding fold with body text baselines on the right page (recto):
  $$\Delta y = |y_{\text{verso\_baseline}} - y_{\text{recto\_baseline}}| < 0.25\,\text{pt}$$

### Micro-Typographic Refinement Rules
1. **Optical Hanging Punctuation (Protrusion):**
   - Opening/closing quotation marks (`“`, `‘`, `«`): $100\%$ glyph width protrusion outside margin.
   - Hyphens (`-`), en-dashes (`–`), em-dashes (`—`): $60\%\text{--}75\%$ protrusion.
   - Periods (`.`) and commas (`,`): $70\%\text{--}80\%$ protrusion.
2. **Knuth-Plass Paragraph Breaking:**
   - Evaluates line-break nodes globally to minimize paragraph badness:
     $$\text{Badness } b = 100 \times \left|\frac{\text{target space} - \text{actual space}}{\text{stretch/shrink}}\right|^3$$
     $$\text{Demerits } d = (1 + b + p)^2 + q$$
     where $p \ge 50$ is hyphen penalty, and $q \ge 3000$ is consecutive hyphen penalty.
3. **Widow & Orphan Elimination:**
   - **Zero 1-Word Orphans:** Trailing lines of paragraphs must never contain a single isolated word. A non-breaking space (`~` in Typst, `&nbsp;` in HTML) must bind the penultimate and ultimate words:
     $$\text{"materials"} + \text{" "} + \text{"assembled."} \longrightarrow \text{"materials~assembled."}$$
   - **Widow & Orphan Threshold $\ge 2$ Lines:** Paragraph splits across columns or pages must keep at least 2 lines together on both pages (`orphans: 2; widows: 2;`).

---

## 4. Binding Mechanics & Gutter Creep Calculus

Sheet thickness and binding clamps displace printable margins across multi-page books. The compositor dynamically computes progressive margins:

### Parameters
- $N$: Total page count.
- $p$: Current 1-based page number ($1 \le p \le N$).
- $c$: Paper caliper in millimeters ($100\,\text{gsm} \approx 0.10\,\text{mm}$; $150\,\text{gsm} \approx 0.15\,\text{mm}$; $170\,\text{gsm} \approx 0.18\,\text{mm}$).
- $S$: Signature size (typically 16 or 32 pages).
- $M_{\text{inner, base}}$: Nominal inner margin ($20.0\,\text{mm}$).
- $M_{\text{outer, base}}$: Nominal outer margin ($18.0\,\text{mm}$).
- $G_{\text{draw}}$: Spine glue clamp gutter draw ($6.0\text{--}9.0\,\text{mm}$).

### Formulas by Binding Type

1. **Smyth-Sewn Signatures:**
   For page $p$, signature sheet index $j = (p - 1) \bmod S$:
   $$\text{leaf}(j) = \min\left(\lfloor j / 2 \rfloor, \, \frac{S}{2} - 1 - \lfloor j / 2 \rfloor\right)$$
   $$\Delta_{\text{creep}}(p) = c \times \text{leaf}(j)$$
   $$M_{\text{inner}}(p) = M_{\text{inner, base}} + \Delta_{\text{creep}}(p), \quad M_{\text{outer}}(p) = M_{\text{outer, base}} - \Delta_{\text{creep}}(p)$$

2. **Perfect Bound / PUR Adhesive:**
   - **Single-Leaf Cut PUR Binding:** Individual leaves are trimmed flush and milled at the spine; pages are not nested. Therefore, shingle creep is strictly zero ($\text{Shingle}(p) \equiv 0.0\,\text{mm}$), and only spine glue draw applies:
     $$M_{\text{inner}}(p) = M_{\text{inner, base}} + G_{\text{draw}}, \quad M_{\text{outer}}(p) = M_{\text{outer, base}}$$
     where $G_{\text{draw}} = 7.0\text{--}9.0\,\text{mm}$ (nominal $7.5\,\text{mm}$).
   - **Folded-Signature PUR Binding (Burst / Milled Signatures):** Sheets are gathered in folded signatures of $S$ pages (typically $S=16$ or $32$). Shingling applies strictly per signature (cyclical across signature size $S$, not globally across book block $N$):
     $$j = (p - 1) \bmod S$$
     $$\text{leaf}(j) = \min\left(\lfloor j / 2 \rfloor, \, \frac{S}{2} - 1 - \lfloor j / 2 \rfloor\right)$$
     $$\text{Shingle}(p) = c \times \text{leaf}(j)$$
     $$M_{\text{inner}}(p) = M_{\text{inner, base}} + G_{\text{draw}} + \text{Shingle}(p)$$
   - **Prepress Outer Margin Safety Clamping:** For all PUR binding configurations, the outer margin is clamped to guarantee the prepress safety buffer:
     $$M_{\text{outer}}(p) = \max\left(M_{\text{outer, base}} - \text{Shingle}(p),\, 5.0\,\text{mm}\right)$$
     preventing content clipping even at extreme page counts ($N = 500$).

3. **Lay-Flat Board-Mounted:**
   $$G_{\text{draw}} \equiv 0.0\,\text{mm}, \quad \Delta_{\text{creep}} \equiv 0.0\,\text{mm}$$
   $$M_{\text{inner}}(p) = M_{\text{inner, base}}, \quad M_{\text{outer}}(p) = M_{\text{outer, base}}$$

4. **Saddle-Stitched Booklets ($N \le 64$ pages, or 96 with thin paper $\le 100\,\text{gsm}$):**
   Saddle-stitching is restricted to booklets with $N \le 64$ pages (or 96 with thin paper). Imposition symmetry is enforced using the discrete leaf-indexed formula so that both recto and verso of the identical physical leaf experience identical displacement ($\Delta_{\text{creep}}(1) = \Delta_{\text{creep}}(2) = 0.0\,\text{mm}$):
   $$\text{leaf}(p) = \left\lfloor \frac{p - 1}{2} \right\rfloor$$
   $$\Delta_{\text{creep}}(p) = c \times \left( \frac{N}{4} - \min\left(\text{leaf}(p),\, \frac{N}{2} - 1 - \text{leaf}(p)\right) \right)$$
   or normalized relative to the outermost wrap sheet:
   $$\Delta_{\text{creep}}(p) = c \times \min\left(\text{leaf}(p),\, \frac{N}{2} - 1 - \text{leaf}(p)\right)$$
   $$M_{\text{inner}}(p) = M_{\text{inner, base}} + \Delta_{\text{creep}}(p), \quad M_{\text{outer}}(p) = \max\left(M_{\text{outer, base}} - \Delta_{\text{creep}}(p),\, 5.0\,\text{mm}\right)$$

---

## 5. Orthographic Technical Drafting & ISO 128 Standards

### ISO 128 Calibrated Stroke Weight Hierarchy

All vector drawings (SVGs, Typst shapes, CeTZ paths) must adhere strictly to standard metric line widths:

| Metric Width | Point Width | Hex Color | Architectural & Detailing Application |
|:---|:---|:---|:---|
| **0.70 mm** | **2.00 pt** | `#111110` | Ground cut, bedrock datum, heavy mass cut plane |
| **0.50 mm** | **1.42 pt** | `#111110` | Primary structural cut plane (concrete slabs, steel columns, loadbearing walls) |
| **0.35 mm** | **1.00 pt** | `#33322E` | Secondary partitions, window/door frames, joinery carcass |
| **0.25 mm** | **0.71 pt** | `#55544E` | Uncut projected edges, dimension chains, witness lines, leader arrows |
| **0.13 mm** | **0.37 pt** | `#84827A` | Material hatching, thermal insulation cross-hatch, centerlines, structural grid |
| **0.25 mm Dash** | **0.71 pt** | `#111110` | EPDM waterproof membranes, concealed structure, PMR turning circle arc |
| **0.35 mm Dot** | **1.00 pt** | `#8B263E` | Section cut indicator, emergency egress travel paths |

### Scale-Aware Vector Downsampling Algorithm
When resizing vector plates to fit half-page or quadrant frames ($S_r < 1.0$):
1. **Stroke Clamping:**
   $$w_{\text{effective}} = \max(w_{\text{native}} \cdot S_r, \, w_{\min})$$
   where $w_{\min} = 0.08\,\text{mm}$ ($0.227\,\text{pt}$) for offset print ($0.10\,\text{mm}$ laser).
2. **Hatch Decimation:**
   Let $s$ be native hatch spacing, scaled spacing $s' = s \cdot S_r$:
   - $s' \ge 0.75\,\text{mm}$: Retain individual hatch lines.
   - $0.35\,\text{mm} \le s' < 0.75\,\text{mm}$: Decimate lines by $2\times$ ($s_{\text{new}} = 2s'$).
   - $s' < 0.35\,\text{mm}$: Replace line hatching with solid $10\%$ tint poché (`fill="#F1F1EB"`).
3. **Annotation Culling:**
   - $S_r \ge 0.75$: Render all dimension strings and layer callouts.
   - $0.40 \le S_r < 0.75$: Suppress sub-layer dimensions; retain overall thickness and structural grid.
   - $S_r < 0.40$: Suppress all internal dimensions; retain only graphic scale bar and north arrow.

### Constructive Physics & Envelope Detailing
1. **Hygrothermal Glaser U-Value Calculation:**
   Layer thickness input in millimeters must be converted to meters ($d_i = \text{thickness\_mm} \times 10^{-3}\,\text{m}$):
   $$R_i = \frac{\text{thickness\_mm} \times 10^{-3}}{\lambda_i}, \quad R_{\text{tot}} = R_{\text{si}} + \sum_{i=1}^n R_i + R_{\text{se}}$$
   $$U = \frac{1}{R_{\text{tot}}}$$
   - Passivhaus standard: $U \le 0.15\,\text{W/m}^2\cdot\text{K}$.
   - RE2020 standard: $U \le 0.20\,\text{W/m}^2\cdot\text{K}$.
   - Continuous thermal breaks (Schöck Isokorb, cellular glass plinths, EPDM seals) required across all envelope penetrations.
2. **1:5 Bespoke Joinery Reveals:**
   - Mandatory $3\text{--}8\,\text{mm}$ negative shadow reveal (*joint creux*) at all perimeter cabinet junctions to absorb seasonal hygroscopic expansion ($2\text{--}3\,\text{mm/m}$).
   - Blum/Hettich concealed hinge cup pockets routed to $12.8\,\text{mm}$ depth in $\ge 19\,\text{mm}$ carcase substrate.
3. **PMR / ADA Egress Verification:**
   - $\varnothing 1500\,\text{mm}$ wheelchair turning circles unencumbered by door swings.
   - Clear door opening width $\ge 830\,\text{mm}$ ($900\,\text{mm}$ leaf).
   - Maximum egress travel distance $\le 30\,\text{m}$ ($\le 45\,\text{m}$ if sprinklered).

---

## 6. Standardized Project Passport Schema

Every project opening spread must feature an uncropped Project Passport data block:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ProjectPassport",
  "type": "object",
  "required": [
    "title", "typology", "location", "coordinates", "year", "area_m2",
    "client", "stage", "candidate_role", "line_item_contributions",
    "software_stack", "work_authorization", "executive_premise"
  ],
  "properties": {
    "title": {"type": "string"},
    "typology": {"type": "string"},
    "location": {"type": "string"},
    "coordinates": {"type": "string"},
    "year": {"type": "string"},
    "area_m2": {"type": "number"},
    "budget_eur": {"type": "integer"},
    "client": {"type": "string"},
    "stage": {"type": "string"},
    "team_size": {"type": "integer"},
    "candidate_role": {"type": "string"},
    "line_item_contributions": {
      "type": "array",
      "items": {"type": "string"},
      "minItems": 3
    },
    "software_stack": {
      "type": "array",
      "items": {"type": "string"}
    },
    "work_authorization": {"type": "string"},
    "executive_premise": {"type": "string"}
  }
}
```

---

## 7. Dual-Engine Compilation & Layout Framework

The system provides declarative parity between two compilation targets:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              DUAL-ENGINE COMPILATION TARGETS                           │
├──────────────────────────────────────────┬─────────────────────────────────────────────┤
│ TYPST ENGINE                             │ PAGED.JS / HTML-CSS ENGINE                  │
├──────────────────────────────────────────┼─────────────────────────────────────────────┤
│ • Sub-second native CLI compilation      │ • W3C CSS Paged Media (@page, @bottom)      │
│ • Direct mathematical baseline locking   │ • Headless Chromium / Puppeteer export      │
│ • CeTZ & native SVG vector integration   │ • Interactive spread inspection in browser  │
│ • Ideal for rapid compilation (< 3s)     │ • Dynamic CSS Grid/Flexbox & web viewer     │
└──────────────────────────────────────────┴─────────────────────────────────────────────┘
```

### CLI Build Procedures

1. **Typst Build:**
   ```bash
   # Direct Typst compilation
   typst compile engine/typst/template.typ output/publication.pdf --root .
   ```
2. **Paged.js Build:**
   ```bash
   # Headless browser compilation via pagedjs-cli
   pagedjs-cli engine/pagedjs/template.html -o output/publication.pdf --paper-size A4 --landscape
   ```
3. **Unified Compilation CLI (`compile.py`):**
   ```bash
   python engine/compile.py \
     --engine typst \
     --manifest examples/monograph/manifest.json \
     --output dist/monograph_typst.pdf
   ```

---

## 8. Automated Preflight Validation & Vision-in-the-Loop Linting

The preflight audit script (`audit_publication.py`) executes automated checks prior to release:

1. **PDF/X-4 Conformance:** Conforms to ISO 15930-7 (OutputIntents dictionary, GTS_PDFXVersion, Trapped flag).
2. **Color Space & Total Area Coverage (TAC):**
   - Color model must be FOGRA51 (PSO Coated v3) or FOGRA52 (PSO Uncoated v3) CMYK.
   - Total Area Coverage evaluated pixel-by-pixel:
     $$\text{TAC}(x,y) = C(x,y) + M(x,y) + Y(x,y) + K(x,y) \le 320\%$$
3. **Bleeds & Margins:**
   - BleedBox must exceed TrimBox by exactly $3.0\,\text{mm}$ on all bleeding edges.
   - Margin safety zone: zero text or critical annotations within $5.0\,\text{mm}$ of the TrimBox line.
4. **Font Subsetting:**
   - 100% of fonts must be embedded as subsets with `^[A-Z]{6}\+` prefix. No Type 3 bitmap fonts.
5. **Image Resolution:**
   - Effective resolution at physical printed size: $\text{DPI} \ge 300\,\text{DPI}$ (line art $\ge 1200\,\text{DPI}$).
6. **Vision-in-the-Loop Collision Linting:**
   - Spreads rendered to 300 DPI rasters; OCR and element bounding boxes extracted.
   - Axis-Aligned Bounding Box (AABB) intersection testing ensures zero text-graphic collisions:
     $$\text{BBox}_{\text{text}} \cap \text{BBox}_{\text{graphic}} = \emptyset$$

### Preflight Audit CLI Signature & Schema
```bash
python preflight/audit_publication.py dist/monograph.pdf --icc FOGRA51 --json dist/audit.json
```

---

## 9. The 100-Point Sara Bensalem Portfolio Audit Rubric

Every architectural portfolio or monograph is evaluated across 5 core dimensions (passing score $\ge 85/100$):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 100-POINT SARA BENSALEM AUDIT RUBRIC                        │
├──────────────────────────────────────┬───────┬─────────────────────────────────────────┤
│ Dimension                            │ Score │ Criteria & Verification Check           │
├──────────────────────────────────────┼───────┼─────────────────────────────────────────┤
│ 1. Constructive & Tectonic Proof     │ 25 pt │ 1:20 wall section, EPDM, PIR, mm dims   │
│ 2. Spatial Anatomy & Statutory Egress│ 20 pt │ 1:100 plan, PMR 1500mm arc, door widths │
│ 3. Bioclimatic & Environmental Physics│ 15 pt │ Glaser U-value, solar azimuth, wind loop│
│ 4. 5-Act Narrative Curation          │ 20 pt │ Hook -> Context -> Anatomy -> Tech -> Climax │
│ 5. Swiss Typographic Grid Integrity  │ 20 pt │ 12-col grid, baseline lock, passports   │
├──────────────────────────────────────┼───────┼─────────────────────────────────────────┤
│ TOTAL PASSING THRESHOLD              │ 85/100│ Reject if < 85 or any lethal antipattern│
└──────────────────────────────────────┴───────┴─────────────────────────────────────────┘
```

---

## 10. Commercial Service Packages

The insights and auditing capabilities of `editorial-studio` translate directly into 5 sellable commercial offerings:
1. **The 100-Point Forensic Portfolio Audit & Roast** ($250 – $500): 12–15 page diagnostic PDF, scorecard, red-flag breakdown, and layout re-ordering roadmap.
2. **The 5-Act Monograph Redesign & Layout Service** ($1,200 – $3,500): Full restructuring of raw assets into a 24–40 page Swiss monograph (print PDF + editable package).
3. **The "Tectonic Rescue" 1:20 Construction Detailing Service** ($1,500 – $4,000): Drafting publication-grade 1:20 wall sections, 1:5 millwork reveals, and Glaser calculations for conceptual 3D projects.
4. **Interactive Web Monograph & Spatial-Stitch Prototyping** ($2,500 – $7,500): Responsive dark titanium glassmorphic web portfolio with SVG layer toggles and 60fps scrolling.
5. **Socratic Interview & Defense Simulator** ($350 – $750): 3 simulated technical grilling rounds preparing candidates for Senior Associate/Project Architect interviews.
