import json

p = r'g:\My Drive\Projects\sara-bensalem-skills\skills\portfolio-monograph\resources\architectural_languages.json'
with open(p, 'r', encoding='utf-8') as f:
    langs = json.load(f)

new_langs = {
    "indic_spatial_systems": {
        "name": "Indic Spatial Systems & Cognitive Continuum",
        "lineage": "Balkrishna Doshi (Sangath, Aranya), Charles Correa (Jawahar Kala Kendra), Vāstu-Purusha Mandala, Pearl Gupta",
        "spatial_concepts": [
            "Concentric mandala spatial matrix organizing movement from profane periphery to sacred center",
            "Perception continuum linking psychological awareness, sensory body, and built enclosure",
            "Stereotomic thermal massing with deep shaded colonnades and passive microclimatic courtyards",
            "Porous stone jali screens filtering harsh tropical sunlight while maintaining airflow"
        ],
        "monograph_expression": "Square 1:1 or double-A3 spreads, mandala 9-square diagrammatic overlays, Jaipur sandstone and saffron ochre accents, 100-year institutional lifecycle charts."
    },
    "ephemeral_scenography": {
        "name": "Ephemeral Scenography & Olfactory Monument",
        "lineage": "Yasmine Chouchane, Atelier Adeline (Al-'Ula), Robert Irwin, James Turrell, Peter Sloterdijk",
        "spatial_concepts": [
            "Material dialectic: raw prehistoric rock vs fluid midnight drapery vs specular mirror steel",
            "Atomized microclimatic fragrance chambers altering temporal perception in open desert",
            "Radical negative space framing where void occupies greater mass than the architectural intervention",
            "Dissolving boundaries between interior luxury banquets and boundless nocturnal horizons"
        ],
        "monograph_expression": "Cinematic 16:9 landscape spreads, 50%+ negative space breathing room, petrol blue and sandstone contrast palette, technical atomization mist callouts."
    },
    "japandi_wabi_sabi": {
        "name": "Japandi Hybrid & Wabi-Sabi Tectonics",
        "lineage": "Kengo Kuma, Axel Vervoordt, Kenya Hara (White), Tadao Ando, Jun'ichirō Tanizaki (In Praise of Shadows)",
        "spatial_concepts": [
            "Ma (間) — the pregnant pause and spatial void that gives meaning to form",
            "Truth to weathering and impermanence: charred shou sugi ban cedar and unlacquered raw brass",
            "Shadow reveals (joint creux) decoupling base plinth from wall plane by 5mm",
            "Acoustic buffering via hand-troweled washi lime plaster and slatted hinoki screens"
        ],
        "monograph_expression": "Minimalist square or A4 spreads, warm greige and cedar palettes, 1:5 custom millwork joinery reveals, raking clerestory lighting diagrams."
    },
    "alpine_monocoque": {
        "name": "Alpine Lightweight Monocoque & Extreme Terrain",
        "lineage": "Charlotte Perriand (Tonneau Refuge), Jean Prouvé, Renzo Piano (Building Workshop), Thibault Chrétien",
        "spatial_concepts": [
            "Aerodynamic shell deflecting 250 km/h blizzard winds and extreme snowdrift loads",
            "Helicopter-deployable modular prefabrication with zero heavy machinery required on site",
            "Super-insulated thermal envelope with continuous aerogel thermal breaks (U < 0.12 W/m²K)",
            "Minimal-impact rock pin foundations eliminating mass concrete excavation in pristine ecosystems"
        ],
        "monograph_expression": "Aeronautical 16-column engineering grid, exploded monocoque axonometrics, titanium-zinc and rescue orange palette, helicopter assembly sequencing diagrams."
    },
    "landscape_ecology": {
        "name": "Landscape Ecology & Topographical Cartography",
        "lineage": "Ian McHarg (Design with Nature), Gilles Clément, Anu Kottummel Joy, OMGEVING, West 8",
        "spatial_concepts": [
            "Micro-topographical stormwater overland flow modeling via 0.25m contour vectors",
            "Stratified ecological planting matrices from pioneer canopy trees down to wetland phytoremediation",
            "Urban heat island mitigation through quantified tree crown density and Leaf Area Index (LAI)",
            "Weeping-tile dry stone terracing managing steep soil hydrology without hydrostatic pressure"
        ],
        "monograph_expression": "Double-page monograph spreads with vector contour stippling, botanical phenology calendars, soft sage and wetland ochre palettes, cross-sectional root vault details."
    },
    "urban_morphology": {
        "name": "Urban Morphology & Public Space Continuum",
        "lineage": "Aldo Rossi (The Architecture of the City), Jan Gehl, Palak Bhattad (CEPT MUD), Camillo Sitte",
        "spatial_concepts": [
            "Deconstruction of medieval burgage lot subdivisions and perimeter block typologies",
            "The green ring buffer (e.g. Kraków Planty loop) managing pedestrian-vehicular modal transitions",
            "Three-phase diurnal temporal cycles along urban spines (logistics -> tourist -> cultural/jazz)",
            "Active ground-floor edges and microclimate shading prioritizing non-motorized pedestrian life"
        ],
        "monograph_expression": "2:1 panoramic double-square spreads (1190 x 595 mm), 50% left analytical text breathing zone, terracotta roof and cobblestone sand palette, exploded block axonometrics."
    },
    "tropical_resilience": {
        "name": "Tropical Resilience & Demountable Modular Infrastructure",
        "lineage": "David Romaldo Sitepu (PUPR BIM), Ken Yeang, Tay Kheng Soon, Vo Trong Nghia",
        "spatial_concepts": [
            "Elevated stilt boardwalks accommodating extreme riverine tidal flood fluctuations",
            "Prefabricated demountable steel frames joined via stainless steel locking pins without welding",
            "Diurnal lighting adaptation: daytime deep solar shading vs night-time warm lantern community activation",
            "Integrated Non-Motorized Transport (NMT) matrices and multi-modal bicycle/riparian hubs"
        ],
        "monograph_expression": "4:3 presentation plates, multi-scalar sheets (site plan + elevation + 1:10 pin connection), polycarbonate cyan and steel blue palette, diurnal day/night paired views."
    },
    "speculative_critical": {
        "name": "Speculative Critical Fiction & Low-Gravity Habitats",
        "lineage": "Superstudio, Archigram, Lebbeus Woods, Hana Moharram (AASTMT), Liam Young",
        "spatial_concepts": [
            "Planetary reduced-gravity kinetic choreography (G = 0.7 - 0.6) replacing stairs with bouncing ramps",
            "Cyclopean Nubian stone stereotomy creating deep thermal inertia against harsh desert solar radiation",
            "Speculative critical narrative pacing confronting institutional hegemony and planetary degradation",
            "Grounding speculative concepts with verified real-world staircase shop drawings and stone cladding anchors"
        ],
        "monograph_expression": "A4 landscape narrative frames, running cosmic timeline headers, celestial obsidian and Nubian ochre palette, multi-story steel stair fabrication plates."
    },
    "trauma_informed_commons": {
        "name": "Trauma-Informed Civic Commons & Liminal Thresholds",
        "lineage": "Krithika Srivastva (Shared Thresholds), MASS Design Group, Christopher Alexander, Jallasmaa",
        "spatial_concepts": [
            "The 'Space for Hesitation': deep transitional porticos allowing voluntary entry and orientation without exposure",
            "Non-threatening panoramic 120-degree sightlines eliminating blind corners and institutional entrapment",
            "Intimacy and acoustic gradient sequencing: public street -> shaded colonnade -> hesitation buffer -> quiet sanctuary",
            "Hybrid representation: soft hand-drawn graphite concept overlays softening rigid vector CAD plans"
        ],
        "monograph_expression": "3:2 studio monograph spreads (840 x 560 mm), crimson sanctuary and graphite charcoal palette, 40%+ white space breathing room, psychological tension vector diagrams."
    },
    "environmental_simulation": {
        "name": "Environmental Simulation & Regional Craft Infrastructure",
        "lineage": "Sneha Goel (SPA Bhopal), Ralph Knowles (Solar Envelope), Mahadev Raman (Arup), Ladybug Tools",
        "spatial_concepts": [
            "Computational Ladybug/Honeybee solar radiation mapping guiding building massing and overhang depths",
            "Inverted vaulted roofs collecting rainwater and driving natural stack effect cross-ventilation",
            "Parametric terracotta jali screens calibrated for 78% spatial daylight autonomy without solar glare",
            "Evaporative cooling water courtyards reducing perceived outdoor temperatures by 4.8 K"
        ],
        "monograph_expression": "Technical spreads with environmental simulation metric sidebars, solar radiation heatmaps, Zari terracotta and comfort sage palette, 1:1 physical prototype photographs."
    },
    "commercial_courtyard": {
        "name": "Shaded Commercial Courtyards & Retail Circulation",
        "lineage": "Yassin Saber (Avora Mall), Victor Gruen, Jon Jerde, Benoy, CallisonRTKL",
        "spatial_concepts": [
            "Self-shading stepped building volumes casting natural afternoon shadows over central dining courtyards",
            "Venturi wind corridors capturing prevailing coastal sea breezes and flushing open-air gallerias",
            "Continuous multi-level pedestrian circulation loops maximizing retail storefront visibility without dead ends",
            "Integrated underground parking, grade-level civic water plazas, and open-air rooftop dining terraces"
        ],
        "monograph_expression": "16:9 panoramic landscape spreads, clear leasing zone color coding, Avora Mediterranean blue and travertine limestone palette, multi-level retail loop circulation plans."
    }
}

langs.update(new_langs)
print(f'Total architectural languages now: {len(langs)}')

for out_p in [
    r'g:\My Drive\Projects\sara-bensalem-skills\skills\portfolio-monograph\resources\architectural_languages.json',
    r'g:\My Drive\Projects\sara-bensalem-skills\skills\portfolio-design\resources\architectural_languages.json'
]:
    with open(out_p, 'w', encoding='utf-8') as f:
        json.dump(langs, f, indent=2)
    print(f'Wrote {out_p}')
