import random
from vector import Vec3

class Color(Vec3):
    def __init__(self, r=0, g=0, b=0):
        super().__init__(r, g, b)

    def randomize(self):
        self.x = random.randint(0, 255)
        self.y = random.randint(0, 255)
        self.z = random.randint(0, 255)
        return self

    def white(self):
        self.x = 255
        self.y = 255
        self.z = 255
        return self

    def black(self):
        self.x = 0
        self.y = 0
        self.z = 0
        return self

    def red(self):
        self.x = 255
        self.y = 0
        self.z = 0
        return self

    def green(self):
        self.x = 0
        self.y = 255
        self.z = 0
        return self

    def blue(self):
        self.x = 0
        self.y = 0
        self.z = 255
        return self

    def __repr__(self):
        return (self.x, self.y, self.z).__repr__()

if __name__ == "__main__":
    print(Color().white())
    print(Color().black())
    print(Color().red())
    print(Color().green())
    print(Color().blue())