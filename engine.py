from color import Color
from ray import Ray
from vector import Vec3
from image import Image
from tqdm import tqdm
import math

MIN_OFFSET = 0.001
SPECULAR_K = 80

def render(scene, 
        max_bounces=3, 
        antialiasing=False,
        samples=2,
        max_sample_displacement=0.001):
    width = scene.width
    height = scene.height
    cam = scene.cam
    img = Image(width, height)

    tl, right, down = create_viewing_plane(scene)
    for row in tqdm(range(height)):
        y_fraq = row / (height - 1)
        for col in range(width):
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
                    color += raytrace(ray, scene, samples, max_bounces)
                color = color / samples
                img.pixels[row][col] = color
            else:
                ray = Ray(
                    origin=cam.origin, 
                    dir=plane_target-cam.origin)
                img.pixels[row][col] = raytrace(ray, scene, samples, max_bounces)

    render_lines(img, scene)
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

def render_lines(self, scene):
    view_plane_center = scene.cam.dir * scene.dist_to_viewplane
    for line in scene.lines:
        projection = line.project(scene.cam.dir)
        print(projection)


def raytrace(ray, scene, samples, max_bounces):
    color = Color()
    color += raytrace_inner(ray, scene, samples, 0, max_bounces)
    return color

def raytrace_inner(ray, scene, samples, depth, max_depth):
    if depth == max_depth:
        return Color()

    dist, obj_hit = nearest_intersection(ray, scene)
    if obj_hit is None:
        return Color()
    hit_pos = ray.origin + ray.dir * dist
    hit_normal = obj_hit.normal(ray.dir, hit_pos)
    color = color_at(obj_hit, hit_pos, hit_normal, scene)

    '''lambertian diffuse reflection'''
    new_ray = Ray(
        origin=hit_pos + hit_normal * MIN_OFFSET,
        dir=hit_pos + hit_normal * MIN_OFFSET + hit_normal + Vec3.random_in_unit_sphere()
    )

    '''true reflection'''
    # new_ray = Ray(  #   bounce ray
    #     origin=hit_pos + hit_normal * MIN_OFFSET,
    #     dir=ray.dir - (2 * ray.dir.dot(hit_normal)) * hit_normal)

    for _ in range(samples):
        color += raytrace_inner(new_ray, scene, samples, depth + 1, max_depth) * 0.5#\
            # * obj_hit.material.reflection
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
    material = obj_hit.material
    u, v = obj_hit.get_hit_uv(hit_pos)
    obj_color = material.color_at(u, v, hit_pos)
    to_cam = scene.cam.origin - hit_pos

    # color = material.ambient * obj_color
    color = Vec3()
    for light in scene.lights:
        to_light = Ray(hit_pos, light.pos - hit_pos)
    #     half_vector = (to_light.dir + to_cam).norm()

        # ''' Diffuse shading (Lambert) '''
        color += (
            obj_color
            * material.diffuse
            * max(hit_normal.dot(to_light.dir), 0)
        )

        # '''faux light'''
        # t

        # Specular shading (Blinn-Phong)
        # color += (
        #     light.color
        #     * material.specular
        #     * max(hit_normal.dot(half_vector), 0) ** SPECULAR_K
        # )

        #   normal visualization
        # color += (hit_normal + Vec3(1, 1, 1)) * 0.5 * 255
    return color