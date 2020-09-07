class Scene:
    def __init__(self, cam, objects, lights, width, height):
        self.cam = cam
        self.objects = objects
        self.lights = lights
        self.width = width
        self.height = height