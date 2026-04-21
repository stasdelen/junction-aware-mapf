from wopbs.models import (
    Vertex, AgentRoute, PrecedenceType, PrecedenceConstraint,
    CollisionType, Collision
)


def test_vertex_equality():
    assert Vertex(1, 2) == Vertex(1, 2)
    assert Vertex(1, 2) != Vertex(1, 3)


def test_vertex_hashable():
    d = {Vertex(0, 0): "a", Vertex(1, 1): "b"}
    assert d[Vertex(0, 0)] == "a"


def test_agent_route_defaults():
    route = AgentRoute(agent_id=0, path=[Vertex(0, 0), Vertex(1, 0)])
    assert route.release_time == 0


def test_precedence_constraint_key_unique():
    c1 = PrecedenceConstraint(
        type=PrecedenceType.VERTEX_CLEAR_BEFORE_REACH,
        before_agent=0, before_index=1,
        after_agent=1, after_index=2,
        safety_gap_ticks=1,
    )
    c2 = PrecedenceConstraint(
        type=PrecedenceType.VERTEX_CLEAR_BEFORE_REACH,
        before_agent=1, before_index=2,
        after_agent=0, after_index=1,
        safety_gap_ticks=1,
    )
    assert c1.canonical_key() != c2.canonical_key()


def test_precedence_constraint_key_stable():
    c = PrecedenceConstraint(
        type=PrecedenceType.EDGE_CLEAR_BEFORE_TRAVERSE,
        before_agent=0, before_index=0,
        after_agent=1, after_index=0,
        safety_gap_ticks=1,
    )
    assert c.canonical_key() == c.canonical_key()


def test_constraint_set_canonical_key():
    c1 = PrecedenceConstraint(PrecedenceType.VERTEX_CLEAR_BEFORE_REACH, 0, 1, 1, 2, 1)
    c2 = PrecedenceConstraint(PrecedenceType.VERTEX_CLEAR_BEFORE_REACH, 1, 2, 0, 1, 1)
    key_ab = _constraints_key([c1, c2])
    key_ba = _constraints_key([c2, c1])
    assert key_ab == key_ba


def _constraints_key(constraints):
    return tuple(sorted(c.canonical_key() for c in constraints))
