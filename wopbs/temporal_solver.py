from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .models import AgentRoute, PrecedenceConstraint, PrecedenceType
from .schedule import Schedule


def compute_earliest_schedule(
    routes: List[AgentRoute],
    constraints: List[PrecedenceConstraint],
    max_time_ticks: int,
    safety_gap: int = 1,
) -> Optional[Schedule]:
    nodes: List[Tuple[int, int]] = []
    for route in routes:
        for k in range(len(route.path)):
            nodes.append((route.agent_id, k))

    node_index: Dict[Tuple[int, int], int] = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)

    # T[i] = current lower bound for node i; -1e18 means unreachable
    T: List[float] = [-1e18] * n

    # 1 - Apply release times
    for route in routes:
        idx = node_index[(route.agent_id, 0)]
        T[idx] = max(T[idx], float(route.release_time))

    # Build edge list: (from_node_idx, to_node_idx, weight)
    edges: List[Tuple[int, int, float]] = []

    # 2 - Path move constraints: T(i, k+1) >= T(i, k) + 1
    for route in routes:
        for k in range(len(route.path) - 1):
            u = node_index[(route.agent_id, k)]
            v = node_index[(route.agent_id, k + 1)]
            edges.append((u, v, 1.0))

    # 3 - Precedence constraints
    for c in constraints:
        if c.type == PrecedenceType.VERTEX_CLEAR_BEFORE_REACH:
            # T(after_agent, after_index) >= T(before_agent, before_index + 1) + safety_gap
            before_route = next(r for r in routes if r.agent_id == c.before_agent)
            is_goal = c.before_index == len(before_route.path) - 1
            if is_goal:
                return None
            u = node_index[(c.before_agent, c.before_index + 1)]
            v = node_index[(c.after_agent, c.after_index)]
            edges.append((u, v, float(c.safety_gap_ticks)))

        elif c.type == PrecedenceType.EDGE_CLEAR_BEFORE_TRAVERSE:
            # T(after_agent, after_index + 1) >= T(before_agent, before_index + 1) + safety_gap + 1
            u = node_index[(c.before_agent, c.before_index + 1)]
            v = node_index[(c.after_agent, c.after_index + 1)]
            edges.append((u, v, float(c.safety_gap_ticks + 1)))

    # Bellman-Ford
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if T[u] > -1e17 and T[u] + w > T[v]:
                T[v] = T[u] + w
                updated = True
        if not updated:
            break

    # Positive cycle check: one more pass
    for u, v, w in edges:
        if T[u] > -1e17 and T[u] + w > T[v] + 1e-9:
            return None

    arrival_time: Dict[int, List[int]] = {}
    for route in routes:
        times = []
        for k in range(len(route.path)):
            raw = T[node_index[(route.agent_id, k)]]
            t = int(round(raw)) if raw > -1e17 else route.release_time
            if t > max_time_ticks:
                return None
            times.append(t)
        arrival_time[route.agent_id] = times

    return Schedule(routes, arrival_time)
