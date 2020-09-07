import math

class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersects(self, ray):
        sphere_to_ray = ray.origin - self.center

        #a = 1
        b = 2 * ray.dir.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - self.radius ** 2.0
        disc = b * b - 4 * c

        if disc >= 0.0:
            dist =  (-b - math.sqrt(disc)) / 2.0
            if dist > 0:
                return dist
        else:
            return None

    def normal(self, surface_point):
        return (surface_point - self.center).norm()

