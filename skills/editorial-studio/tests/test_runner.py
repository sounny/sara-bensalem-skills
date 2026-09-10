#!/usr/bin/env python3
"""
tests/test_runner.py
Standalone, executable Python test runner for editorial-studio publishing system.
Supports --tier {all,tier1,tier2,tier3,tier4}, --json <report.json>, and formatted CLI output.
"""

import sys
import os
import time
import json
import argparse
import unittest
from datetime import datetime, timezone

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

TIER_DIRECTORIES = {
    "tier1": os.path.join(PROJECT_ROOT, "tests", "tier1_features"),
    "tier2": os.path.join(PROJECT_ROOT, "tests", "tier2_boundaries"),
    "tier3": os.path.join(PROJECT_ROOT, "tests", "tier3_combinations"),
    "tier4": os.path.join(PROJECT_ROOT, "tests", "tier4_workloads"),
    "tier5": os.path.join(PROJECT_ROOT, "tests", "tier5_adversarial"),
}

TIER_DISPLAY_NAMES = {
    "tier1": "Tier 1 (Features)",
    "tier2": "Tier 2 (Boundaries)",
    "tier3": "Tier 3 (Combinations)",
    "tier4": "Tier 4 (Workloads)",
    "tier5": "Tier 5 (Adversarial Hardening)",
}

class DetailedTestResult(unittest.TestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append(test)


def run_tier(tier_key: str, verbose: bool = False) -> dict:
    """Discovers and executes tests within a specific tier directory."""
    tier_dir = TIER_DIRECTORIES[tier_key]
    if not os.path.isdir(tier_dir):
        return {
            "tier": tier_key,
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "duration_s": 0.0,
            "failures_details": []
        }

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=tier_dir, pattern="test_*.py", top_level_dir=PROJECT_ROOT)
    result = DetailedTestResult()

    start_time = time.perf_counter()
    suite.run(result)
    duration = time.perf_counter() - start_time

    failures_details = []
    for test, err in result.failures:
        failures_details.append({
            "type": "FAILURE",
            "test": str(test),
            "traceback": err
        })
    for test, err in result.errors:
        failures_details.append({
            "type": "ERROR",
            "test": str(test),
            "traceback": err
        })

    return {
        "tier": tier_key,
        "total": result.testsRun,
        "passed": len(result.successes),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "duration_s": round(duration, 3),
        "failures_details": failures_details
    }


def main():
    parser = argparse.ArgumentParser(
        description="editorial-studio E2E Multi-Tier Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--tier",
        choices=["all", "tier1", "tier2", "tier3", "tier4", "tier5", "1", "2", "3", "4", "5"],
        default="all",
        help="Test tier to execute (default: all)"
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        default=None,
        help="Path to output JSON test report"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    tier_alias = {
        "1": "tier1", "2": "tier2", "3": "tier3", "4": "tier4", "5": "tier5",
        "tier1": "tier1", "tier2": "tier2", "tier3": "tier3", "tier4": "tier4", "tier5": "tier5",
        "all": "all"
    }
    resolved_tier = tier_alias.get(args.tier, args.tier)
    selected_tiers = (
        ["tier1", "tier2", "tier3", "tier4"]
        if resolved_tier == "all"
        else [resolved_tier]
    )

    print("=" * 80)
    print(f" EDITORIAL-STUDIO PUBLISHING SYSTEM -- E2E TEST RUNNER")
    print(f" Target Tier: {args.tier.upper()} | Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 80)

    overall_start = time.perf_counter()
    tier_results = {}
    total_run = 0
    total_passed = 0
    total_failed = 0
    total_errors = 0
    total_skipped = 0
    all_failures = []

    for tier_key in selected_tiers:
        display_name = TIER_DISPLAY_NAMES.get(tier_key, tier_key)
        if args.verbose:
            print(f"--> Executing {display_name}...")
        res = run_tier(tier_key, verbose=args.verbose)
        tier_results[tier_key] = res
        total_run += res["total"]
        total_passed += res["passed"]
        total_failed += res["failed"]
        total_errors += res["errors"]
        total_skipped += res["skipped"]
        all_failures.extend(res["failures_details"])

    overall_duration = time.perf_counter() - overall_start

    # Format CLI table
    print(f"{'Tier':<25} {'Total':>7} {'Passed':>8} {'Failed':>8} {'Errors':>8} {'Skipped':>9} {'Duration':>10}")
    print("-" * 80)
    for tier_key in selected_tiers:
        r = tier_results[tier_key]
        dname = TIER_DISPLAY_NAMES.get(tier_key, tier_key)
        print(f"{dname:<25} {r['total']:>7} {r['passed']:>8} {r['failed']:>8} {r['errors']:>8} {r['skipped']:>9} {r['duration_s']:>9.2f}s")
    print("-" * 80)
    print(f"{'TOTAL':<25} {total_run:>7} {total_passed:>8} {total_failed:>8} {total_errors:>8} {total_skipped:>9} {overall_duration:>9.2f}s")
    print("=" * 80)

    is_clean_pass = (total_failed == 0 and total_errors == 0 and total_run > 0)
    status_str = "PASS" if is_clean_pass else "FAIL"
    exit_code = 0 if is_clean_pass else 1

    if all_failures:
        print("\nFAILURE & ERROR DETAILS:")
        print("=" * 80)
        for idx, f in enumerate(all_failures, 1):
            print(f"[{f['type']} {idx}] {f['test']}")
            print(f['traceback'])
            print("-" * 80)

    print(f"\nOVERALL RESULT: {status_str} (Exit Code {exit_code})")
    print("=" * 80)

    if args.json_output:
        report_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tier_requested": args.tier,
            "status": status_str,
            "exit_code": exit_code,
            "total": total_run,
            "passed": total_passed,
            "failed": total_failed,
            "errors": total_errors,
            "skipped": total_skipped,
            "duration_seconds": round(overall_duration, 3),
            "tier_summary": tier_results,
            "failures": all_failures
        }
        json_path = os.path.abspath(args.json_output)
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(report_data, jf, indent=2)
        print(f"Test report exported to JSON: {json_path}")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
