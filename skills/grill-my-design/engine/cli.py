"""
CLI Runner for Grill My Design
Usage: python -m engine.cli "project description or portfolio text"
"""
import sys
import os
import json

try:
    from .critique_engine import GrillEngine
    from .models import JuryPersona
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from critique_engine import GrillEngine
    from models import JuryPersona

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2:
        print("Usage: python -m engine.cli \"<design statement or portfolio text>\"")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    engine = GrillEngine()
    report = engine.grill(text)

    print("=" * 72)
    print(" 🏛️  GRILL MY DESIGN — SOCRATIC CRITIQUE REPORT")
    print(' Sara Bensalem Studio • Strasbourg Atelier [48°35\'05"N 07°45\'02"E]')
    print("=" * 72)
    print(f"VERDICT:       {report.verdict}")
    print(f"OVERALL SCORE: {report.overall_score} / 100")
    print(f"15s TAKEAWAY:  {report.recruiter_15s_takeaway}")
    print("-" * 72)
    print("📊 DIMENSION SCORES:")
    for d in report.dimension_scores:
        bar = "█" * int(d.score / 10) + "░" * (10 - int(d.score / 10))
        print(f"  • {d.name:<36} [{bar}] {d.score:>3}/100")
        print(f"    {d.critique}")
    print("-" * 72)
    print("🔥 TOP SOCRATIC INTERROGATION QUESTIONS:")
    for idx, v in enumerate(report.top_vulnerabilities, 1):
        print(f"  [{idx}] [{v.severity.value}] {v.interrogation_question}")
        print(f"      Vulnerability: {v.vulnerability_detected}")
        print(f"      Redline Fix:   {v.redline_fix}")
    print("-" * 72)
    print(f"⚡ NEXT CRIT DEFENSE PROMPT:")
    print(f"   \"{report.next_crit_prompt}\"")
    print("=" * 72)

if __name__ == "__main__":
    main()
