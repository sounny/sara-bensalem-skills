"""
grid_system.py - Swiss Modular Grid & Coordinate Calculator for Spatial Stitch
"""

from typing import Dict
from .models import CanvasFormat, EditorialTokens


class SwissGridCalculator:
    DIMENSIONS = {
        CanvasFormat.LANDSCAPE_16_9: (1920, 1080),
        CanvasFormat.DOUBLE_A3: (1680, 595),
        CanvasFormat.PORTRAIT_A4: (1240, 1754),
        CanvasFormat.PRINT_MONOGRAPH: (1440, 960),
    }

    def __init__(self, format: CanvasFormat = CanvasFormat.LANDSCAPE_16_9, tokens: EditorialTokens = None):
        self.format = format
        self.tokens = tokens or EditorialTokens()
        self.width, self.height = self.DIMENSIONS.get(format, (1920, 1080))
        self.margin = self.tokens.margin_px
        self.gutter = self.tokens.gutter_px
        self.cols = self.tokens.column_count
        self.baseline = self.tokens.baseline_grid_pt

        usable_width = self.width - (2 * self.margin) - ((self.cols - 1) * self.gutter)
        self.col_width = usable_width / self.cols

    def get_column_rect(self, col_start: int, col_span: int, y_start: float, height: float) -> Dict[str, float]:
        x = self.margin + (col_start * (self.col_width + self.gutter))
        w = (col_span * self.col_width) + ((col_span - 1) * self.gutter)
        y_snapped = round(y_start / self.baseline) * self.baseline
        h_snapped = round(height / self.baseline) * self.baseline
        return {"x": round(x, 1), "y": round(y_snapped, 1), "width": round(w, 1), "height": round(h_snapped, 1)}

    def generate_grid_svg_layer(self) -> str:
        svg_parts = ['<g id="swiss-grid-overlay" opacity="0.4" pointer-events="none">']
        for c in range(self.cols):
            x = self.margin + (c * (self.col_width + self.gutter))
            svg_parts.append(
                f'<rect x="{x}" y="{self.margin}" width="{self.col_width}" '
                f'height="{self.height - 2 * self.margin}" fill="{self.tokens.grid_line_color}" fill-opacity="0.12" />'
            )
            svg_parts.append(
                f'<line x1="{x}" y1="0" x2="{x}" y2="{self.height}" '
                f'stroke="{self.tokens.grid_line_color}" stroke-width="0.75" stroke-dasharray="2 4" />'
            )
            svg_parts.append(
                f'<line x1="{x + self.col_width}" y1="0" x2="{x + self.col_width}" y2="{self.height}" '
                f'stroke="{self.tokens.grid_line_color}" stroke-width="0.75" stroke-dasharray="2 4" />'
            )
        svg_parts.append(
            f'<rect x="{self.margin}" y="{self.margin}" width="{self.width - 2 * self.margin}" '
            f'height="{self.height - 2 * self.margin}" fill="none" stroke="{self.tokens.accent_color}" '
            f'stroke-width="1" stroke-opacity="0.5" />'
        )
        for cx, cy in [
            (self.margin, self.margin),
            (self.width - self.margin, self.margin),
            (self.margin, self.height - self.margin),
            (self.width - self.margin, self.height - self.margin)
        ]:
            svg_parts.append(
                f'<line x1="{cx - 12}" y1="{cy}" x2="{cx + 12}" y2="{cy}" stroke="{self.tokens.accent_color}" stroke-width="1.2" />'
            )
            svg_parts.append(
                f'<line x1="{cx}" y1="{cy - 12}" x2="{cx}" y2="{cy + 12}" stroke="{self.tokens.accent_color}" stroke-width="1.2" />'
            )
            svg_parts.append(
                f'<circle cx="{cx}" cy="{cy}" r="2" fill="{self.tokens.accent_color}" />'
            )
        svg_parts.append('</g>')
        return "\n".join(svg_parts)
