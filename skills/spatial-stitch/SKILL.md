---
name: spatial-stitch
description: Google Stitch-style generative design skillset for architectural portfolios, monograph publishing, multi-spread case studies, and editorial document design. Operates on spreads, tectonic plates, constructive 1:20 drawings, and Swiss typographic grids rather than web UI.
---

# Spatial Stitch (Portfolio Stitch)
### *Frontier Generative Design for Spatial Architecture, Editorial Monographs & Physical Documents*

Spatial Stitch adapts Google Stitch's generative paradigm (`projects`, `canvases/spreads`, `variants`, `design_systems`, `DESIGN.md`) into a specialized engine for physical architecture, interior design, urban planning portfolios, and publication design.

Instead of generating mobile app screens or SaaS dashboards, **Spatial Stitch** operates on **spreads, tectonic plates, constructive drawings, and editorial monographs**, enforcing Swiss typographic grids, 1:20 wall section proof, Project Passports, recruiter trust ergonomics, and anti-render-trap metrics.

---

## 🏛️ Mental Model: Stitch vs. Spatial Stitch

| Concept | Google Stitch (App UI) | Spatial Stitch (Document & Spatial) |
| :--- | :--- | :--- |
| **Canvas** | Mobile 390x844 / Desktop 1440x900 | **Landscape 16:9 (`1920x1080`), Double-A3 (`1680x595`), Portrait A4 (`1240x1754`)** |
| **Grid** | CSS Flexbox / 8pt responsive layout | **Swiss Modular Grid (8, 12, 16 columns + 4pt/8pt baseline + folio markers)** |
| **Design System** | Web UI buttons, inputs, cards | **Editorial & Constructive Tokens: Neutral Grotesks + Technical Mono, line weights (0.13–0.50mm), tectonic swatches, dimension strings** |
| **System Spec** | `DESIGN.md` | **`PORTFOLIO_DESIGN.md`** |
| **Generative Action** | `generate_screen_from_text` | **`generate_spread_from_text`** |
| **Variants** | Layout / Color / Text variations | **`generate_variants` across 10 Archetypes with `REFINE`, `EXPLORE`, `REIMAGINE`** |
| **Quality Gate** | WCAG / Responsive checks | **100-Point Anti-Render-Trap Audit (Constructive proof ratio, 10s recruiter scan path, PMR compliance, work rights)** |
| **Output** | React / Tailwind code | **Vector SVG Spreads, HTML5 Print Sheets, InDesign JSON, PDF Dossiers** |

---

## 🛠️ Tool Catalog & JSON-RPC RPCs

1. **`create_project(name, description, format, passport)`**: Initializes an architectural monograph or portfolio project.
2. **`get_project(projectId)`**: Retrieves project metadata, active design system, spread sequences, and audit metrics.
3. **`list_projects()`**: Lists all active portfolio monograph projects.
4. **`generate_spread_from_text(projectId, prompt, archetype, format)`**: Synthesizes a publication-ready vector spread from an architectural description or narrative act.
5. **`edit_spreads(projectId, selectedSpreadIds, prompt)`**: Surgically edits spread elements.
6. **`get_spread(spreadId)`**: Returns the vector SVG and semantic HTML5 of a specific spread.
7. **`generate_variants(projectId, spreadId, creativeRange, variantCount)`**: Generates 3-4 distinct variations across `REFINE`, `EXPLORE`, and `REIMAGINE`.
8. **`audit_spread(spreadId)`**: Evaluates the spread against the 100-point anti-render-trap rubric and recruiter scan path.

---

## 📐 The 10 Layout Archetypes

1. **The Project Passport (Cover / Signpost)**: Left-aligned metadata card, key plan, individual attribution, work rights, and project thesis statement.
2. **The Constructive Proof (1:20 Wall Section)**: High-density technical drawing lead with multi-layered envelope callouts, thermal breaks, rainscreen sub-framing, and dimension chains.
3. **The Spatial Anatomy (1:100 Plan)**: Uncropped floor plan with circulation vectors, threshold clearances, and programmatic fills.
4. **The Cartographic Context (Territory & Site)**: Scaled regional context, topography contours, transit nodes, and urban morphology.
5. **The Environmental Engine (Bioclimatic Flows)**: Solar radiation vectors, diurnal cross-ventilation loops, and thermal mass exchange.
6. **The Tectonic Triptych (1:5 Joinery & Millwork)**: Custom cabinetry details, shadow reveals, concealed hardware clearances, and material sample swatches.
7. **The Process Matrix (Iterations & Tests)**: Basswood study models, massing transformations, structural calculation sketches.
8. **The Scenographic Spread (Atmospheric Climax)**: Single high-contrast raking light photograph or perspective rendering grounded by technical micro-captions.
9. **The Urban Territory (Civic Realm & Safety)**: CPTED sightline analysis, nighttime illumination lux gradients, active ground-floor transparency.
10. **The Typographic Index (Monograph Colophon)**: Complete project catalog, drawing index, structural collaborators, and software toolchain.

---

## 🎭 The 5-Act Narrative Monograph Structure

When generating multi-spread architectural case studies, sequence spreads through the 5 Acts:
- **Act 1: The Hook & Project Passport** (Spread 1: Left = Passport Block, Right = Urban Site Section / Thesis).
- **Act 2: Environmental & Urban Context** (Spread 2: Microclimatic flow diagram + Territorial context map).
- **Act 3: Spatial Anatomy** (Spread 3: Full 1:100 floor plan + Programmatic circulation hierarchy).
- **Act 4: Tectonic Proof (1:20 Wall Section)** (Spread 4: The Hero technical plate. Multi-layered envelope callouts, thermal breaks, rainscreen assembly).
- **Act 5: Lived Climax & Tactile Scenography** (Spread 5: 1:5 joinery detail + tactile material triptych + atmospheric lived photograph).
