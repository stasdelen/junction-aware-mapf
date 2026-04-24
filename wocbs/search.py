import heapq
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from .collision import find_first_collision
from .models import (
    AgentRoute,
    Collision,
    CollisionType,
    PrecedenceConstraint,
    PrecedenceType,
)
from .schedule import Schedule
from .temporal_solver import compute_earliest_schedule


@dataclass
class SearchNode:
    constraints: List[PrecedenceConstraint]
    schedule: Schedule
    _counter: int = field(compare=False)  # insertion-order tiebreak

    def cost(self) -> Tuple:
        delay = self.schedule.total_delay()
        makespan = self.schedule.makespan()
        nc = len(self.constraints)
        # The order of these components determines the search's optimization criteria:
        return (delay, makespan, nc, self._counter)

    def __lt__(self, other: "SearchNode") -> bool:
        return self.cost() < other.cost()


class WaitOnlyConflictSearch:
    def __init__(
        self,
        routes: List[AgentRoute],
        max_time_ticks: int,
        safety_gap: int = 1,
        disappear_at_goal: bool = False,
        max_expanded: int = 100_000,
    ):
        self.routes = routes
        self.max_time_ticks = max_time_ticks
        self.safety_gap = safety_gap
        self.disappear_at_goal = disappear_at_goal
        self.max_expanded = max_expanded

        # Debug counters
        self.nodes_expanded = 0
        self.nodes_generated = 0
        self.nodes_infeasible = 0

    def solve(self) -> Optional[Schedule]:
        root_schedule = compute_earliest_schedule(
            self.routes, [], self.max_time_ticks, self.safety_gap
        )
        if root_schedule is None:
            return None

        counter = 0
        root = SearchNode(constraints=[], schedule=root_schedule, _counter=counter)
        open_list: List[SearchNode] = []
        heapq.heappush(open_list, root)
        closed: set = set()

        while open_list:
            node = heapq.heappop(open_list)

            key = self._constraint_key(node.constraints)
            if key in closed:
                continue
            closed.add(key)
            self.nodes_expanded += 1

            if self.nodes_expanded > self.max_expanded:
                return None

            collision = find_first_collision(
                self.routes, node.schedule, self.max_time_ticks, self.disappear_at_goal
            )
            if collision is None:
                self._print_stats(node)
                return node.schedule

            for child_constraints in self._branch(node.constraints, collision):
                child_key = self._constraint_key(child_constraints)
                if child_key in closed:
                    continue
                self.nodes_generated += 1
                child_schedule = compute_earliest_schedule(
                    self.routes, child_constraints, self.max_time_ticks, self.safety_gap
                )
                if child_schedule is None:
                    self.nodes_infeasible += 1
                    continue
                counter += 1
                child = SearchNode(child_constraints, child_schedule, counter)
                heapq.heappush(open_list, child)

        return None  # no solution found

    def _branch(
        self,
        existing: List[PrecedenceConstraint],
        col: Collision,
    ) -> List[List[PrecedenceConstraint]]:
        children = []
        route_map = {r.agent_id: r for r in self.routes}

        def _add_child(before_agent, before_index, after_agent, after_index, ctype):
            if ctype == PrecedenceType.VERTEX_CLEAR_BEFORE_REACH:
                r = route_map[before_agent]
                is_goal = before_index == len(r.path) - 1
                if is_goal and not self.disappear_at_goal:
                    return  # this branch is infeasible: robot never clears its goal
            new_c = PrecedenceConstraint(
                type=ctype,
                before_agent=before_agent,
                before_index=before_index,
                after_agent=after_agent,
                after_index=after_index,
                safety_gap_ticks=self.safety_gap,
            )
            if new_c not in existing:
                children.append(existing + [new_c])

        if col.type == CollisionType.VERTEX:
            _add_child(
                col.agent_a,
                col.index_a,
                col.agent_b,
                col.index_b,
                PrecedenceType.VERTEX_CLEAR_BEFORE_REACH,
            )
            _add_child(
                col.agent_b,
                col.index_b,
                col.agent_a,
                col.index_a,
                PrecedenceType.VERTEX_CLEAR_BEFORE_REACH,
            )
        else:  # EDGE_SWAP or SAME_EDGE
            _add_child(
                col.agent_a,
                col.index_a,
                col.agent_b,
                col.index_b,
                PrecedenceType.EDGE_CLEAR_BEFORE_TRAVERSE,
            )
            _add_child(
                col.agent_b,
                col.index_b,
                col.agent_a,
                col.index_a,
                PrecedenceType.EDGE_CLEAR_BEFORE_TRAVERSE,
            )

        return children

    @staticmethod
    def _constraint_key(constraints: List[PrecedenceConstraint]) -> tuple:
        return tuple(sorted(c.canonical_key() for c in constraints))

    def _print_stats(self, solution_node: SearchNode) -> None:
        print(f"\n=== WOPBS Solution Found ===")
        print(f"Nodes expanded:   {self.nodes_expanded}")
        print(f"Nodes generated:  {self.nodes_generated}")
        print(f"Nodes infeasible: {self.nodes_infeasible}")
        print(f"Constraints:      {len(solution_node.constraints)}")
        print(f"Total delay:      {solution_node.schedule.total_delay()}")
        print(f"Makespan:         {solution_node.schedule.makespan()}")
