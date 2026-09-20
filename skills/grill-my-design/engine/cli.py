"""
CLI Runner for Grill My Design (2026 Enhanced Edition)
Sara Bensalem Studio • Strasbourg Atelier [48°35'05"N 07°45'02"E]
Usage: python -m engine.cli --text "project description" [--svg crit_plate.svg] [--ask-questions]
"""
import sys
import os
import json
import argparse

try:
    from .critique_engine import GrillEngine
    from .models import JuryPersona
    from .typologies import ArchitecturalTypology
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from critique_engine import GrillEngine
    from models import JuryPersona
    from typologies import ArchitecturalTypology

# ANSI Terminal Color Helpers
class TermColor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    DIM = "\033[2m"

def supports_color():
    """Detects whether terminal supports ANSI color."""
    return sys.platform != "win32" or "ANSICON" in os.environ or "WT_SESSION" in os.environ or os.environ.get("TERM") == "xterm-256color"

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser(
        description="Grill My Design: Socratic Architectural Critique & Cross-Examination Tribunal"
    )
    parser.add_argument("--text", "-t", type=str, default=None, help="Design statement or portfolio text")
    parser.add_argument("--persona", "-p", choices=["full", "technical", "recruiter", "spatial", "environmental", "visual"], default="full", help="Jury persona")
    parser.add_argument("--typology", choices=[t.value for t in ArchitecturalTypology], default=None, help="Architectural typology override")
    parser.add_argument("--round", type=int, choices=[1, 2, 3], default=None, help="Interrogation round filter (1: Constructive/Code, 2: Climate/Acoustic, 3: Recruiter/Grid)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Launch interactive Socratic cross-examination loop")
    parser.add_argument("--ask-questions", action="store_true", help="Output JSON payload formatted for the ask_question tool (/grill-me parity)")
    parser.add_argument("--svg", type=str, default=None, help="Generate publication-grade 16:9 vector SVG crit sheet plate to specified path")
    parser.add_argument("--title", type=str, default="ARCHITECTURAL DESIGN SUBMISSION", help="Project title for SVG crit sheet")
    parser.add_argument("--eval-defense", type=str, default=None, help="JSON string or file of candidate defense answers to evaluate")
    parser.add_argument("--json", action="store_true", help="Output full JSON report")
    parser.add_argument("rest", nargs="*", help="Positional text tokens if --text is omitted")
    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.rest:
        text = " ".join(args.rest)
    else:
        print("Usage: python -m engine.cli --text \"<design statement>\" [--svg crit_sheet.svg] [--ask-questions] [--persona full|technical|...]")
        sys.exit(1)

    p_enum = JuryPersona.FULL_TRIBUNAL
    if args.persona == "technical": p_enum = JuryPersona.CONSTRUCTIVE_LEAD
    elif args.persona == "recruiter": p_enum = JuryPersona.HIRING_DIRECTOR
    elif args.persona == "spatial": p_enum = JuryPersona.SPATIAL_CHAIR
    elif args.persona == "environmental": p_enum = JuryPersona.ENVIRONMENTAL_AUDITOR
    elif args.persona == "visual": p_enum = JuryPersona.VISUAL_CURATOR

    engine = GrillEngine()
    report = engine.grill(
        text, 
        persona=p_enum, 
        typology_override=args.typology,
        current_round=args.round or 1
    )

    # Optional defense evaluation from JSON argument
    if args.eval_defense:
        try:
            if os.path.exists(args.eval_defense):
                with open(args.eval_defense, "r", encoding="utf-8") as f:
                    answers = json.load(f)
            else:
                answers = json.loads(args.eval_defense)
            report = engine.evaluate_defense(report, answers)
        except Exception as e:
            print(f"Warning: Failed to evaluate defense JSON: {e}", file=sys.stderr)

    # Output ask_question tool payload
    if args.ask_questions:
        payload = engine.get_ask_question_payload(report, max_questions=3, round_num=args.round)
        print(json.dumps(payload, indent=2))
        return

    # Output full JSON
    if args.json:
        dump_fn = getattr(report, "model_dump", getattr(report, "dict", None))
        print(json.dumps(dump_fn() if dump_fn else report.__dict__, indent=2))
        return

    # Generate SVG plate if requested
    if args.svg:
        svg_content = engine.generate_svg_stamp(report, output_path=args.svg, project_title=args.title)
        print(f"Generated 16:9 Socratic Crit Sheet SVG: {args.svg} ({len(svg_content)} bytes)")

    # Interactive defense terminal flow
    is_interactive = args.interactive or (sys.stdin.isatty() and not args.json and not args.ask_questions and not args.svg and not args.eval_defense)
    if is_interactive and report.top_vulnerabilities:
        print("=" * 76)
        print(" PHASE 1: JURY VULNERABILITY AUDIT COMPLETE")
        print(f" INITIAL PRE-DEFENSE VERDICT: {report.verdict} ({report.overall_score}/100)")
        print(f" DETECTED TYPOLOGY: {report.typology.upper() if report.typology else 'GENERAL'}")
        print("=" * 76)
        print("\n>>> LAUNCHING SOCRATIC CROSS-EXAMINATION DEFENSE LOOP <<<\n")
        
        user_defenses = {}
        target_probes = report.top_vulnerabilities
        if args.round is not None:
            target_probes = [p for p in target_probes if getattr(p, "round_number", 1) == args.round] or target_probes

        for idx, v in enumerate(target_probes[:4], 1):
            persona_name = v.persona.value.replace("_", " ").upper() if hasattr(v.persona, "value") else str(v.persona).upper()
            print(f"\n[PROBE {idx}/{min(4, len(target_probes))}] [{v.severity.value}] [{persona_name}]")
            print(f"QUESTION: {v.interrogation_question}")
            if v.defense_options:
                print("Available Defense Strategies:")
                for opt_idx, opt in enumerate(v.defense_options, 1):
                    print(f"  ({opt_idx}) {opt}")
                print(f"  ({len(v.defense_options)+1}) Custom write-in technical defense")
                try:
                    choice = input(f"\nSelect defense (1-{len(v.defense_options)+1}) or enter text: ").strip()
                    if choice.isdigit() and 1 <= int(choice) <= len(v.defense_options):
                        user_defenses[v.dimension] = v.defense_options[int(choice) - 1]
                    else:
                        user_defenses[v.dimension] = choice
                except (EOFError, KeyboardInterrupt):
                    break
            else:
                try:
                    ans = input("\nEnter your defense: ").strip()
                    user_defenses[v.dimension] = ans
                except (EOFError, KeyboardInterrupt):
                    break

        if user_defenses:
            print("\n>>> TRIBUNAL DELIBERATION: EVALUATING DEFENSE RIGOR... <<<\n")
            report = engine.evaluate_defense(report, user_defenses)
            if args.svg:
                engine.generate_svg_stamp(report, output_path=args.svg, project_title=args.title)
                print(f"Updated Crit Sheet SVG: {args.svg}")

    # Render Terminal Report
    use_color = supports_color()
    c_bold = TermColor.BOLD if use_color else ""
    c_reset = TermColor.RESET if use_color else ""
    c_red = TermColor.RED if use_color else ""
    c_green = TermColor.GREEN if use_color else ""
    c_yellow = TermColor.YELLOW if use_color else ""
    c_cyan = TermColor.CYAN if use_color else ""

    print("=" * 76)
    print(f"{c_bold}SARA BENSALEM STUDIO • SOCRATIC DESIGN REVIEW TRIBUNAL{c_reset}")
    print(f"{c_cyan}Strasbourg Atelier [48°35'05\"N 07°45'02\"E] • Plate 07 Audit Dossier{c_reset}")
    print("=" * 76)
    
    # Verdict display
    v_color = c_green if report.overall_score >= 85 else (c_yellow if report.overall_score >= 70 else c_red)
    print(f"VERDICT:       {v_color}{c_bold}{report.verdict}{c_reset}")
    print(f"SCORE:         {v_color}{c_bold}{report.overall_score} / 100{c_reset} (Pre-defense: {report.pre_defense_score or report.overall_score})")
    print(f"TYPOLOGY:      {report.typology.upper() if report.typology else 'GENERAL COMMERCIAL'}")
    print(f"15s TAKEAWAY:  {report.recruiter_15s_takeaway}")
    print("-" * 76)

    print(f"{c_bold}5 DIAGNOSTIC LENSES & DIMENSION SCORES:{c_reset}")
    for d in report.dimension_scores:
        score_color = c_green if d.score >= 80 else (c_yellow if d.score >= 65 else c_red)
        bar_len = int(d.score / 10)
        bar = "#" * bar_len + "-" * (10 - bar_len)
        print(f"  • {d.name:<38} [{bar}] {score_color}{d.score:>3}/100{c_reset}")
        print(f"    {d.critique}")

    print("-" * 76)
    print(f"{c_bold}TOP REDLINE MARKUPS & SOCRATIC INTERROGATION PROBES:{c_reset}")
    for idx, v in enumerate(report.top_vulnerabilities[:4], 1):
        sev_color = c_red if v.severity.value == "FATAL" else (c_yellow if v.severity.value == "CRITICAL" else c_cyan)
        trap_tag = f" [TRAP #{v.trap_id}]" if v.trap_id else ""
        print(f"  [{idx}] {sev_color}[{v.severity.value}]{c_reset}{trap_tag} {v.interrogation_question}")
        print(f"      Defect:        {v.vulnerability_detected}")
        print(f"      Redline Fix:   {v.redline_fix}")
        if v.remediation_command:
            print(f"      Tectonic CLI:  {v.remediation_command}")

    print("-" * 76)
    print(f"{c_bold}NEXT CRIT DEFENSE PROMPT:{c_reset}")
    print(f'   "{report.next_crit_prompt}"')
    print("=" * 76)

    # Standardized Exit Code: 0 = PASS (>=70 and no unaddressed fatal traps), 1 = REWORK / CODE INFRACTION
    has_unaddressed_fatal = any(v.severity.value == "FATAL" for v in report.top_vulnerabilities) and not ("ACCEPTED" in report.verdict)
    if report.overall_score < 70 or has_unaddressed_fatal:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
