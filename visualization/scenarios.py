# visualization/scenarios.py
from wocbs.models import AgentRoute, Vertex


def _v(x: int, y: int) -> Vertex:
    return Vertex(x, y)


def _r(agent_id: int, coords, release: int = 0) -> AgentRoute:
    return AgentRoute(agent_id, [_v(*c) for c in coords], release_time=release)


def get_scenarios():
    return [
        {
            "name": "1_parallel_paths",
            "description": "2 agents on non-intersecting parallel paths — zero delay baseline",
            "routes": [
                _r(0, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]),
                _r(1, [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]),
            ],
            "max_time_ticks": 8,
            "safety_gap": 1,
            "disappear_at_goal": False,
        },
        {
            "name": "2_vertex_conflict",
            "description": "2 agents converge at (2,1) at t=2 — one waits 1 tick",
            "routes": [
                _r(0, [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]),
                _r(1, [(2, -1), (2, 0), (2, 1), (2, 2)]),
            ],
            "max_time_ticks": 10,
            "safety_gap": 1,
            "disappear_at_goal": False,
        },
        {
            "name": "3_edge_swap",
            "description": "2 agents traverse edge (1,0)↔(2,0) in opposite directions — edge-swap resolved",
            "routes": [
                _r(0, [(0, 0), (1, 0), (2, 0), (3, 0)]),
                _r(1, [(2, 1), (2, 0), (1, 0), (1, 1)]),
            ],
            "max_time_ticks": 12,
            "safety_gap": 1,
            "disappear_at_goal": False,
        },
        {
            "name": "4_three_way_junction",
            "description": "3 agents converge at (2,2) from W, S, NW — cascading waits",
            "routes": [
                _r(0, [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]),
                _r(1, [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]),
                _r(2, [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]),
            ],
            "max_time_ticks": 14,
            "safety_gap": 1,
            "disappear_at_goal": False,
        },
        {
            "name": "5_chain_conflict",
            "description": "3 agents: horizontal robot conflicts independently at (2,2) and (4,2)",
            "routes": [
                _r(0, [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)]),
                _r(1, [(2, 4), (2, 3), (2, 2), (2, 1), (2, 0)]),
                _r(2, [(4, 4), (4, 3), (4, 2), (4, 1), (4, 0)]),
            ],
            "max_time_ticks": 14,
            "safety_gap": 1,
            "disappear_at_goal": False,
        },
        {
            "name": "6_four_intersection",
            "description": "4 agents converge at (2,2) from W, S, NW, NE — 3 agents wait in sequence",
            "routes": [
                _r(0, [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]),
                _r(1, [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]),
                _r(2, [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]),
                _r(3, [(4, 4), (3, 3), (2, 2), (1, 1), (0, 0)]),
            ],
            "max_time_ticks": 16,
            "safety_gap": 1,
            "disappear_at_goal": False,
        },
    ]
