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
    ]
