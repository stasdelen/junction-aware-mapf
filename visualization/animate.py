# visualization/animate.py
from pathlib import Path
from typing import List

import matplotlib

matplotlib.use("Agg")  # non-interactive backend

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from wocbs.models import AgentRoute
from wocbs.search import WaitOnlyConflictSearch

from .common import draw_frame, grid_bounds


def animate_scenario(scenario: dict, output_dir: Path) -> None:
    name: str = scenario["name"]
    routes: List[AgentRoute] = scenario["routes"]
    max_t: int = scenario["max_time_ticks"]
    safety_gap: int = scenario.get("safety_gap", 1)
    disappear: bool = scenario.get("disappear_at_goal", False)
    description: str = scenario.get("description", "")

    solver = WaitOnlyPrecedenceSearch(
        routes, max_t, safety_gap=safety_gap, disappear_at_goal=disappear
    )
    schedule = solver.solve()

    if schedule is None:
        print(f"[SKIP] {name}: no solution found")
        return

    x_min, x_max, y_min, y_max = grid_bounds(routes)
    fig_w = max(4, x_max - x_min + 1)
    fig_h = max(3, y_max - y_min + 1)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    def update(t: int):
        draw_frame(ax, routes, schedule, t, max_t, name)

    anim = FuncAnimation(
        fig,
        update,
        frames=range(max_t + 1),
        interval=500,
        repeat=False,
        blit=False,
    )

    out_path = output_dir / f"{name}.gif"
    anim.save(str(out_path), writer=PillowWriter(fps=2))
    plt.close(fig)

    delay = schedule.total_delay()
    makespan = schedule.makespan()
    print(
        f"[OK] {name} -> output/{name}.gif  delay={delay}  makespan={makespan}  ({description})"
    )
