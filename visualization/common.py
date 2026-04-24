from typing import List, Tuple

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from wocbs.models import AgentRoute
from wocbs.schedule import Schedule

# Agent colors: blue, orange, green, red
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
    ax.cla()
    x_min, x_max, y_min, y_max = grid_bounds(routes)

    # Background and grid
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

    # Route paths with start/goal markers
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

    # Agent positions
    for route in routes:
        color = agent_color(route.agent_id)
        vx = schedule.vertex_at(route.agent_id, t)

        # Wait indicator
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
