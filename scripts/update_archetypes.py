import json

existing_p = r'g:\My Drive\Projects\sara-bensalem-skills\skills\portfolio-monograph\resources\archetypes.json'
with open(existing_p, 'r', encoding='utf-8') as f:
    archetypes = json.load(f)

new_archetypes = [
    {
        'id': '11_indic_spatial_systems',
        'name': 'The Indic Spatial Systems & Cognitive Continuum',
        'typology_focus': 'Sacred Geometry, Vāstu Mandala & 100-Year Institutional Systems',
        'page_budget': '24-30 Pages / Spreads',
        'aspect_ratio': 'Square (1:1) or Double-A3',
        'target_firms': 'Institutional masterplanners, cultural foundations, educational think-tanks (Vāstu Shilpa, Correa Foundation)',
        'key_elements': [
            'Vāstu-Purusha mandala 9-square spatial matrix',
            'Perception continuum charts (Mind-Body-Space)',
            'Jaipur sandstone stereotomic massing',
            'Passive courtyard microclimate systems'
        ]
    },
    {
        'id': '12_ephemeral_scenography',
        'name': 'The Ephemeral Scenography & Olfactory Monument',
        'typology_focus': 'Luxury Desert Scenography, Exhibition Architecture & Brand Atmosphere',
        'page_budget': '20-24 Spreads',
        'aspect_ratio': '16:9 Cinematic Landscape',
        'target_firms': 'Haute perfumery scenographers, luxury brand experiential agencies, museum pavilions',
        'key_elements': [
            'Material dialectics (raw rock vs petrol-blue velvet vs mirror stainless)',
            'Atomized scent mist diffusion details',
            '50%+ negative space breathing room',
            'Open-air desert chandeliers'
        ]
    },
    {
        'id': '13_japandi_wabi_sabi',
        'name': 'The Japandi Hybrid & Wabi-Sabi Tectonics',
        'typology_focus': 'Minimalist Residential Tea Pavilions, Wellness Sanctuaries & Bespoke Joinery',
        'page_budget': '18-24 Pages',
        'aspect_ratio': 'Square 1:1 or A4 Landscape',
        'target_firms': 'Boutique residential architects, tea pavilion designers, meditative wellness studios (Kengo Kuma, Axel Vervoordt)',
        'key_elements': [
            'Charred shou sugi ban cedar & hinoki cypress',
            'Hand-troweled acoustic washi lime plaster',
            '5mm shadow reveals (joint creux)',
            'Concealed mortise-and-tenon framing'
        ]
    },
    {
        'id': '14_alpine_bivouac',
        'name': 'The Alpine Bivouac & Extreme Climate Shelter',
        'typology_focus': 'Prefabricated Aerodynamic Monocoque, Extreme Terrain & Helicopter Assembly',
        'page_budget': '24 Spreads / 48 Pages',
        'aspect_ratio': '16:9 Landscape Monograph',
        'target_firms': 'High-altitude expedition architects, modular prefab studios, disaster resilience agencies',
        'key_elements': [
            'Aerodynamic 250 km/h wind deflection monocoque',
            'Aerogel thermal break and titanium-zinc cladding',
            'Helicopter-drop sequence diagrams',
            'Pin-foundation anchorage to alpine rock'
        ]
    },
    {
        'id': '15_landscape_ecology',
        'name': 'The Landscape Ecology & Topographical Cartographer',
        'typology_focus': 'Ecological Urbanism, Tree Crown Canopy Density & Wetland Hydrology',
        'page_budget': '28-36 Spreads / Monograph',
        'aspect_ratio': 'A4 Landscape / Double-Page Monograph',
        'target_firms': 'International landscape agencies (OMGEVING, West 8, Vogt, Gustafson Porter + Bowman)',
        'key_elements': [
            '0.25m vector topographical contour stippling',
            'Stratified botanical planting matrices (canopy to wetland)',
            'Urban canopy microclimate cooling data (LAI)',
            'Weeping tile dry-stone retaining wall sections (1:20)'
        ]
    },
    {
        'id': '16_urban_morphology',
        'name': 'The Urban Morphology & Block Typology Specialist',
        'typology_focus': 'Urban Morphology, Medieval Burgage Parcels & Pedestrian Riverfronts',
        'page_budget': '30-36 Spreads',
        'aspect_ratio': '2:1 Panoramic Double-Square (1190 x 595 mm)',
        'target_firms': 'Masterplanning agencies, civic design consultancies, urban research think-tanks (Gehl, CEPT, UN-Habitat)',
        'key_elements': [
            '2:1 panoramic format with 50% left text breathing zone',
            'Three-phase diurnal activity cycle along urban spines',
            'Burgage parcel lot subdivision diagrams',
            'Planty green belt pedestrian loop flow transitions'
        ]
    },
    {
        'id': '17_tropical_resilience',
        'name': 'The Tropical Resilience & Modular BIM Specialist',
        'typology_focus': 'Demountable Riparian Infrastructure, Modular MSME Kiosks & Tropical BIM',
        'page_budget': '24-35 Pages',
        'aspect_ratio': '4:3 Studio Presentation Portfolio',
        'target_firms': 'Tropical design consultancies, national public works ministries, BIM coordination firms',
        'key_elements': [
            '1st Place National PUPR BIM award proof',
            'Modular demountable steel locking pin details (1:10)',
            'Diurnal day/night paired elevation lighting studies',
            'Stilt riparian boardwalk flood-resilience'
        ]
    },
    {
        'id': '18_speculative_critical',
        'name': 'The Speculative Critical Futurist & Vernacularist',
        'typology_focus': 'Critical Architecture Fiction, Reduced-Gravity Habitats & Nilotic Terracing',
        'page_budget': '40-54 Pages',
        'aspect_ratio': 'A4 Landscape (1:1.414)',
        'target_firms': 'Speculative research practices, extreme environment design agencies, experimental academic studios',
        'key_elements': [
            'Planetary reduced-gravity trajectory choreography (G = 0.7 - 0.6)',
            'Aswan cyclopean stone terraced hospitality hub',
            'Cosmic timeline narrative running header',
            'Working drawing set: staircase and stone cladding details'
        ]
    },
    {
        'id': '19_trauma_informed_commons',
        'name': 'The Trauma-Informed Commons Architect',
        'typology_focus': 'Trauma-Informed Civic Architecture, Psychological Safety & Liminal Sanctuaries',
        'page_budget': '24-30 Spreads',
        'aspect_ratio': '3:2 Studio Monograph (840 x 560 mm)',
        'target_firms': 'Civic foundations, healthcare design studios, public commons masterplanners (MASS Design Group, Studio Gang)',
        'key_elements': [
            'The Space for Hesitation transitional buffer zones',
            'Hybrid hand-drawn graphite concept overlays on CAD plans',
            'Civic-to-sanctuary intimacy and acoustic gradient sections',
            '120-degree panoramic sightlines eliminating blind corners'
        ]
    },
    {
        'id': '20_environmental_simulation',
        'name': 'The Environmental Simulation & Craft Technologist',
        'typology_focus': 'Computational Climate Analysis (Ladybug/Honeybee) & Regional Artisan Bazaars',
        'page_budget': '24-30 Spreads',
        'aspect_ratio': 'A4 Portrait & Landscape Working Set',
        'target_firms': 'Environmental performance consultancies, sustainable architecture studios (Transsolar, Atelier Ten, Buro Happold)',
        'key_elements': [
            'Ladybug annual incident radiation heatmaps (kWh/m²)',
            'Spatial daylight autonomy (sDA) and UTCI thermal comfort indices',
            'Porous terracotta jali screens with evaporative cooling courtyards',
            '1:1 physical prototype fabrication plates'
        ]
    },
    {
        'id': '21_commercial_courtyard',
        'name': 'The Shaded Commercial Courtyard Masterplanner',
        'typology_focus': 'Mixed-Use Retail Malls, Self-Shading Massing & Pedestrian Circulation Loops',
        'page_budget': '45-65 Spreads',
        'aspect_ratio': '16:9 Panoramic Landscape Monograph',
        'target_firms': 'Commercial retail consultancies, mixed-use developers, hospitality masterplanners (CallisonRTKL, Benoy, Gensler)',
        'key_elements': [
            'Self-shading massing casting courtyard afternoon shadows (13:00-16:00)',
            'Continuous multi-level pedestrian retail circulation loops',
            'Venturi wind corridors channeling coastal sea breezes',
            'Travertine limestone rainscreen facade specifications'
        ]
    }
]

existing_ids = {a['id'] for a in archetypes}
for a in new_archetypes:
    if a['id'] not in existing_ids:
        archetypes.append(a)

print(f'Total archetypes now: {len(archetypes)}')
for path in [
    r'g:\My Drive\Projects\sara-bensalem-skills\skills\portfolio-monograph\resources\archetypes.json',
    r'g:\My Drive\Projects\sara-bensalem-skills\skills\portfolio-design\resources\archetypes.json'
]:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(archetypes, f, indent=2)
    print(f'Wrote {path}')
