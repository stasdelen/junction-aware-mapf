from wopbs.models import Vertex, AgentRoute
from wopbs.schedule import Schedule


def _make_routes():
    return [
        AgentRoute(0, [Vertex(0, 0), Vertex(1, 0), Vertex(2, 0)], release_time=0),
        AgentRoute(1, [Vertex(0, 1), Vertex(1, 1), Vertex(2, 1)], release_time=0),
    ]


def test_schedule_path_index_at_time_basic():
    routes = _make_routes()
    arrival = {0: [0, 1, 2], 1: [0, 1, 2]}
    sched = Schedule(routes, arrival)
    assert sched.path_index_at(agent_id=0, t=0) == 0
    assert sched.path_index_at(agent_id=0, t=1) == 1
    assert sched.path_index_at(agent_id=0, t=2) == 2
    # t > final arrival: robot stays at last index
    assert sched.path_index_at(agent_id=0, t=5) == 2


def test_schedule_vertex_at_time():
    routes = _make_routes()
    arrival = {0: [0, 1, 2], 1: [0, 1, 2]}
    sched = Schedule(routes, arrival)
    assert sched.vertex_at(agent_id=0, t=0) == Vertex(0, 0)
    assert sched.vertex_at(agent_id=0, t=1) == Vertex(1, 0)
    assert sched.vertex_at(agent_id=0, t=2) == Vertex(2, 0)


def test_schedule_with_wait():
    routes = [AgentRoute(0, [Vertex(0, 0), Vertex(1, 0)], release_time=0)]
    arrival = {0: [0, 3]}
    sched = Schedule(routes, arrival)
    assert sched.path_index_at(0, 0) == 0
    assert sched.path_index_at(0, 1) == 0
    assert sched.path_index_at(0, 2) == 0
    assert sched.path_index_at(0, 3) == 1


def test_schedule_total_delay():
    routes = _make_routes()
    arrival = {0: [0, 2, 4], 1: [0, 1, 2]}  # agent 0 delayed by 2
    sched = Schedule(routes, arrival)
    assert sched.total_delay() == 2


def test_schedule_makespan():
    routes = _make_routes()
    arrival = {0: [0, 2, 4], 1: [0, 1, 2]}
    sched = Schedule(routes, arrival)
    assert sched.makespan() == 4
