from vector import Vec3
from sphere import Sphere
from light import Light
from material import *
from texture import ColorTexture
from ray import Ray
from color import Color
from line import Line

class Scene:
    def __init__(self, width, height, cam, objects=[], lights=[], lines=[]):
        self.cam = cam
        self.objects = objects
        self.lights = lights
        self.lines = lines
        self.width = width
        self.height = height
        self.aspect_ratio = float(width) / float(height)
        self.dist_to_viewplane = 1
        self.viewplane_height = 2
        self.viewplane_width = self.viewplane_height * self.aspect_ratio
        self.moon_and_friends_with_sky()

    def moon_and_friends_with_sky(self):
        # moon_texture = ColorTexture("textures\lroc_color_poles_2k.tif")
        # moon_texture = ColorTexture("textures\lroc_color_poles_4k.tif")
        # kirby_texture = ColorTexture("textures\kirbigger2.png")
        # sphere_texture = moon_texture

        objects = []
        NUM_SPHERES = 3
        for i in range(1, NUM_SPHERES):
            new_obj = Sphere(
                center=Vec3(
                    x=-0.5 - 1 + i, 
                    y=0.0,
                    z=-1.0),
                radius=0.1 * (i + 1),
                material=DiffuseMaterial(
                    color=Color().randomize(),
                    ambient=0.3,
                    diffuse=0.1,
                    specular=0.1,
                    reflection=0.8)
                # material=TexturedMaterial(
                #     color_texture=moon_texture,
                #     ambient=0.3,
                #     diffuse=1.0,
                #     specular=0.0, 
                #     reflection=0.7,),
            )
            objects.append(new_obj)

        # center_sphere = Sphere(
        #     center=Vec3(
        #         x=0, 
        #         y=-0.1,
        #         z=-1.0),
        #     radius=0.4,
        #     material=IdealMaterial(
        #         color=Color().randomize(),
        #         ambient=0.1,
        #         diffuse=0.5,
        #         specular=0.1,
        #         reflection=0.8
        #     )
        # )
        # objects.append(center_sphere)

        # ground_sphere = Sphere(
        #     center=Vec3(
        #         x=0.0, 
        #         y=-100.5,
        #         z=0.0),
        #     radius=100.0,
        #     material=IdealMaterial(
        #         color=Color().randomize(),
        #         ambient=0.5,
        #         diffuse=0.5,
        #         specular=0.0, 
        #         reflection=0.5
        #     )
        # )
        # objects.append(ground_sphere)

        # moon_sphere = Sphere(
        #     center=Vec3(
        #         x=0, 
        #         y=0.5,
        #         z=-1.0),
        #     radius=0.4,
        #     material=TexturedMaterial(
        #         color_texture=moon_texture,
        #         ambient=0.01,
        #         diffuse=0.3,
        #         specular=0.1, 
        #         reflection=0.8,),
        #     orientation=Vec3(0.43, -0.1, 0.0)
        # )
        # objects.append(moon_sphere)

        ground_sphere = Sphere(
            center=Vec3(
                x=0.0, 
                y=-100.5,
                z=0.0),
            radius=100.0,
            material=CheckMaterial(
                ambient=1.0,
                diffuse=1.0,
                specular=0.0, 
                reflection=0.8
            )
        )
        objects.append(ground_sphere)

        # sky_sphere = Sphere(
        #     center=Vec3(
        #         x=0.0, 
        #         y=0.0,
        #         z=2000),
        #     radius=1000.0,
        #     material=Material(
        #             color=Color(18,204,255),
        #             ambient=0.1,
        #             diffuse=1.0,
        #             specular=0.0, 
        #             reflection=0.6
        #     )
        # )
        # objects.append(sky_sphere)

        lights = []
        # NUM_LIGHTS = 4
        # for i in range(NUM_LIGHTS):
        #     new_light = Light(
        #         pos=Vec3(
        #             x=-5 + 2 * i, 
        #             y=-5 + 3 * i, 
        #             # x=-50 + 3 * i, 
        #             # y=100 + 3 * i, 
        #             z=1.0),
        #         color=(Color().white(), Color().red(), Color().green(), Color().blue())[i])
        #     lights.append(new_light)

        new_light = Light(
            pos=Vec3(0.0, 10.0, 100.0)
        )
        lights.append(new_light)

        lines = []
        # lines.append(
        #     Line(
        #         start=Vec3(0.0, 0.0, 0.0),
        #         end=Vec3(1.0, 0.0, 0.0))
        # )
        # lines.append(
        #     Line(
        #         start=Vec3(0.0, 0.0, 0.0),
        #         end=Vec3(0.0, 1.0, 0.0))
        # )
        # lines.append(
        #     Line(
        #         start=Vec3(0.0, 0.0, 0.0),
        #         end=Vec3(0.0, 0.0, 1.0))
        # )
        # for y in range(10):
        #     for x in range(10):
        #         lines.append(
        #             Line(
        #                 start=Vec3(
        #                     x=0.0, 
        #                     y=0.0, 
        #                     z=-2),
        #                 end=Vec3(
        #                     x=-0.5 + 0.1*x, 
        #                     y=-0.5 + 0.1*y, 
        #                     z=-2))
        #         )



        self.objects = objects
        self.lights = lights
        self.lines = lines