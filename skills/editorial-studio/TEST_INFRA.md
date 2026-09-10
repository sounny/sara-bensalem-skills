# Test Infrastructure Specification: editorial-studio

**Project:** `editorial-studio` — Antigravity Publishing & Architectural Monograph Design Engine  
**Document:** `TEST_INFRA.md`  
**Status:** Authoritative Test Architecture & Harness Specification  
**Version:** 1.0.0  
**Author:** E2E Test Writer (`test_writer_e2e`)  
**Date:** 2026-09-05  

---

## 1. Test Philosophy & Core Principles

The `editorial-studio` test infrastructure is engineered to enforce publication-grade quality, physical print integrity, and rigorous Swiss typographic discipline. Unlike ordinary software suites that test only internal code paths, this test harness operates under three non-negotiable principles:

### 1.1 Opaque-Box Verification
All tests are executed against external contracts, mathematical definitions, file schemas, CLI interfaces, and compiled binary artifacts (PDFs, SVGs, CSS, JSON). Tests never rely on private implementation details or volatile internal variables. If an implementation is refactored from pure Python to Rust or C, the opaque-box test suite remains 100% valid and binding.

### 1.2 Requirement-Driven Expected Output Derivation
Every single test case has an explicit authoritative origin traced directly to:
- `ORIGINAL_REQUEST.md` (§R1–R5 and Acceptance Criteria)
- `PROJECT.md` (§Architecture, §Feature Inventory, §Interface Contracts)
- `spec_miner_skills/report.md` (Persona definitions, Swiss modular formulas, ISO 128 lineweights, Gutter creep equations)
- `spec_miner_print_engine/report.md` (PDF/X-4 compliance, PyMuPDF inspection routines, FOGRA51/52 TAC thresholds, baseline registration math)

Expected outputs are derived from physical print standards (ISO 128, ISO 15930-7 / PDF/X-4, ISO 12647-2, W3C CSS Paged Media Module Level 3) rather than arbitrary developer heuristics.

### 1.3 Progressive Testability & Deterministic Isolation
Tests are completely self-contained and order-independent. During development and implementation milestones (M1 through M6), tests can be run progressively. When an external CLI or tool (such as `typst` binary) is present in the host system, real subprocess compilation is benchmarked. When running in environments where binaries are being built, tests exercise the syntactic generators, mathematical models, schema validators, and preflight inspection algorithms deterministically.

---

## 2. Complete Feature Inventory & Requirement Traceability

The test harness provides 100% coverage mapping across all five fundamental requirements (R1 through R5) and acceptance criteria:

| Feature ID | Requirement | Feature Name | Primary Contract / Interface | Authoritative Source |
| :--- | :--- | :--- | :--- | :--- |
| **F-01** | R1 | Master Antigravity Skill & Personas | `SKILL.md`, `personas/*.md` | ORIGINAL_REQUEST §R1, Spec Miner Skills §1 |
| **F-02** | R1 | Art Director Persona Contract | 5-act narrative sequence, 10 archetypes, palette tokens | ORIGINAL_REQUEST §R1, Spec Miner Skills §1 |
| **F-03** | R1 | Typographer Persona Contract | Modular type scale, baseline grid step, Knuth-Plass | ORIGINAL_REQUEST §R1, Spec Miner Skills §1 |
| **F-04** | R1 | Compositor Persona Contract | 2-page facing spreads, gutter creep, margins | ORIGINAL_REQUEST §R1, Spec Miner Skills §1 |
| **F-05** | R1 | Tectonic Detailer Contract | ISO 128 lineweights, Glaser U-value, 1:20 / 1:5 details | ORIGINAL_REQUEST §R1, Spec Miner Skills §1 |
| **F-06** | R1 | Pre-flight Auditor Contract | Print physics, FOGRA51 CMYK, TAC $\le 320\%$, bleeds | ORIGINAL_REQUEST §R1, Spec Miner Skills §1 |
| **F-07** | R3 | Tripartite Font Mapping | Grotesque (display), Serif (body), Monospace (metadata) | ORIGINAL_REQUEST §R3, Spec Miner Skills §3 |
| **F-08** | R3 | Baseline Grid Locking Calculus | Snapping formula $y = \text{round}(y/B) \cdot B$, $\Delta y = 0$ cross-spine | ORIGINAL_REQUEST §R3, Spec Miner Skills §3 |
| **F-09** | R3 | Dynamic Gutter Creep Calculus | Smyth-sewn, perfect-bound ($G_{\text{draw}}$), lay-flat, saddle | ORIGINAL_REQUEST §R3, Spec Miner Skills §3 |
| **F-10** | R3 | Micro-Typography Rules | Optical hanging punctuation, widow $\ge 2$, zero 1-word orphans | ORIGINAL_REQUEST §R3, Spec Miner Skills §3 |
| **F-11** | R4 | ISO 128 Lineweight Hierarchy | 0.70mm, 0.50mm, 0.35mm, 0.25mm, 0.13mm stroke weights | ORIGINAL_REQUEST §R4, Spec Miner Skills §4 |
| **F-12** | R4 | Scale-Aware Vector Downsampling | Stroke clamping ($w \ge 0.08\text{mm}$), hatch decimation | ORIGINAL_REQUEST §R4, Spec Miner Skills §4 |
| **F-13** | R4 | Standardized Project Passport | JSON schema validation, 13 mandatory fields, scannability | ORIGINAL_REQUEST §R4, Spec Miner Skills §4 |
| **F-14** | R4 | Orthographic Detail Templates | 1:20 wall section, 1:5 joinery reveal, 1:100 PMR plan | ORIGINAL_REQUEST §R4, Spec Miner Skills §4 |
| **F-15** | R2 | Typst Declarative Engine | `template.typ`, `#set page`, `#grid`, CeTZ vector drafting | ORIGINAL_REQUEST §R2, Spec Miner Print §4 |
| **F-16** | R2 | Paged.js HTML-CSS Engine | W3C `@page`, `:left`/`:right`, `marks: crop cross; bleed: 3mm;` | ORIGINAL_REQUEST §R2, Spec Miner Print §5 |
| **F-17** | R2 | Unified Compilation CLI | `compile.py` build interface, multi-target output | ORIGINAL_REQUEST §R2, PROJECT.md §Architecture |
| **F-18** | R5 | Preflight CLI & Report Schema | `audit_publication.py <doc.pdf> [--json <out>]` | ORIGINAL_REQUEST §R5, Spec Miner Print §6–7 |
| **F-19** | R5 | Bleed & Trimbox Geometry Audit | TrimBox, BleedBox ($3.0\,\text{mm}$ delta), MediaBox containment | ORIGINAL_REQUEST §R5, Spec Miner Print §6.1 |
| **F-20** | R5 | Margin Safety Zone Compliance | Programmatic $5\,\text{mm}$ inner safety boundary audit | ORIGINAL_REQUEST §R5, Spec Miner Print §6.2 |
| **F-21** | R5 | Font Embedding & Subsetting Audit | 100% font embedding, `^[A-Z]{6}\+` prefix, no Type 3 fonts | ORIGINAL_REQUEST §R5, Spec Miner Print §6.3 |
| **F-22** | R5 | Image Resolution (Effective DPI) | Effective $\text{DPI} = (px \cdot 72) / pt \ge 300\,\text{DPI}$ | ORIGINAL_REQUEST §R5, Spec Miner Print §6.4 |
| **F-23** | R5 | Color Space & Total Area Coverage | CMYK pixel extraction, $\text{TAC}_{\max} \le 320.0\%$ | ORIGINAL_REQUEST §R5, Spec Miner Print §6.5 |
| **F-24** | R5 | PDF/X-4 Conformance Audit | `/OutputIntents`, `/GTS_PDFX`, `/Trapped`, no encryption | ORIGINAL_REQUEST §R5, Spec Miner Print §6.6 |
| **F-25** | R5 | Vision-in-the-Loop Collision Lint | AABB collision detection between text and image bounding boxes | ORIGINAL_REQUEST §R5, Spec Miner Print §6.7 |

---

## 3. Test Tier Architecture & Coverage Thresholds

The test harness is organized into four hierarchical testing tiers, designed to guarantee absolute coverage from atomic units to production workloads:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   EDITORIAL-STUDIO TEST ARCHITECTURE                   │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   TIER 1: FEATURE BASELINE (Happy-Path)                                │
│   • 10 Features × >=5 Tests = >=50 Tests                               │
│   • Verifies functional contracts, calculations, schemas, generators   │
│                                                                        │
│   TIER 2: BOUNDARIES & STRESS (Edge & Negative Cases)                  │
│   • 10 Features × >=5 Tests = >=50 Tests                               │
│   • Tests 0/negative margins, 500-page creep, TAC 340%, DPI 299, etc.  │
│                                                                        │
│   TIER 3: COMBINATIONS & INTEGRATION (Cross-Feature Scenarios)         │
│   • >=15 Tests                                                         │
│   • Spread layout + creep + baseline lock + preflight validation       │
│                                                                        │
│   TIER 4: PRODUCTION WORKLOADS (Real-World E2E Performance)            │
│   • >=5 High-Fidelity Workloads                                        │
│   • Sub-3s Typst compilation, 5-act monograph, 1:20 Glaser section     │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Quantitative Thresholds

| Test Tier | Focus / Scope | Minimum Required Tests | Implemented Tests | Pass Requirement |
| :--- | :--- | :---: | :---: | :---: |
| **Tier 1: Features** | Fundamental contracts, valid inputs, mathematical accuracy | 50 | $\ge 50$ | 100% Pass |
| **Tier 2: Boundaries** | Boundary values, negative inputs, threshold triggers, error catching | 50 | $\ge 50$ | 100% Pass |
| **Tier 3: Combinations** | Cross-feature interactions, pipeline dataflow, facing spread balance | 15 | $\ge 15$ | 100% Pass |
| **Tier 4: Workloads** | Real-world publication artifacts, compilation speed, 5-act narrative | 5 | $\ge 5$ | 100% Pass |
| **Total Test Suite** | Comprehensive Opaque-Box E2E Quality Assurance | **120** | **$\ge 120$** | **100% Pass** |

---

## 4. Test Suite Layout & Module Organization

All test modules, fixtures, and runners reside exclusively within `g:/My Drive/Portfolios/editorial-studio/tests/`:

```
tests/
├── __init__.py
├── test_runner.py                     # Master standalone CLI test runner
├── fixtures/                          # Reusable synthetic PDFs, SVGs, schemas, test helpers
│   ├── __init__.py
│   ├── sample_passport.json
│   ├── sample_wall_section.svg
│   └── pdf_generator.py               # Generates test PDFs with calibrated boxes, fonts, TAC
├── tier1_features/                    # Tier 1: Happy path feature tests (>=50 tests)
│   ├── __init__.py
│   ├── test_personas.py               # F-01 to F-06: Persona contracts & prompts
│   ├── test_font_mapping.py           # F-07: Tripartite font mappings & fallbacks
│   ├── test_baseline_grid.py          # F-08: 4pt/6pt baseline math & cross-spine lock
│   ├── test_gutter_creep.py           # F-09: Smyth-sewn, perfect, lay-flat formulas
│   ├── test_iso128_strokes.py         # F-11: Metric stroke weights & line hierarchies
│   ├── test_vector_downsampling.py    # F-12: Min stroke clamping (0.08mm) & hatch decimation
│   ├── test_project_passport.py       # F-13: Passport JSON schema & scannability
│   ├── test_typst_pipeline.py         # F-15: Typst document structure & templates
│   ├── test_pagedjs_pipeline.py       # F-16: W3C @page rules, bleed, CSS grid
│   └── test_preflight_cli.py          # F-18: Preflight CLI signature & JSON schema
├── tier2_boundaries/                  # Tier 2: Boundary, edge, & negative tests (>=50 tests)
│   ├── __init__.py
│   ├── test_boundary_creep.py         # Single-page (N=1) and extreme page counts (500 pages)
│   ├── test_boundary_margins.py       # Zero, negative, and page-exceeding margins
│   ├── test_boundary_strokes.py       # Sub-0.08mm strokes, negative and invalid weights
│   ├── test_boundary_bleeds.py        # Missing bleeds (0mm vs 3mm), corrupt box deltas
│   ├── test_boundary_color_tac.py     # Untagged RGB, TAC > 320% (340%, 350%), TAC limit 320%
│   ├── test_boundary_fonts.py         # Un-embedded fonts, missing glyphs, Type 3 fonts
│   ├── test_boundary_resolution.py    # Image DPI 299 vs 300, degraded images <250 DPI
│   ├── test_boundary_collision.py     # Overlapping text-image AABBs & contrast thresholds
│   ├── test_boundary_microtypography.py # 1-word orphans, widow penalty <2 lines, hanging breaks
│   └── test_boundary_passport_schema.py # Missing passport fields, line items <3, invalid stages
├── tier3_combinations/                # Tier 3: Combinatorial & multi-feature tests (>=15 tests)
│   ├── __init__.py
│   ├── test_facing_spread_baseline_creep.py # Baseline lock + dynamic creep across spreads
│   ├── test_iso128_typst_embedding.py       # ISO 128 SVG / CeTZ embedded in Typst layout
│   ├── test_passport_preflight_audit.py     # Passport block compiled and audited by preflight
│   ├── test_five_act_dual_engine.py         # 5-act narrative compiled across both engines
│   └── test_cross_engine_parity.py          # Typst and Paged.js layout and margin parity
└── tier4_workloads/                   # Tier 4: Real-world publication workloads (>=5 tests)
    ├── __init__.py
    ├── test_monograph_compilation_speed.py  # 10-page monograph compiled in Typst in <3.0s
    ├── test_full_5act_case_study.py         # Complete 5-act portfolio across >=3 spreads
    ├── test_constructive_wall_section.py    # 1:20 wall section with Glaser U-value calculation
    ├── test_cmyk_fogra51_photo_spread.py    # Photo spread with CMYK FOGRA51 TAC verification
    └── test_e2e_preflight_audit.py          # Complete preflight audit execution on output artifacts
```

---

## 5. Execution Semantics & CLI Interface

The test suite is driven by `tests/test_runner.py`, a pure Python standalone test runner that requires zero third-party testing frameworks.

### 5.1 CLI Invocations

```bash
# Execute all test tiers (Tier 1 through Tier 4)
python tests/test_runner.py --tier all

# Execute specific tier
python tests/test_runner.py --tier tier1
python tests/test_runner.py --tier tier2
python tests/test_runner.py --tier tier3
python tests/test_runner.py --tier tier4

# Execute with JSON report export
python tests/test_runner.py --tier all --json test_report.json

# Run via standard Python unittest discovery
python -m unittest discover -s tests -p "test_*.py"
```

### 5.2 Exit Code Semantics
- `0`: All executed tests passed cleanly.
- `1`: One or more tests failed or encountered errors.
- `2`: Invalid CLI invocation arguments or runtime setup error.

### 5.3 JSON Output Schema
```json
{
  "timestamp": "2026-09-05T11:30:00Z",
  "tier": "all",
  "total": 125,
  "passed": 125,
  "failed": 0,
  "errors": 0,
  "skipped": 0,
  "duration_seconds": 2.45,
  "status": "PASS",
  "results_by_tier": {
    "tier1_features": { "total": 52, "passed": 52, "failed": 0 },
    "tier2_boundaries": { "total": 52, "passed": 52, "failed": 0 },
    "tier3_combinations": { "total": 16, "passed": 16, "failed": 0 },
    "tier4_workloads": { "total": 5, "passed": 5, "failed": 0 }
  },
  "failures": []
}
```

---

## 6. Implementation Bug Escalation Protocol

As mandated by the QA role constraints, the Test Writer **never modifies implementation code**.
When a test failure indicates a defect in the implementation:
1. Document the exact reproducing test command and failure traceback.
2. Formulate the discrepancy between specification requirement and observed behavior.
3. Log the escalation in `report.md` and `handoff.md`.
4. Dispatch notification to the implementing agent (Worker M1–M6) via parent orchestrator.
