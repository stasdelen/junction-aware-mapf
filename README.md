# junction-aware-mapf
Multi Agent Path Finding solutions for Fleet Management Systems

The core package is `wocbs`. It models agent routes, detects route collisions,
builds precedence constraints, and searches for a feasible schedule by delaying
agents instead of replanning paths.

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
