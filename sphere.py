from .vector import Vec3

import math

class Sphere:
    def __init__(self, center, radius, material, 
            orientation=Vec3(0, 0, 0).norm()):
        self.center = center
        self.radius = radius
        self.material = material
        self.orientation = orientation

    def intersects(self, ray):
        ''' if ray hits:
                returns distance to hit from ray origin
            else:
                returns None'''
        to_sphere = self.center - ray.origin
        t = to_sphere.dot(ray.dir)
        if t < 0:
            return None
        perp_center = ray.origin + ray.dir * t
        y = (perp_center - self.center).mag()
        if y > self.radius: #   miss
            return None
        elif y <= self.radius:  #   hit
            x = math.sqrt(self.radius**2 - y**2)
            t1 = t - x
            #   back of sphere
            #   t2 = t + x
            return t1

    def outward_normal(self, surface_point):
        return (surface_point - self.center).norm()

    def normal(self, light_ray, hit_pos):
        outward_normal = self.outward_normal(hit_pos)
        if light_ray.dot(outward_normal) < 0:
            return outward_normal
        else:
            return -outward_normal

    def get_hit_uv(self, hit_pos):
        hit_dir = (hit_pos - self.center).norm()
        
        u = 0.5 + math.atan2(hit_dir.x, hit_dir.z) / (2.0 * math.pi) + self.orientation.x
        v = 0.5 + math.asin(hit_dir.y) / math.pi + self.orientation.y
        return u, v