// ==============================================================================
// EDITORIAL-STUDIO: DECLARATIVE TYPST PUBLICATION MASTER TEMPLATE
// Standards: Swiss 12-Column Grid, Baseline Locking (6pt/12pt), ISO 128 Drafting
// Author: Sara Bensalem (Master Monograph & Portfolio System)
// ==============================================================================

#set document(
  title: "Sara Bensalem Monograph: The Tectonic Rescue",
  author: "Sara Bensalem",
  keywords: ("Architecture", "Swiss Grid", "1:20 Detail", "ISO 128", "Tectonic Proof")
)

// Spread Geometry: A4 Landscape (297mm x 210mm), Asymmetric Facing Margins
#set page(
  paper: "a4",
  flipped: true,
  margin: (
    inside: 25.0mm,  // spine gutter clearance for lay-flat / smyth-sewn binding
    outside: 15.0mm, // outer trim safety edge
    top: 20mm,
    bottom: 20mm
  ),
  binding: left,
  header: context {
    let p = counter(page).get().first()
    if p > 1 {
      set text(font: ("JetBrains Mono", "Consolas", "Courier New"), size: 7.5pt, fill: luma(100))
      if calc.even(p) {
        // Verso (Left Page Spread)
        grid(
          columns: (1fr, 1fr),
          align(left)[#p | SARA BENSALEM MONOGRAPH],
          align(right)[ACT 4: TECTONIC PROOF]
        )
      } else {
        // Recto (Right Page Spread)
        grid(
          columns: (1fr, 1fr),
          align(left)[PROJECT: ATLAS TERRACE],
          align(right)[1:20 WALL SECTION | #p]
        )
      }
    }
  }
)

// ------------------------------------------------------------------------------
// Baseline Grid Locking & Snapping Calculus (6pt Step, 12pt Line Pitch)
// ------------------------------------------------------------------------------
#let baseline-step = 6.0pt
#let snap(val) = calc.round(val / baseline-step) * baseline-step

// Tripartite Typography Hierarchy:
// 1. Structural Grotesque: Display & System Labels (Space Grotesk / Bahnschrift)
// 2. Rationalist Serif: Continuous Editorial Body (Garamond)
// 3. Monospace: Technical Drafting & Project Passport Metadata (JetBrains Mono / Consolas)
#set text(
  font: ("Space Grotesk", "Bahnschrift", "Neue Haas Grotesk Text Pro", "Arial"),
  size: 9pt,
  weight: "regular",
  fill: cmyk(0%, 0%, 0%, 100%)
)

#set par(
  leading: 3pt,       // 9pt font + 3pt leading = 12pt line pitch (2 * 6pt)
  spacing: 12pt,      // Exact snap to major baseline pitch
  justify: true
)

// ------------------------------------------------------------------------------
// Calibrated ISO 128 Lineweight Hierarchy & CMYK Drafting Palette
// ------------------------------------------------------------------------------
#let stroke-cut = 0.50mm + cmyk(0%, 0%, 0%, 100%)        // Structural cut planes (concrete, masonry)
#let stroke-heavy = 0.70mm + cmyk(0%, 0%, 0%, 100%)      // Ground boundary & heavy cut lines
#let stroke-partition = 0.35mm + cmyk(0%, 0%, 0%, 100%)  // Secondary partitions & joinery frames
#let stroke-projection = 0.25mm + cmyk(0%, 0%, 0%, 80%)  // Visible edges & door swing arcs
#let stroke-hatch = 0.13mm + cmyk(0%, 0%, 0%, 50%)       // Thermal insulation hatch & dimension strings

// ------------------------------------------------------------------------------
// Swiss 12-Column Modular Grid System
// ------------------------------------------------------------------------------
#let swiss-grid(..cells) = grid(
  columns: (1fr,) * 12,
  column-gutter: 4mm,
  row-gutter: 12pt,
  ..cells
)

// ------------------------------------------------------------------------------
// Component Macros: Project Passport Data Block
// ------------------------------------------------------------------------------
#let project-passport(
  title: "PROJECT PASSPORT",
  typology: "Cultural Pavilion",
  scale: "1:20 Detailing",
  location: "Basel, Switzerland",
  climate: "Cfb (Marine West Coast)",
  target-u: "0.18 W/m²K",
  thermal-break: "Continuous Schöck Isokorb",
  client: "Fondation des Arts",
  team: "Sara Bensalem (Lead Architect), Tectonic Studio"
) = block(
  stroke: (left: 2pt + cmyk(0%, 0%, 0%, 100%)),
  inset: (left: 8pt, top: 4pt, bottom: 4pt),
  fill: luma(248),
  [
    #set text(font: ("JetBrains Mono", "Consolas"), size: 8pt)
    #strong(title) \
    #v(4pt)
    *Typology:* #typology \
    *Scale:* #scale \
    *Location:* #location \
    *Climate Zone:* #climate \
    *Target U-Value:* #target-u \
    *Thermal Break:* #thermal-break \
    *Client:* #client \
    *Team Attribution:* #team
  ]
)

// ------------------------------------------------------------------------------
// Component Macros: Glaser Hygrothermal Calculation Block
// ------------------------------------------------------------------------------
#let glaser-u-value-block(
  u-val: "0.178 W/m²K",
  condensation-risk: "Zero (Interstitial VCL sealed)",
  dew-point: "9.4°C at inner insulation boundary"
) = block(
  stroke: 0.25mm + cmyk(0%, 0%, 0%, 80%),
  inset: 6pt,
  fill: luma(252),
  [
    #set text(font: ("JetBrains Mono", "Consolas"), size: 7.5pt)
    #strong[HYGROTHERMAL GLASER ANALYSIS (ISO 13788)] \
    #line(length: 100%, stroke: stroke-hatch)
    Calculated Assembly U-Value: #strong(u-val) \
    Condensation Status: #condensation-risk \
    Calculated Dew Point: #dew-point
  ]
)

// ------------------------------------------------------------------------------
// Component Macros: 1:20 Constructive Wall Section Vector Plate
// ------------------------------------------------------------------------------
#let vector-plate-1-20(title: "1:20 CONSTRUCTIVE WALL SECTION") = block(
  stroke: 0.50mm + cmyk(0%, 0%, 0%, 100%),
  inset: 10pt,
  fill: luma(245),
  [
    #set text(font: ("JetBrains Mono", "Consolas"), size: 8pt)
    #grid(
      columns: (1fr, auto),
      strong(title),
      text(fill: luma(100))[ISO 128 COMPLIANT | CALIBRATED STROKES]
    )
    #v(8pt)
    #rect(
      width: 100%,
      height: 140pt,
      stroke: stroke-cut,
      fill: luma(235)
    )[
      #place(center + horizon)[
        #set text(size: 9pt, weight: "medium")
        [1:20 Tectonic Section: Exterior Rain-Screen, PIR Insulation, Schöck Isokorb, Cast-in-Place Concrete]
      ]
    ]
  ]
)

// ==============================================================================
// 5-ACT NARRATIVE PUBLICATION BODY
// ==============================================================================

// ACT 1: The Hook and Project Passport (Spread 1 / Recto Opening)
= Act 1: The Hook and Project Passport

#swiss-grid(
  grid.cell(colspan: 4)[
    #project-passport(
      title: "PROJECT PASSPORT: ATLAS TERRACE",
      typology: "Terraced Cultural Center",
      scale: "1:20 Detailing",
      location: "Atlas Mountains, Morocco",
      target-u: "0.18 W/m²K"
    )
    #v(8pt)
    #glaser-u-value-block()
  ],
  grid.cell(colspan: 8)[
    #vector-plate-1-20(title: "1:20 Constructive Plate Placeholder")
  ]
)

#pagebreak()

// ACT 2: Territorial & Environmental Context (Spread 2 / Verso-Recto)
= Act 2: Territorial & Environmental Context

#swiss-grid(
  grid.cell(colspan: 6)[
    == Macro-Geomorphic Topography
    The design emerges from solar azimuth vectors and seasonal katabatic wind channels. 
    By grounding the foundation plinth directly into bedrock, diurnal thermal mass dampens 
    interior temperature fluctuations by over 14 Kelvin without active mechanical chillers.
  ],
  grid.cell(colspan: 6)[
    #rect(width: 100%, height: 160pt, stroke: stroke-projection, fill: luma(250))[
      #place(center + horizon)[#text(font: "JetBrains Mono", size: 8pt)[Bioclimatic Psychrometric & Wind Vector Matrix]]
    ]
  ]
)

#pagebreak()

// ACT 3: Spatial Anatomy & Statutory Code Compliance (Spread 3)
= Act 3: Spatial Anatomy (1:100 Architectural Plan)

#swiss-grid(
  grid.cell(colspan: 3)[
    == Statutory Egress
    - Wheelchair Turning: 1500mm clear arc
    - Corridor Clear Width: 1800mm primary
    - Maximum Egress Travel: 28.4m (< 45m statutory)
    - Door Clear Opening: 920mm throughout
  ],
  grid.cell(colspan: 9)[
    #rect(width: 100%, height: 180pt, stroke: stroke-cut, fill: luma(252))[
      #place(center + horizon)[#text(font: "JetBrains Mono", size: 9pt)[1:100 Dimensioned Architectural Plan with PMR Turning Radii]]
    ]
  ]
)

#pagebreak()

// ACT 4: Tectonic Proof & Constructive Detailing (Spread 4 / Flagship)
= Act 4: Tectonic Proof (1:20 Wall Section)

#swiss-grid(
  grid.cell(colspan: 4)[
    == Constructive Rigor
    Eliminating the superficial render trap requires undeniable constructive detailing.
    The primary load path transfers through 250mm reinforced concrete slab into shear cores.
    A continuous 120mm polyisocyanurate (PIR) envelope breaks all cold bridges at slab perimeter.
  ],
  grid.cell(colspan: 8)[
    #vector-plate-1-20(title: "Flagship 1:20 Constructive Wall Section Vector Plate")
  ]
)

#pagebreak()

// ACT 5: Lived Climax & Scenography (Spread 5)
= Act 5: Lived Climax & Scenography

#swiss-grid(
  grid.cell(colspan: 6)[
    == 1:5 Millwork Joinery
    Custom walnut cabinetry detailed with 3mm black shadow line reveal.
    Concealed Blum Movento drawer runners, 45-degree mitered solid edging, 
    and acoustic drop-down perimeter gaskets guarantee acoustic separation.
  ],
  grid.cell(colspan: 6)[
    == Colophon & Production Integrity
    - Compiled via Editorial Studio Dual-Engine Pipeline
    - Typography: Space Grotesk, Garamond, JetBrains Mono
    - Preflight Standard: ISO 15930-7 (PDF/X-4), FOGRA51 CMYK
    - Grid: 12-Column Swiss Modular with 4mm Gutters
  ]
)
