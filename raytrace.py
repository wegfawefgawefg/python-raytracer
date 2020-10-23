from color import Color
from image import Image
from vector import Vec3
import engine as Engine
from scene import Scene
from texture import ColorTexture
from ray import Ray

def main():
    # WIDTH, HEIGHT = 200, 200
    WIDTH, HEIGHT = 300, 200
    # WIDTH, HEIGHT = 500, 500
    # WIDTH, HEIGHT = 1920, 1080
    # WIDTH, HEIGHT = 4096, 2160
    # WIDTH, HEIGHT = 7680, 4320
    
    cam = Ray(
        origin=Vec3(0, 0, 0),
        dir=Vec3(0, 0, -1))

    # cam = Vec3(0, 0, -4)

    scene = Scene(WIDTH, HEIGHT, cam)
    img = Engine.render(scene)
    img.write_as_png("render", show_when_done=True)
    # img.show()

if __name__ == "__main__":
    main()
