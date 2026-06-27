#!/usr/bin/env python3
from __future__ import annotations

import os

from python_raytracer.raymarcher import Raymarcher


def main() -> None:
    width = int(os.environ.get("WIDTH", "160"))
    height = int(os.environ.get("HEIGHT", "90"))
    time = float(os.environ.get("TIME", "1.25"))
    output = os.environ.get("OUT", "frame.ppm")
    pixels = bytearray(width * height * 4)
    Raymarcher(width, height).render_into(pixels, time)

    with open(output, "w", encoding="ascii") as file:
        file.write("P3\n")
        file.write(f"{width} {height}\n")
        file.write("255\n")
        for y in range(height):
            row = []
            for x in range(width):
                offset = (y * width + x) * 4
                row.append(f"{pixels[offset]} {pixels[offset + 1]} {pixels[offset + 2]}")
            file.write(" ".join(row))
            file.write("\n")

    print(f"wrote {output}")


if __name__ == "__main__":
    main()

