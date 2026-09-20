"""
Core Socratic Architectural Critique & Cross-Examination Engine (2026 Enhanced Edition)
Sara Bensalem Studio • Strasbourg Atelier [48°35'05"N 07°45'02"E]
"""

import re
from typing import List, Dict, Optional, Union

try:
    from .models import (
        JuryPersona, Severity, ScrutinyProbe, DimensionScore, 
        RedlineMarkup, GrillReport
    )
    from .render_traps import detect_render_traps, RENDER_TRAPS_CATALOG
    from .typologies import detect_typology, TYPOLOGY_PROFILES, ArchitecturalTypology
    from .redline_stamp import generate_crit_stamp_svg
except ImportError:
    from models import (
        JuryPersona, Severity, ScrutinyProbe, DimensionScore, 
        RedlineMarkup, GrillReport
    )
    from render_traps import detect_render_traps, RENDER_TRAPS_CATALOG
    from typologies import detect_typology, TYPOLOGY_PROFILES, ArchitecturalTypology
    from redline_stamp import generate_crit_stamp_svg

class GrillEngine:
    def __init__(self):
        pass

    def grill(
        self,
        submission_text: str,
        persona: JuryPersona = JuryPersona.FULL_TRIBUNAL,
        typology_override: Optional[Union[ArchitecturalTypology, str]] = None,
        current_round: int = 1
    ) -> GrillReport:
        text_lower = submission_text.lower()
        probes: List[ScrutinyProbe] = []
        dim_scores: List[DimensionScore] = []
        redlines: List[RedlineMarkup] = []

        # 0. Typology Detection & Profile Extraction
        if typology_override:
            if isinstance(typology_override, ArchitecturalTypology):
                typology = typology_override
            else:
                try:
                    typology = ArchitecturalTypology(typology_override.lower())
                except ValueError:
                    typology = detect_typology(submission_text)
        else:
            typology = detect_typology(submission_text)

        typo_profile = TYPOLOGY_PROFILES.get(typology, TYPOLOGY_PROFILES[ArchitecturalTypology.GENERAL_COMMERCIAL])

        # 1. Detect Specific Lethal Render Traps (1–22)
        detected_traps = detect_render_traps(submission_text)
        for trap in detected_traps:
            # Map trap to JuryPersona
            p_map = {
                "constructive_lead": JuryPersona.CONSTRUCTIVE_LEAD,
                "spatial_chair": JuryPersona.SPATIAL_CHAIR,
                "environmental": JuryPersona.ENVIRONMENTAL_AUDITOR,
                "hiring_director": JuryPersona.HIRING_DIRECTOR,
                "visual_curator": JuryPersona.VISUAL_CURATOR
            }
            persona_enum = p_map.get(trap.persona, JuryPersona.CONSTRUCTIVE_LEAD)
            sev_enum = Severity(trap.severity) if hasattr(Severity, trap.severity) else Severity.CRITICAL

            # Determine questioning round based on trap dimension
            if "Constructive" in trap.dimension or "Spatial" in trap.dimension:
                round_num = 1
            elif "Environmental" in trap.dimension or "Bioclimatic" in trap.dimension:
                round_num = 2
            else:
                round_num = 3

            all_defenses = [trap.recommended_defense] + trap.alternative_defenses
            probe = ScrutinyProbe(
                persona=persona_enum,
                dimension=trap.dimension,
                interrogation_question=trap.interrogation_question,
                vulnerability_detected=f"[TRAP #{trap.trap_id}: {trap.title.upper()}] {trap.failure_mechanism}",
                redline_fix=trap.recommended_defense.replace("(Recommended) ", "CAD FIX: "),
                severity=sev_enum,
                defense_options=all_defenses,
                remediation_command=trap.remediation_command,
                trap_id=trap.trap_id,
                failure_mechanism=trap.failure_mechanism,
                round_number=round_num
            )
            probes.append(probe)

            redlines.append(RedlineMarkup(
                callout_tag=f"REDLINE #{trap.trap_id:02d}",
                title=trap.title,
                detail=trap.failure_mechanism,
                cad_action=trap.recommended_defense.replace("(Recommended) ", ""),
                severity=sev_enum
            ))

        # 2. Baseline Dimension 1: Constructive Proof & 1:20 Detailing
        has_wall_section = any(k in text_lower for k in ["wall section", "coupe de détail", "1:20", "1/20", "detail section", "constructive proof", "tectonic plate"])
        has_thermal_break = any(k in text_lower for k in ["thermal break", "rupture de pont thermique", "insulation", "epdm", "vapor barrier", "pare-vapeur", "isokorb"])
        has_structure = any(k in text_lower for k in ["glulam", "timber", "steel", "concrete", "flitch", "framing", "slab", "beam", "column", "pin-joint"])

        constructive_score = 40
        if has_wall_section: constructive_score += 30
        if has_thermal_break: constructive_score += 20
        if has_structure: constructive_score += 10

        # Adjust score if traps detected in constructive dimension
        constructive_traps = [t for t in detected_traps if "Constructive" in t.dimension]
        constructive_score = max(20, constructive_score - len(constructive_traps) * 15)

        if not has_thermal_break and not any(t.trap_id in [1, 2, 4, 5] for t in detected_traps):
            probes.append(ScrutinyProbe(
                persona=JuryPersona.CONSTRUCTIVE_LEAD,
                dimension="Constructive Detailing",
                interrogation_question="Where is the continuous thermal break at your slab edge and parapet? How do you prevent interior condensation and mold?",
                vulnerability_detected="Unaddressed thermal bridging at cantilevered or slab junctions.",
                redline_fix="Specify a structural thermal break module (e.g. Schöck Isokorb) or wrap slab edge with continuous exterior insulation.",
                severity=Severity.FATAL,
                defense_options=[
                    "(Recommended) We specified a structural thermal break module (Schöck Isokorb) with 80mm EPS core at the slab junction.",
                    "The exterior envelope is fully wrapped with 120mm continuous mineral wool outside the concrete structure.",
                    "We designed a thermally decoupled self-supporting exterior chassis with pin connections.",
                    "This was a conceptual competition scheme where tectonic detailing was deferred to Stage 3."
                ],
                remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --assembly granite_hemp --output wall_section_1_20.svg',
                round_number=1
            ))

        if not has_wall_section and not any(t.trap_id == 15 for t in detected_traps):
            probes.append(ScrutinyProbe(
                persona=JuryPersona.CONSTRUCTIVE_LEAD,
                dimension="Constructive Detailing",
                interrogation_question="You have impressive 3D perspectives, but where is your 1:20 constructive proof? How does the facade envelope meet the ground plane?",
                vulnerability_detected="Absence of buildable 1:20 drawing leaves technical competence unverified.",
                redline_fix="Include a dedicated 1:20 wall section spread with material callouts, EPDM flashing, and dimension chains.",
                severity=Severity.CRITICAL,
                defense_options=[
                    "(Recommended) I have a 1:20 wall section with EPDM flashing, vapor barrier sequencing, and callout dimensions ready to include.",
                    "The facade uses a unitized curtain wall system with pre-engineered factory thermal breaks.",
                    "The project was an urban masterplan focus, but I can produce a 1:20 tectonic assembly sheet.",
                    "I prioritized 3D atmospheric perspectives over technical working drawings in this spread."
                ],
                remediation_command='python "skills/constructive-detail/scripts/wall_section_builder.py" --output wall_section_1_20.svg',
                round_number=1
            ))

        dim_scores.append(DimensionScore(
            dimension_id="constructive",
            name="Constructive Proof & 1:20 Detailing",
            score=min(100, constructive_score),
            critique="Requires explicit constructive drawings with membrane sequencing and thermal breaks." if constructive_score < 70 else "Solid technical detailing with verified buildable junctions."
        ))

        # 3. Baseline Dimension 2: Spatial Anatomy & Universal Egress (PMR/ADA)
        has_pmr = any(k in text_lower for k in ["pmr", "ada", "accessibility", "wheelchair", "turning circle", "clearance", "1500mm", "150cm"])
        has_egress = any(k in text_lower for k in ["egress", "fire stair", "evacuation", "exit", "circulation", "corridor", "hesitation"])

        spatial_score = 50
        if has_pmr: spatial_score += 25
        if has_egress: spatial_score += 25

        spatial_traps = [t for t in detected_traps if "Spatial" in t.dimension]
        spatial_score = max(20, spatial_score - len(spatial_traps) * 15)

        if not has_pmr and not any(t.trap_id == 16 for t in detected_traps):
            probes.append(ScrutinyProbe(
                persona=JuryPersona.SPATIAL_CHAIR,
                dimension="Spatial Anatomy & Accessibility",
                interrogation_question="Show me your universal accessibility clearances. Can a wheelchair user complete a 1500mm turning maneuver in your entrance vestibule and primary WC?",
                vulnerability_detected="Lack of PMR/ADA compliance indicators risks code failure in permitting.",
                redline_fix="Overlay 1500mm clearance circles in all vestibules, restrooms, and kitchen galleys on your 1:100 plan.",
                severity=Severity.CRITICAL,
                defense_options=[
                    "(Recommended) All entrance vestibules and primary sanitary facilities maintain verified 1500mm turning diameter circles.",
                    "Door openings are minimum 930mm clear width with zero-threshold flush sills.",
                    "Accessible routes are integrated into the main public sequence rather than segregated.",
                    "PMR clearances were not explicitly drafted on this schematic plan."
                ],
                remediation_command='python "skills/spatial-anatomy/scripts/plan_compliance_engine.py" --door 930 --vestibule 1500 --corridor 1600 --output plan_1_100_pmr.svg',
                round_number=1
            ))

        dim_scores.append(DimensionScore(
            dimension_id="spatial",
            name="Spatial Anatomy & PMR Ergonomics",
            score=min(100, spatial_score),
            critique="Check corridor dead-ends and PMR turning clearance circles." if spatial_score < 75 else "Well-articulated spatial hierarchy and universal egress logic."
        ))

        # 4. Baseline Dimension 3: Environmental Rigor & Bioclimatic Flows
        has_solar = any(k in text_lower for k in ["solar", "shading", "orientation", "south-facing", "brise-soleil", "louver", "overheating", "shgc", "overhang"])
        has_ventilation = any(k in text_lower for k in ["cross-ventilation", "ventilation", "stack effect", "airflow", "thermal mass", "bioclimatic", "ladybug", "comfort"])

        enviro_score = 45
        if has_solar: enviro_score += 30
        if has_ventilation: enviro_score += 25

        enviro_traps = [t for t in detected_traps if "Environmental" in t.dimension or "Bioclimatic" in t.dimension]
        enviro_score = max(20, enviro_score - len(enviro_traps) * 15)

        if not has_solar and not any(t.trap_id == 1 for t in detected_traps):
            probes.append(ScrutinyProbe(
                persona=JuryPersona.ENVIRONMENTAL_AUDITOR,
                dimension="Environmental Performance",
                interrogation_question="You have expansive glazing on the primary facade. What is your calculated Solar Heat Gain Coefficient (SHGC), and how do you mitigate late-afternoon solar heat gain?",
                vulnerability_detected="Unprotected large-span glazing risks extreme summer solar overheating.",
                redline_fix="Integrate deep vertical exterior louvers or dynamic solar shading with calculated overhang depth D = H / tan(altitude).",
                severity=Severity.MODERATE,
                defense_options=[
                    "(Recommended) We specified triple-glazed Low-E units with an SHGC of 0.22 and deep 450mm architectural louvers.",
                    "The west facade incorporates dynamic motorized exterior louvers with automated solar tracking.",
                    "The massing uses self-shading overhangs calibrated to 45° summer solar zenith angle.",
                    "Solar loads were managed primarily via mechanical active chilled beam cooling."
                ],
                remediation_command='python "skills/bioclimatic-flows/scripts/bioclimatic_calculator.py" --zone temperate_strasbourg --output bioclimatic_plate.svg',
                round_number=2
            ))

        dim_scores.append(DimensionScore(
            dimension_id="environmental",
            name="Bioclimatic & Environmental Rigor",
            score=min(100, enviro_score),
            critique="Ground passive diagrams in orientation physics rather than generic arrows." if enviro_score < 70 else "Rigorous solar and natural airflow logic demonstrated."
        ))

        # 5. Baseline Dimension 4: Recruiter Trust Ergonomics (The 15-Second Test)
        has_passport = any(k in text_lower for k in ["passport", "project passport", "role", "scale", "location", "attribution", "individual work", "team:"])
        has_work_rights = any(k in text_lower for k in ["visa", "work rights", "citizenship", "eu citizen", "authorized", "sponsorship"])
        has_renders_only = any(k in text_lower for k in ["lumion", "enscape", "d5", "midjourney", "photorealistic render", "mood board"]) and not has_wall_section

        recruiter_score = 60
        if has_passport: recruiter_score += 20
        if has_work_rights: recruiter_score += 15
        if has_renders_only: recruiter_score -= 25

        recruiter_traps = [t for t in detected_traps if "Recruiter" in t.dimension]
        recruiter_score = max(20, recruiter_score - len(recruiter_traps) * 15)

        if not has_passport and not any(t.trap_id in [12, 13, 19, 20] for t in detected_traps):
            probes.append(ScrutinyProbe(
                persona=JuryPersona.HIRING_DIRECTOR,
                dimension="Recruiter Trust Ergonomics",
                interrogation_question="I have 15 seconds to review this portfolio. What was your exact individual line-item contribution versus the senior partner or team members?",
                vulnerability_detected="Ambiguous individual role attribution causes hiring directors to discount the project.",
                redline_fix="Place a standardized Project Passport card top-left stating exact role (e.g. 'Lead Envelope Detailer & Permitting Documentation').",
                severity=Severity.CRITICAL,
                defense_options=[
                    "(Recommended) I was the Lead Technical Detailer responsible for 1:20 envelope sections and BIM coordination.",
                    "I led the schematic design and spatial massing in a 3-person competition team.",
                    "I was an architectural intern handling 3D visualization, physical modeling, and diagramming.",
                    "This was an individual academic thesis project conceived and drafted entirely by me."
                ],
                remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_PASSPORT --output passport_spread.svg',
                round_number=3
            ))

        dim_scores.append(DimensionScore(
            dimension_id="recruiter",
            name="Recruiter Trust & 15-Second Ergonomics",
            score=max(20, min(100, recruiter_score)),
            critique="Ambiguous individual contribution risks screening rejection." if recruiter_score < 75 else "Clean, transparent attribution and outcome-forward passport."
        ))

        # 6. Baseline Dimension 5: Visual Communication & Swiss Grid
        has_grid = any(k in text_lower for k in ["grid", "swiss", "column", "baseline", "margin", "modular", "8-column", "12-column", "16-column"])
        has_multiscale = any(k in text_lower for k in ["macro", "meso", "micro", "site plan", "urban transect", "1:500", "1:100", "1:20", "1:5", "multi-scalar", "trifecta"])
        has_palette = any(k in text_lower for k in ["palette", "materiality", "stone", "terracotta", "timber", "swatch", "monochrome", "contrast", "granite", "travertine"])

        visual_score = 50
        if has_grid: visual_score += 20
        if has_multiscale: visual_score += 20
        if has_palette: visual_score += 15

        visual_traps = [t for t in detected_traps if "Visual" in t.dimension]
        visual_score = max(20, visual_score - len(visual_traps) * 15)

        if not has_grid and not any(t.trap_id in [10, 11, 14, 18, 21, 22] for t in detected_traps):
            probes.append(ScrutinyProbe(
                persona=JuryPersona.VISUAL_CURATOR,
                dimension="Visual Communication & Swiss Grid",
                interrogation_question="Your page layout appears chaotic and ungrounded. What modular grid system (8, 12, or 16 columns) governs your margins, baselines, and image viewports?",
                vulnerability_detected="Lack of columnar grid discipline creates cognitive friction and visual vibration.",
                redline_fix="Snap all drawing viewports, captions, and Project Passports to a strict 12-column modular Swiss grid with 16px gutters.",
                severity=Severity.MODERATE,
                defense_options=[
                    "(Recommended) The spread is structured on a strict 12-column Swiss modular grid with 5mm gutters and 4pt baseline locking.",
                    "We utilized an asymmetric 8-column layout with 35% negative space breathing room.",
                    "I used a dynamic editorial grid with varying column widths to differentiate drawings from narrative.",
                    "The layout was placed organically without a fixed underlying columnar grid."
                ],
                remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_CONSTRUCTIVE_PROOF --output swiss_grid_spread.svg',
                round_number=3
            ))

        if not has_multiscale and not any(t.trap_id == 14 for t in detected_traps):
            probes.append(ScrutinyProbe(
                persona=JuryPersona.VISUAL_CURATOR,
                dimension="Multi-Scalar Hierarchy",
                interrogation_question="You have a scalar disconnect between your site concept and perspective. Where is the intermediate meso-scale plan and micro-scale 1:20 assembly detail?",
                vulnerability_detected="Absence of multi-scalar drawing progression fails to prove buildability.",
                redline_fix="Deploy the Trust Trifecta on every project case study: Macro context (1:500) + Meso floor plan (1:100) + Micro detail (1:20/1:5).",
                severity=Severity.CRITICAL,
                defense_options=[
                    "(Recommended) I have the complete Trust Trifecta: 1:500 urban context, 1:100 statutory plan, and 1:20 assembly detail.",
                    "I have the 1:100 floor plan and can insert the 1:20 detail section into the next spread.",
                    "This project was focused purely on macro-urban territorial analysis and transit infrastructure.",
                    "I omitted the 1:20 detail because I wanted to emphasize the atmospheric interior perspective."
                ],
                remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_CONSTRUCTIVE_PROOF --output trifecta_spread.svg',
                round_number=3
            ))

        if any(k in text_lower for k in ["without white space", "no white space", "dense text", "wall of text", "crowded spread"]):
            probes.append(ScrutinyProbe(
                persona=JuryPersona.VISUAL_CURATOR,
                dimension="Visual Breathing Room & Negative Space",
                interrogation_question="Your spreads suffer from extreme visual crowding with no negative space. Why is there no breathing room for reviewers to absorb technical drawings?",
                vulnerability_detected="Lack of minimum 35% negative space creates cognitive fatigue in portfolio reviewers.",
                redline_fix="Re-allocate spread real estate to preserve at least 35% intentional white space breathing room.",
                severity=Severity.CRITICAL,
                defense_options=[
                    "(Recommended) We re-structured the layout with 38% intentional white space breathing room on an asymmetric 12-column Swiss grid.",
                    "We split the dense project across two facing pages to improve visual pacing.",
                    "We reduced secondary text blocks to 3-line curatorial summaries to give drawings room to breathe.",
                    "The layout was designed to pack maximum content into limited page limits."
                ],
                remediation_command='python "skills/spatial-stitch/scripts/spatial_stitch.py" generate --archetype THE_MONOGRAPH_SPREAD --output airy_spread.svg',
                round_number=3
            ))

        dim_scores.append(DimensionScore(
            dimension_id="visual",
            name="Swiss Typographic & Grid Precision",
            score=min(100, visual_score),
            critique="Adopt strict Swiss grid discipline and multi-scalar drawing progression." if visual_score < 75 else "Excellent layout discipline, negative space breathing room, and typographic hierarchy."
        ))

        # 7. Add Typology-Specific Probe
        all_defenses_typo = [typo_profile.recommended_defense] + typo_profile.alternative_defenses
        probes.append(ScrutinyProbe(
            persona=JuryPersona.CONSTRUCTIVE_LEAD if "constructive" in typo_profile.dimension_weight_adjustments else JuryPersona.SPATIAL_CHAIR,
            dimension=f"Typology Verification ({typo_profile.title})",
            interrogation_question=typo_profile.typology_probe,
            vulnerability_detected=f"Failure to demonstrate mastery of {typo_profile.title} statutory requirements ({typo_profile.primary_code_reference}).",
            redline_fix=typo_profile.recommended_defense.replace("(Recommended) ", "CAD FIX: "),
            severity=Severity.CRITICAL,
            defense_options=all_defenses_typo,
            remediation_command=typo_profile.remediation_command,
            round_number=1
        ))

        # 8. Filter probes by persona if requested
        if persona == JuryPersona.CONSTRUCTIVE_LEAD:
            active_probes = [p for p in probes if p.persona == JuryPersona.CONSTRUCTIVE_LEAD]
        elif persona == JuryPersona.HIRING_DIRECTOR:
            active_probes = [p for p in probes if p.persona == JuryPersona.HIRING_DIRECTOR]
        elif persona == JuryPersona.SPATIAL_CHAIR:
            active_probes = [p for p in probes if p.persona == JuryPersona.SPATIAL_CHAIR]
        elif persona == JuryPersona.ENVIRONMENTAL_AUDITOR:
            active_probes = [p for p in probes if p.persona == JuryPersona.ENVIRONMENTAL_AUDITOR]
        elif persona == JuryPersona.VISUAL_CURATOR:
            active_probes = [p for p in probes if p.persona == JuryPersona.VISUAL_CURATOR]
        else:
            active_probes = probes

        # Sort probes: FATAL first, then CRITICAL, then MODERATE
        sev_rank = {Severity.FATAL: 0, Severity.CRITICAL: 1, Severity.MODERATE: 2, Severity.MINOR: 3}
        active_probes.sort(key=lambda p: sev_rank.get(p.severity, 4))

        # Calculate Overall Score & Verdict
        overall = int(sum(d.score for d in dim_scores) / len(dim_scores))
        
        # Penalize overall score if FATAL traps present
        fatal_count = sum(1 for p in active_probes if p.severity == Severity.FATAL)
        if fatal_count > 0:
            overall = min(64, overall)

        if overall >= 85:
            verdict = "STRONG HIRE / ADVANCE TO NEXT ROUND"
            takeaway = f"Exceptional {typo_profile.title} presentation. Demonstrates tectonic proof, code rigor, and Swiss grid discipline."
            seal = "PASSED TRIBUNAL // STRONG HIRE"
        elif overall >= 70:
            verdict = "CONDITIONAL PASS / ADDRESS WEAK SPOTS"
            takeaway = f"Promising {typo_profile.title} concept, but vulnerable on technical constructibility and 1:20 detailing."
            seal = "CONDITIONAL // REDLINE AMENDMENTS"
        elif has_renders_only or fatal_count > 0 or constructive_score < 50:
            verdict = "RENDER TRAP ALERT / SUSPECT CONSTRUCTIBILITY"
            takeaway = f"Fatal render trap detected in {typo_profile.title}. Insufficient constructive evidence for partner review."
            seal = "RENDER TRAP ALERT // REWORK REQUIRED"
        else:
            verdict = "REWORK REQUIRED / STRENGTHEN TECHNICAL PROOF"
            takeaway = "Fundamental omissions in thermal integrity, PMR clearances, grid discipline, or role transparency."
            seal = "REWORK REQUIRED"

        remedies = [p.redline_fix for p in active_probes[:4]]
        next_prompt = active_probes[0].interrogation_question if active_probes else "Walk me through how your structural column grid informs the interior ceiling plenum."

        return GrillReport(
            verdict=verdict,
            overall_score=overall,
            dimension_scores=dim_scores,
            top_vulnerabilities=active_probes,
            defense_remedies=remedies,
            next_crit_prompt=next_prompt,
            recruiter_15s_takeaway=takeaway,
            typology=typology.value,
            pre_defense_score=overall,
            redline_markups=redlines,
            audit_seal=seal,
            current_round=current_round
        )

    def get_ask_question_payload(
        self,
        report: GrillReport,
        max_questions: int = 3,
        round_num: Optional[int] = None
    ) -> dict:
        """
        Generates an exact payload formatted for the `ask_question` tool.
        Directly matches Antigravity /grill-me multi-choice interrogation modal schema:
          {"questions": [{"question": "...", "options": [...], "is_multi_select": false}]}
        """
        # Filter probes by round if specified
        if round_num is not None:
            candidate_probes = [p for p in report.top_vulnerabilities if getattr(p, "round_number", 1) == round_num]
            if not candidate_probes:
                candidate_probes = report.top_vulnerabilities
        else:
            candidate_probes = report.top_vulnerabilities

        questions = []
        for v in candidate_probes[:max_questions]:
            persona_label = v.persona.value.replace("_", " ").title() if hasattr(v.persona, "value") else str(v.persona)
            opts = [opt.strip() for opt in v.defense_options if opt and opt.strip()]
            if len(opts) < 2:
                opts = [
                    "(Recommended) We resolved this detailing in our Stage 3 technical tender package.",
                    "This was an early conceptual competition scheme where detailing was deferred to execution phase."
                ]
            cleaned_opts = [re.sub(r"^(\d+[\.\)]|\([a-z0-9]+\))\s*", "", o) for o in opts]
            if cleaned_opts and not cleaned_opts[0].startswith("(Recommended)"):
                cleaned_opts[0] = f"(Recommended) {cleaned_opts[0]}"
            questions.append({
                "question": f"[{persona_label}] {v.interrogation_question}",
                "options": cleaned_opts[:4],
                "is_multi_select": False
            })
        return {"questions": questions}

    def evaluate_defense(self, base_report: GrillReport, user_answers: dict) -> GrillReport:
        """
        Re-scores a design based on the user's interactive defense responses.
        Awards up to +25 points per defended dimension if the response demonstrates tectonic/spatial/environmental rigor.
        Penalizes or maintains flags if answers are evasive or defer to 'early conceptual phase'.
        """
        updated_scores = []
        answers_str = " ".join(str(v) for v in user_answers.values()).lower()

        # Check for evasive keywords
        is_evasive = any(k in answers_str for k in ["conceptual competition", "deferred to", "early concept", "not explicitly drafted", "treated conceptually"])

        for dim in base_report.dimension_scores:
            score = dim.score
            critique = dim.critique
            
        # Check for rigorous technical solutions
        has_rigorous_defense = any(k in answers_str for k in [
            "schöck", "isokorb", "mineral wool", "epdm", "1:20", "curtain wall", 
            "chassis", "stringer", "flitch", "screw piles", "aerolam", "damp-proof", "plinth",
            "shgc", "louvers", "overhang", "tracking", "low-e", "0.22", "1500mm", "turning"
        ])

        for dim in base_report.dimension_scores:
            score = dim.score
            critique = dim.critique
            
            if dim.dimension_id == "constructive":
                if any(k in answers_str for k in [
                    "schöck", "isokorb", "mineral wool", "epdm", "1:20", "curtain wall", 
                    "chassis", "stringer", "flitch", "screw piles", "aerolam", "damp-proof", "plinth"
                ]):
                    gain = 25 if is_evasive else 35
                    score = min(100, score + gain)
                    critique = "Vigorously defended: Constructive detailing, structural load paths, and thermal breaks verified."
            elif dim.dimension_id == "spatial":
                if any(k in answers_str for k in ["1500mm", "turning", "930mm", "flush sill", "integrated", "travel distance", "far", "net-to-gross"]):
                    gain = 22 if is_evasive else 30
                    score = min(100, score + gain)
                    critique = "Vigorously defended: Universal PMR/ADA accessibility and statutory egress verified."
            elif dim.dimension_id == "environmental":
                if any(k in answers_str for k in ["shgc", "louvers", "overhang", "tracking", "low-e", "0.22", "stack", "rt60", "sylomer"]):
                    gain = 22 if is_evasive else 35
                    score = min(100, score + gain)
                    critique = "Vigorously defended: Solar heat gain, ventilation aerodynamics, and acoustic buffers quantified."
            elif dim.dimension_id == "recruiter":
                if any(k in answers_str for k in ["lead", "responsible", "individual", "thesis", "attribution", "passport", "sanitized"]) or (has_rigorous_defense and not is_evasive):
                    gain = 20 if is_evasive else 25
                    score = min(100, score + gain)
                    critique = "Vigorously defended: Transparent individual attribution and outcome-forward passport verified."
            elif dim.dimension_id == "visual":
                if any(k in answers_str for k in ["swiss", "12-column", "8-column", "trifecta", "1:500", "scalable vector", "wcag", "7:1", "full bleed"]) or (has_rigorous_defense and not is_evasive):
                    gain = 18 if is_evasive else 22
                    score = min(100, score + gain)
                    critique = "Vigorously defended: Typographic grid discipline, negative space, and multi-scalar progression established."
            
            updated_scores.append(DimensionScore(
                dimension_id=dim.dimension_id,
                name=dim.name,
                score=score,
                critique=critique,
                pre_score=dim.score
            ))

        overall = int(sum(d.score for d in updated_scores) / len(updated_scores))
        
        if overall >= 80 or (has_rigorous_defense and not is_evasive and overall >= 70):
            verdict = "STRONG HIRE / ADVANCE TO NEXT ROUND (DEFENSE ACCEPTED)"
            takeaway = "Jury tribunal convinced. Socratic defense proved constructive rigor, building physics mastery, and professional attribution."
            seal = "PASSED TRIBUNAL // DEFENSE ACCEPTED"
        elif overall >= 60 or (has_rigorous_defense and not is_evasive):
            verdict = "CONDITIONAL PASS / SUBMIT REDLINE AMENDMENTS (DEFENSE ACCEPTED)"
            takeaway = "Passable defense. Socratic defense accepted, but tangible drawings must be inserted into drawing sheets."
            seal = "CONDITIONAL // DEFENSE ACCEPTED"
        else:
            verdict = "REWORK REQUIRED / SKEPTICAL JURY"
            takeaway = "Defense failed to satisfy critical statutory, constructive, or accessibility concerns."
            seal = "REWORK REQUIRED"

        return GrillReport(
            verdict=verdict,
            overall_score=overall,
            dimension_scores=updated_scores,
            top_vulnerabilities=base_report.top_vulnerabilities,
            defense_remedies=base_report.defense_remedies,
            next_crit_prompt="Defense cycle complete. Ensure all verbal concessions are drafted into your drawing sheets.",
            recruiter_15s_takeaway=takeaway,
            typology=base_report.typology,
            pre_defense_score=base_report.overall_score,
            redline_markups=base_report.redline_markups,
            audit_seal=seal,
            current_round=base_report.current_round + 1
        )

    def generate_svg_stamp(
        self,
        report: GrillReport,
        output_path: Optional[str] = None,
        project_title: str = "ARCHITECTURAL DESIGN SUBMISSION"
    ) -> str:
        """Generates a publication-grade 16:9 vector SVG Socratic Crit Sheet."""
        return generate_crit_stamp_svg(
            report=report,
            output_path=output_path,
            project_title=project_title,
            typology_str=report.typology
        )
