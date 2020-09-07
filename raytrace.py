from color import Color
# from image import Image
from vector import Vec3
from PIL import Image

from vector import Vec3
from sphere import Sphere
from engine import RenderEngine
from scene import Scene
from light import Light
from material import Material

def main():
    # WIDTH, HEIGHT = 1920, 1080
    # WIDTH, HEIGHT = 500, 500
    WIDTH, HEIGHT = 200, 200
    
    cam = Vec3(0, 0, -4)
    
    NUM_SPHERES = 3
    objects = []
    for i in range(NUM_SPHERES):
        new_obj = Sphere(
            center=Vec3(
                x=-1 + i, 
                y=0.0,
                z=1.0 + i),
            radius=0.1 * (i + 1),
            material=Material(
                color=(Color().red(), Color().green(), Color().blue())[i],
                ambient=0.05,
                diffuse=0.1 + 0.3 * (i+1),
                specular=0.1 + 0.3 * (i+1))
        )
        objects.append(new_obj)

    NUM_LIGHTS = 4
    lights = []
    for i in range(NUM_LIGHTS):
        new_light = Light(
            pos=Vec3(
                x=-5 + 2 * i, 
                y=-5 + 3 * i, 
                z=-1.0),
            color=(Color().white(), Color().red(), Color().green(), Color().blue())[i])
        lights.append(new_light)

    scene = Scene(cam, objects, lights, WIDTH, HEIGHT)
    engine = RenderEngine()
    img = engine.render(scene)
    # img.write_as_ppm("raytrace_demo")

    file_image = Image.new('RGB', (WIDTH, HEIGHT), color = 'black')
    pixels = file_image.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixels[x, y] = (
                int(min(img.pixels[y][x].x, 255)), 
                int(min(img.pixels[y][x].y, 255)), 
                int(min(img.pixels[y][x].z, 255)))

    file_image.show()

if __name__ == "__main__":
    main()
