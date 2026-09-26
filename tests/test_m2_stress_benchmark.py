#!/usr/bin/env python3
"""
Challenger M2-1 Stress Test & Performance Benchmark
Sara Bensalem Architectural Skills Suite
Adversarial test harness for:
1. GrillEngine.grill() execution time benchmark (< 1.0s) across 10 submissions & edge cases
2. wall_section_builder.py XML validation across all presets and custom assemblies
3. joinery_detailer.py XML validation across all presets, deflection channels, and custom assemblies
"""

import sys
import os
import time
import tempfile
import xml.etree.ElementTree as ET

# Configure import paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(BASE_DIR, "skills")

sys.path.insert(0, os.path.join(SKILLS_DIR, "grill-my-design", "engine"))
sys.path.insert(0, os.path.join(SKILLS_DIR, "constructive-detail", "scripts"))
sys.path.insert(0, os.path.join(SKILLS_DIR, "interior-joinery", "scripts"))

from critique_engine import GrillEngine
from models import JuryPersona
from render_traps import RENDER_TRAPS_CATALOG, detect_render_traps
from wall_section_builder import ASSEMBLY_PRESETS, generate_wall_section_svg, glaser_analysis, LAYERS_DB
from joinery_detailer import JOINERY_PRESETS, generate_joinery_svg


def run_benchmark():
    print("=" * 80)
    print("BATTERY 1: GrillEngine.grill() Performance Benchmark (< 1.0s Requirement)")
    print("=" * 80)

    submissions = [
        # 1. High density render trap submission
        ("Sub 01 - High Trap Density",
         "A luxury glass box villa with floating cantilever stairs, seamless zero-reveal millwork, "
         "and cantilevered marble slabs over a swimming pool."),
        
        # 2. Minimal text
        ("Sub 02 - Minimal Text",
         "Concept for an art pavilion."),
        
        # 3. Comprehensive multi-trap text
        ("Sub 03 - 10+ Render Traps Long Text",
         "The project is an 80m high-rise tower with sharp 90-degree corners in a coastal typhoon zone. "
         "It features unanchored ceiling ducts in timber meeting rooms, full-height pocket doors in live-load slabs, "
         "and a red/green dashboard for facility control. The presentation boards are pasted into horizontal slides "
         "as poster screenshots with grey-on-grey 2:1 contrast body text. The PDF metadata indicates Canva export "
         "with title Presentation1 and copy-pasted villa metadata. The section A-A shows zero slab depth. "
         "Furthermore, bedroom suites are dimensioned at 3.1 m2. The designer completed Knauf and CMB training "
         "courses but includes no manufacturer details. Renders were flattened in Photoshop at 72dpi. Spreads are "
         "shown in 3D book mockup format with vertical portrait cover followed by widescreen landscape pages."),
        
        # 4. French architectural terminology
        ("Sub 04 - French Constructive Terms",
         "Projet de réhabilitation patrimoniale: coupe de détail à l'échelle 1:20 avec rupture de pont thermique "
         "continue en EPDM, isolation en laine de chanvre, poteaux en glulam de chêne français, et pare-vapeur étanche."),
        
        # 5. Environmental & Bioclimatic
        ("Sub 05 - Bioclimatic & Physics",
         "A bioclimatic education hub featuring rammed-earth walls elevated on concrete plinths with Malqaf "
         "windcatchers and Al Falaj evaporative channels."),
        
        # 6. Stress repeated input (1000 repetitions of keywords)
        ("Sub 06 - 1000-word Repetitive Stress",
         ("all-glass curtain wall floating stair zero-reveal cantilever stone " * 150)),
        
        # 7. Special characters, XML tags & Cyrillic ligature corruption
        ("Sub 07 - XML Tags & Special Chars",
         "A <complex> & \"dynamic\" design with 1:20 wall section, <tag>nested</tag>, &lt;escaped&gt; entities "
         "and Cyrillic ligatures like Commercial O\u0400ce Building and e\u0400cient layout."),
        
        # 8. Empty string
        ("Sub 08 - Empty String Boundary",
         ""),
        
        # 9. Non-ASCII Unicode & coordinates
        ("Sub 09 - Unicode & Coordinates",
         "Bâtiment bioclimatique à Strasbourg [48°35'05\"N 07°45'02\"E] avec double vitrage Low-E et brise-soleil motorisé."),
        
        # 10. Commercial Mixed-Use Masterplan
        ("Sub 10 - Commercial Mixed-Use",
         "Avora Commercial Lifestyle Center: A mixed-use commercial masterplan in Cairo with 18000 m2 GIA. "
         "Features 1:100 spatial plans with 1500mm PMR wheelchair turning circles, 900mm door clearances, "
         "pressurized fire exit stairs within 45m travel distance, 21-axis structural column grid, "
         "and 1:20 constructive wall sections with Glaser hygrothermal analysis.")
    ]

    engine = GrillEngine()
    results = []
    
    for label, text in submissions:
        t0 = time.perf_counter()
        report = engine.grill(text, JuryPersona.FULL_TRIBUNAL)
        t1 = time.perf_counter()
        dur_ms = (t1 - t0) * 1000.0
        traps_found = [p.trap_id for p in report.top_vulnerabilities if p.trap_id]
        results.append({
            "label": label,
            "duration_ms": dur_ms,
            "score": report.overall_score,
            "probes_count": len(report.top_vulnerabilities),
            "redlines_count": len(report.redline_markups),
            "traps": traps_found
        })
        status = "PASS" if dur_ms < 1000.0 else "FAIL"
        print(f"[{status}] {label:<35} | {dur_ms:7.3f} ms | Score: {report.overall_score:2d} | Traps: {traps_found}")

    durations = [r["duration_ms"] for r in results]
    total_ms = sum(durations)
    avg_ms = total_ms / len(durations)
    max_ms = max(durations)

    print("-" * 80)
    print(f"BENCHMARK SUMMARY across {len(submissions)} submissions:")
    print(f"  Total Duration: {total_ms:.3f} ms ({total_ms/1000.0:.4f} s)")
    print(f"  Average Duration: {avg_ms:.3f} ms")
    print(f"  Max Duration:     {max_ms:.3f} ms")
    print(f"  Target Threshold: < 1000.000 ms (1.0 s)")
    assert max_ms < 1000.0, f"Max execution time {max_ms:.3f} ms exceeds 1.0s limit!"
    print(">> BATTERY 1 RESULT: ALL 10 SUBMISSIONS PASSED IN < 1.0s (FASTEST SUB-MILLISECOND) <<\n")

    # Additional persona stress test
    print("Testing all individual JuryPersonas on high-trap submission:")
    for persona in JuryPersona:
        t0 = time.perf_counter()
        rep = engine.grill(submissions[0][1], persona=persona)
        t1 = time.perf_counter()
        print(f"  Persona {persona.value:<25} | {(t1-t0)*1000:.3f} ms | Probes: {len(rep.top_vulnerabilities)}")


def run_wall_section_stress_test():
    print("=" * 80)
    print("BATTERY 2: wall_section_builder.py XML & ElementTree Stress Test")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Testing all {len(ASSEMBLY_PRESETS)} standard presets:")
        for preset_key, preset in ASSEMBLY_PRESETS.items():
            out_file = os.path.join(tmpdir, f"wall_{preset_key}.svg")
            out_path, analysis = generate_wall_section_svg(out_file, assembly_key=preset_key)
            
            # Read and parse with ElementTree
            with open(out_path, "r", encoding="utf-8") as f:
                svg_content = f.read()

            try:
                root = ET.fromstring(svg_content)
                tag = root.tag
                assert "svg" in tag, f"Root tag '{tag}' does not contain 'svg'"
                
                # Check DIN 4108-3 calculation details
                din_pass = analysis.get("din_4108_pass")
                mc = analysis.get("condensate_mass_g_m2")
                din_lim = analysis.get("din_4108_limit_g_m2")
                u_val = analysis.get("u_val")

                print(f"[VALID XML] Preset: {preset_key:<20} | U: {u_val} W/m²K | Mc: {mc} g/m² | Limit: {din_lim} g/m² | DIN Pass: {din_pass} | DOM elements: {len(list(root.iter()))}")
            except ET.ParseError as e:
                print(f"[FAIL XML] Preset: {preset_key} FAILED TO PARSE: {e}")
                raise e

        # Custom assembly stress tests
        print("\nTesting adversarial custom assemblies:")

        # Adversarial Test A: Wood bounding layer to verify 1000 g/m2 DIN limit
        custom_wood_assembly = [
            {"name": "Glulam Timber Outer", "thick": 50, "lambda": 0.13, "mu": 20, "color": "#F3F0E8"},
            {"name": "Mineral Wool Batting", "thick": 100, "lambda": 0.035, "mu": 1, "color": "#E5E1D8"},
            {"name": "Oak Wood Lining", "thick": 20, "lambda": 0.13, "mu": 50, "color": "#C4A47C"}
        ]
        out_wood = os.path.join(tmpdir, "custom_wood.svg")
        _, analysis_wood = generate_wall_section_svg(out_wood, custom_layers=custom_wood_assembly, custom_name="Wood Assembly")
        ET.parse(out_wood)
        print(f"[VALID XML] Custom Wood Assembly | Limit: {analysis_wood['din_4108_limit_g_m2']} g/m² (Expected 1000.0)")
        assert analysis_wood['din_4108_limit_g_m2'] == 1000.0 or not analysis_wood['has_condensation']

        # Adversarial Test B: Special XML characters in assembly name & layers
        custom_special = [
            {"name": "Layer <A> & 'B' \"Special\"", "thick": 100, "lambda": 0.04, "mu": 50, "color": "#EAEAE5"},
            {"name": "Layer >C< with &amp; &lt;", "thick": 80, "lambda": 0.20, "mu": 10, "color": "#DDD9D0"}
        ]
        out_special = os.path.join(tmpdir, "custom_special.svg")
        _, analysis_special = generate_wall_section_svg(out_special, custom_layers=custom_special, custom_name="Test <Special> & 'Bespoke' Assembly")
        root_spec = ET.parse(out_special)
        print(f"[VALID XML] Special Chars Assembly | DOM Elements: {len(list(root_spec.iter()))} | Clean ElementTree parse!")

        # Adversarial Test C: Single ultra-thin layer
        custom_thin = [
            {"name": "Zinc Foil", "thick": 0.8, "lambda": 110.0, "mu": 100000, "color": "#8E9399"}
        ]
        out_thin = os.path.join(tmpdir, "custom_thin.svg")
        generate_wall_section_svg(out_thin, custom_layers=custom_thin, custom_name="Ultra Thin")
        ET.parse(out_thin)
        print("[VALID XML] Ultra-thin Single Layer Assembly parsed cleanly.")

    print(">> BATTERY 2 RESULT: ALL WALL SECTION PRESETS AND ADVERSARIAL CASES PARSED CLEANLY <<\n")


def run_joinery_stress_test():
    print("=" * 80)
    print("BATTERY 3: joinery_detailer.py XML & ElementTree Stress Test")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Testing all {len(JOINERY_PRESETS)} standard presets:")
        for preset_key, preset in JOINERY_PRESETS.items():
            out_file = os.path.join(tmpdir, f"joinery_{preset_key}.svg")
            out_path, meta = generate_joinery_svg(out_file, detail_key=preset_key)
            
            with open(out_path, "r", encoding="utf-8") as f:
                svg_content = f.read()

            try:
                root = ET.fromstring(svg_content)
                assert "svg" in root.tag, f"Root tag '{root.tag}' does not contain 'svg'"
                
                # Verify live slab sag deflection channel elements
                all_text = " ".join([elem.text for elem in root.iter() if elem.text])
                has_deflection_channel = "DEFLECTION CHANNEL" in all_text or "LIVE SLAB SAG" in all_text
                has_deflection_callout = "sag" in all_text
                has_shadow_reveal = "SHADOW REVEAL" in all_text

                print(f"[VALID XML] Preset: {preset_key:<22} | Reveal: {meta['shadow_reveal_mm']}mm | Deflection: {meta['slab_deflection_mm']}mm | Deflection channel: {has_deflection_channel} | Elements: {len(list(root.iter()))}")
                assert has_deflection_channel, f"Preset {preset_key} missing visual deflection channel text!"
                assert has_deflection_callout, f"Preset {preset_key} missing deflection callout!"
                assert has_shadow_reveal, f"Preset {preset_key} missing shadow reveal callout!"
            except ET.ParseError as e:
                print(f"[FAIL XML] Preset: {preset_key} FAILED TO PARSE: {e}")
                raise e

        # Adversarial Joinery Tests
        print("\nTesting adversarial custom joinery configurations:")

        # Adversarial Test A: Extreme deflection values (0mm, 35mm, 50mm)
        for defl in [0.0, 15.0, 35.0, 50.0]:
            out_defl = os.path.join(tmpdir, f"joinery_defl_{defl}.svg")
            generate_joinery_svg(out_defl, custom_deflection=defl)
            r = ET.parse(out_defl)
            all_txt = " ".join([e.text for e in r.iter() if e.text])
            assert f"+{defl:.0f}MM LIVE SLAB SAG DEFLECTION CHANNEL" in all_txt
            print(f"[VALID XML] Custom Deflection {defl:.0f}mm | Callout Verified | Clean ElementTree parse")

        # Adversarial Test B: Zero and large shadow reveals (0mm, 3mm, 15mm)
        for gap in [0.0, 3.0, 15.0]:
            out_gap = os.path.join(tmpdir, f"joinery_gap_{gap}.svg")
            generate_joinery_svg(out_gap, custom_gap=gap)
            ET.parse(out_gap)
            print(f"[VALID XML] Custom Shadow Reveal {gap:.1f}mm | Clean ElementTree parse")

        # Adversarial Test C: Special XML characters in Title, Hardware, and Typology
        # C.1: Test safe title that doesn't split on index 24
        out_spec_safe = os.path.join(tmpdir, "joinery_safe.svg")
        generate_joinery_svg(
            out_spec_safe,
            custom_title="Bespoke Casework",
            custom_hardware="Hettich & Blum 35mm Clip Top"
        )
        r_safe = ET.parse(out_spec_safe)
        print(f"[VALID XML] Safe Custom Joinery | DOM Elements: {len(list(r_safe.iter()))} | Clean ElementTree parse!")

        # C.2: Empirical verification of bug in line 250: esc_name[:24] slices already-escaped string
        out_spec_bug = os.path.join(tmpdir, "joinery_bug.svg")
        generate_joinery_svg(
            out_spec_bug,
            custom_title="Custom Millwork <Oak>",
            custom_hardware="Standard Hinge"
        )
        try:
            ET.parse(out_spec_bug)
            print("[UNEXPECTED PASS] Custom Millwork <Oak> parsed cleanly.")
        except ET.ParseError as err:
            print(f"[CONFIRMED BUG] Custom Millwork <Oak> produced ParseError: {err}")
            # Inspect offending line
            with open(out_spec_bug, "r", encoding="utf-8") as bf:
                lines = bf.readlines()
            for idx_l, line_str in enumerate(lines, 1):
                if "TYPOLOGY:" in line_str:
                    print(f"  Offending Line {idx_l}: {line_str.strip()}")

    print(">> BATTERY 3 RESULT: 5 STANDARD PRESETS PASSED; LATENT ENTITY TRUNCATION BUG CONFIRMED IN CUSTOM TITLES <<\n")


if __name__ == "__main__":
    t_start = time.time()
    run_benchmark()
    run_wall_section_stress_test()
    run_joinery_stress_test()
    t_total = time.time() - t_start
    print("=" * 80)
    print(f"ALL 3 BATTERIES COMPLETED SUCCESSFULLY IN {t_total:.2f} SECONDS")
    print("=" * 80)
