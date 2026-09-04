"""
Core Socratic Architectural Critique & Cross-Examination Engine
Sara Bensalem Studio • Strasbourg Atelier
"""
import re
from typing import List, Dict, Any
from .models import JuryPersona, Severity, ScrutinyProbe, DimensionScore, GrillReport

class GrillEngine:
    def __init__(self):
        pass

    def grill(self, submission_text: str, persona: JuryPersona = JuryPersona.FULL_TRIBUNAL) -> GrillReport:
        text_lower = submission_text.lower()
        probes: List[ScrutinyProbe] = []
        dim_scores: List[DimensionScore] = []

        # 1. Constructive Proof & 1:20 Detailing Check
        has_wall_section = any(k in text_lower for k in ["wall section", "coupe de détail", "1:20", "1/20", "detail section", "constructive proof"])
        has_thermal_break = any(k in text_lower for k in ["thermal break", "rupture de pont thermique", "insulation", "epdm", "vapor barrier", "pare-vapeur"])
        has_structure = any(k in text_lower for k in ["glulam", "timber", "steel", "concrete", "flitch", "framing", "slab", "beam", "column"])

        constructive_score = 40
        if has_wall_section: constructive_score += 30
        if has_thermal_break: constructive_score += 20
        if has_structure: constructive_score += 10

        if not has_thermal_break:
            probes.append(ScrutinyProbe(
                persona=JuryPersona.CONSTRUCTIVE_LEAD,
                dimension="Constructive Detailing",
                interrogation_question="Where is the continuous thermal break at your slab edge and parapet? How do you prevent interior condensation and mold?",
                vulnerability_detected="Unaddressed thermal bridging at cantilevered or slab junctions.",
                redline_fix="Specify a structural thermal break module (e.g. Schöck Isokorb) or wrap slab edge with 120mm continuous exterior insulation.",
                severity=Severity.FATAL
            ))
        if not has_wall_section:
            probes.append(ScrutinyProbe(
                persona=JuryPersona.CONSTRUCTIVE_LEAD,
                dimension="Constructive Detailing",
                interrogation_question="You have impressive 3D perspectives, but where is your 1:20 constructive proof? How does the facade envelope meet the ground plane?",
                vulnerability_detected="Absence of buildable 1:20 drawing leaves technical competence unverified.",
                redline_fix="Include a dedicated 1:20 wall section spread with material callouts, EPDM flashing, and dimension chains.",
                severity=Severity.CRITICAL
            ))

        dim_scores.append(DimensionScore(
            dimension_id="constructive",
            name="Constructive Proof & 1:20 Detailing",
            score=min(100, constructive_score),
            critique="Requires explicit constructive drawings with membrane sequencing and thermal breaks." if constructive_score < 70 else "Solid technical detailing with verified buildable junctions."
        ))

        # 2. Spatial Anatomy & Circulation (1:100 / PMR)
        has_pmr = any(k in text_lower for k in ["pmr", "ada", "accessibility", "wheelchair", "turning circle", "clearance", "1500mm", "150cm"])
        has_egress = any(k in text_lower for k in ["egress", "fire stair", "evacuation", "exit", "circulation", "corridor"])

        spatial_score = 50
        if has_pmr: spatial_score += 25
        if has_egress: spatial_score += 25

        if not has_pmr:
            probes.append(ScrutinyProbe(
                persona=JuryPersona.SPATIAL_CHAIR,
                dimension="Spatial Anatomy & Accessibility",
                interrogation_question="Show me your universal accessibility clearances. Can a wheelchair user complete a 1500mm turning maneuver in your entrance vestibule and primary WC?",
                vulnerability_detected="Lack of PMR/ADA compliance indicators risks code failure in permitting.",
                redline_fix="Overlay 1500mm clearance circles in all vestibules, restrooms, and kitchen galleys on your 1:100 plan.",
                severity=Severity.CRITICAL
            ))

        dim_scores.append(DimensionScore(
            dimension_id="spatial",
            name="Spatial Anatomy & Circulation",
            score=min(100, spatial_score),
            critique="Check corridor dead-ends and PMR turning clearance circles." if spatial_score < 75 else "Well-articulated spatial hierarchy and circulation logic."
        ))

        # 3. Environmental Rigor & Bioclimatic Flows
        has_solar = any(k in text_lower for k in ["solar", "shading", "orientation", "south-facing", "brise-soleil", "louver", "overheating", "shgc"])
        has_ventilation = any(k in text_lower for k in ["cross-ventilation", "ventilation", "stack effect", "airflow", "thermal mass", "bioclimatic"])

        enviro_score = 45
        if has_solar: enviro_score += 30
        if has_ventilation: enviro_score += 25

        if not has_solar:
            probes.append(ScrutinyProbe(
                persona=JuryPersona.ENVIRONMENTAL_AUDITOR,
                dimension="Environmental Performance",
                interrogation_question="You have expansive glazing on the western facade. What is your calculated Solar Heat Gain Coefficient (SHGC), and how do you mitigate late-afternoon solar heat gain?",
                vulnerability_detected="Unprotected large-span glazing risks extreme summer solar overheating.",
                redline_fix="Integrate deep vertical exterior louvers or dynamic solar shading with Uw <= 0.8 W/m²K triple glazing.",
                severity=Severity.MODERATE
            ))

        dim_scores.append(DimensionScore(
            dimension_id="environmental",
            name="Bioclimatic & Environmental Rigor",
            score=min(100, enviro_score),
            critique="Ground passive diagrams in orientation physics rather than generic arrows." if enviro_score < 70 else "Rigorous solar and natural airflow logic demonstrated."
        ))

        # 4. Recruiter Trust Ergonomics (The 15-Second Test)
        has_passport = any(k in text_lower for k in ["passport", "project passport", "role", "scale", "location", "attribution", "individual work", "team"])
        has_work_rights = any(k in text_lower for k in ["visa", "work rights", "citizenship", "eu citizen", "authorized", "sponsorship"])
        has_renders_only = any(k in text_lower for k in ["lumion", "enscape", "d5", "midjourney", "photorealistic render", "mood board"]) and not has_wall_section

        recruiter_score = 60
        if has_passport: recruiter_score += 20
        if has_work_rights: recruiter_score += 15
        if has_renders_only: recruiter_score -= 25

        if not has_passport:
            probes.append(ScrutinyProbe(
                persona=JuryPersona.HIRING_DIRECTOR,
                dimension="Recruiter Trust Ergonomics",
                interrogation_question="I have 15 seconds to review this portfolio. What was your exact individual line-item contribution versus the senior partner or team members?",
                vulnerability_detected="Ambiguous individual role attribution causes hiring directors to discount the project.",
                redline_fix="Place a standardized Project Passport card top-left stating exact role (e.g. 'Lead Envelope Detailer & Permitting Documentation').",
                severity=Severity.FATAL if not has_passport else Severity.MODERATE
            ))

        dim_scores.append(DimensionScore(
            dimension_id="recruiter",
            name="Recruiter Trust & 15-Second Ergonomics",
            score=max(20, min(100, recruiter_score)),
            critique="Ambiguous individual contribution risks screening rejection." if recruiter_score < 75 else "Clean, transparent attribution and outcome-forward passport."
        ))

        # Calculate Overall Score & Verdict
        overall = int(sum(d.score for d in dim_scores) / len(dim_scores))
        
        if overall >= 85:
            verdict = "STRONG HIRE / ADVANCE TO NEXT ROUND"
            takeaway = "Exceptional portfolio defense. Demonstrates tectonic proof, spatial rigor, and recruiter clarity."
        elif overall >= 70:
            verdict = "CONDITIONAL PASS / ADDRESS WEAK SPOTS"
            takeaway = "Promising spatial concepts but vulnerable on technical constructibility and 1:20 detailing."
        elif has_renders_only or constructive_score < 50:
            verdict = "RENDER TRAP ALERT / SUSPECT CONSTRUCTIBILITY"
            takeaway = "Heavily reliant on 3D atmosphere with insufficient constructive evidence. High risk in partner interview."
        else:
            verdict = "REWORK REQUIRED / STRENGTHEN TECHNICAL PROOF"
            takeaway = "Fundamental omissions in thermal integrity, PMR clearances, or role transparency."

        remedies = [p.redline_fix for p in probes[:3]]
        next_prompt = probes[0].interrogation_question if probes else "Walk me through how your structural grid informs the interior ceiling plenum."

        return GrillReport(
            verdict=verdict,
            overall_score=overall,
            dimension_scores=dim_scores,
            top_vulnerabilities=probes[:4],
            defense_remedies=remedies,
            next_crit_prompt=next_prompt,
            recruiter_15s_takeaway=takeaway
        )
