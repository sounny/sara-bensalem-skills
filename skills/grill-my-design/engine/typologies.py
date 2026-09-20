"""
Architectural Typologies & Context-Aware Audit Intelligence
Sara Bensalem Studio • Strasbourg Atelier [48°35'05"N 07°45'02"E]
"""

from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass

class ArchitecturalTypology(str, Enum):
    RESIDENTIAL_VILLA = "residential_villa"
    HIGH_RISE_COMMERCIAL = "high_rise_commercial"
    CULTURAL_MUSEUM = "cultural_museum"
    ADAPTIVE_REUSE = "adaptive_reuse"
    MASS_TIMBER = "mass_timber"
    RIPARIAN_WATERFRONT = "riparian_waterfront"
    URBAN_MASTERPLAN = "urban_masterplan"
    GENERAL_COMMERCIAL = "general_commercial"

@dataclass
class TypologyAuditProfile:
    typology: ArchitecturalTypology
    title: str
    primary_code_reference: str
    dimension_weight_adjustments: Dict[str, float]  # constructive, spatial, environmental, recruiter, visual
    critical_checkpoints: List[str]
    typology_probe: str
    recommended_defense: str
    alternative_defenses: List[str]
    remediation_command: str

TYPOLOGY_PROFILES: Dict[ArchitecturalTypology, TypologyAuditProfile] = {
    ArchitecturalTypology.RESIDENTIAL_VILLA: TypologyAuditProfile(
        typology=ArchitecturalTypology.RESIDENTIAL_VILLA,
        title="Private Residential Villa / Domestic Habitat",
        primary_code_reference="Eurocode 5 / RE2020 / French PMR Arrêté 2015",
        dimension_weight_adjustments={"constructive": 1.2, "spatial": 1.1, "environmental": 1.0, "recruiter": 0.9, "visual": 0.8},
        critical_checkpoints=[
            "Continuous thermal envelope with zero thermal bridges at foundation and terrace cantilevers",
            "Ground floor universal PMR accessibility (1500mm turning diameter in vestibule and WC)",
            "Acoustic threshold decoupling between private sleeping suites and living spaces (DnTw >= 53 dB)",
            "Window reveal and sill flashing with minimum 150mm splash plinth clearance"
        ],
        typology_probe="For this private villa, walk the tribunal through the hygrothermal moisture barrier at your terrace threshold: how do you achieve zero-step PMR flush entry while preventing rain penetration?",
        recommended_defense="(Recommended) We detailed a flush recessed drainage channel (Aco SlotDrain) over a dual EPDM tanking membrane with continuous sub-sill capillary breaks.",
        alternative_defenses=[
            "The terrace slab is thermally broken using Schöck Isokorb with a 15mm drop to an exterior linear trench drain.",
            "We integrated a sheltered 1200mm canopy overhang above the threshold preventing driving rain exposure.",
            "Threshold detailing was treated conceptually in schematic presentation."
        ],
        remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --assembly granite_hemp --output villa_wall_section.svg'
    ),
    ArchitecturalTypology.HIGH_RISE_COMMERCIAL: TypologyAuditProfile(
        typology=ArchitecturalTypology.HIGH_RISE_COMMERCIAL,
        title="High-Rise Tower / Commercial Headquarters",
        primary_code_reference="IBC 2024 Chapter 4 High-Rise / Eurocode 1 Wind Actions",
        dimension_weight_adjustments={"constructive": 1.3, "spatial": 1.2, "environmental": 1.1, "recruiter": 0.8, "visual": 0.6},
        critical_checkpoints=[
            "Cross-wind aerodynamic mitigation (corner chamfering, wind-relief slots, TMD integration)",
            "Core-to-floorplate spatial efficiency (>= 75% Net-to-Gross)",
            "Dual pressurized fire egress stair cores with travel distance <45m",
            "Curtain wall inter-story drift accommodation (+/-25mm bellows) and thermal breaks"
        ],
        typology_probe="In high-rise commercial structures, cross-wind vortex shedding and core efficiency dictate feasibility. What is your core Net-to-Gross ratio, and how does your curtain wall absorb +/-25mm seismic/wind drift?",
        recommended_defense="(Recommended) We maintained a 78% Net-to-Gross core efficiency and specified 4-sided unitized curtain wall cassettes with continuous +/-25mm silicone movement bellows and internal condensation weeping.",
        alternative_defenses=[
            "The structural core houses dual pressurized stairs with a central MEP spine, keeping travel distance under 38m.",
            "Corner chamfers (15% building width) reduce aerodynamic cross-wind vortex shedding forces by 22%.",
            "Core and envelope engineering were estimated using standard commercial benchmark ratios."
        ],
        remediation_command='python "skills/bioclimatic-flows/scripts/bioclimatic_calculator.py" --output tower_wind_aerodynamics.svg'
    ),
    ArchitecturalTypology.CULTURAL_MUSEUM: TypologyAuditProfile(
        typology=ArchitecturalTypology.CULTURAL_MUSEUM,
        title="Cultural Institution / Museum / Scenography",
        primary_code_reference="CIE 157:2004 Museum Lighting / DIN 18041 Acoustic Quality",
        dimension_weight_adjustments={"spatial": 1.3, "visual": 1.2, "environmental": 1.1, "constructive": 0.9, "recruiter": 0.8},
        critical_checkpoints=[
            "Luminance gradient choreography preventing retinal shock (max delta log10 lux < 1.8)",
            "Acoustic reverberation control in public galleries (RT60 <= 0.85s)",
            "Daylight autonomy (sDA) with 100% UV filtration (<50 lux for sensitive artifacts)",
            "Continuous PMR universal promenade (1:12 ramp maximum slope with 1500mm landings every 10m)"
        ],
        typology_probe="For a public museum, light and acoustic sanctuary are sacred. What is your calculated lux transition curve from exterior sunlight to artifact galleries, and how do you achieve museum RT60 acoustic dampening?",
        recommended_defense="(Recommended) We choreographed a 3-stage light decompression airlock (5000 lux -> 350 lux -> 50 lux) with micro-perforated acoustic timber ceiling baffles achieving RT60 = 0.75s.",
        alternative_defenses=[
            "All gallery glazing incorporates double-laminated UV-filtering interlayers (Tuv < 0.5%) and automated motorized blackout louvers.",
            "The circulation sequence flows through a continuous 1:15 universal ramp system with verified 1800mm passing bays.",
            "Gallery illumination was planned based on standard indirect diffuse ceiling cove fixtures."
        ],
        remediation_command='python "skills/spatial-choreography/scripts/spatial_journey_matrix.py" --output museum_spatial_journey.svg'
    ),
    ArchitecturalTypology.ADAPTIVE_REUSE: TypologyAuditProfile(
        typology=ArchitecturalTypology.ADAPTIVE_REUSE,
        title="Adaptive Reuse / Heritage Conservation",
        primary_code_reference="EN 16883 Heritage Energy Performance / WTA 6-2 Internal Insulation",
        dimension_weight_adjustments={"constructive": 1.4, "environmental": 1.1, "spatial": 1.0, "recruiter": 0.8, "visual": 0.7},
        critical_checkpoints=[
            "Hygrothermal vapor breathability of historic masonry (lime-based, no cementitious vapor barriers)",
            "Interstitial condensation prevention via Glaser / WUFI analysis on interior insulation",
            "Decoupled structural load transfer (flitch plates, independent steel/timber frame)",
            "Reversible tectonic interventions preserving historic fabric integrity"
        ],
        typology_probe="In historic masonry retrofit, applying impervious interior insulation causes frost spalling and structural rot. How does your wall assembly ensure vapor breathability and prevent interstitial condensation?",
        recommended_defense="(Recommended) We specified 140mm breathable lime-hemp biotamping with interior breathable lime plaster, verified by Glaser hygrothermal analysis to produce zero interstitial condensation dew points.",
        alternative_defenses=[
            "We inserted a thermally decoupled self-supporting timber frame leaving a 50mm ventilated air cavity behind the historic stone.",
            "All new floor loads are carried by internal steel flitch plates bolted to reversible chemical anchors.",
            "Insulation was planned as standard rigid PIR with interior vapor retarder."
        ],
        remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --assembly granite_hemp --output heritage_wall_glaser.svg'
    ),
    ArchitecturalTypology.MASS_TIMBER: TypologyAuditProfile(
        typology=ArchitecturalTypology.MASS_TIMBER,
        title="Mass Timber / CLT / Glulam Architecture",
        primary_code_reference="Eurocode 5 (EN 1995-1-2 Fire) / ISO 10140 Acoustic Impact",
        dimension_weight_adjustments={"constructive": 1.3, "environmental": 1.2, "spatial": 0.9, "recruiter": 0.9, "visual": 0.7},
        critical_checkpoints=[
            "End-grain moisture sealing and continuous capillary breaks at wet plinths",
            "Acoustic impact sound isolation (L'n,w <= 50 dB via Sylomer resilient mounts and dry screed)",
            "Charring rate fire resistance engineering (60–90 min char depth calculation)",
            "Concealed flitch plate and dowel connections with certified fire protection"
        ],
        typology_probe="Mass timber's primary structural failure modes are acoustic impact flanking and end-grain moisture rot. What resilient acoustic mounts isolate your CLT slabs, and how is end-grain protected?",
        recommended_defense="(Recommended) We decoupled the CLT slab using 50mm Sylomer elastomeric acoustic strips beneath a 70mm dry acoustic screed, with factory-applied hydrophobic paraffin end-grain sealing.",
        alternative_defenses=[
            "All beam-column junctions utilize concealed structural steel knife plates with internal steel dowels recessed behind 25mm oak fire plugs.",
            "Timber elements are elevated 200mm on hot-dip galvanized steel plinths with continuous EPDM capillary breaks.",
            "Mass timber detailing will be coordinated with the timber prefabricator during Stage 4."
        ],
        remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --assembly alpine_monocoque --output clt_mass_timber_detail.svg'
    ),
    ArchitecturalTypology.RIPARIAN_WATERFRONT: TypologyAuditProfile(
        typology=ArchitecturalTypology.RIPARIAN_WATERFRONT,
        title="Riparian Waterfront / Coastal / Wetland Architecture",
        primary_code_reference="FEMA P-55 Coastal Construction / Eurocode 7 Geotechnical",
        dimension_weight_adjustments={"constructive": 1.3, "environmental": 1.3, "spatial": 0.9, "recruiter": 0.8, "visual": 0.7},
        critical_checkpoints=[
            "Finished floor level elevated minimum +300mm above 100-year flood splash line",
            "Hot-dip galvanized helical screw piles or marine concrete pier foundations",
            "Continuous EPDM capillary breaks isolating timber substructure from capillary moisture",
            "Corrosion-resistant 316 A4 marine-grade stainless steel fasteners"
        ],
        typology_probe="For waterfront structures, moisture wicking and tidal splash destroy substructures rapidly. What foundation engineering elevates your structure above 100-year flood levels, and where are your capillary breaks?",
        recommended_defense="(Recommended) We specified hot-dip galvanized helical screw piles socketed into bedrock, elevating the substructure +450mm above 100-year flood level with continuous EPDM capillary breaks.",
        alternative_defenses=[
            "All structural timbers are Class 4 acetylated Accoya secured with 316 A4 marine stainless hardware.",
            "The foundation consists of precast reinforced concrete pier caps isolated by neoprene elastomeric pads.",
            "The water level shown in the render is conceptual and will be engineered above statutory flood lines."
        ],
        remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --assembly tropical_timber --output waterfront_pier_detail.svg'
    ),
    ArchitecturalTypology.URBAN_MASTERPLAN: TypologyAuditProfile(
        typology=ArchitecturalTypology.URBAN_MASTERPLAN,
        title="Urban Masterplan / Transit-Oriented Development",
        primary_code_reference="TOD Standards / City Transit & FAR Zoning Regulations",
        dimension_weight_adjustments={"spatial": 1.4, "environmental": 1.2, "recruiter": 0.9, "visual": 1.0, "constructive": 0.5},
        critical_checkpoints=[
            "Explicit calculation of FAR (Floor Area Ratio) and ground coverage percentage",
            "Multi-modal transit catchment isochrones (400m / 5-minute pedestrian radius)",
            "Microclimate wind comfort corridors and urban heat island mitigation",
            "Clear decoupling of public civic realm vs service/logistics circulation"
        ],
        typology_probe="At the macro urban scale, empty masterplan diagrams fail review without zoning math. What are your declared FAR, ground coverage, and 5-minute pedestrian transit catchment metrics?",
        recommended_defense="(Recommended) We declared an FAR of 3.2, 42% ground coverage, and verified that 94% of residential parcels fall within a 400m (5-minute) pedestrian walk to the BRT transit node.",
        alternative_defenses=[
            "The masterplan morphology preserves continuous 30m-wide prevailing wind corridors to mitigate urban heat island effects.",
            "Service and delivery logistics are completely separated into an underground ring corridor decoupled from pedestrian plazas.",
            "FAR and density metrics were estimated based on local district zoning targets."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_URBAN_SYSTEM --output urban_masterplan_spread.svg'
    ),
    ArchitecturalTypology.GENERAL_COMMERCIAL: TypologyAuditProfile(
        typology=ArchitecturalTypology.GENERAL_COMMERCIAL,
        title="Mixed-Use Commercial / Public Architecture",
        primary_code_reference="IBC 2024 / ADA Standards / Eurocode Structural",
        dimension_weight_adjustments={"constructive": 1.0, "spatial": 1.0, "environmental": 1.0, "recruiter": 1.0, "visual": 1.0},
        critical_checkpoints=[
            "Verified universal accessibility and emergency egress corridors",
            "Multi-scalar drawing hierarchy (1:500 context, 1:100 plan, 1:20 constructive detail)",
            "Clear role attribution and Project Passport specification",
            "Disciplined 12-column Swiss typographic grid layout"
        ],
        typology_probe="To prove professional commercial competence, walk the tribunal through your multi-scalar drawing hierarchy: how does your urban concept translate directly into a buildable 1:20 constructive assembly?",
        recommended_defense="(Recommended) We deployed the Trust Trifecta: pairing a 1:500 urban context plan, a 1:100 PMR-compliant statutory floor plan, and a 1:20 constructive wall section with verified manufacturer specs.",
        alternative_defenses=[
            "All programmatic areas maintain verified 1500mm PMR turning circles and exit travel distances under 30m.",
            "The envelope incorporates continuous thermal breaks and calculated solar shading louvers.",
            "The project was an academic exercise emphasizing schematic massing over working drawings."
        ],
        remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_CONSTRUCTIVE_PROOF --output trifecta_spread.svg'
    )
}

def detect_typology(text: str) -> ArchitecturalTypology:
    """Infers the architectural typology from project description or text."""
    t_lower = text.lower()
    
    if any(k in t_lower for k in ["masterplan", "urban design", "transit", "tod", "zoning", "catchment", "neighborhood", "brt", "tram"]):
        return ArchitecturalTypology.URBAN_MASTERPLAN
    elif any(k in t_lower for k in ["waterfront", "riparian", "boardwalk", "river", "lake", "ocean", "coastal", "flood", "pier", "wetland"]):
        return ArchitecturalTypology.RIPARIAN_WATERFRONT
    elif any(k in t_lower for k in ["clt", "mass timber", "glulam", "cross-laminated", "timber tower", "wood construction"]):
        return ArchitecturalTypology.MASS_TIMBER
    elif any(k in t_lower for k in ["adaptive reuse", "heritage", "renovation", "historic", "retrofit", "stone barn", "masonry restoration", "rehabilitation"]):
        return ArchitecturalTypology.ADAPTIVE_REUSE
    elif any(k in t_lower for k in ["museum", "gallery", "exhibition", "cultural", "theater", "auditorium", "scenography", "monument"]):
        return ArchitecturalTypology.CULTURAL_MUSEUM
    elif any(k in t_lower for k in ["tower", "high-rise", "skyscraper", "office headquarters", "commercial center", "lifestyle center", "avora"]):
        return ArchitecturalTypology.HIGH_RISE_COMMERCIAL
    elif any(k in t_lower for k in ["villa", "house", "residence", "residential", "domestic", "home", "maison", "apartment", "dwelling"]):
        return ArchitecturalTypology.RESIDENTIAL_VILLA
    else:
        return ArchitecturalTypology.GENERAL_COMMERCIAL
