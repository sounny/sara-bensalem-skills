"""
models.py - Domain Models for Spatial Stitch (Portfolio & Editorial Document Design)
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field
import uuid
import time


class CanvasFormat(str, Enum):
    LANDSCAPE_16_9 = "LANDSCAPE_16_9"
    DOUBLE_A3 = "DOUBLE_A3"
    PORTRAIT_A4 = "PORTRAIT_A4"
    PRINT_MONOGRAPH = "PRINT_MONOGRAPH"


class LayoutArchetype(str, Enum):
    THE_PASSPORT = "THE_PASSPORT"
    THE_CONSTRUCTIVE_PROOF = "THE_CONSTRUCTIVE_PROOF"
    THE_SPATIAL_ANATOMY = "THE_SPATIAL_ANATOMY"
    THE_CARTOGRAPHIC_CONTEXT = "THE_CARTOGRAPHIC_CONTEXT"
    THE_ENVIRONMENTAL_ENGINE = "THE_ENVIRONMENTAL_ENGINE"
    THE_TECTONIC_TRIPTYCH = "THE_TECTONIC_TRIPTYCH"
    THE_PROCESS_MATRIX = "THE_PROCESS_MATRIX"
    THE_SCENOGRAPHIC_SPREAD = "THE_SCENOGRAPHIC_SPREAD"
    THE_URBAN_TERRITORY = "THE_URBAN_TERRITORY"
    THE_TYPOGRAPHIC_INDEX = "THE_TYPOGRAPHIC_INDEX"


class CreativeRange(str, Enum):
    REFINE = "REFINE"
    EXPLORE = "EXPLORE"
    REIMAGINE = "REIMAGINE"


class VariantAspect(str, Enum):
    LAYOUT = "LAYOUT"
    GRID_SYSTEM = "GRID_SYSTEM"
    COLOR_PALETTE = "COLOR_PALETTE"
    TYPOGRAPHY = "TYPOGRAPHY"
    TECTONIC_DENSITY = "TECTONIC_DENSITY"


class ProjectPassport(BaseModel):
    title: str = "Project Monograph"
    typology: str = "Civic & Cultural Architecture"
    location: str = "Paris, France"
    coordinates: str = "48°51'24\"N 02°21'07\"E"
    year: str = "2026"
    area: str = "3,200 m²"
    client: str = "Municipal Heritage Trust"
    stage: str = "RIBA Stage 4 / Construction Documentation"
    team_size: int = 4
    candidate_role: str = "Lead Project Architect & Construction Detailing"
    line_item_contributions: List[str] = Field(default_factory=lambda: [
        "1:20 constructive wall section envelope detailing",
        "Breton stone masonry stabilization schedule",
        "Lime-hemp thermal insulation specifications",
        "PMR accessibility corridor clearance compliance"
    ])
    software_stack: List[str] = Field(default_factory=lambda: [
        "Revit 2026 (BIM)", "Rhino 8 + Grasshopper", "AutoCAD", "InDesign"
    ])
    work_rights_status: str = "Permanent EU Citizen / No Sponsorship Required"
    thesis_statement: str = "Reconciling historical vernacular granite fabric with contemporary low-carbon hygrothermal retrofits."


class EditorialTokens(BaseModel):
    name: str = "Swiss Monograph Standard"
    paper_color: str = "#FBFBF8"
    ink_color: str = "#090B0E"
    ink_secondary: str = "#5C6470"
    accent_color: str = "#FFAF01"
    accent_secondary: str = "#002B49"
    grid_line_color: str = "#E6E2DA"
    
    font_family_display: str = "Inter, 'Helvetica Neue', Arial, sans-serif"
    font_family_body: str = "Inter, -apple-system, sans-serif"
    font_family_mono: str = "'IBM Plex Mono', 'JetBrains Mono', monospace"
    
    baseline_grid_pt: int = 8
    column_count: int = 12
    gutter_px: int = 24
    margin_px: int = 64
    
    line_hairline_px: float = 0.5
    line_thin_px: float = 1.0
    line_medium_px: float = 1.5
    line_cut_px: float = 2.5


class SpreadInstance(BaseModel):
    id: str = Field(default_factory=lambda: f"spread_{uuid.uuid4().hex[:10]}")
    project_id: str
    spread_number: int = 1
    act_number: int = 1
    archetype: LayoutArchetype = LayoutArchetype.THE_PASSPORT
    title: str = "Spread Title"
    subtitle: str = "Architectural Case Study"
    format: CanvasFormat = CanvasFormat.LANDSCAPE_16_9
    width: int = 1920
    height: int = 1080
    prompt: str = ""
    svg_content: str = ""
    html_content: str = ""
    created_at: float = Field(default_factory=time.time)
    audit_score: Optional[int] = None
    audit_notes: List[str] = Field(default_factory=list)


class PortfolioProject(BaseModel):
    id: str = Field(default_factory=lambda: f"proj_{uuid.uuid4().hex[:8]}")
    name: str
    description: str = ""
    canvas_format: CanvasFormat = CanvasFormat.LANDSCAPE_16_9
    design_system_id: str = "ds_swiss_standard"
    passport: ProjectPassport = Field(default_factory=ProjectPassport)
    spread_ids: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class AuditCategoryScore(BaseModel):
    category_id: str
    category_name: str
    max_points: int
    awarded_points: int
    status: str
    critique: str


class AuditReport(BaseModel):
    spread_id: str
    total_score: int
    max_score: int = 100
    rank: str
    render_trap_alert: bool
    drawing_to_render_ratio: float
    category_scores: List[AuditCategoryScore]
    passed_checks: List[str]
    critical_failures: List[str]
    constructive_remediations: List[str]
