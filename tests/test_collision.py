from wocbs.models import Vertex, AgentRoute, CollisionType
from wocbs.schedule import Schedule
from wocbs.collision import find_first_collision


def _sched(routes, arrival):
    return Schedule(routes, arrival)


def _route(aid, coords, release=0):
    return AgentRoute(aid, [Vertex(*c) for c in coords], release_time=release)


def test_no_collision_parallel():
    routes = [_route(0, [(0, 0), (1, 0), (2, 0)]), _route(1, [(0, 1), (1, 1), (2, 1)])]
    sched = _sched(routes, {0: [0, 1, 2], 1: [0, 1, 2]})
    assert find_first_collision(routes, sched, max_time_ticks=5) is None


def test_vertex_collision_detected():
    routes = [_route(0, [(0, 0), (1, 0), (2, 0)]), _route(1, [(1, -1), (1, 0), (1, 1)])]
    sched = _sched(routes, {0: [0, 1, 2], 1: [0, 1, 2]})
    col = find_first_collision(routes, sched, max_time_ticks=5)
    assert col is not None
    assert col.type == CollisionType.VERTEX
    assert col.time == 1
    assert col.agent_a == 0
    assert col.agent_b == 1


def test_vertex_collision_resolved_by_delay():
    routes = [_route(0, [(0, 0), (1, 0), (2, 0)]), _route(1, [(1, -1), (1, 0), (1, 1)])]
    # Agent 1 delayed: reaches (1,0) at t=2 instead of t=1
    sched = _sched(routes, {0: [0, 1, 2], 1: [0, 2, 3]})
    col = find_first_collision(routes, sched, max_time_ticks=5)
    assert col is None


def test_edge_swap_collision_detected():
    routes = [_route(0, [(0, 0), (1, 0)]), _route(1, [(1, 0), (0, 0)])]
    sched = _sched(routes, {0: [0, 1], 1: [0, 1]})
    col = find_first_collision(routes, sched, max_time_ticks=5)
    assert col is not None
    assert col.type == CollisionType.EDGE_SWAP


def test_edge_swap_resolved_by_wait():
    # a0 and a1 both traverse edge (1,0)↔(2,0) in opposite directions.
    # a0 waits 2 ticks at (0,0) so a1 clears the edge before a0 enters it.
    # All vertices are distinct, so no vertex collision after the wait.
    routes = [
        _route(0, [(0, 0), (1, 0), (2, 0)]),
        _route(1, [(2, 1), (2, 0), (1, 0), (1, 1)]),
    ]
    sched = _sched(routes, {0: [0, 3, 4], 1: [0, 1, 2, 3]})
    col = find_first_collision(routes, sched, max_time_ticks=6)
    assert col is None


def test_disappear_at_goal_no_collision():
    routes = [_route(0, [(1, 0)]), _route(1, [(0, 0), (1, 0), (2, 0)])]
    sched = _sched(routes, {0: [0], 1: [0, 1, 2]})
    # disappear_at_goal=False: collision at t=1
    col_nodisappear = find_first_collision(routes, sched, max_time_ticks=5, disappear_at_goal=False)
    assert col_nodisappear is not None
    # disappear_at_goal=True: agent 0 is gone after t=0
    col_disappear = find_first_collision(routes, sched, max_time_ticks=5, disappear_at_goal=True)
    assert col_disappear is None
