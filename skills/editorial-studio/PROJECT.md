# Project: editorial-studio

## Architecture
`editorial-studio` is a production-grade Antigravity publishing and visual product design system for books, magazines, architectural monographs, and portfolios.
The system is built on a modular, decoupled architecture:
1. **Multi-Agent Editorial Personas**: Role definitions and structured prompts for Art Director, Typographer, Compositor, Tectonic Vector Detailer, and Pre-flight Auditor under `skills/editorial-studio/`.
2. **Typography & Grid Engine**: Mathematical baseline grid locking (4pt/6pt), tripartite font mapping (Grotesque, Serif, Monospace), and automated gutter creep calculation under `engine/grid/`.
3. **Orthographic Drafting Library**: ISO 128 vector templates (1:20 wall section, 1:5 joinery, 1:100 plan), scale-aware downsampling, and standardized Project Passport blocks under `engine/drafting/`.
4. **Dual-Engine Compilation Framework**: Declarative Typst templates and CLI compilation (`engine/typst/`) alongside W3C CSS Paged Media Paged.js headless browser compilation (`engine/pagedjs/`), unified via `compile.py`.
5. **Automated Preflight Validation Engine**: Standalone vision-and-data linter `audit_publication.py` inspecting bleeds, margins, font embedding/subsetting, DPI $\ge 300$, CMYK TAC $\le 320\%$, PDF/X-4 compliance, and raster bounding-box collision detection under `preflight/`.
6. **E2E Monograph Demonstration**: 10-page sample monograph adhering to the 5-act narrative structure across consecutive spreads, compiling in sub-second execution time under `examples/monograph/`.

## Feature Inventory
Every feature from the Survey phase is mapped to an assigned milestone:
| # | Feature | Description | Milestone | Source |
|---|---|---|---|---|
| 1 | Master Antigravity Skill | `SKILL.md` with system overview, workflows, and invocation rules | M1 | ORIGINAL_REQUEST §R1 |
| 2 | Art Director Persona | 5-act narrative arc, 12-column modular grid geometry, color tokens | M1 | ORIGINAL_REQUEST §R1 |
| 3 | Typographer Persona | Modular scale, 4pt/6pt baseline grid locking, Knuth-Plass, hanging punctuation | M1 | ORIGINAL_REQUEST §R1 |
| 4 | Compositor Persona | Recto/verso facing spread tension, gutter creep, image framing, headers/folios | M1 | ORIGINAL_REQUEST §R1 |
| 5 | Tectonic Vector Detailer Persona | 1:20 constructive wall sections, 1:5 joinery reveals, ISO 128 lineweights | M1 | ORIGINAL_REQUEST §R1 |
| 6 | Pre-flight Auditor Persona | Print physics, FOGRA51/52 CMYK, TAC $\le 320\%$, bleeds, export compliance | M1 | ORIGINAL_REQUEST §R1 |
| 7 | Tripartite Font Mapping | Grotesque (display), Rationalist Serif (body), Monospace (metadata/drafting) | M2 | ORIGINAL_REQUEST §R3 |
| 8 | Baseline Grid Locking | Snap line leading to 4pt/6pt increments with zero cross-spine offset | M2 | ORIGINAL_REQUEST §R3 |
| 9 | Gutter Creep Calculus | Dynamic inner margin displacement $c \times (N - p)$ and binding gutter draw | M2 | ORIGINAL_REQUEST §R3 |
| 10 | Micro-Typography Rules | Optical hanging punctuation (50–100%), widow penalty $\ge 2$ lines, zero 1-word orphans | M2 | ORIGINAL_REQUEST §R3 |
| 11 | ISO 128 Lineweight Hierarchy | 0.13mm, 0.25mm, 0.35mm, 0.50mm, 0.70mm calibrated vector strokes | M3 | ORIGINAL_REQUEST §R4 |
| 12 | Scale-Aware Vector Downsampling | Stroke clamping ($w_{\min} \ge 0.08\text{mm}$) and hatch decimation / poché replacement | M3 | ORIGINAL_REQUEST §R4 |
| 13 | Project Passport Data Block | Standardized scannable metadata block (typology, coordinates, stage, team) | M3 | ORIGINAL_REQUEST §R4 |
| 14 | Orthographic Detail Templates | 1:20 wall section with thermal breaks, 1:5 joinery reveal, 1:100 PMR plan | M3 | ORIGINAL_REQUEST §R4 |
| 15 | Typst Declarative Engine | Declarative templates, sub-second math layout, CeTZ/SVG vector integration | M4 | ORIGINAL_REQUEST §R2 |
| 16 | Paged.js HTML-CSS Engine | W3C CSS Paged Media `@page` spread rules (:left/:right), bleed/crop marks | M4 | ORIGINAL_REQUEST §R2 |
| 17 | Unified Compilation CLI | `compile.py` with multi-target output, automated build scripts | M4 | ORIGINAL_REQUEST §R2 |
| 18 | Automated Preflight Script | `audit_publication.py` executing CLI and returning itemized pass/fail report | M5 | ORIGINAL_REQUEST §R5 |
| 19 | Geometry & Bleed Verification | Validate TrimBox, BleedBox (3mm bleed delta), and 5mm safety margins | M5 | ORIGINAL_REQUEST §R5 |
| 20 | Font Embedding Audit | Verify 100% font subsetting (`^[A-Z]{6}\+`), zero missing glyphs or Type 3 fonts | M5 | ORIGINAL_REQUEST §R5 |
| 21 | Image Resolution Audit | Effective DPI calculation ($(px / (pt / 72)) \ge 300$) for all embedded images | M5 | ORIGINAL_REQUEST §R5 |
| 22 | Color Space & TAC Audit | FOGRA51/52 CMYK validation and pixel-level TAC $\le 320\%$ calculus | M5 | ORIGINAL_REQUEST §R5 |
| 23 | PDF/X-4 Validation | Validate OutputIntents, GTS_PDFXVersion, Trapped key, and standard conformance | M5 | ORIGINAL_REQUEST §R5 |
| 24 | Vision-in-the-Loop Collision Linting | Raster spread preview generation and programmatic AABB text-image collision check | M5 | ORIGINAL_REQUEST §R5 |
| 25 | 5-Act Narrative Case Study | 10-page monograph spread demonstrating Hook -> Context -> Anatomy -> Tectonic -> Climax | M6 | ORIGINAL_REQUEST Acceptance |
| 26 | Sub-3-Second Typst Compilation | Full 10-page monograph compilation in under 3.0s | M6 | ORIGINAL_REQUEST Acceptance |
| 27 | E2E Test Suite (Tiers 1-4) Pass | 100% pass of all requirement-driven opaque-box test cases | M7 | Dual Track Final Milestone |
| 28 | Adversarial Coverage Hardening | Tier 5 white-box challenger stress tests and boundary hardening | M7 | Dual Track Final Milestone |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| M1 | Core Skill System & 5 Personas | `SKILL.md`, persona prompts, schemas, agent definitions | none | DONE |
| M2 | Swiss Modular Grid & Micro-Typography | Baseline grid locking, tripartite fonts, creep calculus | M1 | DONE |
| M3 | ISO 128 Technical Drafting Library | Vector templates (1:20, 1:5, 1:100), ISO 128 strokes, Project Passport | M1 | DONE |
| M4 | Dual-Engine Compilation Framework | Typst engine + Paged.js engine + build scripts + `compile.py` | M2, M3 | DONE |
| M5 | Automated Preflight Validation Engine | `audit_publication.py` (bleeds, fonts, DPI, TAC, PDF/X-4, collision linting) | M4 | DONE |
| M6 | Production Demonstration Monograph | 10-page monograph, 5-act narrative spreads, <3s compilation | M4, M5 | DONE |
| M7 | Final E2E Pass & Adversarial Hardening | Pass 100% E2E tests (Tiers 1-4) + Tier 5 Challenger loop | M1-M6, TEST_READY | DONE |

## Interface Contracts
### Personas ↔ Engine Templates
- Art Director configures `manifest.json` (format, narrative_acts, palette, margins, baseline_step).
- Typographer specifies font families (display, body, mono), sizes, leadings, and hanging punctuation rules.
- Compositor calculates layout spreads, rect/verso margins with creep offset:
  `inner_margin = base_inner + gutter_creep(page, total_pages, binding_type, caliper)`
- Tectonic Detailer provides SVG / CeTZ vector blocks conforming to ISO 128 lineweights:
  `0.13mm` (hatching), `0.25mm` (dimensions), `0.35mm` (partitions), `0.50mm` (structure cuts).

### Engine ↔ Preflight Validation (`audit_publication.py`)
- CLI signature: `python preflight/audit_publication.py <pdf_path> [--icc <profile>] [--json <output_json>]`
- Return code: `0` for clean pass, `1` for preflight violations.
- Output JSON schema:
```json
{
  "file": "path/to/doc.pdf",
  "status": "PASS" | "FAIL",
  "summary": { "passed": 7, "failed": 0, "warnings": 0 },
  "checks": {
    "dimensions_and_bleed": { "status": "PASS", "details": {...} },
    "margin_safety_zone": { "status": "PASS", "details": {...} },
    "font_embedding": { "status": "PASS", "embedded_pct": 100.0, "non_embedded": [] },
    "image_resolution": { "status": "PASS", "min_dpi": 300.0, "violating_images": [] },
    "color_and_tac": { "status": "PASS", "max_tac": 298.0, "limit": 320.0 },
    "pdfx4_compliance": { "status": "PASS", "details": {...} },
    "layout_collisions": { "status": "PASS", "collision_count": 0, "breaches": [] }
  }
}
```

## Code Layout
```
g:/My Drive/Portfolios/editorial-studio/
├── SKILL.md                          # Master Antigravity skill specification
├── personas/                         # 5 Editorial persona definitions and prompt packages
│   ├── art_director.md
│   ├── typographer.md
│   ├── compositor.md
│   ├── tectonic_detailer.md
│   └── preflight_auditor.md
├── engine/
│   ├── grid/
│   │   ├── font_mapping.json         # Tripartite font configurations & system fallbacks
│   │   ├── baseline.py               # Baseline snapping and alignment utilities
│   │   └── creep_calculator.py       # Automated gutter creep calculus for binding types
│   ├── drafting/
│   │   ├── iso_128.py                # ISO 128 stroke hierarchy and downsampling rules
│   │   ├── project_passport.py       # Standardized Project Passport data block generator
│   │   └── templates/                # Reusable vector templates (1:20 section, 1:5 joinery, 1:100 plan)
│   ├── typst/
│   │   ├── template.typ              # Declarative Typst publication master template
│   │   └── build_typst.py            # Typst build execution script
│   ├── pagedjs/
│   │   ├── template.html             # W3C CSS Paged Media master template
│   │   ├── styles.css                # Spread geometry, @page rules, Swiss typography
│   │   └── build_pagedjs.py          # Headless Chromium / pagedjs-cli build runner
│   └── compile.py                    # Unified dual-engine build and export CLI
├── preflight/
│   ├── audit_publication.py          # Automated preflight validator & vision-in-the-loop linter
│   └── icc/                          # Standard color profiles (FOGRA51 / PSO Coated v3)
├── examples/
│   └── monograph/                    # 10-page sample monograph demonstrating 5-act narrative
│       ├── source.typ
│       ├── source.html
│       └── assets/
└── tests/                            # E2E Testing Track test infrastructure and test suites
    ├── test_runner.py
    ├── tier1_features/
    ├── tier2_boundaries/
    ├── tier3_combinations/
    ├── tier4_workloads/
    └── tier5_adversarial/
```
