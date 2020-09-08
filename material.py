from color import Color

class Material:
    def __init__(self, 
            color=Color().white(),
            ambient=0.05,
            diffuse=1.0, 
            specular=1.0,
            reflection=0.5):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, pos):
        return self.color

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

    def color_at(self, pos):
        if int((pos.x + 5.0) * 3.0) % 2 == int(pos.z * 3.0) % 2:
            return self.color_one
        return self.color_two