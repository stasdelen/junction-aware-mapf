from dataclasses import dataclass
from enum import Enum, auto
from typing import List


@dataclass(frozen=True)
class Vertex:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"


@dataclass
class AgentRoute:
    agent_id: int
    path: List[Vertex]
    release_time: int = 0

    def __post_init__(self):
        if len(self.path) < 1:
            raise ValueError(
                f"Agent {self.agent_id}: path must have at least one vertex"
            )


class PrecedenceType(Enum):
    VERTEX_CLEAR_BEFORE_REACH = auto()
    EDGE_CLEAR_BEFORE_TRAVERSE = auto()


@dataclass(frozen=True)
class PrecedenceConstraint:
    type: PrecedenceType
    before_agent: int
    before_index: int
    after_agent: int
    after_index: int
    safety_gap_ticks: int = 1

    def canonical_key(self) -> tuple:
        return (
            self.type.value,
            self.before_agent,
            self.before_index,
            self.after_agent,
            self.after_index,
            self.safety_gap_ticks,
        )


class CollisionType(Enum):
    VERTEX = auto()
    EDGE_SWAP = auto()
    SAME_EDGE = auto()


@dataclass
class Collision:
    type: CollisionType
    time: int
    agent_a: int
    index_a: int
    agent_b: int
    index_b: int
