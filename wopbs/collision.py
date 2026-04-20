from typing import List, Optional

from .models import AgentRoute, Collision, CollisionType
from .schedule import Schedule


def find_first_collision(
    routes: List[AgentRoute],
    schedule: Schedule,
    max_time_ticks: int,
    disappear_at_goal: bool = False,
) -> Optional[Collision]:
    route_map = {r.agent_id: r for r in routes}
    agent_ids = sorted(route_map.keys())
    best: Optional[Collision] = None

    def _is_better(cand: Collision, current: Optional[Collision]) -> bool:
        if current is None:
            return True
        if cand.time != current.time:
            return cand.time < current.time
        type_rank = {
            CollisionType.VERTEX: 0,
            CollisionType.EDGE_SWAP: 1,
            CollisionType.SAME_EDGE: 2,
        }
        if cand.type != current.type:
            return type_rank[cand.type] < type_rank[current.type]
        if (cand.index_a, cand.index_b) != (current.index_a, current.index_b):
            return (cand.index_a, cand.index_b) < (current.index_a, current.index_b)
        return False

    for i_idx, agent_a in enumerate(agent_ids):
        for agent_b in agent_ids[i_idx + 1 :]:
            for t in range(max_time_ticks + 1):
                # Agent disappears after reaching its goal (t strictly after goal arrival)
                a_done = disappear_at_goal and t > schedule.arrival_time[agent_a][-1]
                b_done = disappear_at_goal and t > schedule.arrival_time[agent_b][-1]
                if a_done or b_done:
                    continue

                ka = schedule.path_index_at(agent_a, t)
                kb = schedule.path_index_at(agent_b, t)
                va = schedule.vertex_at(agent_a, t)
                vb = schedule.vertex_at(agent_b, t)

                # Vertex collision
                if va == vb:
                    cand = Collision(CollisionType.VERTEX, t, agent_a, ka, agent_b, kb)
                    if _is_better(cand, best):
                        best = cand

                # Edge collision for interval [t, t+1]
                if t < max_time_ticks:
                    ka_next = schedule.path_index_at(agent_a, t + 1)
                    kb_next = schedule.path_index_at(agent_b, t + 1)
                    a_moves = ka_next > ka
                    b_moves = kb_next > kb

                    if a_moves and b_moves:
                        va_next = schedule.vertex_at(agent_a, t + 1)
                        vb_next = schedule.vertex_at(agent_b, t + 1)

                        # Edge-swap: a goes u→v, b goes v→u
                        if va == vb_next and vb == va_next:
                            cand = Collision(
                                CollisionType.EDGE_SWAP, t, agent_a, ka, agent_b, kb
                            )
                            if _is_better(cand, best):
                                best = cand

                        # Same-edge same-direction
                        elif va == vb and va_next == vb_next and va != va_next:
                            cand = Collision(
                                CollisionType.SAME_EDGE, t, agent_a, ka, agent_b, kb
                            )
                            if _is_better(cand, best):
                                best = cand

    return best
