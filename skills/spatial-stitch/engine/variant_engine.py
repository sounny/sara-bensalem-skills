"""
variant_engine.py - Generates REFINE, EXPLORE, and REIMAGINE variants of Spreads
"""

from typing import List
from .models import (
    SpreadInstance,
    CreativeRange,
    LayoutArchetype,
    EditorialTokens,
    ProjectPassport
)
from .spread_generator import SpreadGenerator


class VariantEngine:
    ARCHETYPE_COMPLEMENTS = {
        LayoutArchetype.THE_PASSPORT: [LayoutArchetype.THE_CARTOGRAPHIC_CONTEXT, LayoutArchetype.THE_TYPOGRAPHIC_INDEX],
        LayoutArchetype.THE_CONSTRUCTIVE_PROOF: [LayoutArchetype.THE_TECTONIC_TRIPTYCH, LayoutArchetype.THE_SPATIAL_ANATOMY],
        LayoutArchetype.THE_SPATIAL_ANATOMY: [LayoutArchetype.THE_CONSTRUCTIVE_PROOF, LayoutArchetype.THE_URBAN_TERRITORY],
        LayoutArchetype.THE_ENVIRONMENTAL_ENGINE: [LayoutArchetype.THE_CARTOGRAPHIC_CONTEXT, LayoutArchetype.THE_CONSTRUCTIVE_PROOF],
        LayoutArchetype.THE_TECTONIC_TRIPTYCH: [LayoutArchetype.THE_CONSTRUCTIVE_PROOF, LayoutArchetype.THE_SCENOGRAPHIC_SPREAD]
    }

    def __init__(self, tokens: EditorialTokens = None):
        self.tokens = tokens or EditorialTokens()
        self.generator = SpreadGenerator(tokens=self.tokens)

    def generate_variants(
        self,
        base_spread: SpreadInstance,
        passport: ProjectPassport = None,
        creative_range: CreativeRange = CreativeRange.EXPLORE,
        variant_count: int = 3
    ) -> List[SpreadInstance]:
        variants = []
        passport = passport or ProjectPassport()

        for i in range(variant_count):
            var_archetype = base_spread.archetype

            if creative_range == CreativeRange.REFINE:
                var_tokens = EditorialTokens(
                    name=f"Refined Variant {i+1}",
                    baseline_grid_pt=4,
                    column_count=16,
                    margin_px=48
                )
                gen = SpreadGenerator(tokens=var_tokens)
                var = gen.generate(
                    project_id=base_spread.project_id,
                    prompt=f"{base_spread.prompt} [Refined Swiss Baseline]",
                    archetype=var_archetype,
                    format=base_spread.format,
                    passport=passport,
                    spread_number=base_spread.spread_number,
                    act_number=base_spread.act_number
                )
                var.title = f"{base_spread.title} (Refined Variant {i+1})"
                variants.append(var)

            elif creative_range == CreativeRange.EXPLORE:
                complements = self.ARCHETYPE_COMPLEMENTS.get(
                    base_spread.archetype,
                    [LayoutArchetype.THE_CONSTRUCTIVE_PROOF, LayoutArchetype.THE_SPATIAL_ANATOMY]
                )
                target_arch = complements[i % len(complements)]
                var = self.generator.generate(
                    project_id=base_spread.project_id,
                    prompt=f"{base_spread.prompt} [Exploration: {target_arch.value}]",
                    archetype=target_arch,
                    format=base_spread.format,
                    passport=passport,
                    spread_number=base_spread.spread_number,
                    act_number=base_spread.act_number
                )
                var.title = f"Exploration: {target_arch.value} (Variant {i+1})"
                variants.append(var)

            elif creative_range == CreativeRange.REIMAGINE:
                dark_tokens = EditorialTokens(
                    name="Reimagined Dark Atelier",
                    paper_color="#090B0E",
                    ink_color="#F3EFEA",
                    ink_secondary="#7E8B9B",
                    accent_color="#FFAF01",
                    grid_line_color="#1F242D"
                )
                gen = SpreadGenerator(tokens=dark_tokens)
                var = gen.generate(
                    project_id=base_spread.project_id,
                    prompt=f"{base_spread.prompt} [Reimagined Dark Atelier]",
                    archetype=base_spread.archetype,
                    format=base_spread.format,
                    passport=passport,
                    spread_number=base_spread.spread_number,
                    act_number=base_spread.act_number
                )
                var.title = f"{base_spread.title} (Reimagined Atelier Variant)"
                variants.append(var)

        return variants
