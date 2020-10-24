from .vector import Vec3

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def project(self, plane_normal):
        return Line(
            start=self.start.plane_projection(plane_normal), 
            end=self.end.plane_projection(plane_normal))

    def __repr__(self):
        return f"Line( s: {self.start} e: {self.end} )"


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