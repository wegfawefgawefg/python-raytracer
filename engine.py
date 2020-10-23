from color import Color
from ray import Ray
from vector import Vec3
from image import Image
from tqdm import tqdm
import math
from line import *

SPECULAR_K = 80

def render(scene, 
        max_bounces=3, 
        antialiasing=False,
        samples=30,
        max_sample_displacement=0.001):
    width = scene.width
    height = scene.height
    cam = scene.cam
    img = Image(width, height)

    tl, right, down = create_viewing_plane(scene)
    for row in tqdm(range(height)):
        y_fraq = row / (height - 1)
        for col in range(width):
            tracking = False
            x_fraq = col / (width - 1)
            plane_target = tl + y_fraq * down + x_fraq * right
            if antialiasing:
                color = Vec3()
                for _ in range(samples):
                    noisy_plane_target = plane_target + Vec3.random(
                        max_val=max_sample_displacement)
                    ray = Ray(
                        origin=cam.origin, 
                        dir=noisy_plane_target-cam.origin)
                    color += raytrace(ray, scene, samples, max_bounces, tracking)
                color = color / samples
                img.pixels[row][col] = color
            else:
                ray = Ray(
                    origin=cam.origin, 
                    dir=plane_target-cam.origin)
                img.pixels[row][col] = raytrace(ray, scene, samples, max_bounces, tracking)

    render_lines(img, scene, tl, right, down)
    return img

def create_viewing_plane(scene):
    cam = scene.cam
    half_pi = math.pi/2
    left_vec = cam.dir.rotate_y(half_pi).norm()
    up_vec = cam.dir.rotate_x(half_pi).norm()

    view_plane_spot = cam.dir * scene.dist_to_viewplane
    up_vec = up_vec * (scene.viewplane_height / 2)
    left_vec = left_vec * (scene.viewplane_width / 2)

    right_vec = -left_vec * 2
    down_vec = -up_vec * 2

    tl = view_plane_spot + left_vec + up_vec
    return tl, right_vec, down_vec

def raytrace(ray, scene, samples, max_bounces, tracking):
    color = Color()
    color += raytrace_inner(ray, scene, samples, 0, max_bounces, tracking)
    return color

def raytrace_inner(ray, scene, samples, depth, max_depth, tracking):
    if depth == max_depth:
        return Color()

    dist, obj_hit = nearest_intersection(ray, scene)

    ''' MISS    '''
    if obj_hit is None:
        t = 0.5*(ray.dir.y + 1.0)
        return ((1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)) * 255
        # return Color()
    
    ''' HIT     ''' 
    hit_pos = ray.origin + ray.dir * dist
    hit_normal = obj_hit.normal(ray.dir, hit_pos)

    if tracking:
        scene.lines.append(Line(start=ray.origin, end=ray.dir))

    color = color_at(obj_hit, hit_pos, hit_normal, scene)
    new_ray = obj_hit.material.bounce(ray, hit_pos, hit_normal)

    for _ in range(samples):
        color += raytrace_inner(new_ray, scene, samples, depth + 1, max_depth, tracking) \
            * obj_hit.material.reflection
    color = color / samples
    return color

def nearest_intersection(ray, scene):
    min_dist = 0.0
    obj_hit = None
    for obj in scene.objects:
        dist = obj.intersects(ray)
        if dist is not None:
            if obj_hit is None or dist < min_dist:
                min_dist = dist
                obj_hit = obj

    return min_dist, obj_hit

def color_at(obj_hit, hit_pos, hit_normal, scene):
    u, v = obj_hit.get_hit_uv(hit_pos)
    obj_color = obj_hit.material.color_at(u, v, hit_pos) \
        * obj_hit.material.ambient

    to_cam = scene.cam.origin - hit_pos

    ''' ADDITIONAL LIGHT MODELS'''
    color = Color()
    for light in scene.lights:
        to_light = Ray(hit_pos, light.pos - hit_pos)
        half_vector = (to_light.dir + to_cam).norm()

        ''' Diffuse shading (Lambert) '''
        color += (
            obj_color
            * obj_hit.material.diffuse
            * max(hit_normal.dot(to_light.dir), 0)
        )

        '''Specular shading (Blinn-Phong)'''
        color += (
            light.color
            * obj_hit.material.specular
            * max(hit_normal.dot(half_vector), 0) ** SPECULAR_K
        )

        '''normal visualization'''
        # color += (hit_normal + Vec3(1, 1, 1)) * 0.5 * 255
    return color