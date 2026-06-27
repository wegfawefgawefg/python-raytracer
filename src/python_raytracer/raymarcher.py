from __future__ import annotations

from math import cos, floor, sin, sqrt

MAX_STEPS = 96
MAX_DIST = 8.0
SURFACE_DIST = 0.0008
NORMAL_EPS = 0.002

MATERIAL_MIRROR = 1
MATERIAL_RED = 2
MATERIAL_BLUE = 3
MATERIAL_FLOOR = 4

LIGHT_X = -0.35
LIGHT_Y = 0.82
LIGHT_Z = -0.52
LIGHT_LEN = sqrt(LIGHT_X * LIGHT_X + LIGHT_Y * LIGHT_Y + LIGHT_Z * LIGHT_Z)
LIGHT_X /= LIGHT_LEN
LIGHT_Y /= LIGHT_LEN
LIGHT_Z /= LIGHT_LEN


class Raymarcher:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.aspect = width / height

    def render_into(self, pixels: bytearray, time: float) -> None:
        width = self.width
        height = self.height
        aspect = self.aspect
        cam_x, cam_y, cam_z = orbit_camera(time)

        # Camera basis, same as the Ruby/Dudu setup.
        fx, fy, fz = normalize3(-cam_x, 0.15 - cam_y, -cam_z)
        rx, ry, rz = normalize3(-fz, 0.0, fx)
        ux, uy, uz = cross3(rx, ry, rz, fx, fy, fz)

        offset = 0
        for y in range(height):
            v = 1.0 - ((y + 0.5) / height) * 2.0
            for x in range(width):
                u = (((x + 0.5) / width) * 2.0 - 1.0) * aspect
                dx, dy, dz = normalize3(fx * 2.0 + rx * u + ux * v, fy * 2.0 + ry * u + uy * v, fz * 2.0 + rz * u + uz * v)
                r, g, b = trace(cam_x, cam_y, cam_z, dx, dy, dz, time, 0)
                pixels[offset] = r
                pixels[offset + 1] = g
                pixels[offset + 2] = b
                pixels[offset + 3] = 255
                offset += 4


def color_at(width: int, height: int, x: int, y: int, time: float) -> tuple[int, int, int]:
    pixels = bytearray(width * height * 4)
    Raymarcher(width, height).render_into(pixels, time)
    offset = (y * width + x) * 4
    return pixels[offset], pixels[offset + 1], pixels[offset + 2]


def orbit_camera(time: float) -> tuple[float, float, float]:
    orbit = 2.9
    yaw = time * 0.35
    return orbit * cos(yaw), 0.9 + 0.15 * sin(time * 0.17), orbit * sin(yaw)


def trace(ox: float, oy: float, oz: float, dx: float, dy: float, dz: float, time: float, depth: int) -> tuple[int, int, int]:
    hit, dist, steps, material = march(ox, oy, oz, dx, dy, dz, time)
    if not hit:
        return tone_map(*sky(dy))

    px = ox + dx * dist
    py = oy + dy * dist
    pz = oz + dz * dist
    nx, ny, nz = estimate_normal(px, py, pz, time)
    cr, cg, cb = shade(px, py, pz, nx, ny, nz, dx, dy, dz, material, steps, time)

    if material == MATERIAL_MIRROR and depth < 1:
        dot = dx * nx + dy * ny + dz * nz
        rdx, rdy, rdz = normalize3(dx - nx * (2.0 * dot), dy - ny * (2.0 * dot), dz - nz * (2.0 * dot))
        rr, rg, rb = trace(px + nx * 0.025, py + ny * 0.025, pz + nz * 0.025, rdx, rdy, rdz, time, depth + 1)
        cr = cr * 0.35 + (rr / 255.0) * 0.65
        cg = cg * 0.35 + (rg / 255.0) * 0.65
        cb = cb * 0.35 + (rb / 255.0) * 0.65

    return tone_map(cr, cg, cb)


def march(ox: float, oy: float, oz: float, dx: float, dy: float, dz: float, time: float) -> tuple[bool, float, int, int]:
    dist = 0.0
    material = 0
    for step in range(MAX_STEPS):
        px = ox + dx * dist
        py = oy + dy * dist
        pz = oz + dz * dist
        sdf, material = scene(px, py, pz, time)
        if sdf < SURFACE_DIST:
            return True, dist, step, material
        dist += sdf
        if dist > MAX_DIST:
            break
    return False, dist, MAX_STEPS, material


def scene(px: float, py: float, pz: float, time: float) -> tuple[float, int]:
    sphere = wobbly_sphere(px, py, pz, 0.0, 0.35, 0.0, 1.0, time)
    left = sd_sphere(px + 1.45, py + 0.28, pz - 0.85, 0.32)
    right = sd_sphere(px - 1.25, py + 0.35, pz + 0.75, 0.28)
    floor_dist = py + 1.0

    sdf = sphere
    material = MATERIAL_MIRROR
    if left < sdf:
        sdf = left
        material = MATERIAL_RED
    if right < sdf:
        sdf = right
        material = MATERIAL_BLUE
    if floor_dist < sdf:
        sdf = floor_dist
        material = MATERIAL_FLOOR
    return sdf, material


def sd_sphere(x: float, y: float, z: float, radius: float) -> float:
    return sqrt(x * x + y * y + z * z) - radius


def wobbly_sphere(px: float, py: float, pz: float, cx: float, cy: float, cz: float, radius: float, time: float) -> float:
    x = px - cx
    y = py - cy
    z = pz - cz
    return sqrt(x * x + y * y + z * z) - radius + sin(x * 12.0 + time * 1.4) * 0.025 + cos(y * 13.0 + time * 1.1) * 0.025


def estimate_normal(px: float, py: float, pz: float, time: float) -> tuple[float, float, float]:
    e = NORMAL_EPS
    dx = scene(px + e, py, pz, time)[0] - scene(px - e, py, pz, time)[0]
    dy = scene(px, py + e, pz, time)[0] - scene(px, py - e, pz, time)[0]
    dz = scene(px, py, pz + e, time)[0] - scene(px, py, pz - e, time)[0]
    return normalize3(dx, dy, dz)


def shade(px: float, py: float, pz: float, nx: float, ny: float, nz: float, view_x: float, view_y: float, view_z: float, material: int, steps: int, time: float) -> tuple[float, float, float]:
    diffuse = max(nx * LIGHT_X + ny * LIGHT_Y + nz * LIGHT_Z, 0.0)
    hx, hy, hz = normalize3(LIGHT_X - view_x, LIGHT_Y - view_y, LIGHT_Z - view_z)
    specular = max(nx * hx + ny * hy + nz * hz, 0.0) ** 24.0
    rim = (1.0 - max(nx * -view_x + ny * -view_y + nz * -view_z, 0.0)) ** 2.0
    shadow = soft_shadow(px + nx * 0.02, py + ny * 0.02, pz + nz * 0.02, time)
    ao = 1.0 - steps / MAX_STEPS * 0.35

    if material == MATERIAL_MIRROR:
        br, bg, bb = 0.95, 0.35, 0.22
        spec_weight = 0.95
    elif material == MATERIAL_RED:
        br, bg, bb = 0.95, 0.18, 0.1
        spec_weight = 0.45
    elif material == MATERIAL_BLUE:
        br, bg, bb = 0.1, 0.34, 1.0
        spec_weight = 0.45
    else:
        br, bg, bb = checker(px, pz)
        spec_weight = 0.45

    light = (0.12 + diffuse * shadow * 0.85) * ao
    cr = br * light + 1.0 * specular * shadow * spec_weight + 0.25 * rim * 0.18
    cg = bg * light + 0.92 * specular * shadow * spec_weight + 0.45 * rim * 0.18
    cb = bb * light + 0.78 * specular * shadow * spec_weight + 0.9 * rim * 0.18
    return cr, cg, cb


def soft_shadow(ox: float, oy: float, oz: float, time: float) -> float:
    result = 1.0
    dist = 0.04
    for _ in range(20):
        px = ox + LIGHT_X * dist
        py = oy + LIGHT_Y * dist
        pz = oz + LIGHT_Z * dist
        h = scene(px, py, pz, time)[0]
        if h < 0.001:
            return 0.12
        result = min(result, 10.0 * h / dist)
        dist += clamp(h, 0.025, 0.42)
        if dist > 7.0:
            break
    return clamp(result, 0.12, 1.0)


def checker(px: float, pz: float) -> tuple[float, float, float]:
    cell = (floor(px * 1.35) + floor(pz * 1.35)) & 1
    if cell == 0:
        return 0.24, 0.29, 0.33
    return 0.14, 0.18, 0.21


def sky(dy: float) -> tuple[float, float, float]:
    t = clamp(dy * 0.5 + 0.5, 0.0, 1.0)
    return (
        0.025 * (1.0 - t) + 0.28 * t,
        0.03 * (1.0 - t) + 0.38 * t,
        0.05 * (1.0 - t) + 0.55 * t,
    )


def tone_map(r: float, g: float, b: float) -> tuple[int, int, int]:
    r = r / (1.0 + r)
    g = g / (1.0 + g)
    b = b / (1.0 + b)
    return round(clamp(r, 0.0, 1.0) * 255), round(clamp(g, 0.0, 1.0) * 255), round(clamp(b, 0.0, 1.0) * 255)


def normalize3(x: float, y: float, z: float) -> tuple[float, float, float]:
    length = sqrt(x * x + y * y + z * z)
    if length <= 0.000001:
        return 0.0, 0.0, 0.0
    inv = 1.0 / length
    return x * inv, y * inv, z * inv


def cross3(ax: float, ay: float, az: float, bx: float, by: float, bz: float) -> tuple[float, float, float]:
    return ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx


def clamp(value: float, low: float, high: float) -> float:
    if value < low:
        return low
    if value > high:
        return high
    return value

