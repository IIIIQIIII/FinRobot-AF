#!/usr/bin/env python3
"""
Run all FinRobot-AF tests in organized sequence.

Usage:
    python tests/run_all.py                # Run all tests
    python tests/run_all.py --unit         # Run only unit tests
    python tests/run_all.py --integration  # Run only integration tests
    python tests/run_all.py --tools        # Run only tool tests
    python tests/run_all.py --e2e          # Run only E2E tests
    python tests/run_all.py --fast         # Run unit + tool tests (fast)
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime


class TestRunner:
    """Organized test runner for FinRobot-AF."""

    def __init__(self):
        self.tests_dir = Path(__file__).parent
        self.results = {}

    def run_test(self, test_path: Path, category: str) -> bool:
        """Run a single test file."""
        print(f"\n{'=' * 80}")
        print(f"Running: {test_path.name} ({category})")
        print(f"{'=' * 80}\n")

        try:
            # Use conda environment Python directly
            python_exe = "/Users/admin/miniconda3/envs/finrobot/bin/python"

            result = subprocess.run(
                [python_exe, str(test_path)],
                cwd=self.tests_dir.parent,
                capture_output=False,
                text=True
            )

            success = result.returncode == 0
            self.results[test_path.name] = (category, success)
            return success

        except Exception as e:
            print(f"❌ Failed to run {test_path.name}: {e}")
            self.results[test_path.name] = (category, False)
            return False

    def run_category(self, category: str) -> int:
        """Run all tests in a category."""
        category_dir = self.tests_dir / category
        if not category_dir.exists():
            print(f"⚠️  Category '{category}' not found")
            return 0

        test_files = sorted(category_dir.glob("test_*.py"))
        if not test_files:
            print(f"⚠️  No tests found in '{category}'")
            return 0

        passed = 0
        for test_file in test_files:
            if self.run_test(test_file, category):
                passed += 1

        return passed

    def print_summary(self):
        """Print test results summary."""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)

        by_category = {}
        for test_name, (category, success) in self.results.items():
            if category not in by_category:
                by_category[category] = {"passed": 0, "failed": 0, "tests": []}

            if success:
                by_category[category]["passed"] += 1
            else:
                by_category[category]["failed"] += 1

            by_category[category]["tests"].append((test_name, success))

        total_passed = 0
        total_failed = 0

        for category in sorted(by_category.keys()):
            data = by_category[category]
            print(f"\n{category.upper()}:")
            for test_name, success in data["tests"]:
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"  {status}: {test_name}")

            passed = data["passed"]
            failed = data["failed"]
            total = passed + failed
            print(f"  Results: {passed}/{total} passed")

            total_passed += passed
            total_failed += failed

        print("\n" + "=" * 80)
        total = total_passed + total_failed
        print(f"OVERALL: {total_passed}/{total} tests passed")
        print("=" * 80 + "\n")

        if total_passed == total:
            print("🎉 All tests passed!")
            return 0
        else:
            print(f"⚠️  {total_failed} test(s) failed")
            return 1


def main():
    """Main test runner."""
    import argparse

    parser = argparse.ArgumentParser(description="Run FinRobot-AF tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--tools", action="store_true", help="Run tool tests only")
    parser.add_argument("--e2e", action="store_true", help="Run E2E tests only")
    parser.add_argument("--fast", action="store_true", help="Run fast tests (unit + tools)")

    args = parser.parse_args()

    print("=" * 80)
    print("FINROBOT-AF TEST SUITE")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    runner = TestRunner()

    # Determine which tests to run
    if args.unit:
        categories = ["unit"]
    elif args.integration:
        categories = ["integration"]
    elif args.tools:
        categories = ["tools"]
    elif args.e2e:
        categories = ["e2e"]
    elif args.fast:
        categories = ["unit", "tools"]
    else:
        # Run all tests in order
        categories = ["unit", "tools", "integration", "e2e"]

    # Run tests
    for category in categories:
        runner.run_category(category)

    # Print summary
    return runner.print_summary()


if __name__ == "__main__":
    sys.exit(main())
