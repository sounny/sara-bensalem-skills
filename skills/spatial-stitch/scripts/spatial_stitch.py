#!/usr/bin/env python3
"""
spatial_stitch.py - Unified Standalone CLI for Spatial Stitch Engine
Generates publication-ready vector spreads, performs 100-point anti-render-trap audits,
and produces creative variants without requiring an MCP server.
"""

import sys
import os
import argparse
from pathlib import Path

# Add engine directory to sys.path
engine_dir = Path(__file__).resolve().parent.parent / "engine"
if str(engine_dir) not in sys.path:
    sys.path.insert(0, str(engine_dir))

from models import (
    CanvasFormat,
    LayoutArchetype,
    CreativeRange,
    ProjectPassport,
    SpreadInstance
)
from spread_generator import SpreadGenerator
from auditor import PortfolioAuditor
from variant_engine import VariantEngine
from design_system import EditorialDesignSystemManager


def main():
    parser = argparse.ArgumentParser(
        description="Spatial Stitch - Architectural Monograph & Spread Generator CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Command: generate
    gen_parser = subparsers.add_parser("generate", help="Generate a publication-ready vector spread")
    gen_parser.add_argument(
        "--archetype", "-a",
        default="THE_CONSTRUCTIVE_PROOF",
        choices=[a.name for a in LayoutArchetype],
        help="Layout archetype"
    )
    gen_parser.add_argument(
        "--format", "-f",
        default="LANDSCAPE_16_9",
        choices=[f.name for f in CanvasFormat],
        help="Canvas format"
    )
    gen_parser.add_argument("--title", "-t", default="Pavillon Tectonique", help="Project title")
    gen_parser.add_argument("--location", "-l", default="Strasbourg, France", help="Project location")
    gen_parser.add_argument("--role", "-r", default="Lead Envelope Architect", help="Candidate role")
    gen_parser.add_argument("--prompt", "-p", default="Tectonic wall section and facade assembly", help="Design description")
    gen_parser.add_argument("--output", "-o", default="spread.svg", help="Output file path (.svg or .html)")

    # Command: audit
    audit_parser = subparsers.add_parser("audit", help="Run 100-point anti-render-trap audit on an SVG spread")
    audit_parser.add_argument("svg_file", help="Path to SVG spread file")

    # Command: archetypes
    subparsers.add_parser("archetypes", help="List the 10 layout archetypes")

    args = parser.parse_args()

    if not args.command or args.command == "archetypes":
        print("=" * 70)
        print("SPATIAL STITCH -- THE 10 ARCHITECTURAL LAYOUT ARCHETYPES")
        print("=" * 70)
        for i, arch in enumerate(LayoutArchetype, 1):
            print(f"[{i:02d}] {arch.name:<30} -> {arch.value}")
        print("=" * 70)
        return

    if args.command == "generate":
        generator = SpreadGenerator()
        auditor = PortfolioAuditor()
        fmt = CanvasFormat[args.format]
        arch = LayoutArchetype[args.archetype]

        passport = ProjectPassport(
            title=args.title,
            location=args.location,
            role=args.role,
            year="2026",
            typology="Cultural / Civic Architecture",
            scale_notations="1:20 / 1:100"
        )

        spread = generator.generate(
            project_id="cli_proj",
            prompt=args.prompt,
            archetype=arch,
            format=fmt,
            passport=passport,
            spread_number=1,
            act_number=4
        )

        audit = auditor.audit(spread, passport)
        out_path = Path(args.output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if out_path.suffix.lower() == ".html":
            out_path.write_text(spread.html_content, encoding="utf-8")
        else:
            out_path.write_text(spread.svg_content, encoding="utf-8")

        print(f"[+] Spread generated successfully: {out_path}")
        print(f"[+] Format: {fmt.name} ({fmt.value})")
        print(f"[+] Archetype: {arch.name}")
        print(f"[+] Sara Bensalem 100-Point Audit Score: {audit.total_score}/100")
        for sc in audit.category_scores:
            print(f"    - {sc.category_name}: {sc.awarded_points}/{sc.max_points}")

    elif args.command == "audit":
        p = Path(args.svg_file).resolve()
        if not p.exists():
            print(f"[-] Error: file not found {p}")
            sys.exit(1)
        svg_content = p.read_text(encoding="utf-8")
        auditor = PortfolioAuditor()
        spread = SpreadInstance(
            spread_id="audit_cli",
            project_id="cli",
            title=p.stem,
            archetype=LayoutArchetype.THE_CONSTRUCTIVE_PROOF,
            format=CanvasFormat.LANDSCAPE_16_9,
            svg_content=svg_content,
            html_content=""
        )
        audit = auditor.audit(spread)
        print("=" * 70)
        print(f"PORTFOLIO AUDIT REPORT FOR: {p.name}")
        print(f"OVERALL SCORE: {audit.total_score}/100")
        print("=" * 70)
        for sc in audit.category_scores:
            print(f"  * {sc.category_name:<40} {sc.awarded_points:>3}/{sc.max_points}")
        if audit.critical_failures:
            print("\nCRITICAL FAILURES:")
            for cf in audit.critical_failures:
                print(f"  [!] {cf}")
        if audit.constructive_remediations:
            print("\nRECOMMENDED TECTONIC REMEDIATIONS:")
            for rem in audit.constructive_remediations:
                print(f"  [+] {rem}")
        print("=" * 70)


if __name__ == "__main__":
    main()
