# junction-aware-mapf
Multi Agent Path Finding solutions for Fleet Management Systems


# Wait-Only Conflict-Based Search (WOCBS)

WOCBS is a CBS-variant that operates over **temporal precedence constraints**. Instead of replanning routes, it enforces ordering between specific path events (vertex arrivals and edge traversals):

The constraint graph is solved with **Bellman-Ford longest-path** to compute earliest feasible arrival times. A positive cycle in the constraint graph means the ordering is infeasible (e.g., A before B and B before A).

Search is **best-first** over constraint sets: at each node, the first collision is detected deterministically, two child nodes are generated (one per ordering), and the heap is ordered by `(total_delay, makespan, constraint_count)`.

## Requirements

- Python 3.10+
- `matplotlib` 3.10+ (for `FuncAnimation`)
- `Pillow` (for `PillowWriter` GIF export)

## Layout

- `wocbs/` contains the solver, schedule model, and collision logic
- `tests/` covers the core modules
- `visualization/` defines demo scenarios and GIF generation
- `output/` stores the rendered example runs

## Run tests

```bash
pytest -q
```

## Generate example GIFs

```bash
python visualization/run_all.py
```
