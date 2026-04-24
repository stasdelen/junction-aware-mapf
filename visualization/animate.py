# visualization/animate.py
from pathlib import Path
from typing import List

import matplotlib

matplotlib.use("Agg")  # non-interactive backend

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from wopbs.models import AgentRoute
from wopbs.search import WaitOnlyPrecedenceSearch

AGENT_COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]


def agent_color(agent_id: int) -> str:
    return AGENT_COLORS[agent_id % len(AGENT_COLORS)]


def grid_bounds(routes: List[AgentRoute]) -> Tuple[int, int, int, int]:
    xs = [v.x for r in routes for v in r.path]
    ys = [v.y for r in routes for v in r.path]
    return min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1


def draw_frame(
    ax,
    routes: List[AgentRoute],
    schedule: Schedule,
    t: int,
    max_t: int,
    scenario_name: str,
) -> None:
    """Clear and redraw ax for time tick t."""
    ax.cla()
    x_min, x_max, y_min, y_max = grid_bounds(routes)

    ax.set_facecolor("white")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal")
    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))
    ax.tick_params(labelsize=7)
    for x in range(x_min, x_max + 1):
        ax.axvline(x, color="#dddddd", linewidth=0.5, zorder=0)
    for y in range(y_min, y_max + 1):
        ax.axhline(y, color="#dddddd", linewidth=0.5, zorder=0)

    for route in routes:
        color = agent_color(route.agent_id)
        xs = [v.x for v in route.path]
        ys = [v.y for v in route.path]
        ax.plot(
            xs, ys, color=color, alpha=0.25, linewidth=1.5, linestyle="--", zorder=1
        )
        # Start marker
        ax.text(
            route.path[0].x,
            route.path[0].y + 0.35,
            "S",
            color=color,
            fontsize=6,
            ha="center",
            va="center",
            fontweight="bold",
            zorder=2,
        )
        # Goal marker
        ax.text(
            route.path[-1].x,
            route.path[-1].y + 0.35,
            "G",
            color=color,
            fontsize=6,
            ha="center",
            va="center",
            fontweight="bold",
            zorder=2,
        )

    for route in routes:
        color = agent_color(route.agent_id)
        vx = schedule.vertex_at(route.agent_id, t)

        # Wait indicator: thick border if agent did not move since last tick
        if t > 0:
            prev_k = schedule.path_index_at(route.agent_id, t - 1)
            curr_k = schedule.path_index_at(route.agent_id, t)
            waiting = prev_k == curr_k
        else:
            waiting = False

        lw = 3.0 if waiting else 1.0
        circle = mpatches.Circle(
            (vx.x, vx.y),
            radius=0.3,
            facecolor=color,
            edgecolor="black",
            linewidth=lw,
            zorder=3,
        )
        ax.add_patch(circle)
        ax.text(
            vx.x,
            vx.y,
            str(route.agent_id),
            color="white",
            fontsize=8,
            ha="center",
            va="center",
            fontweight="bold",
            zorder=4,
        )

    ax.set_title(f"{scenario_name}   t={t} / {max_t}", fontsize=10)


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
