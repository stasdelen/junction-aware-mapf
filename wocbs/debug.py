from __future__ import annotations
from typing import List
from .models import AgentRoute, Vertex
from .schedule import Schedule


def print_schedule(routes: List[AgentRoute], schedule: Schedule) -> None:
    """Print a human-readable schedule: each agent's path index, vertex, arrival time."""
    route_map = {r.agent_id: r for r in routes}
    print("\n=== Schedule ===")
    for agent_id in sorted(schedule.arrival_time.keys()):
        route = route_map[agent_id]
        print(f"  Agent {agent_id} (release={route.release_time}):")
        for k, t in enumerate(schedule.arrival_time[agent_id]):
            v = route.path[k]
            label = " [GOAL]" if k == len(route.path) - 1 else ""
            print(f"    index={k}  vertex={v}  arrival_t={t}{label}")
    print(f"  Total delay: {schedule.total_delay()}")
    print(f"  Makespan:    {schedule.makespan()}")


def get_timed_positions(
    agent_id: int,
    route: AgentRoute,
    schedule: Schedule,
    max_time: int,
) -> List[Vertex]:
    """
    Expand schedule into a time-indexed position list.
    Returns list of length max_time+1 where index t is the vertex at time t.
    """
    return [schedule.vertex_at(agent_id, t) for t in range(max_time + 1)]
