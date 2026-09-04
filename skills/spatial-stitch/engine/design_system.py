"""
design_system.py - Ingests and compiles PORTFOLIO_DESIGN.md into EditorialTokens
"""

import re
from typing import Dict
from .models import EditorialTokens


class EditorialDesignSystemManager:
    def __init__(self):
        self.systems: Dict[str, EditorialTokens] = {
            "ds_swiss_standard": EditorialTokens(name="Swiss Monograph Standard"),
            "ds_alpine_quietude": EditorialTokens(
                name="Alpine Stone Quietude",
                paper_color="#F4F1EA",
                ink_color="#181B1E",
                accent_color="#C87D55",
                accent_secondary="#2C4D56"
            ),
            "ds_titanium_monochrome": EditorialTokens(
                name="Dark Titanium Atelier",
                paper_color="#0D0F12",
                ink_color="#F5F7FA",
                ink_secondary="#8E99A8",
                accent_color="#FFAF01",
                accent_secondary="#4E95FF",
                grid_line_color="#222831"
            )
        }

    def parse_design_md(self, content: str) -> EditorialTokens:
        tokens = EditorialTokens()
        hex_matches = re.findall(r'#([A-Fa-f0-9]{6})', content)
        if len(hex_matches) >= 1:
            tokens.paper_color = f"#{hex_matches[0]}"
        if len(hex_matches) >= 2:
            tokens.ink_color = f"#{hex_matches[1]}"
        if len(hex_matches) >= 3:
            tokens.accent_color = f"#{hex_matches[2]}"

        col_match = re.search(r'(\b8\b|\b12\b|\b16\b)\s*columns?', content, re.IGNORECASE)
        if col_match:
            tokens.column_count = int(col_match.group(1))

        margin_match = re.search(r'margin[:\s]+(\d+)', content, re.IGNORECASE)
        if margin_match:
            tokens.margin_px = int(margin_match.group(1))

        return tokens

    def get(self, system_id: str) -> EditorialTokens:
        return self.systems.get(system_id, self.systems["ds_swiss_standard"])

    def register(self, system_id: str, tokens: EditorialTokens):
        self.systems[system_id] = tokens
