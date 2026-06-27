# Python Raytracer

Python port of `~/Coding/Graphics/ruby-raytracer`, using `uv`, CPython 3.13, scalar hot-path math, and one Raylib texture upload per frame.

The scene mirrors the Ruby/Dudu version: orbit camera, centered reflective wobbly sphere, small colored spheres, checkered floor, sky reflection, basic lighting, and soft shadow.

## Run

```bash
uv run python bin/live.py
```

Useful knobs:

```bash
WIDTH=64 HEIGHT=64 SCALE=10 FPS=60 uv run python bin/live.py
WIDTH=96 HEIGHT=96 SCALE=8 FPS=60 uv run python bin/live.py
```

## Benchmark

Render-only benchmark without a window:

```bash
uv run python bin/bench.py
FRAMES=60 WIDTH=64 HEIGHT=64 uv run python bin/bench.py
```

## Render A Still

```bash
uv run python bin/render_ppm.py
```

## Notes

- `src/python_raytracer/vec3.py` keeps a readable operator-overloaded vector reference.
- `src/python_raytracer/raymarcher.py` intentionally uses scalar floats in the render hot path.
- The goal is to race Python vs Ruby fairly while avoiding the obvious object-allocation trap.

