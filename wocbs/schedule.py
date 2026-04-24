from typing import Dict, List

from .models import AgentRoute, Vertex


class Schedule:
    """Stores arrival_time[agent_id][path_index] which is T_i(k)."""

    def __init__(self, routes: List[AgentRoute], arrival_time: Dict[int, List[int]]):
        self._routes = {r.agent_id: r for r in routes}
        self.arrival_time = arrival_time

    def path_index_at(self, agent_id: int, t: int) -> int:
        """
        Return the largest path index k such that arrival_time[agent_id][k] <= t.
        If t is before the agent's release time, returns 0.
        """
        arrivals = self.arrival_time[agent_id]
        k = 0
        for idx, arr in enumerate(arrivals):
            if arr <= t:
                k = idx
            else:
                break
        return k

    def vertex_at(self, agent_id: int, t: int) -> Vertex:
        k = self.path_index_at(agent_id, t)
        return self._routes[agent_id].path[k]

    def is_at_goal(self, agent_id: int, t: int) -> bool:
        arrivals = self.arrival_time[agent_id]
        return t >= arrivals[-1]

    def goal_arrival(self, agent_id: int) -> int:
        return self.arrival_time[agent_id][-1]

    def total_delay(self) -> int:
        total = 0
        for agent_id, route in self._routes.items():
            nominal = (len(route.path) - 1) + route.release_time
            actual = self.arrival_time[agent_id][-1]
            total += max(0, actual - nominal)
        return total

    def makespan(self) -> int:
        return max(arrivals[-1] for arrivals in self.arrival_time.values())
