# Python Raytracer

Python port of `~/Coding/Graphics/ruby-raytracer`, using `uv`, CPython 3.13, object-style `Vec3` math, and one Raylib texture upload per frame.

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

On this machine, the fair object/operator version is roughly the same class as Ruby:

```text
Python object Vec3: 2.81 fps at 64x64 render-only
Ruby object Vec3:   2.78 fps at 64x64 render-only
```

The earlier scalar Python baseline was much faster, around `17 fps` render-only at `64x64`, because it avoided vector object allocation in the hot loop.

## Render A Still

```bash
uv run python bin/render_ppm.py
```

## Notes

- `src/python_raytracer/vec3.py` is the operator-overloaded vector class.
- `src/python_raytracer/raymarcher.py` intentionally uses `Vec3` in the render hot path for a fairer race with the Ruby version.
