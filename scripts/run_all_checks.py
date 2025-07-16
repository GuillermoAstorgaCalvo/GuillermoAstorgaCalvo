#!/usr/bin/env python3
"""
Run all code quality tools: ruff, black, and mypy.
Prints a summary and exits with nonzero code if any tool fails.
"""
import subprocess
import sys
from error_handling import get_logger

# Set up logging for this module
logger = get_logger(__name__)

TOOLS = [
    ("ruff (lint)", ["ruff", "check", "."]),
    ("black (check)", ["black", "--check", "."]),
    ("mypy", ["mypy", "."]),
]


def run_tool(name: str, cmd: list[str]) -> int:
    logger.info(f"\n=== Running {name} ===")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        logger.info(f"{name}: PASS")
    else:
        logger.error(f"{name}: FAIL (exit code {result.returncode})")
    return result.returncode


def main() -> None:
    failures = 0
    for name, cmd in TOOLS:
        rc = run_tool(name, cmd)
        if rc != 0:
            failures += 1
    logger.info("\n=== Summary ===")
    if failures == 0:
        logger.info("All checks passed! 🎉")
    else:
        logger.error(f"{failures} check(s) failed.")
    sys.exit(failures)


if __name__ == "__main__":
    main()
