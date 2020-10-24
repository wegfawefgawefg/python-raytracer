from .color import Color
from .vector import Vec3
from .ray import Ray

MIN_OFFSET = 0.001

class IdealMaterial:
    def __init__(self, 
            color=Color().white(),
            ambient=1.0,
            diffuse=1.0, 
            specular=1.0,
            reflection=0.5):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, u, v, pos):
        return self.color

    def bounce(self, ray, hit_pos, hit_normal):
        '''perfect mirror reflection'''
        return Ray(
            origin=hit_pos + hit_normal * MIN_OFFSET,
            dir=ray.dir - (2 * ray.dir.dot(hit_normal)) * hit_normal)

class MetalMaterial:
    def __init__(self, 
            color=Color().white(),
            ambient=1.0,
            diffuse=1.0, 
            specular=1.0,
            reflection=0.5,
            fuzz_radius=0.1):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.fuzz_radius = fuzz_radius

    def color_at(self, u, v, pos):
        return self.color

    def bounce(self, ray, hit_pos, hit_normal):
        '''perfect mirror reflection with noise'''
        bounce_dir = ray.dir - (2 * ray.dir.dot(hit_normal)) * hit_normal
        bounce_dir = bounce_dir + Vec3.random_in_unit_sphere() * self.fuzz_radius
        return Ray(
            origin=hit_pos + hit_normal * MIN_OFFSET,
            dir=bounce_dir)

class DiffuseMaterial:
    def __init__(self, 
            color=Color().white(),
            ambient=1.0,
            diffuse=1.0, 
            specular=1.0,
            reflection=0.5):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, u, v, pos):
        return self.color

    def bounce(self, ray, hit_pos, hit_normal):
        '''lambertian diffuse reflection'''
        return Ray(
            origin=hit_pos + hit_normal * MIN_OFFSET,
            dir=hit_normal + Vec3.random_unit_vector()
        )

class CheckMaterial:
    def __init__(self, 
            color_one=Color().white(),
            color_two=Color(),
            ambient=0.05,
            diffuse=1.0, 
            specular=1.0,
            reflection=0.5):
        self.color_one = color_one
        self.color_two = color_two
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, u, v, pos):
        if int((pos.x + 5.0) * 3.0) % 2 == int(pos.z * 3.0) % 2:
            return self.color_one
        return self.color_two

    def bounce(self, ray, hit_pos, hit_normal):
        '''perfect mirror reflection'''
        return Ray(
            origin=hit_pos + hit_normal * MIN_OFFSET,
            dir=ray.dir - (2 * ray.dir.dot(hit_normal)) * hit_normal)

class TexturedMaterial:
    def __init__(self, 
            color_texture,
            ambient=0.3,
            diffuse=0.7, 
            specular=0.4,
            reflection=0.05):
        self.color_texture = color_texture
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, u, v, pos):
        return self.color_texture.color_at(u, v)

    def bounce(self, ray, hit_pos, hit_normal):
        '''perfect mirror reflection'''
        return Ray(
            origin=hit_pos + hit_normal * MIN_OFFSET,
            dir=ray.dir - (2 * ray.dir.dot(hit_normal)) * hit_normal)