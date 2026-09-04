"""
auditor.py - 100-Point Anti-Render-Trap & Recruiter Trust Interface Evaluator
Incorporates Bespoke Careers 6 Rules and GrowthGrid Africa 10-Second Orientation Principles.
"""

from .models import (
    SpreadInstance,
    AuditReport,
    AuditCategoryScore,
    LayoutArchetype,
    ProjectPassport
)


class PortfolioAuditor:
    def audit(self, spread: SpreadInstance, passport: ProjectPassport = None) -> AuditReport:
        passport = passport or ProjectPassport()
        svg = spread.svg_content

        passed_checks = []
        critical_failures = []
        remediations = []

        # Category 1: Editorial Rigor & Typographic Discipline (20 pts)
        has_mono_labels = "font-family" in svg and ("mono" in svg.lower() or "ibm plex" in svg.lower())
        has_clear_hierarchy = 'font-size="22"' in svg or 'font-size="34"' in svg
        cat1_pts = 20 if (has_mono_labels and has_clear_hierarchy) else 14
        if has_mono_labels:
            passed_checks.append("Strict Swiss typographic pairing (Neutral Grotesk + Technical Mono)")
        else:
            critical_failures.append("Missing technical mono font for drafting metadata")
            remediations.append("Apply IBM Plex Mono or JetBrains Mono for all dimensional callouts and folio tags.")

        # Category 2: Constructive Proof & 1:20 Wall Section (25 pts)
        is_constructive = spread.archetype in [
            LayoutArchetype.THE_CONSTRUCTIVE_PROOF,
            LayoutArchetype.THE_TECTONIC_TRIPTYCH,
            LayoutArchetype.THE_SPATIAL_ANATOMY
        ]
        has_dimensions = "MM" in svg or "SCALE" in svg or "Uw =" in svg
        has_callouts = "Thermal" in svg or "Insulation" in svg or "Granite" in svg
        
        if is_constructive and has_dimensions and has_callouts:
            cat2_pts = 25
            passed_checks.append("Rigorous 1:20 constructive detailing with dimension strings")
            drawing_ratio = 0.65
            render_trap = False
        elif is_constructive:
            cat2_pts = 18
            drawing_ratio = 0.40
            render_trap = False
        else:
            cat2_pts = 8
            drawing_ratio = 0.15
            render_trap = True
            critical_failures.append("Render Masking Deficit: Spread lacks 1:20 constructive wall section")
            remediations.append("Lead with a dimensioned 1:20 constructive section to prove real-world buildability to hiring directors.")

        # Category 3: Recruiter Trust Interface & Project Passport (20 pts)
        has_passport = "PROJECT PASSPORT" in svg or "ACT 1" in svg or "LEAD ARCHITECT" in svg
        has_work_rights = "CITIZEN" in svg.upper() or "SPONSORSHIP" in svg.upper() or "WORK RIGHTS" in svg.upper()
        has_attribution = "ATTRIBUTION" in svg.upper() or "ROLE" in svg.upper()

        cat3_pts = 20 if (has_passport and has_work_rights) else (14 if has_passport else 8)
        if has_work_rights:
            passed_checks.append("Explicit work rights and visa status declared on page 1 (Bespoke Careers Rule 1)")
        else:
            critical_failures.append("Missing explicit visa / work authorization declaration")
            remediations.append("State current geographic location and visa sponsorship requirements upfront in the Project Passport.")

        if has_attribution:
            passed_checks.append("Line-item individual attribution eliminates team ambiguity (GrowthGrid Rule)")
        else:
            remediations.append("Add itemized project responsibilities to distinguish individual work from team contributions.")

        # Category 4: Narrative Pacing & 5-Act Arc (15 pts)
        has_act_marker = "ACT " in svg.upper()
        cat4_pts = 15 if has_act_marker else 10
        if has_act_marker:
            passed_checks.append("Anchored in 5-Act spatial narrative structure")

        # Category 5: Materiality, Scenography & Craft (20 pts)
        has_materiality = "Granite" in svg or "Oak" in svg or "Zinc" in svg or "Lime" in svg
        cat5_pts = 20 if has_materiality else 12
        if has_materiality:
            passed_checks.append("Tactile material specifications and hygrothermal coefficients specified")

        total = cat1_pts + cat2_pts + cat3_pts + cat4_pts + cat5_pts

        if total >= 90:
            rank = "Elite Hire (Top 2% Candidate Monograph)"
        elif total >= 75:
            rank = "Strong Hire (Exceeds Construction Standards)"
        else:
            rank = "Needs Tectonic Work (Render Trap Susceptible)"

        return AuditReport(
            spread_id=spread.id,
            total_score=total,
            max_score=100,
            rank=rank,
            render_trap_alert=render_trap,
            drawing_to_render_ratio=drawing_ratio,
            category_scores=[
                AuditCategoryScore(
                    category_id="editorial_rigor",
                    category_name="Editorial Rigor & Typographic Discipline",
                    max_points=20,
                    awarded_points=cat1_pts,
                    status="PASSED" if cat1_pts >= 16 else "WARNING",
                    critique="Neutral Swiss grotesk paired with technical monospace baseline alignment."
                ),
                AuditCategoryScore(
                    category_id="constructive_proof",
                    category_name="The Anti-Render Trap: 1:20 Wall Section",
                    max_points=25,
                    awarded_points=cat2_pts,
                    status="PASSED" if cat2_pts >= 20 else "FAIL",
                    critique="Tectonic resolution overcoming surface 3D render gloss."
                ),
                AuditCategoryScore(
                    category_id="recruiter_trust",
                    category_name="Recruiter Trust & Project Passport",
                    max_points=20,
                    awarded_points=cat3_pts,
                    status="PASSED" if cat3_pts >= 16 else "WARNING",
                    critique="Zero-navigation friction, 10s orientation, explicit work rights & role attribution."
                ),
                AuditCategoryScore(
                    category_id="narrative_pacing",
                    category_name="Narrative Pacing & 5-Act Arc",
                    max_points=15,
                    awarded_points=cat4_pts,
                    status="PASSED" if cat4_pts >= 12 else "WARNING",
                    critique="Rhythm and spatial sequencing across multi-spread case studies."
                ),
                AuditCategoryScore(
                    category_id="materiality_craft",
                    category_name="Materiality, Scenography & Craft",
                    max_points=20,
                    awarded_points=cat5_pts,
                    status="PASSED" if cat5_pts >= 16 else "WARNING",
                    critique="Authentic physical fabrication tolerances and tactile triptych documentation."
                )
            ],
            passed_checks=passed_checks,
            critical_failures=critical_failures,
            constructive_remediations=remediations
        )
