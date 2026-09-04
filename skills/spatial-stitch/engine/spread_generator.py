"""
spread_generator.py - Generates Complete Publication-Ready Vector Spreads (SVG & HTML5)
"""

import html
from .models import (
    SpreadInstance,
    LayoutArchetype,
    CanvasFormat,
    EditorialTokens,
    ProjectPassport
)
from .grid_system import SwissGridCalculator


class SpreadGenerator:
    def __init__(self, tokens: EditorialTokens = None):
        self.tokens = tokens or EditorialTokens()

    def generate(
        self,
        project_id: str,
        prompt: str,
        archetype: LayoutArchetype = LayoutArchetype.THE_CONSTRUCTIVE_PROOF,
        format: CanvasFormat = CanvasFormat.LANDSCAPE_16_9,
        passport: ProjectPassport = None,
        spread_number: int = 1,
        act_number: int = 4
    ) -> SpreadInstance:
        passport = passport or ProjectPassport()
        calc = SwissGridCalculator(format=format, tokens=self.tokens)
        w, h = calc.width, calc.height

        if archetype == LayoutArchetype.THE_CONSTRUCTIVE_PROOF:
            svg = self._render_constructive_proof_svg(calc, passport, prompt)
            title = "Plate IV: 1:20 Constructive Wall Section & Envelope Detailing"
            subtitle = f"{passport.title} • Technical Documentation"
        elif archetype == LayoutArchetype.THE_PASSPORT:
            svg = self._render_passport_svg(calc, passport, prompt)
            title = f"{passport.title} • Project Dossier & Passport"
            subtitle = "Act 1: Thesis & Individual Attribution"
        elif archetype == LayoutArchetype.THE_SPATIAL_ANATOMY:
            svg = self._render_spatial_anatomy_svg(calc, passport, prompt)
            title = "Plate III: 1:100 Ground Floor Spatial Anatomy & Threshold Circulation"
            subtitle = "Act 3: Scaled Floor Plan & Accessibility Clearances"
        elif archetype == LayoutArchetype.THE_ENVIRONMENTAL_ENGINE:
            svg = self._render_environmental_engine_svg(calc, passport, prompt)
            title = "Plate II: Bioclimatic Microclimate Modeling & Environmental Flows"
            subtitle = "Act 2: Diurnal Cross-Ventilation & Solar Exposure"
        elif archetype == LayoutArchetype.THE_TECTONIC_TRIPTYCH:
            svg = self._render_tectonic_triptych_svg(calc, passport, prompt)
            title = "Plate V: 1:5 Bespoke Joinery Details & Material Triptych"
            subtitle = "Act 5: Tactile Millwork & Scenography"
        else:
            svg = self._render_constructive_proof_svg(calc, passport, prompt)
            title = f"Plate: {archetype.value}"
            subtitle = "Architectural Presentation Plate"

        html_markup = (
            f'<article class="spatial-spread {format.value.lower()}" data-archetype="{archetype.value}">\n'
            f'    <header class="spread-folio-header">\n'
            f'        <span class="folio-proj">{html.escape(passport.title)}</span>\n'
            f'        <span class="folio-act">Act {act_number} / 5</span>\n'
            f'        <span class="folio-coords">{html.escape(passport.coordinates)}</span>\n'
            f'    </header>\n'
            f'    <div class="spread-viewport">\n{svg}\n</div>\n'
            f'    <footer class="spread-folio-footer">\n'
            f'        <span class="folio-attribution">Role: {html.escape(passport.candidate_role)}</span>\n'
            f'        <span class="folio-rights">{html.escape(passport.work_rights_status)}</span>\n'
            f'        <span class="folio-number">{spread_number:02d}</span>\n'
            f'    </footer>\n'
            f'</article>'
        )

        return SpreadInstance(
            project_id=project_id,
            spread_number=spread_number,
            act_number=act_number,
            archetype=archetype,
            title=title,
            subtitle=subtitle,
            format=format,
            width=w,
            height=h,
            prompt=prompt,
            svg_content=svg,
            html_content=html_markup
        )

    def _render_constructive_proof_svg(self, calc: SwissGridCalculator, passport: ProjectPassport, prompt: str) -> str:
        w, h = calc.width, calc.height
        t = self.tokens
        left_box = calc.get_column_rect(0, 4, 120, h - 240)
        right_box = calc.get_column_rect(4, 8, 120, h - 240)

        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:{t.paper_color}; font-family:{t.font_family_body};">\n'
            f'    <text x="{calc.margin}" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}" letter-spacing="1">PROJECT PASSPORT: {html.escape(passport.title).upper()}</text>\n'
            f'    <text x="{w - calc.margin}" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.accent_color}" font-weight="600" text-anchor="end">ACT 4 // CONSTRUCTIVE PROOF (1:20)</text>\n'
            f'    <line x1="{calc.margin}" y1="64" x2="{w - calc.margin}" y2="64" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'    <g transform="translate({left_box["x"]}, {left_box["y"]})">\n'
            f'        <text x="0" y="24" font-family="{t.font_family_display}" font-size="22" font-weight="700" fill="{t.ink_color}">1:20 Wall Section Detail</text>\n'
            f'        <text x="0" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}">SCALE 1:20 @ A3 // DIMENSIONS IN MM</text>\n'
            f'        <g transform="translate(0, 80)">\n'
            f'            <rect x="0" y="0" width="24" height="24" fill="{t.accent_color}" />\n'
            f'            <text x="12" y="16" font-family="{t.font_family_mono}" font-size="11" font-weight="bold" fill="{t.paper_color}" text-anchor="middle">01</text>\n'
            f'            <text x="36" y="12" font-size="13" font-weight="600" fill="{t.ink_color}">Breton Granite Ashlar (180mm)</text>\n'
            f'            <text x="36" y="28" font-size="11" fill="{t.ink_secondary}">Consolidated lime mortar joints, pointing repointing</text>\n'
            f'        </g>\n'
            f'        <g transform="translate(0, 140)">\n'
            f'            <rect x="0" y="0" width="24" height="24" fill="{t.ink_color}" />\n'
            f'            <text x="12" y="16" font-family="{t.font_family_mono}" font-size="11" font-weight="bold" fill="{t.paper_color}" text-anchor="middle">02</text>\n'
            f'            <text x="36" y="12" font-size="13" font-weight="600" fill="{t.ink_color}">Lime-Hemp Biotamping (140mm)</text>\n'
            f'            <text x="36" y="28" font-size="11" fill="{t.ink_secondary}">Hygrothermal breathable insulation, λ = 0.076 W/m·K</text>\n'
            f'        </g>\n'
            f'        <g transform="translate(0, 200)">\n'
            f'            <rect x="0" y="0" width="24" height="24" fill="{t.accent_secondary}" />\n'
            f'            <text x="12" y="16" font-family="{t.font_family_mono}" font-size="11" font-weight="bold" fill="{t.paper_color}" text-anchor="middle">03</text>\n'
            f'            <text x="36" y="12" font-size="13" font-weight="600" fill="{t.ink_color}">Thermal Break & EPDM Flashing</text>\n'
            f'            <text x="36" y="28" font-size="11" fill="{t.ink_secondary}">Continuous moisture seal at foundation-wall interface</text>\n'
            f'        </g>\n'
            f'        <g transform="translate(0, 260)">\n'
            f'            <rect x="0" y="0" width="24" height="24" fill="{t.ink_color}" />\n'
            f'            <text x="12" y="16" font-family="{t.font_family_mono}" font-size="11" font-weight="bold" fill="{t.paper_color}" text-anchor="middle">04</text>\n'
            f'            <text x="36" y="12" font-size="13" font-weight="600" fill="{t.ink_color}">Oak Glulam Post & Beam (160x280)</text>\n'
            f'            <text x="36" y="28" font-size="11" fill="{t.ink_secondary}">Concealed steel plate flitch connector w/ dowels</text>\n'
            f'        </g>\n'
            f'        <g transform="translate(0, {left_box["height"] - 140})">\n'
            f'            <rect x="0" y="0" width="{left_box["width"]}" height="120" fill="{t.grid_line_color}" fill-opacity="0.3" stroke="{t.grid_line_color}" />\n'
            f'            <text x="16" y="28" font-family="{t.font_family_mono}" font-size="10" font-weight="bold" fill="{t.accent_color}">CONSTRUCTIVE PROOF GUARANTEE</text>\n'
            f'            <text x="16" y="48" font-size="12" fill="{t.ink_color}">Individual Line-Item Work: Envelope detailing &</text>\n'
            f'            <text x="16" y="66" font-size="12" fill="{t.ink_color}">construction administration documentation.</text>\n'
            f'            <text x="16" y="94" font-family="{t.font_family_mono}" font-size="10" fill="{t.ink_secondary}">ANTI-RENDER-TRAP COMPLIANT • 100% BUILDABLE</text>\n'
            f'        </g>\n'
            f'    </g>\n'
            f'    <g transform="translate({right_box["x"]}, {right_box["y"]})">\n'
            f'        <rect x="0" y="0" width="{right_box["width"]}" height="{right_box["height"]}" fill="#FFFFFF" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'        <rect x="140" y="520" width="800" height="120" fill="#EAE6DF" stroke="{t.ink_color}" stroke-width="{t.line_cut_px}" />\n'
            f'        <line x1="150" y1="550" x2="930" y2="550" stroke="{t.ink_secondary}" stroke-width="1" stroke-dasharray="8 6" />\n'
            f'        <line x1="150" y1="610" x2="930" y2="610" stroke="{t.ink_secondary}" stroke-width="1" stroke-dasharray="8 6" />\n'
            f'        <rect x="140" y="40" width="160" height="480" fill="#DFD9D0" stroke="{t.ink_color}" stroke-width="{t.line_cut_px}" />\n'
            f'        <line x1="140" y1="120" x2="300" y2="120" stroke="{t.ink_color}" stroke-width="1" />\n'
            f'        <line x1="140" y1="200" x2="300" y2="200" stroke="{t.ink_color}" stroke-width="1" />\n'
            f'        <line x1="140" y1="280" x2="300" y2="280" stroke="{t.ink_color}" stroke-width="1" />\n'
            f'        <line x1="140" y1="360" x2="300" y2="360" stroke="{t.ink_color}" stroke-width="1" />\n'
            f'        <line x1="140" y1="440" x2="300" y2="440" stroke="{t.ink_color}" stroke-width="1" />\n'
            f'        <rect x="300" y="40" width="100" height="480" fill="#F4EFE6" stroke="{t.ink_color}" stroke-width="{t.line_medium_px}" stroke-dasharray="4 2" />\n'
            f'        <rect x="400" y="40" width="20" height="480" fill="{t.paper_color}" stroke="{t.ink_color}" stroke-width="{t.line_thin_px}" />\n'
            f'        <rect x="420" y="160" width="480" height="240" fill="#E8F1F5" fill-opacity="0.4" stroke="{t.accent_secondary}" stroke-width="{t.line_medium_px}" />\n'
            f'        <line x1="420" y1="280" x2="900" y2="280" stroke="{t.accent_secondary}" stroke-width="2" />\n'
            f'        <text x="660" y="270" font-family="{t.font_family_mono}" font-size="11" fill="{t.accent_secondary}" text-anchor="middle">TRIPLE GLAZED UNITS // Uw = 0.78 W/m²K</text>\n'
            f'        <g stroke="{t.accent_color}" stroke-width="1.2">\n'
            f'            <line x1="90" y1="40" x2="90" y2="520" />\n'
            f'            <line x1="80" y1="40" x2="100" y2="40" />\n'
            f'            <line x1="80" y1="520" x2="100" y2="520" />\n'
            f'        </g>\n'
            f'        <text x="75" y="290" font-family="{t.font_family_mono}" font-size="12" font-weight="bold" fill="{t.accent_color}" text-anchor="middle" transform="rotate(-90 75 290)">4800 MM</text>\n'
            f'    </g>\n'
            f'    <line x1="{calc.margin}" y1="{h - 56}" x2="{w - calc.margin}" y2="{h - 56}" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'    <text x="{calc.margin}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}">LEAD ARCHITECT: {html.escape(passport.candidate_role).upper()}</text>\n'
            f'    <text x="{w / 2}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}" text-anchor="middle">{html.escape(passport.work_rights_status).upper()}</text>\n'
            f'    <text x="{w - calc.margin}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="12" font-weight="bold" fill="{t.ink_color}" text-anchor="end">SPREAD 04</text>\n'
            f'</svg>'
        )
        return svg

    def _render_passport_svg(self, calc: SwissGridCalculator, passport: ProjectPassport, prompt: str) -> str:
        w, h = calc.width, calc.height
        t = self.tokens
        left_box = calc.get_column_rect(0, 5, 120, h - 240)
        right_box = calc.get_column_rect(5, 7, 120, h - 240)

        items_html = ""
        y_pos = 120
        for label, val in [
            ("PROJECT", passport.title),
            ("TYPOLOGY", passport.typology),
            ("LOCATION", f"{passport.location} ({passport.coordinates})"),
            ("STAGE", passport.stage),
            ("GROSS AREA", passport.area),
            ("TEAM SCALE", f"{passport.team_size} Architects"),
            ("CANDIDATE ROLE", passport.candidate_role),
            ("WORK RIGHTS", passport.work_rights_status)
        ]:
            items_html += (
                f'<g transform="translate(0, {y_pos})">\n'
                f'    <text x="0" y="0" font-family="{t.font_family_mono}" font-size="10" font-weight="600" fill="{t.ink_secondary}" letter-spacing="1">{label}</text>\n'
                f'    <text x="0" y="18" font-family="{t.font_family_display}" font-size="13" font-weight="600" fill="{t.ink_color}">{html.escape(str(val))}</text>\n'
                f'    <line x1="0" y1="28" x2="{left_box["width"]}" y2="28" stroke="{t.grid_line_color}" stroke-width="0.75" />\n'
                f'</g>\n'
            )
            y_pos += 44

        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:{t.paper_color}; font-family:{t.font_family_body};">\n'
            f'    <text x="{calc.margin}" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}">MONOGRAPH DOSSIER // VOL. 01</text>\n'
            f'    <text x="{w - calc.margin}" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.accent_color}" font-weight="bold" text-anchor="end">ACT 1 // THE HOOK & PROJECT PASSPORT</text>\n'
            f'    <line x1="{calc.margin}" y1="64" x2="{w - calc.margin}" y2="64" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'    <g transform="translate({left_box["x"]}, {left_box["y"]})">\n'
            f'        <text x="0" y="32" font-family="{t.font_family_display}" font-size="34" font-weight="800" fill="{t.ink_color}">{html.escape(passport.title)}</text>\n'
            f'        <text x="0" y="64" font-size="15" fill="{t.ink_secondary}">{html.escape(passport.thesis_statement)}</text>\n'
            f'        {items_html}\n'
            f'    </g>\n'
            f'    <g transform="translate({right_box["x"]}, {right_box["y"]})">\n'
            f'        <rect x="0" y="0" width="{right_box["width"]}" height="{right_box["height"]}" fill="#FFFFFF" stroke="{t.grid_line_color}" />\n'
            f'        <path d="M 0,200 Q 250,150 500,220 T 1000,180" fill="none" stroke="{t.grid_line_color}" stroke-width="1.5" />\n'
            f'        <path d="M 0,260 Q 300,200 600,280 T 1000,240" fill="none" stroke="{t.grid_line_color}" stroke-width="1.5" />\n'
            f'        <rect x="250" y="160" width="420" height="260" fill="#F4F1EB" stroke="{t.ink_color}" stroke-width="{t.line_cut_px}" />\n'
            f'        <polygon points="250,160 460,80 670,160" fill="#E4DEC8" stroke="{t.ink_color}" stroke-width="{t.line_cut_px}" />\n'
            f'        <text x="270" y="240" font-family="{t.font_family_mono}" font-size="14" font-weight="bold" fill="{t.accent_color}">SITE CONTEXT AXIS</text>\n'
            f'        <text x="270" y="264" font-size="12" fill="{t.ink_secondary}">Solar North: +14° azimuth orientation</text>\n'
            f'        <line x1="270" y1="280" x2="600" y2="280" stroke="{t.grid_line_color}" />\n'
            f'        <text x="270" y="304" font-size="12" fill="{t.ink_color}">Granite Envelope Restored: 680 m²</text>\n'
            f'        <text x="270" y="324" font-size="12" fill="{t.ink_color}">Glazed Contemporary Pavilion Added: 240 m²</text>\n'
            f'    </g>\n'
            f'    <line x1="{calc.margin}" y1="{h - 56}" x2="{w - calc.margin}" y2="{h - 56}" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'    <text x="{calc.margin}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}">SWISS 12-COLUMN MODULAR SYSTEM</text>\n'
            f'    <text x="{w - calc.margin}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="12" font-weight="bold" fill="{t.ink_color}" text-anchor="end">SPREAD 01</text>\n'
            f'</svg>'
        )

    def _render_spatial_anatomy_svg(self, calc: SwissGridCalculator, passport: ProjectPassport, prompt: str) -> str:
        w, h = calc.width, calc.height
        t = self.tokens
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:{t.paper_color}; font-family:{t.font_family_body};">\n'
            f'    <text x="{calc.margin}" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}">PROJECT: {html.escape(passport.title).upper()}</text>\n'
            f'    <text x="{w - calc.margin}" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.accent_color}" font-weight="bold" text-anchor="end">ACT 3 // SPATIAL ANATOMY (1:100)</text>\n'
            f'    <line x1="{calc.margin}" y1="64" x2="{w - calc.margin}" y2="64" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'    <rect x="{calc.margin}" y="100" width="{w - 2 * calc.margin}" height="{h - 200}" fill="#FFFFFF" stroke="{t.grid_line_color}" />\n'
            f'    <rect x="260" y="240" width="1380" height="520" fill="none" stroke="{t.ink_color}" stroke-width="{t.line_cut_px}" />\n'
            f'    <line x1="680" y1="240" x2="680" y2="760" stroke="{t.ink_color}" stroke-width="{t.line_cut_px}" />\n'
            f'    <line x1="1180" y1="240" x2="1180" y2="760" stroke="{t.ink_color}" stroke-width="{t.line_cut_px}" />\n'
            f'    <text x="470" y="500" font-family="{t.font_family_display}" font-size="18" font-weight="bold" fill="{t.ink_color}" text-anchor="middle">ATELIER PUBLIC / CAFE</text>\n'
            f'    <text x="470" y="524" font-family="{t.font_family_mono}" font-size="12" fill="{t.ink_secondary}" text-anchor="middle">140 m² • PMR ACCESSIBLE</text>\n'
            f'    <text x="930" y="500" font-family="{t.font_family_display}" font-size="18" font-weight="bold" fill="{t.ink_color}" text-anchor="middle">CENTRAL GLAZED CLOISTER</text>\n'
            f'    <text x="930" y="524" font-family="{t.font_family_mono}" font-size="12" fill="{t.accent_color}" font-weight="bold" text-anchor="middle">BIO-MICROCLIMATE NUCLEUS</text>\n'
            f'    <text x="1420" y="500" font-family="{t.font_family_display}" font-size="18" font-weight="bold" fill="{t.ink_color}" text-anchor="middle">VERNACULAR RESIDENCE</text>\n'
            f'    <text x="1420" y="524" font-family="{t.font_family_mono}" font-size="12" fill="{t.ink_secondary}" text-anchor="middle">180 m² • RESTORED TIMBER FRAME</text>\n'
            f'    <line x1="{calc.margin}" y1="{h - 56}" x2="{w - calc.margin}" y2="{h - 56}" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'    <text x="{calc.margin}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}">SCALE 1:100 @ A3 • ORTHOGRAPHIC SPATIAL PLAN</text>\n'
            f'    <text x="{w - calc.margin}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="12" font-weight="bold" fill="{t.ink_color}" text-anchor="end">SPREAD 03</text>\n'
            f'</svg>'
        )

    def _render_environmental_engine_svg(self, calc: SwissGridCalculator, passport: ProjectPassport, prompt: str) -> str:
        w, h = calc.width, calc.height
        t = self.tokens
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:{t.paper_color}; font-family:{t.font_family_body};">\n'
            f'    <text x="{calc.margin}" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}">MICROCLIMATE PERFORMANCE // VOL. 01</text>\n'
            f'    <text x="{w - calc.margin}" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.accent_color}" font-weight="bold" text-anchor="end">ACT 2 // ENVIRONMENTAL ENGINE</text>\n'
            f'    <line x1="{calc.margin}" y1="64" x2="{w - calc.margin}" y2="64" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'    <g transform="translate({calc.margin}, 120)">\n'
            f'        <rect x="0" y="0" width="{w - 2 * calc.margin}" height="{h - 240}" fill="#FFFFFF" stroke="{t.grid_line_color}" />\n'
            f'        <path d="M 120,680 Q 800,80 1600,680" fill="none" stroke="{t.accent_color}" stroke-width="2.5" stroke-dasharray="6 4" />\n'
            f'        <circle cx="540" cy="220" r="28" fill="{t.accent_color}" />\n'
            f'        <text x="540" y="226" font-family="{t.font_family_mono}" font-size="11" font-weight="bold" fill="{t.paper_color}" text-anchor="middle">SUMMER +68°</text>\n'
            f'        <polygon points="400,680 400,420 800,280 1200,420 1200,680" fill="#F0EDE6" stroke="{t.ink_color}" stroke-width="{t.line_cut_px}" />\n'
            f'        <g stroke="{t.accent_secondary}" stroke-width="3" fill="none">\n'
            f'            <path d="M 100,560 Q 300,540 460,520 T 780,360" />\n'
            f'            <polygon points="780,360 765,350 768,368" fill="{t.accent_secondary}" />\n'
            f'        </g>\n'
            f'        <text x="240" y="530" font-family="{t.font_family_mono}" font-size="11" font-weight="bold" fill="{t.accent_secondary}">PREVAILING S-W BREEZE (4.2 m/s)</text>\n'
            f'    </g>\n'
            f'    <line x1="{calc.margin}" y1="{h - 56}" x2="{w - calc.margin}" y2="{h - 56}" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'    <text x="{calc.margin}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}">PASSIVE SOLAR GAIN: 34% REDUCTION IN ACTIVE HEATING DEMAND</text>\n'
            f'    <text x="{w - calc.margin}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="12" font-weight="bold" fill="{t.ink_color}" text-anchor="end">SPREAD 02</text>\n'
            f'</svg>'
        )

    def _render_tectonic_triptych_svg(self, calc: SwissGridCalculator, passport: ProjectPassport, prompt: str) -> str:
        w, h = calc.width, calc.height
        t = self.tokens
        col_w = (w - 2 * calc.margin - 2 * calc.gutter) / 3
        y_top = 120
        box_h = h - 240

        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:{t.paper_color}; font-family:{t.font_family_body};">\n'
            f'    <text x="{calc.margin}" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}">TECTONIC FABRICATION // VOL. 01</text>\n'
            f'    <text x="{w - calc.margin}" y="48" font-family="{t.font_family_mono}" font-size="11" fill="{t.accent_color}" font-weight="bold" text-anchor="end">ACT 5 // 1:5 JOINERY & MATERIAL TRIPTYCH</text>\n'
            f'    <line x1="{calc.margin}" y1="64" x2="{w - calc.margin}" y2="64" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'    <g transform="translate({calc.margin}, {y_top})">\n'
            f'        <rect x="0" y="0" width="{col_w}" height="{box_h}" fill="#FFFFFF" stroke="{t.grid_line_color}" />\n'
            f'        <rect x="30" y="30" width="{col_w - 60}" height="320" fill="#D7C4A5" stroke="{t.ink_color}" stroke-width="1.5" />\n'
            f'        <text x="30" y="380" font-family="{t.font_family_display}" font-size="16" font-weight="bold" fill="{t.ink_color}">01. 8mm Shadow Reveal</text>\n'
            f'        <text x="30" y="405" font-size="12" fill="{t.ink_secondary}">Concealed Blum Clip-Top hinges w/ 2.5mm tolerance</text>\n'
            f'    </g>\n'
            f'    <g transform="translate({calc.margin + col_w + calc.gutter}, {y_top})">\n'
            f'        <rect x="0" y="0" width="{col_w}" height="{box_h}" fill="#FFFFFF" stroke="{t.grid_line_color}" />\n'
            f'        <rect x="30" y="30" width="{col_w - 60}" height="320" fill="#C2BBB0" stroke="{t.ink_color}" stroke-width="1.5" />\n'
            f'        <text x="30" y="380" font-family="{t.font_family_display}" font-size="16" font-weight="bold" fill="{t.ink_color}">02. Bush-Hammered Granite</text>\n'
            f'        <text x="30" y="405" font-size="12" fill="{t.ink_secondary}">Tactile rusticated plinth resisting ground splash-back</text>\n'
            f'    </g>\n'
            f'    <g transform="translate({calc.margin + 2 * (col_w + calc.gutter)}, {y_top})">\n'
            f'        <rect x="0" y="0" width="{col_w}" height="{box_h}" fill="#FFFFFF" stroke="{t.grid_line_color}" />\n'
            f'        <rect x="30" y="30" width="{col_w - 60}" height="320" fill="#9DA7B2" stroke="{t.ink_color}" stroke-width="1.5" />\n'
            f'        <text x="30" y="380" font-family="{t.font_family_display}" font-size="16" font-weight="bold" fill="{t.ink_color}">03. Pre-Weathered Quartz Zinc</text>\n'
            f'        <text x="30" y="405" font-size="12" fill="{t.ink_secondary}">Standing seam roof interface w/ ventilated air gap</text>\n'
            f'    </g>\n'
            f'    <line x1="{calc.margin}" y1="{h - 56}" x2="{w - calc.margin}" y2="{h - 56}" stroke="{t.grid_line_color}" stroke-width="1" />\n'
            f'    <text x="{calc.margin}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="11" fill="{t.ink_secondary}">STUDIO CRAFT & MATERIALITY DOSSIER</text>\n'
            f'    <text x="{w - calc.margin}" y="{h - 32}" font-family="{t.font_family_mono}" font-size="12" font-weight="bold" fill="{t.ink_color}" text-anchor="end">SPREAD 05</text>\n'
            f'</svg>'
        )
