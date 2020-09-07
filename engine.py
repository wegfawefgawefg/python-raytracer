from color import Color
from ray import Ray
from vector import Vec3
from image import Image
from tqdm import tqdm

class RenderEngine:
    def render(self, scene):
        width = scene.width
        height = scene.height
        cam = scene.cam
        img = Image(width, height)

        aspect_ratio = float(width) / height

        PLANE_Z = 0
        x0 = -1.0
        x1 = 1.0
        x_delta = (x1 - x0) / (width - 1)

        y0 = -1.0 / aspect_ratio
        y1 = 1.0 / aspect_ratio
        y_delta = (y1 - y0) / (height - 1)

        y = y0 - y_delta
        for row in tqdm(range(height)):
            y += y_delta
            x = x0 - x_delta
            for col in range(width):
                x += x_delta

                plane_target = Vec3(x, y, PLANE_Z)
                ray = Ray(
                    origin=cam, 
                    direction=plane_target-cam)

                img.pixels[row][col] = self.raytrace(ray, scene)

        return img

    def raytrace(self, ray, scene):
        color = Color()
        dist, obj_hit = self.nearest_intersection(ray, scene)
        if obj_hit is None:
            return color
        hit_pos = ray.origin + ray.dir * dist
        hit_normal = obj_hit.normal(hit_pos)
        color += self.color_at(obj_hit, hit_pos, hit_normal, scene)
        return color

    def nearest_intersection(self, ray, scene):
        min_dist = 0.0
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None:
                if obj_hit is None or dist < min_dist:
                    min_dist = dist
                    obj_hit = obj

        return min_dist, obj_hit

    def color_at(self, obj_hit, hit_pos, hit_normal, scene):
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        to_cam = scene.cam - hit_pos
        specular_k = 50

        color = material.ambient * Color()
        for light in scene.lights:
            to_light = Ray(hit_pos, light.pos - hit_pos)
            # Diffuse shading (Lambert)
            color += (
                obj_color
                * material.diffuse
                * max(hit_normal.dot(to_light.dir), 0)
            )
            # Specular shading (Blinn-Phong)
            half_vector = (to_light.dir + to_cam).norm()
            color += (
                light.color
                * material.specular
                * max(hit_normal.dot(half_vector), 0) ** specular_k
            )
        return color