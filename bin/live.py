#!/usr/bin/env python3
from __future__ import annotations

import os

import pyray as rl

from python_raytracer.raymarcher import Raymarcher


def main() -> None:
    width = int(os.environ.get("WIDTH", "64"))
    height = int(os.environ.get("HEIGHT", "64"))
    scale = int(os.environ.get("SCALE", "10"))
    fps = int(os.environ.get("FPS", "60"))

    pixels = bytearray(width * height * 4)
    raymarcher = Raymarcher(width, height)

    rl.init_window(width * scale, height * scale, "python-raytracer raymarcher")
    rl.set_target_fps(fps)

    image = rl.gen_image_color(width, height, rl.Color(0, 0, 0, 255))
    texture = rl.load_texture_from_image(image)
    rl.unload_image(image)

    source = rl.Rectangle(0, 0, width, height)
    dest = rl.Rectangle(0, 0, width * scale, height * scale)
    origin = rl.Vector2(0, 0)

    pixel_pointer = rl.ffi.cast("void *", rl.ffi.from_buffer(pixels))

    try:
        while not rl.window_should_close():
            raymarcher.render_into(pixels, rl.get_time())
            rl.update_texture(texture, pixel_pointer)
            rl.begin_drawing()
            rl.clear_background(rl.BLACK)
            rl.draw_texture_pro(texture, source, dest, origin, 0.0, rl.WHITE)
            rl.draw_fps(8, 8)
            rl.end_drawing()
    finally:
        rl.unload_texture(texture)
        rl.close_window()


if __name__ == "__main__":
    main()
