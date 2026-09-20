"""
The 22 Lethal Render Traps Detection & Socratic Interrogation Catalog
Sara Bensalem Studio • Strasbourg Atelier [48°35'05"N 07°45'02"E]
Based on empirical tectonic auditing of 43+ international architectural portfolios.
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class RenderTrapDefinition:
    trap_id: int
    title: str
    dimension: str
    persona: str  # "constructive_lead", "spatial_chair", "environmental", "hiring_director", "visual_curator"
    severity: str # "FATAL", "CRITICAL", "MODERATE", "MINOR"
    regex_triggers: List[str]
    failure_mechanism: str
    interrogation_question: str
    recommended_defense: str
    alternative_defenses: List[str]
    remediation_command: str

RENDER_TRAPS_CATALOG: Dict[int, RenderTrapDefinition] = {
    1: RenderTrapDefinition(
        trap_id=1,
        title="The Floating Glass Box",
        dimension="Bioclimatic & Environmental Rigor",
        persona="environmental",
        severity="FATAL",
        regex_triggers=[
            r"\b(glass box|all-glass|fully glazed|floor-to-ceiling glass|frameless curtain)\b",
            r"\b(curtain wall|perimeter glazing)\b(?!.*(louver|shading|shgc|overhang|brise-soleil))"
        ],
        failure_mechanism="Unmitigated solar radiation induces extreme greenhouse overheating (>45°C) and thermal shock cracking at frame perimeters.",
        interrogation_question="You specified expansive floor-to-ceiling glazing with no exterior louvers. What is your calculated Solar Heat Gain Coefficient (SHGC), and how do you prevent severe summer greenhouse overheating?",
        recommended_defense="(Recommended) We specified triple glazing with Low-E soft coatings (SHGC <= 0.22) and integrated motorized external venetian louvers.",
        alternative_defenses=[
            "The facade incorporates automated exterior solar fins calibrated to the local 48° summer solar azimuth.",
            "We recessed the glazing 600mm beneath deep architectural overhangs to provide complete passive summer shading.",
            "Solar gain was accepted as a passive heating strategy and tempered by active chilled ceiling beams."
        ],
        remediation_command='python "skills/bioclimatic-flows/scripts/bioclimatic_calculator.py" --output bioclimatic_flow_plate.svg'
    ),
    2: RenderTrapDefinition(
        trap_id=2,
        title="The Magic Cantilever Stair",
        dimension="Constructive Proof & 1:20 Detailing",
        persona="constructive_lead",
        severity="FATAL",
        regex_triggers=[
            r"\b(cantilever(?:ed)? stair|floating tread|floating stair|suspended stair)\b",
            r"\b(treads? anchored in (?:drywall|plaster))\b"
        ],
        failure_mechanism="Unchassis'd cantilever treads generate dynamic torsional moments that crack partition plaster on day one, violating statutory 1.5 kN/m guard load codes.",
        interrogation_question="Where is the concealed structural stringer for your floating cantilever stair, and how does the assembly transfer live load moments without shearing the partition wall?",
        recommended_defense="(Recommended) We concealed a 250x100x8mm welded structural steel box stringer inside the partition, sliding solid timber sleeves over rigid steel box outriggers.",
        alternative_defenses=[
            "The treads are welded to an embedded structural flitch plate bolted through reinforced concrete shear walls.",
            "We integrated a structural laminated glass balustrade (21.5mm SGP interlayer) designed as a load-bearing girder.",
            "This was an early conceptual competition render; structural chassis engineering was deferred to execution phase."
        ],
        remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --output wall_section_1_20.svg'
    ),
    3: RenderTrapDefinition(
        trap_id=3,
        title="The Zero-Reveal Millwork",
        dimension="Constructive Proof & 1:20 Detailing",
        persona="constructive_lead",
        severity="CRITICAL",
        regex_triggers=[
            r"\b(zero-reveal|flush cabinet|seamless millwork|handleless cabinetry)\b",
            r"\b(cabinetry flush against plaster)\b"
        ],
        failure_mechanism="Seasonal hygroscopic wood expansion (2–3mm/m) forces flush-fitted doors to bind, rub, and destroy perimeter site plaster.",
        interrogation_question="Your cabinetry meets wet plaster with zero tolerance. What expansion reveals are detailed at floor, ceiling, and wall perimeters to prevent door binding?",
        recommended_defense="(Recommended) We detailed a continuous 3mm matte black shadow line reveal around all perimeter cabinet edges and against site plaster using aluminum reveal beads.",
        alternative_defenses=[
            "All cabinetry panels incorporate Blum Movento runners with 4D front alignment and 2.5mm perimeter air expansion tolerances.",
            "Perimeter infill scribes (25mm) were integrated for on-site scribing against uneven masonry walls.",
            "The millwork was rendered flush for aesthetic minimalism without modeling physical construction tolerances."
        ],
        remediation_command='python "skills/interior-joinery/scripts/joinery_detailer.py" --gap 3 --output joinery_1_5_detail.svg'
    ),
    4: RenderTrapDefinition(
        trap_id=4,
        title="The Cantilevered Stone Slab",
        dimension="Constructive Proof & 1:20 Detailing",
        persona="constructive_lead",
        severity="FATAL",
        regex_triggers=[
            r"\b(cantilever(?:ed)? (?:stone|granite|marble|travertine|slab))\b",
            r"\b(floating (?:stone|granite|marble|travertine|masonry))\b"
        ],
        failure_mechanism="Natural stone has negligible tensile bending strength (4–6 MPa) and brittle failure modes; unreinforced stone cantilevers snap under self-weight.",
        interrogation_question="Natural stone possesses almost zero tensile strength under bending. What internal tensile reinforcement or steel chassis supports your cantilevered stone element?",
        recommended_defense="(Recommended) We built an internal welded RHS steel chassis and clad it in lightweight 20mm aluminum honeycomb stone composite panels (Aerolam).",
        alternative_defenses=[
            "The cantilever is engineered using post-tensioned stainless steel tendons threaded through core-drilled stone segments.",
            "The stone acts strictly as cosmetic non-structural cladding over a cast-in-place post-tensioned concrete bracket.",
            "The rendering depicted solid stone conceptually; engineering review will replace it with composite cladding."
        ],
        remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --assembly commercial_curtain --output wall_section_1_20.svg'
    ),
    5: RenderTrapDefinition(
        trap_id=5,
        title="The Uninsulated Rammed-Earth Wall",
        dimension="Constructive Proof & 1:20 Detailing",
        persona="constructive_lead",
        severity="FATAL",
        regex_triggers=[
            r"\b(rammed[- ]earth|pisé|compressed earth|adobe)\b(?!.*(plinth|dpc|footing|stem wall))",
            r"\b(rammed[- ]earth directly on ground)\b"
        ],
        failure_mechanism="Capillary groundwater suction wicks up to 1.2m through unstabilized earth, causing moisture softening and basal wall shear collapse under freeze-thaw.",
        interrogation_question="Your rammed-earth wall touches the ground plane directly. Where is your splash plinth and dual EPDM damp-proof barrier to stop catastrophic capillary wicking?",
        recommended_defense="(Recommended) The rammed-earth wall is elevated 300mm above grade on an insulated hydraulic lime concrete plinth with dual EPDM damp-proof courses and French perimeter drainage.",
        alternative_defenses=[
            "We specified 8% hydraulic lime stabilization in the outer earth lift and a continuous subsurface gravel capillary break.",
            "The wall is sheltered by a 1200mm roof overhang and finished with a breathable potassium silicate water-repellent impregnation.",
            "The drawing represented an early massing study where foundation and base detailing were omitted."
        ],
        remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --assembly nubian_sandstone --output wall_section_1_20.svg'
    ),
    6: RenderTrapDefinition(
        trap_id=6,
        title="The Frameless Timber-on-Water Deck",
        dimension="Constructive Proof & 1:20 Detailing",
        persona="constructive_lead",
        severity="CRITICAL",
        regex_triggers=[
            r"\b(timber deck|wooden deck|boardwalk)\b.*?\b(water|lake|river|ocean|pond|riparian)\b",
            r"\b(deck hovering over water)\b"
        ],
        failure_mechanism="Submerged or splash-zone timber without continuous capillary breaks undergoes fungal rot, cellular collapse, and connection shear within 18 months.",
        interrogation_question="How is your riparian boardwalk decoupled from water splash, and what marine-grade foundation prevents timber substructure rot?",
        recommended_defense="(Recommended) We specified hot-dip galvanized steel helical screw piles with timber joists elevated 300mm above 100-year flood level with continuous EPDM capillary breaks.",
        alternative_defenses=[
            "All sub-framing utilizes Class 4 acetylated Accoya timber fastened with 316 A4 marine stainless steel hardware.",
            "The deck rests on precast reinforced concrete pier caps isolated by neoprene elastomeric vibration pads.",
            "Water levels in the render were dramatized; physical construction sits above the statutory flood embankment."
        ],
        remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --assembly tropical_timber --output wall_section_1_20.svg'
    ),
    7: RenderTrapDefinition(
        trap_id=7,
        title="The Sharp 90° High-Rise Tower",
        dimension="Constructive Proof & 1:20 Detailing",
        persona="constructive_lead",
        severity="CRITICAL",
        regex_triggers=[
            r"\b(high[- ]rise|tower|skyscraper)\b.*?\b(sharp corners?|90[- ]degree corners?|pure rectangular extrusion)\b",
            r"\b(sharp edged tower)\b"
        ],
        failure_mechanism="Coherent cross-wind vortex shedding induces severe dynamic cross-wind resonance, overstressing curtain wall gaskets and causing occupant motion sickness.",
        interrogation_question="Your high-rise massing features sharp 90-degree corners. What aerodynamic corner modifications or wind-relief slots prevent dynamic vortex shedding?",
        recommended_defense="(Recommended) We chamfered tower corners with a 15% building radius, added intermediate wind-relief refuge slots, and specified 4-sided structural silicone with +/-25mm drift bellows.",
        alternative_defenses=[
            "The structural core incorporates a 400-tonne tuned mass damper (TMD) at the crown to damp cross-wind accelerations.",
            "Aerodynamic wind tunnel testing was conducted to verify corner drag coefficients under 1.15.",
            "The tower form is an early masterplan block; aerodynamic shaping will occur during wind tunnel engineering."
        ],
        remediation_command='python "skills/bioclimatic-flows/scripts/bioclimatic_calculator.py" --output bioclimatic_flow_plate.svg'
    ),
    8: RenderTrapDefinition(
        trap_id=8,
        title="The Unanchored Ceiling Duct",
        dimension="Constructive Proof & 1:20 Detailing",
        persona="constructive_lead",
        severity="MODERATE",
        regex_triggers=[
            r"\b(exposed ducts?|industrial ceiling|exposed mep|rigidly clamped ducts?)\b",
            r"\b(ducts? touching timber|ducts? through acoustic wall)\b"
        ],
        failure_mechanism="Air-handling mechanical vibrations transmit through rigid ceiling hangers into timber partitions, destroying acoustic STC ratings (NC > 40).",
        interrogation_question="Exposed mechanical ducts are shown running directly through timber partitions. How do you prevent flanking vibration transmission and sound breakout?",
        recommended_defense="(Recommended) We specified 2400mm inline silencer splitter baffles, sleeved ducts through 50mm elastomeric acoustic collars (Sylomer), and kept airflow velocity below 1.5 m/s.",
        alternative_defenses=[
            "All ductwork is isolated on spring-and-neoprene vibration hangers with flexible canvas couplings at all wall penetrations.",
            "Exposed ducts are double-walled spiral insulated acoustic pipe with perforated inner liners.",
            "The MEP visual was a generic Revit placeholder; acoustic coordination will be detailed in technical tender."
        ],
        remediation_command='python "skills/spatial-choreography/scripts/spatial_journey_matrix.py" --output spatial_journey_plate.svg'
    ),
    9: RenderTrapDefinition(
        trap_id=9,
        title="The Full-Height Jamming Pocket Door",
        dimension="Constructive Proof & 1:20 Detailing",
        persona="constructive_lead",
        severity="CRITICAL",
        regex_triggers=[
            r"\b(full[- ]height pocket door|floor-to-ceiling sliding door|frameless pocket door)\b",
            r"\b(3m sliding door|ceiling-recessed pocket track)\b"
        ],
        failure_mechanism="Live-load ceiling slab deflection (10–12mm) crushes top pocket carriage tracks, causing full-height doors to jam permanently and leak acoustic sound.",
        interrogation_question="What structural deflection head channel protects your full-height ceiling-recessed pocket door from being crushed by upper slab live-load sag?",
        recommended_defense="(Recommended) We detailed an extruded aluminum deflection head track allowing 15mm vertical ceiling slab sag without transferring load to the door carriage, paired with Athmer drop seals.",
        alternative_defenses=[
            "The sliding track is suspended from an independent secondary steel sub-frame decoupled from the structural slab.",
            "We specified heavy-duty Hawa Junior 100 pocket systems with integrated soft-close and vertical tolerance adjustment.",
            "The door was rendered full-height schematically; site framing will include a 150mm structural lintel drop."
        ],
        remediation_command='python "skills/interior-joinery/scripts/joinery_detailer.py" --detail pocket_door_head --output joinery_1_5_detail.svg'
    ),
    10: RenderTrapDefinition(
        trap_id=10,
        title="The Red/Green Cockpit / Dashboard",
        dimension="Visual Communication & Swiss Grid",
        persona="visual_curator",
        severity="MODERATE",
        regex_triggers=[
            r"\b(red and green indicators?|red/green buttons?|traffic light color scheme)\b"
        ],
        failure_mechanism="Protanopic and deuteranopic colorblind users (8% of male evaluators) cannot distinguish red from green alerts without redundant geometric coding.",
        interrogation_question="Your diagrammatic alerts rely exclusively on red and green hues. How do colorblind reviewers or occupants verify system safety states?",
        recommended_defense="(Recommended) We enforce redundant visual encoding: pairing color with distinct geometric glyphs (triangles for warning, octagons for stop), typographic labels, and audio cues.",
        alternative_defenses=[
            "We switched the color palette to an accessible blue-orange-amber spectrum compliant with WCAG 2.1 AAA.",
            "All diagrams include high-contrast typographic text labels directly adjacent to every indicator icon.",
            "The presentation slide was an early graphic concept and will be updated to accessible symbology."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_PASSPORT --output accessible_spread.svg'
    ),
    11: RenderTrapDefinition(
        trap_id=11,
        title="The Grey-on-Grey / Beige UI",
        dimension="Visual Communication & Swiss Grid",
        persona="visual_curator",
        severity="CRITICAL",
        regex_triggers=[
            r"\b(light grey text on white|beige text on cream|low contrast text|grey-on-grey)\b",
            r"\b(contrast ratio < ?3:1)\b"
        ],
        failure_mechanism="Contrast ratios below 3:1 fail WCAG AAA accessibility, causing extreme eye strain and immediate cognitive rejection by hiring directors.",
        interrogation_question="Your analytical body copy uses light grey text on muted backgrounds. What is your verified contrast ratio, and can it pass the 15-second recruiter legibility test?",
        recommended_defense="(Recommended) We mandate a strict minimum 7:1 contrast ratio for all analytical body text using deep charcoal typography (#111110) on crisp museum white substrate (#FFFFFF).",
        alternative_defenses=[
            "We increased the body text weight to Neue Haas Grotesk Medium and set type size to minimum 9.5pt.",
            "We adopted dark titanium glassmorphic tokens with high-contrast slate text (#F1F5F9 text on #0B0F17 substrate).",
            "The portfolio was exported in high contrast for print; digital screen settings will be calibrated."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_MONOGRAPH_SPREAD --output high_contrast_spread.svg'
    ),
    12: RenderTrapDefinition(
        trap_id=12,
        title="The 100-Page Student Dump",
        dimension="Recruiter Trust & 15-Second Ergonomics",
        persona="hiring_director",
        severity="CRITICAL",
        regex_triggers=[
            r"\b(100[- ]pages?|80[- ]pages?|60[- ]pages?|all projects included|chronological portfolio)\b",
            r"\b(every studio project)\b"
        ],
        failure_mechanism="Exhaustive portfolios overwhelm evaluators within 45 seconds, burying technical flagship competence under weak first-year school sketches.",
        interrogation_question="Your portfolio contains dozens of projects in chronological order. Why did you not curate down to 4–6 flagship case studies tailored to our firm's typology?",
        recommended_defense="(Recommended) We curated the submission into a disciplined 5-act monograph of 5 flagship projects (Tectonic Hero, Urban System, Research Thesis, Working Detail Set).",
        alternative_defenses=[
            "The full 80-page document is an archival reference; I prepared a concise 24-page executive teaser for initial screening.",
            "Each project demonstrates a distinct technical competency (BIM, parametric facade, adaptive reuse, PMR).",
            "I will curate the portfolio down to the 4 most relevant commercial projects for the partner interview."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_5_ACT_PORTFOLIO --output curated_portfolio.svg'
    ),
    13: RenderTrapDefinition(
        trap_id=13,
        title="The Placeholder Latin Leak",
        dimension="Recruiter Trust & 15-Second Ergonomics",
        persona="hiring_director",
        severity="FATAL",
        regex_triggers=[
            r"\b(lorem ipsum|dolor sit amet|consectetur adipiscing|insert text here|\[project name\])\b"
        ],
        failure_mechanism="Leaving dummy filler Latin in body copy or contents communicates total lack of quality control, resulting in immediate applicant rejection.",
        interrogation_question="Reviewers found 'Lorem ipsum' dummy text in your document. How can a project partner trust you with technical tender drawings if layout copy is unedited?",
        recommended_defense="(Recommended) All placeholder copy has been replaced with an authored 3-line Curatorial Statement defining structural load paths, environmental physics, and programmatic intent.",
        alternative_defenses=[
            "This was a template draft exported before text proofing; the verified final monograph contains full specifications.",
            "I drafted concise Project Passport blocks specifying GIA, scale, structural system, and client program for every plate.",
            "I take full responsibility for the typographical oversight and have sanitized all document copy."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_PASSPORT --output clean_passport.svg'
    ),
    14: RenderTrapDefinition(
        trap_id=14,
        title="The Poster Screenshot Infill Hack",
        dimension="Visual Communication & Swiss Grid",
        persona="visual_curator",
        severity="CRITICAL",
        regex_triggers=[
            r"\b(pasted (?:a1|a2|poster)|board into slide|letterbox poster|vertical board pasted)\b",
            r"\b(tiny unreadable 4pt text on poster)\b"
        ],
        failure_mechanism="Shrinking vertical A1 presentation sheets onto horizontal 16:9 slides produces illegible 3.5pt text and massive lateral letterbox voids.",
        interrogation_question="You pasted vertical A1 exhibition boards into horizontal landscape spreads. Why are drawings reduced to microscopic unreadable fractions rather than typeset across dedicated spreads?",
        recommended_defense="(Recommended) We extracted raw vector drawings and re-typeset them across a disciplined 12-column Swiss grid across 4 dedicated editorial spreads with calibrated ISO 128 lineweights.",
        alternative_defenses=[
            "The A1 boards were included as contextual thumbnails; subsequent spreads show full 1:100 floor plans and 1:20 details at true scale.",
            "We zoomed into primary tectonic details at full bleed, isolating individual orthographic drawings from the competition board.",
            "I will split the presentation board into dedicated landscape case-study leaves."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_CONSTRUCTIVE_PROOF --output disassembled_spread.svg'
    ),
    15: RenderTrapDefinition(
        trap_id=15,
        title="The Fake CAD Section Trap",
        dimension="Constructive Proof & 1:20 Detailing",
        persona="constructive_lead",
        severity="FATAL",
        regex_triggers=[
            r"\b(fake section|elevation labeled as section|zero slab thickness|hollow floor slab)\b",
            r"\b(section.*?(?:zero depth|single line slab|no ceiling plenum))\b"
        ],
        failure_mechanism="Presenting flat 2D unrendered wall elevations as building sections with zero slab or ceiling plenum depth proves a candidate has never detailed a real building.",
        interrogation_question="Your drawing is labeled 'SECTION A-A' but shows zero slab thickness, no screed, and no suspended ceiling plenum. Is this merely an unrendered elevation masquerading as a section?",
        recommended_defense="(Recommended) We cut a genuine building section detailing 250mm reinforced concrete slabs, 70mm acoustic screed to fall, 400mm ceiling plenum with MEP clearance, and continuous perimeter insulation.",
        alternative_defenses=[
            "The drawing was a schematic envelope massing cut; I have verified 1:20 technical wall sections showing complete slab-to-facade assemblies.",
            "We integrated complete foundation strip footings, moisture barrier lap splices, and acoustic floating floor buildups.",
            "I mislabeled the drawing sheet; it will be corrected to show true tectonic sectional depth."
        ],
        remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --output wall_section_1_20.svg'
    ),
    16: RenderTrapDefinition(
        trap_id=16,
        title="The Impossible Spatial Math Error",
        dimension="Spatial Anatomy & Accessibility",
        persona="spatial_chair",
        severity="FATAL",
        regex_triggers=[
            r"\b(impossible area|room area < bed area|bedroom 3\.1 ?m|unbuildable dimensions?)\b",
            r"\b(furniture bounding box exceeds room)\b"
        ],
        failure_mechanism="Declaring room areas smaller than standard furniture bounding boxes (e.g. 3.1 m² master bedroom) reveals gross dimensional illiteracy and lack of spatial checking.",
        interrogation_question="Your floor plan declares a bedroom suite area of 3.1 m², yet a standard double bed requires 3.2 m² of clear floor footprint. How does this room physically function?",
        recommended_defense="(Recommended) We conducted a complete spatial math audit: verifying all Net Internal Areas (NIA) with room dimensions adhering to statutory minimums (bedroom >= 11.5 m², living >= 20 m²).",
        alternative_defenses=[
            "The 3.1 m² tag was a typographical annotation error for an en-suite dressing nook; the master bedroom is 18.5 m².",
            "All functional zones maintain verified furniture footprints plus statutory 1500mm PMR wheelchair turning envelopes.",
            "We recalculated GIA and NIA schedules directly from CAD polylines to eliminate manual entry errors."
        ],
        remediation_command='python "skills/spatial-anatomy/scripts/plan_compliance_engine.py" --output plan_1_100_pmr.svg'
    ),
    17: RenderTrapDefinition(
        trap_id=17,
        title="The Wasted Manufacturer Credential",
        dimension="Constructive Proof & 1:20 Detailing",
        persona="constructive_lead",
        severity="MODERATE",
        regex_triggers=[
            r"\b(knauf|schöck|isokorb|cmb|velux|dormakaba|reynearts)\b.*?\b(cv|resume|certification)\b(?!.*(?:1:20|detail|callout))"
        ],
        failure_mechanism="Boasting manufacturer certifications on CV while failing to include a single manufacturer-grade constructive detail or spec code in portfolio spreads.",
        interrogation_question="You list certified training in Knauf and Schöck building systems on your CV, yet your portfolio spreads omit manufacturer product codes and details. Where is the tangible proof of that expertise?",
        recommended_defense="(Recommended) We included dedicated 1:20 working detail plates citing exact manufacturer system codes (e.g., Knauf W112 acoustic drywall, Schöck Isokorb Type K, EPDM 1.52mm).",
        alternative_defenses=[
            "We integrated complete door/window hardware schedules citing Dormakaba locksets and Reynaers CW50 curtain wall profiles.",
            "The manufacturer certifications were acquired in professional practice; the academic portfolio has now been updated with technical tender plates.",
            "I will supplement the portfolio case study with our practice tender specification package."
        ],
        remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --assembly commercial_curtain --output wall_section_1_20.svg'
    ),
    18: RenderTrapDefinition(
        trap_id=18,
        title="The Flattened Raster Print Trap",
        dimension="Visual Communication & Swiss Grid",
        persona="visual_curator",
        severity="CRITICAL",
        regex_triggers=[
            r"\b(flattened raster|blurry linework|low res pdf|pixelated cad|rasterized vector)\b"
        ],
        failure_mechanism="Exporting technical plans and sections as rasterized JPEG/PNG spreads destroys line weight differentiation and produces blurry, unreadable linework on 4K monitors.",
        interrogation_question="Your technical plans are flattened raster images with pixelated lines and bloated file sizes. Why were drawings not exported as scalable vector graphics with calibrated ISO 128 lineweights?",
        recommended_defense="(Recommended) All orthographic drawings are exported as 100% scalable vector graphics (PDF/SVG) with ISO 128 lineweights (0.50mm cut, 0.25mm boundary, 0.13mm hairline).",
        alternative_defenses=[
            "We re-plotted directly from CAD vectors at 300 DPI vector PDF to preserve hair-line crispness across all zoom levels.",
            "Raster elements are strictly restricted to 300 DPI photography and material textures behind crisp vector linework.",
            "The sample was compressed for email transfer; high-resolution vector PDF is provided for review."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_CONSTRUCTIVE_PROOF --output vector_spread.svg'
    ),
    19: RenderTrapDefinition(
        trap_id=19,
        title="The Metadata Copy-Paste Leak",
        dimension="Recruiter Trust & 15-Second Ergonomics",
        persona="hiring_director",
        severity="CRITICAL",
        regex_triggers=[
            r"\b(metadata mismatch|wrong project title|copy-pasted passport|residential villa labeled resort)\b"
        ],
        failure_mechanism="Copy-pasting project passport metadata across disparate projects (e.g. residential villa claiming 18,000 m² resort footprint) demonstrates reckless carelessness.",
        interrogation_question="Your project passport describes a 3-storey family villa but declares an 18,000 m² footprint and a luxury hospitality program. Why does your passport metadata contradict your drawings?",
        recommended_defense="(Recommended) Every project passport is programmatically bound to verified spatial metrics: Gross Internal Area (GIA), site footprint, typology, and individual role attribution.",
        alternative_defenses=[
            "This was a template duplication error during spread assembly; the corrected passport shows 420 m² GIA single-family residential.",
            "We audited all drawing title blocks and metadata tables to ensure 100% concordance with architectural programs.",
            "I corrected the project data passport across all portfolio sheets."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_PASSPORT --output clean_passport.svg'
    ),
    20: RenderTrapDefinition(
        trap_id=20,
        title="The Default Consumer PDF Metadata Trap",
        dimension="Recruiter Trust & 15-Second Ergonomics",
        persona="hiring_director",
        severity="MODERATE",
        regex_triggers=[
            r"\b(canva|ilovepdf|smallpdf|presentation1|untitled presentation|my tech together)\b"
        ],
        failure_mechanism="Leaving consumer tool creator stamps ('Canva', 'iLovePDF') and generic default titles ('Presentation1') in PDF document properties signals amateurism.",
        interrogation_question="Your document properties show creator stamps from consumer web tools like Canva and a title of 'Presentation1'. Why is your professional architectural monograph not compiled using professional publishing tools?",
        recommended_defense="(Recommended) We sanitized all document metadata using InDesign preflight and Ghostscript, embedding professional credentials, full candidate name, and curated keywords.",
        alternative_defenses=[
            "The final monograph is compiled via InDesign / Typst with sanitized PDF/X-4 metadata tags.",
            "Web compression was applied as a temporary measure; the official master PDF is authored with studio metadata.",
            "I have updated the PDF title and metadata dictionary to reflect professional monograph standards."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_MONOGRAPH_SPREAD --output sanitized_spread.svg'
    ),
    21: RenderTrapDefinition(
        trap_id=21,
        title="The 3D Book Mockup Letterbox Trap",
        dimension="Visual Communication & Swiss Grid",
        persona="visual_curator",
        severity="CRITICAL",
        regex_triggers=[
            r"\b(3d book mockup|open book render|angled spread mockup|perspective book render)\b"
        ],
        failure_mechanism="Embedding spreads inside 3D renders of open physical books with artificial drop shadows wastes >=35% of display canvas and makes drawings unreadable.",
        interrogation_question="You embedded your portfolio spreads inside a 3D photograph of an open book with artificial shadows and grey margins, wasting 35% of the screen. Why are drawings not displayed at full 1:1 bleed?",
        recommended_defense="(Recommended) We eliminated artificial 3D book mockups, exporting true 1:1 full-bleed vector spreads (16:9 widescreen) maximizing canvas area and technical linework resolution.",
        alternative_defenses=[
            "The physical mockup was prepared for social media preview; the formal submission features true 1:1 flat digital spreads.",
            "Every spread is rendered full bleed without artificial shadow borders to optimize 4K screen readability.",
            "I will replace the mockup angles with direct full-bleed PDF spreads."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_MONOGRAPH_SPREAD --output full_bleed_spread.svg'
    ),
    22: RenderTrapDefinition(
        trap_id=22,
        title="The Cover-to-Spread Aspect Ratio Mismatch",
        dimension="Visual Communication & Swiss Grid",
        persona="visual_curator",
        severity="MODERATE",
        regex_triggers=[
            r"\b(vertical cover horizontal spreads|aspect ratio mismatch|jumping aspect ratio|portrait cover landscape pages)\b"
        ],
        failure_mechanism="Combining a vertical portrait cover (1:1.41) with horizontal landscape spreads (16:9) causes PDF viewers to jump and rescale erratically during the recruiter scan.",
        interrogation_question="Your front cover is formatted as a vertical portrait sheet while your interior spreads are horizontal widescreen. Why does your portfolio jump aspect ratios during initial screen scanning?",
        recommended_defense="(Recommended) We unified the entire document geometry on a consistent 16:9 widescreen landscape aspect ratio for seamless, zero-jump full-screen recruiter review.",
        alternative_defenses=[
            "Both front and back covers match the exact geometry and pixel dimensions of interior spreads.",
            "For print publication, we adhere strictly to ISO A4 landscape with unified folio geometry throughout.",
            "I corrected the cover template to match the widescreen landscape grid of the case study leaves."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_PASSPORT --output unified_cover.svg'
    )
}

# Precompile regex triggers for microsecond matching performance across all 22 traps
PRECOMPILED_TRAP_PATTERNS = {
    trap_id: [re.compile(pat, re.IGNORECASE) for pat in trap.regex_triggers]
    for trap_id, trap in RENDER_TRAPS_CATALOG.items()
}

def detect_render_traps(text: str) -> List[RenderTrapDefinition]:
    """Scans text for occurrences of the 22 Lethal Render Traps using precompiled regexes."""
    detected = []
    text_lower = text.lower()
    
    for trap_id, compiled_patterns in PRECOMPILED_TRAP_PATTERNS.items():
        for pat in compiled_patterns:
            if pat.search(text_lower):
                detected.append(RENDER_TRAPS_CATALOG[trap_id])
                break
                
    return detected
