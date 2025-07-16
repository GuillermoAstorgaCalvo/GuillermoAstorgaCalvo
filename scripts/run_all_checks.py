#!/usr/bin/env python3
"""
Run all code quality tools: ruff, black, and mypy.
Prints a summary and exits with nonzero code if any tool fails.
"""
import subprocess
import sys

TOOLS = [
    ("ruff (lint)", ["ruff", "check", "."]),
    ("black (check)", ["black", "--check", "."]),
    ("mypy", ["mypy", "."]),
]


def run_tool(name: str, cmd: list[str]) -> int:
    print(f"\n=== Running {name} ===")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"{name}: PASS")
    else:
        print(f"{name}: FAIL (exit code {result.returncode})")
    return result.returncode


def main() -> None:
    failures = 0
    for name, cmd in TOOLS:
        rc = run_tool(name, cmd)
        if rc != 0:
            failures += 1
    print("\n=== Summary ===")
    if failures == 0:
        print("All checks passed! 🎉")
    else:
        print(f"{failures} check(s) failed.")
    sys.exit(failures)


if __name__ == "__main__":
    main()
