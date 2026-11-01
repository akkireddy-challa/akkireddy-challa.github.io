#!/usr/bin/env python3
"""
E2E Test Runner for akkireddy-challa.github.io
Opaque-box, requirement-driven E2E test runner covering Tiers 1-4.
Zero external dependencies (uses standard Python library).
"""

import sys
import os
import argparse
import json
import time
from typing import List, Dict, Any

# Ensure target repo root and tests module are in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from tests.tier1_feature_tests import Tier1FeatureTests
from tests.tier2_boundary_tests import Tier2BoundaryTests
from tests.tier3_interaction_tests import Tier3InteractionTests
from tests.tier4_scenario_tests import Tier4ScenarioTests

class Color:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    DIM = '\033[2m'

def colorize(text: str, color_code: str, enable: bool = True) -> str:
    if not enable or not sys.stdout.isatty():
        return text
    return f"{color_code}{text}{Color.RESET}"

def run_tests(repo_root: str, tier: str = 'all', verbose: bool = False, json_output: bool = False) -> int:
    start_time = time.time()
    all_results: List[Dict[str, Any]] = []

    print(colorize(f"\n========================================================", Color.CYAN))
    print(colorize(f"  E2E Test Suite Runner — Portfolio Redesign (akkireddy-challa.github.io)", Color.BOLD))
    print(colorize(f"  Target Repository: {repo_root}", Color.DIM))
    print(colorize(f"========================================================\n", Color.CYAN))

    # Tier 1
    if tier in ('all', '1'):
        t1 = Tier1FeatureTests(repo_root)
        t1_results = t1.run_all()
        all_results.extend(t1_results)

    # Tier 2
    if tier in ('all', '2'):
        t2 = Tier2BoundaryTests(repo_root)
        t2_results = t2.run_all()
        all_results.extend(t2_results)

    # Tier 3
    if tier in ('all', '3'):
        t3 = Tier3InteractionTests(repo_root)
        t3_results = t3.run_all()
        all_results.extend(t3_results)

    # Tier 4
    if tier in ('all', '4'):
        t4 = Tier4ScenarioTests(repo_root)
        t4_results = t4.run_all()
        all_results.extend(t4_results)

    duration = time.time() - start_time

    # Group by tier
    tiers = {1: [], 2: [], 3: [], 4: []}
    for r in all_results:
        tiers[r['tier']].append(r)

    tier_names = {
        1: "Tier 1: Feature Coverage (16 Features)",
        2: "Tier 2: Boundary & Corner Cases",
        3: "Tier 3: Cross-Feature Interactions",
        4: "Tier 4: Real-World Application Scenarios"
    }

    # Print results per tier
    for t_idx, t_name in tier_names.items():
        results_in_tier = tiers[t_idx]
        if not results_in_tier:
            continue

        passed = sum(1 for r in results_in_tier if r['passed'])
        total = len(results_in_tier)
        pct = (passed / total * 100) if total > 0 else 0.0

        header_color = Color.GREEN if passed == total else Color.YELLOW
        print(colorize(f"\n--- {t_name} [{passed}/{total} Passed ({pct:.1f}%)] ---", header_color + Color.BOLD))

        for r in results_in_tier:
            if r['passed']:
                if verbose:
                    status_badge = colorize("[PASS]", Color.GREEN)
                    print(f"  {status_badge} {r['test_id']} - {r['name']}")
                    print(colorize(f"         {r['message']}", Color.DIM))
            else:
                status_badge = colorize("[FAIL]", Color.RED + Color.BOLD)
                print(f"  {status_badge} {r['test_id']} - {r['name']}")
                print(colorize(f"         Reason: {r['message']}", Color.RED))

    # Overall Summary
    total_all = len(all_results)
    passed_all = sum(1 for r in all_results if r['passed'])
    failed_all = total_all - passed_all
    overall_pct = (passed_all / total_all * 100) if total_all > 0 else 0.0

    print(colorize(f"\n========================================================", Color.CYAN))
    print(colorize(f"  TEST EXECUTION SUMMARY", Color.BOLD))
    print(colorize(f"========================================================", Color.CYAN))
    print(f"  Total Test Cases : {total_all}")
    print(f"  Passed           : {colorize(str(passed_all), Color.GREEN if passed_all == total_all else Color.YELLOW)}")
    print(f"  Failed / Pending : {colorize(str(failed_all), Color.RED if failed_all > 0 else Color.GREEN)}")
    print(f"  Pass Rate        : {overall_pct:.1f}%")
    print(f"  Duration         : {duration:.3f}s")
    print(colorize(f"========================================================\n", Color.CYAN))

    # JSON export if requested
    report_data = {
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'repo_root': repo_root,
        'duration_seconds': round(duration, 3),
        'summary': {
            'total': total_all,
            'passed': passed_all,
            'failed': failed_all,
            'pass_percentage': round(overall_pct, 1)
        },
        'tier_breakdown': {
            f"tier_{t}": {
                'total': len(tiers[t]),
                'passed': sum(1 for r in tiers[t] if r['passed']),
                'failed': len(tiers[t]) - sum(1 for r in tiers[t] if r['passed'])
            } for t in (1, 2, 3, 4) if tiers[t]
        },
        'tests': all_results
    }

    report_path = os.path.join(repo_root, 'tests', 'e2e_report.json')
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
    except Exception as e:
        pass

    if json_output:
        print(json.dumps(report_data, indent=2))

    return 0 if failed_all == 0 else 1

def main():
    parser = argparse.ArgumentParser(description="Opaque-box E2E test runner for portfolio redesign")
    parser.add_argument('--repo-root', default=REPO_ROOT, help="Absolute or relative path to target repository")
    parser.add_argument('--tier', choices=['all', '1', '2', '3', '4'], default='all', help="Specific test tier to run")
    parser.add_argument('-v', '--verbose', action='store_true', help="Print verbose output including passed tests")
    parser.add_argument('--json', action='store_true', help="Output machine-readable JSON to stdout")

    args = parser.parse_args()
    target_repo = os.path.abspath(args.repo_root)

    exit_code = run_tests(target_repo, tier=args.tier, verbose=args.verbose, json_output=args.json)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
