#!/usr/bin/env python3
from __future__ import annotations

import os
from time import perf_counter

from python_raytracer.raymarcher import Raymarcher


def main() -> None:
    width = int(os.environ.get("WIDTH", "64"))
    height = int(os.environ.get("HEIGHT", "64"))
    frames = int(os.environ.get("FRAMES", "30"))
    pixels = bytearray(width * height * 4)
    raymarcher = Raymarcher(width, height)

    start = perf_counter()
    for frame in range(frames):
        raymarcher.render_into(pixels, frame / 60.0)
    elapsed = perf_counter() - start
    print(f"{frames} frames at {width}x{height}: {elapsed:.3f}s")
    print(f"{frames / elapsed:.2f} fps render-only")
    print(f"{elapsed / frames * 1000:.2f} ms/frame")


if __name__ == "__main__":
    main()

