from __future__ import annotations

from math import cos, floor, sin

from python_raytracer.vec3 import Vec3

MAX_STEPS = 96
MAX_DIST = 8.0
SURFACE_DIST = 0.0008
NORMAL_EPS = 0.002

MATERIAL_MIRROR = "mirror"
MATERIAL_RED = "red"
MATERIAL_BLUE = "blue"
MATERIAL_FLOOR = "floor"

LIGHT_DIR = Vec3(-0.35, 0.82, -0.52).normalize()


class Raymarcher:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.aspect = width / height

    def render_into(self, pixels: bytearray, time: float) -> None:
        offset = 0
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.color_at(x, y, time)
                pixels[offset] = r
                pixels[offset + 1] = g
                pixels[offset + 2] = b
                pixels[offset + 3] = 255
                offset += 4

    def color_at(self, x: int, y: int, time: float) -> tuple[int, int, int]:
        u = ((x + 0.5) / self.width) * 2.0 - 1.0
        v = 1.0 - ((y + 0.5) / self.height) * 2.0
        u *= self.aspect

        camera = orbit_camera(time)
        direction = ray_direction(camera, Vec3(0.0, 0.15, 0.0), u, v)
        color = trace(camera, direction, time, 0)
        return tone_map(color)


def color_at(width: int, height: int, x: int, y: int, time: float) -> tuple[int, int, int]:
    return Raymarcher(width, height).color_at(x, y, time)


def orbit_camera(time: float) -> Vec3:
    orbit = 2.9
    yaw = time * 0.35
    return Vec3(
        orbit * cos(yaw),
        0.9 + 0.15 * sin(time * 0.17),
        orbit * sin(yaw),
    )


def ray_direction(camera: Vec3, target: Vec3, u: float, v: float) -> Vec3:
    forward = (target - camera).normalize()
    right = forward.cross(Vec3(0, 1, 0)).normalize()
    up = right.cross(forward)
    return (forward * 2.0 + right * u + up * v).normalize()


def trace(origin: Vec3, direction: Vec3, time: float, depth: int) -> Vec3:
    hit, distance, steps, material = march(origin, direction, time)
    if not hit:
        return sky(direction)

    point = origin + direction * distance
    normal = estimate_normal(point, time)
    color = shade(point, normal, direction, material, steps, time)

    if material == MATERIAL_MIRROR and depth < 1:
        reflected = reflect(direction, normal).normalize()
        reflection = trace(point + normal * 0.025, reflected, time, depth + 1)
        color = color * 0.35 + reflection * 0.65

    return color


def march(origin: Vec3, direction: Vec3, time: float) -> tuple[bool, float, int, str | None]:
    distance = 0.0
    material = None
    for step in range(MAX_STEPS):
        point = origin + direction * distance
        sdf, material = scene(point, time)
        if sdf < SURFACE_DIST:
            return True, distance, step, material
        distance += sdf
        if distance > MAX_DIST:
            break
    return False, distance, MAX_STEPS, material


def scene(point: Vec3, time: float) -> tuple[float, str]:
    center_sphere = wobbly_sphere(point, Vec3(0.0, 0.35, 0.0), 1.0, time)
    left_sphere = sphere(point - Vec3(-1.45, -0.28, 0.85), 0.32)
    right_sphere = sphere(point - Vec3(1.25, -0.35, -0.75), 0.28)
    floor_dist = point.y + 1.0

    nearest = [
        (center_sphere, MATERIAL_MIRROR),
        (left_sphere, MATERIAL_RED),
        (right_sphere, MATERIAL_BLUE),
        (floor_dist, MATERIAL_FLOOR),
    ]
    return min(nearest, key=lambda sample: sample[0])


def sphere(point: Vec3, radius: float) -> float:
    return point.length() - radius


def wobbly_sphere(point: Vec3, center: Vec3, radius: float, time: float) -> float:
    local = point - center
    return (
        local.length()
        - radius
        + sin(local.x * 12.0 + time * 1.4) * 0.025
        + cos(local.y * 13.0 + time * 1.1) * 0.025
    )


def estimate_normal(point: Vec3, time: float) -> Vec3:
    e = NORMAL_EPS
    dx = scene(point + Vec3(e, 0, 0), time)[0] - scene(point - Vec3(e, 0, 0), time)[0]
    dy = scene(point + Vec3(0, e, 0), time)[0] - scene(point - Vec3(0, e, 0), time)[0]
    dz = scene(point + Vec3(0, 0, e), time)[0] - scene(point - Vec3(0, 0, e), time)[0]
    return Vec3(dx, dy, dz).normalize()


def shade(point: Vec3, normal: Vec3, view_dir: Vec3, material: str | None, steps: int, time: float) -> Vec3:
    diffuse = max(normal.dot(LIGHT_DIR), 0.0)
    half_vec = (LIGHT_DIR - view_dir).normalize()
    specular = max(normal.dot(half_vec), 0.0) ** 24.0
    rim = (1.0 - max(normal.dot(-view_dir), 0.0)) ** 2.0
    shadow = soft_shadow(point + normal * 0.02, time)
    ao = 1.0 - steps / MAX_STEPS * 0.35

    if material == MATERIAL_MIRROR:
        base = Vec3(0.95, 0.35, 0.22)
        spec_weight = 0.95
    elif material == MATERIAL_RED:
        base = Vec3(0.95, 0.18, 0.1)
        spec_weight = 0.45
    elif material == MATERIAL_BLUE:
        base = Vec3(0.1, 0.34, 1.0)
        spec_weight = 0.45
    else:
        base = checker(point)
        spec_weight = 0.45

    color = base * ((0.12 + diffuse * shadow * 0.85) * ao)
    color += Vec3(1.0, 0.92, 0.78) * specular * shadow * spec_weight
    color += Vec3(0.25, 0.45, 0.9) * rim * 0.18
    return color


def soft_shadow(origin: Vec3, time: float) -> float:
    result = 1.0
    distance = 0.04

    for _ in range(20):
        point = origin + LIGHT_DIR * distance
        h = scene(point, time)[0]
        if h < 0.001:
            return 0.12
        result = min(result, 10.0 * h / distance)
        distance += clamp(h, 0.025, 0.42)
        if distance > 7.0:
            break

    return clamp(result, 0.12, 1.0)


def checker(point: Vec3) -> Vec3:
    cell = (floor(point.x * 1.35) + floor(point.z * 1.35)) & 1
    if cell == 0:
        return Vec3(0.24, 0.29, 0.33)
    return Vec3(0.14, 0.18, 0.21)


def sky(direction: Vec3) -> Vec3:
    t = clamp(direction.y * 0.5 + 0.5, 0.0, 1.0)
    return Vec3(0.025, 0.03, 0.05) * (1.0 - t) + Vec3(0.28, 0.38, 0.55) * t


def reflect(direction: Vec3, normal: Vec3) -> Vec3:
    return direction - normal * (2.0 * direction.dot(normal))


def tone_map(color: Vec3) -> tuple[int, int, int]:
    r = color.x / (1.0 + color.x)
    g = color.y / (1.0 + color.y)
    b = color.z / (1.0 + color.z)
    return round(clamp(r, 0.0, 1.0) * 255), round(clamp(g, 0.0, 1.0) * 255), round(clamp(b, 0.0, 1.0) * 255)


def clamp(value: float, low: float, high: float) -> float:
    if value < low:
        return low
    if value > high:
        return high
    return value
