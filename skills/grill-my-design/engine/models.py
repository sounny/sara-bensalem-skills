"""
Domain models for Grill My Design Socratic Critique Engine (2026 Enhanced Edition)
Sara Bensalem Studio • Strasbourg Atelier [48°35'05"N 07°45'02"E]
"""
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class JuryPersona(str, Enum):
    CONSTRUCTIVE_LEAD = "constructive_lead"    # The "Detail Nazi" (1:20, leaks, thermal breaks)
    HIRING_DIRECTOR = "hiring_director"        # The 15-second recruiter filter
    SPATIAL_CHAIR = "spatial_chair"            # The crit chair (program, circulation, PMR)
    ENVIRONMENTAL_AUDITOR = "environmental"    # Bioclimatic, solar, ventilation, carbon
    VISUAL_CURATOR = "visual_curator"          # Swiss grid, typography hierarchy, negative space, scalar flow
    FULL_TRIBUNAL = "full_tribunal"            # Synthesis of all 5 personas

class Severity(str, Enum):
    FATAL = "FATAL"         # Immediate disqualification / build failure
    CRITICAL = "CRITICAL"   # Serious red flag in crit or review
    MODERATE = "MODERATE"   # Needs drawing clarification
    MINOR = "MINOR"         # Polish and presentation refinement

class ScrutinyProbe(BaseModel):
    persona: JuryPersona
    dimension: str
    interrogation_question: str
    vulnerability_detected: str
    redline_fix: str
    severity: Severity

class DimensionScore(BaseModel):
    dimension_id: str
    name: str
    score: int = Field(ge=0, le=100)
    critique: str

class GrillReport(BaseModel):
    verdict: str  # STRONG HIRE, CONDITIONAL PASS, RENDER TRAP ALERT, REWORK
    overall_score: int
    dimension_scores: List[DimensionScore]
    top_vulnerabilities: List[ScrutinyProbe]
    defense_remedies: List[str]
    next_crit_prompt: str
    recruiter_15s_takeaway: str
