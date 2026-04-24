#!/usr/bin/env python3
# visualization/run_all.py
"""
Generate animated GIFs for all WOPBS scenarios.

Usage:
    python visualization/run_all.py
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path when run as a script
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from visualization.animate import animate_scenario
from visualization.scenarios import get_scenarios
from wocbs.models import AgentRoute, Vertex


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    scenarios = get_scenarios()
    print(f"Running {len(scenarios)} scenarios...\n")

    generated = 0
    for scenario in scenarios:
        animate_scenario(scenario, output_dir)
        generated += 1

    print(f"\nDone. {generated} GIF(s) saved to output/")


if __name__ == "__main__":
    main()
