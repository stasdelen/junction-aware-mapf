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
from wopbs.models import AgentRoute, Vertex


def v(x: int, y: int) -> Vertex:
    return Vertex(x, y)


def r(agent_id: int, coords, release: int = 0) -> AgentRoute:
    return AgentRoute(agent_id, [v(*c) for c in coords], release_time=release)


def get_scenarios():
    return [
        {
            "name": "1_parallel_paths",
            "description": "2 agents on non-intersecting parallel paths — zero delay baseline",
            "routes": [
                r(0, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]),
                r(1, [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]),
            ],
            "max_time_ticks": 8,
            "safety_gap": 1,
            "disappear_at_goal": False,
        }
    ]


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
