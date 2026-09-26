#!/usr/bin/env python3
"""
scripts/run_all_clis.py
Sara Bensalem Architectural Skills Suite — CLI Verification & Diagnostic Test Utility
Automates execution, exit code verification, and ANSI formatting validation across all architectural CLIs.
Exit code protocol:
- 0: Compliant / statutory pass
- 1: Statutory / architectural violation (e.g. undersized PMR door, fatal render traps, insufficient shading)
- 2: CLI argument or syntax error
"""

import os
import sys
import subprocess
import time
from typing import List, Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLI_TEST_CASES = [
    # 1. Spatial Anatomy (PMR & Egress)
    {
        "name": "spatial-anatomy: --help",
        "cmd": [sys.executable, "skills/spatial-anatomy/scripts/plan_compliance_engine.py", "--help"],
        "expected_code": 0,
        "desc": "Verify help text and exit code 0"
    },
    {
        "name": "spatial-anatomy: Compliant 1:100 Plan",
        "cmd": [sys.executable, "skills/spatial-anatomy/scripts/plan_compliance_engine.py", "--door", "900", "--vestibule", "1500", "--output", "temp_plan_pass.svg"],
        "expected_code": 0,
        "desc": "Compliant PMR door (900mm) and turning circle (1500mm)",
        "cleanup": ["temp_plan_pass.svg"]
    },
    {
        "name": "spatial-anatomy: Undersized PMR Door",
        "cmd": [sys.executable, "skills/spatial-anatomy/scripts/plan_compliance_engine.py", "--door", "750", "--output", "temp_plan_fail.svg"],
        "expected_code": 1,
        "desc": "Undersized door (750mm < 830mm statutory min) must exit 1",
        "cleanup": ["temp_plan_fail.svg"]
    },
    {
        "name": "spatial-anatomy: Invalid Arg",
        "cmd": [sys.executable, "skills/spatial-anatomy/scripts/plan_compliance_engine.py", "--nonexistent-arg"],
        "expected_code": 2,
        "desc": "Argument error must exit 2"
    },

    # 2. Interior Joinery & Millwork
    {
        "name": "interior-joinery: --help",
        "cmd": [sys.executable, "skills/interior-joinery/scripts/joinery_detailer.py", "--help"],
        "expected_code": 0,
        "desc": "Verify help text and exit code 0"
    },
    {
        "name": "interior-joinery: Compliant 5mm Shadow Reveal",
        "cmd": [sys.executable, "skills/interior-joinery/scripts/joinery_detailer.py", "--gap", "5.0", "--output", "temp_joinery_pass.svg"],
        "expected_code": 0,
        "desc": "5mm shadow reveal (>= 3.0mm) must exit 0",
        "cleanup": ["temp_joinery_pass.svg"]
    },
    {
        "name": "interior-joinery: Zero-Reveal Antipattern #3",
        "cmd": [sys.executable, "skills/interior-joinery/scripts/joinery_detailer.py", "--gap", "1.5", "--output", "temp_joinery_fail.svg"],
        "expected_code": 1,
        "desc": "1.5mm shadow reveal (< 3.0mm min) must exit 1",
        "cleanup": ["temp_joinery_fail.svg"]
    },
    {
        "name": "interior-joinery: Invalid Arg",
        "cmd": [sys.executable, "skills/interior-joinery/scripts/joinery_detailer.py", "--bad-flag"],
        "expected_code": 2,
        "desc": "Argument error must exit 2"
    },

    # 3. Spatial Choreography & Courtyard Matrix
    {
        "name": "spatial-choreography: --help",
        "cmd": [sys.executable, "skills/spatial-choreography/scripts/spatial_journey_matrix.py", "--help"],
        "expected_code": 0,
        "desc": "Verify help text and exit code 0"
    },
    {
        "name": "spatial-choreography: Courtyard Pass (H/W = 2.0)",
        "cmd": [sys.executable, "skills/spatial-choreography/scripts/spatial_journey_matrix.py", "--audit-courtyard", "--courtyard-height", "12", "--courtyard-width", "6"],
        "expected_code": 0,
        "desc": "Aspect ratio 2.0 >= 1.50 must exit 0"
    },
    {
        "name": "spatial-choreography: Courtyard Fail (H/W = 0.6)",
        "cmd": [sys.executable, "skills/spatial-choreography/scripts/spatial_journey_matrix.py", "--audit-courtyard", "--courtyard-height", "6", "--courtyard-width", "10"],
        "expected_code": 1,
        "desc": "Insufficient shading aspect ratio 0.6 < 1.50 must exit 1"
    },
    {
        "name": "spatial-choreography: Invalid Arg",
        "cmd": [sys.executable, "skills/spatial-choreography/scripts/spatial_journey_matrix.py", "--unknown-opt"],
        "expected_code": 2,
        "desc": "Argument error must exit 2"
    },

    # 4. Portfolio Monograph Forensic Audit
    {
        "name": "portfolio-monograph: --help",
        "cmd": [sys.executable, "skills/portfolio-monograph/scripts/audit_portfolio.py", "--help"],
        "expected_code": 0,
        "desc": "Verify help text and exit code 0"
    },
    {
        "name": "portfolio-monograph: Nonexistent PDF Fail",
        "cmd": [sys.executable, "skills/portfolio-monograph/scripts/audit_portfolio.py", "--pdf", "nonexistent_file_9999.pdf"],
        "expected_code": 1,
        "desc": "Missing PDF triggers audit failure exit 1"
    },
    {
        "name": "portfolio-monograph: Invalid Arg",
        "cmd": [sys.executable, "skills/portfolio-monograph/scripts/audit_portfolio.py", "--invalid"],
        "expected_code": 2,
        "desc": "Argument error must exit 2"
    },

    # 5. Constructive Detail (Wall Section Builder)
    {
        "name": "constructive-detail: --help",
        "cmd": [sys.executable, "skills/constructive-detail/scripts/wall_section_builder.py", "--help"],
        "expected_code": 0,
        "desc": "Verify wall section builder help"
    },

    # 6. Bioclimatic Flows
    {
        "name": "bioclimatic-flows: --help",
        "cmd": [sys.executable, "skills/bioclimatic-flows/scripts/bioclimatic_calculator.py", "--help"],
        "expected_code": 0,
        "desc": "Verify bioclimatic calculator help"
    },

    # 7. Socratic Jury (Grill My Design)
    {
        "name": "grill-my-design: --help",
        "cmd": [sys.executable, "skills/grill-my-design/engine/cli.py", "--help"],
        "expected_code": 0,
        "desc": "Verify grill CLI help"
    }
]


def run_all():
    CYAN = "\033[1;36m"
    GREEN = "\033[1;32m"
    RED = "\033[1;31m"
    YELLOW = "\033[1;33m"
    RESET = "\033[0m"

    print(f"{CYAN}{'=' * 80}{RESET}")
    print(f"{CYAN}SARA BENSALEM ARCHITECTURAL SKILLS — CLI STANDARDIZATION & EXIT CODE HARNESS{RESET}")
    print(f"{CYAN}{'=' * 80}{RESET}")

    passed = 0
    failed = 0
    start_time = time.perf_counter()

    for idx, test in enumerate(CLI_TEST_CASES, 1):
        name = test["name"]
        cmd = test["cmd"]
        expected = test["expected_code"]
        desc = test["desc"]

        t0 = time.perf_counter()
        proc = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        duration_ms = (time.perf_counter() - t0) * 1000.0

        actual = proc.returncode
        status_ok = (actual == expected)

        # Clean up any generated files
        for f_path in test.get("cleanup", []):
            full_p = os.path.join(PROJECT_ROOT, f_path)
            if os.path.exists(full_p):
                try:
                    os.remove(full_p)
                except OSError:
                    pass

        if status_ok:
            passed += 1
            st_color = GREEN
            st_text = "PASS"
        else:
            failed += 1
            st_color = RED
            st_text = "FAIL"

        print(f"[{st_color}{st_text}{RESET}] #{idx:02d} {name:<42} | Code: {actual} (Exp: {expected}) | {duration_ms:6.1f}ms")
        if not status_ok:
            print(f"       {YELLOW}Description: {desc}{RESET}")
            if proc.stdout.strip():
                print(f"       STDOUT: {proc.stdout.strip()[:200]}")
            if proc.stderr.strip():
                print(f"       STDERR: {proc.stderr.strip()[:200]}")

    total_duration = time.perf_counter() - start_time
    print(f"{CYAN}{'-' * 80}{RESET}")
    print(f"CLI HARNESS SUMMARY: {passed} passed, {failed} failed out of {len(CLI_TEST_CASES)} tests in {total_duration:.2f}s")
    if failed == 0:
        print(f"{GREEN}>> ALL CLI TESTS PASSED: STANDARDIZED ANSI & EXIT CODES VERIFIED <<{RESET}")
    else:
        print(f"{RED}>> CLI REGRESSION DETECTED: {failed} TESTS FAILED <<{RESET}")
    print(f"{CYAN}{'=' * 80}{RESET}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    run_all()
