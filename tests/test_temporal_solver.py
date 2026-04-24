from wocbs.models import Vertex, AgentRoute, PrecedenceConstraint, PrecedenceType
from wocbs.temporal_solver import compute_earliest_schedule


def _route(aid, coords, release=0):
    return AgentRoute(aid, [Vertex(*c) for c in coords], release_time=release)


def test_no_constraints_unit_moves():
    routes = [_route(0, [(0, 0), (1, 0), (2, 0)]), _route(1, [(0, 1), (1, 1), (2, 1)])]
    sched = compute_earliest_schedule(routes, [], max_time_ticks=10)
    assert sched is not None
    assert sched.arrival_time[0] == [0, 1, 2]
    assert sched.arrival_time[1] == [0, 1, 2]


def test_release_time_respected():
    routes = [_route(0, [(0, 0), (1, 0)], release=3)]
    sched = compute_earliest_schedule(routes, [], max_time_ticks=10)
    assert sched is not None
    assert sched.arrival_time[0] == [3, 4]


def test_vertex_precedence_delays_agent():
    routes = [_route(0, [(0, 0), (1, 0), (2, 0)]), _route(1, [(1, -1), (1, 0), (1, 1)])]
    c = PrecedenceConstraint(
        type=PrecedenceType.VERTEX_CLEAR_BEFORE_REACH,
        before_agent=0, before_index=1,
        after_agent=1, after_index=1,
        safety_gap_ticks=1,
    )
    sched = compute_earliest_schedule(routes, [c], max_time_ticks=10)
    assert sched is not None
    assert sched.arrival_time[1][1] >= sched.arrival_time[0][2] + 1


def test_positive_cycle_is_infeasible():
    routes = [_route(0, [(0, 0), (1, 0)]), _route(1, [(1, 0), (0, 0)])]
    c1 = PrecedenceConstraint(PrecedenceType.VERTEX_CLEAR_BEFORE_REACH, 0, 0, 1, 0, 1)
    c2 = PrecedenceConstraint(PrecedenceType.VERTEX_CLEAR_BEFORE_REACH, 1, 0, 0, 0, 1)
    sched = compute_earliest_schedule(routes, [c1, c2], max_time_ticks=10)
    assert sched is None


def test_max_time_ticks_exceeded_is_infeasible():
    routes = [_route(0, [(0, 0), (1, 0), (2, 0)]), _route(1, [(1, -1), (1, 0), (1, 1)])]
    c = PrecedenceConstraint(PrecedenceType.VERTEX_CLEAR_BEFORE_REACH, 0, 1, 1, 1, 1)
    sched = compute_earliest_schedule(routes, [c], max_time_ticks=2)
    assert sched is None


def test_edge_precedence_delays_agent():
    routes = [_route(0, [(0, 0), (1, 0)]), _route(1, [(1, 0), (0, 0)])]
    c = PrecedenceConstraint(
        type=PrecedenceType.EDGE_CLEAR_BEFORE_TRAVERSE,
        before_agent=0, before_index=0,
        after_agent=1, after_index=0,
        safety_gap_ticks=1,
    )
    sched = compute_earliest_schedule(routes, [c], max_time_ticks=10)
    assert sched is not None
    assert sched.arrival_time[1][1] >= sched.arrival_time[0][1] + 1 + 1
