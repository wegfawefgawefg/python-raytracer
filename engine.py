from color import Color
from ray import Ray
from vector import Vec3
from image import Image
from tqdm import tqdm
import math
from line import Line

MIN_OFFSET = 0.001
SPECULAR_K = 80

def render(scene, 
        max_bounces=3, 
        antialiasing=False,
        samples=10,
        max_sample_displacement=0.001):
    width = scene.width
    height = scene.height
    cam = scene.cam
    img = Image(width, height)

    tl, right, down = create_viewing_plane(scene)
    for row in tqdm(range(height)):
        y_fraq = row / (height - 1)
        for col in range(width):
            # if row == int(scene.height / 2) \
            #         and int(col == scene.width / 2):
            #     tracking = True
            #     print("TRACKING")
            # if (width * row + col) % 10000 == 0:
            #     print("tracking")
            #     tracking = True
            # else:
            #     tracking = False
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

def draw_line(img, scene, start_x_frac, start_y_frac, end_x_frac, end_y_frac):
    width = scene.width - 1
    height = scene.height - 1
    start_x = int(start_x_frac * width)
    start_y = int(start_y_frac * height)
    
    end_x = int(end_x_frac * width)
    end_y = int(end_y_frac * height)

    int_x_dif = end_x - start_x
    int_y_dif = end_y - start_y

    if int_x_dif == 0 and int_y_dif == 0:
        end_x = max(min(end_x, scene.width - 1), 0)
        end_y = max(min(end_y, scene.height - 1), 0)
        img.pixels[end_y][end_x] = Vec3(255, 0, 0)
    elif int_x_dif == 0:
        less_y = min(start_y, end_y)
        more_y = max(start_y, end_y)
        for y in range(less_y, more_y + 1):
            if end_x < 0 or end_x > scene.width - 1 \
                    or y < 0 or y > scene.height - 1:
                break
            img.pixels[y][end_x] = Vec3(255, 0, 0)
    elif int_y_dif == 0:
        less_x = min(start_x, end_x)
        more_x = max(start_x, end_x)
        for x in range(less_x, more_x + 1):
            if x < 0 or x > scene.width - 1 \
                    or end_y < 0 or end_y > scene.height - 1:
                break
            img.pixels[end_y][x] = Vec3(255, 0, 0)
    else:
        x_delta = float(int_x_dif) / float(int_y_dif)
        less_y = min(start_y, end_y)
        more_y = max(start_y, end_y)
        for i, y in enumerate(range(less_y, more_y + 1)):            
            x = start_x + int(x_delta * i)
            if x < 0 or x > scene.width - 1 \
                    or y < 0 or y > scene.height - 1:
                break
            img.pixels[y][x] = Vec3(255 * x / end_x, 255 * y / more_y, 0)

def p_to_frac(p, scene, tl, top_norm, left_norm):
    p_start = -tl - p
    top_proj = p_start.dot(top_norm)
    left_proj = p_start.dot(left_norm)
    start_x_frac = top_proj / scene.viewplane_width
    start_y_frac = left_proj / scene.viewplane_height

    return start_x_frac, start_y_frac

def render_lines(img, scene, tl, right, down):
    view_plane_center = scene.cam.dir * scene.dist_to_viewplane
    top_norm = right.norm()
    left_norm = down.norm()

    for i, line in enumerate(scene.lines):
        projection = line.project(scene.cam.dir)
        # print(projection)
        #   localize points
        start_x_frac, start_y_frac = p_to_frac(projection.start + view_plane_center,
            scene, tl, top_norm, left_norm)
        end_x_frac, end_y_frac = p_to_frac(projection.end + view_plane_center,
            scene, tl, top_norm, left_norm)

        print(f"line {i}")
        print(f"start x y {start_x_frac}, {start_y_frac}")
        print(f"end   x y {end_x_frac}, {end_y_frac}")

        draw_line(img, scene, start_x_frac, start_y_frac, end_x_frac, end_y_frac)


def raytrace(ray, scene, samples, max_bounces, tracking):
    color = Color()
    color += raytrace_inner(ray, scene, samples, 0, max_bounces, tracking)
    return color

def raytrace_inner(ray, scene, samples, depth, max_depth, tracking):
    if depth == max_depth:
        return Color()

    dist, obj_hit = nearest_intersection(ray, scene)
    if obj_hit is None:
        # return Vec3(0.5, 0.5, 0.5)
        t = 0.5*(ray.dir.y + 1.0)
        return ((1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)) * 255
        # return Color()
    hit_pos = ray.origin + ray.dir * dist
    hit_normal = obj_hit.normal(ray.dir, hit_pos)

    if tracking:
        scene.lines.append(
            Line(
                start=ray.origin, 
                end=ray.dir
            )
        )
    color = color_at(obj_hit, hit_pos, hit_normal, scene)

    '''lambertian diffuse reflection'''
    new_ray = Ray(
        origin=hit_pos + hit_normal * MIN_OFFSET,
        dir=hit_normal + Vec3.random_in_unit_sphere()
    )

    '''true reflection'''
    # new_ray = Ray(  #   bounce ray
    #     origin=hit_pos + hit_normal * MIN_OFFSET,
    #     dir=ray.dir - (2 * ray.dir.dot(hit_normal)) * hit_normal)

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
    material = obj_hit.material
    u, v = obj_hit.get_hit_uv(hit_pos)
    obj_color = material.color_at(u, v, hit_pos)
    to_cam = scene.cam.origin - hit_pos

    # color = material.ambient * obj_color
    color = Vec3()
    # for light in scene.lights:
    #     to_light = Ray(hit_pos, light.pos - hit_pos)
    #     half_vector = (to_light.dir + to_cam).norm()

        # ''' Diffuse shading (Lambert) '''
        # color += (
        #     obj_color
        #     * material.diffuse
        #     * max(hit_normal.dot(to_light.dir), 0)
        # )

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