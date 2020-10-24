import random as rand
from .vector import Vec3

class Color(Vec3):
    def __init__(self, r=0, g=0, b=0):
        super().__init__(r, g, b)

    @classmethod
    def random(self):
        return Color(rand.random(),rand.random(),rand.random())

    @classmethod
    def white(self):
        return Color(1, 1, 1)

    @classmethod
    def black(self):
        return Color()

    @classmethod
    def red(self):
        return Color(1, 0, 0)

    @classmethod
    def green(self):
        return Color(0, 1, 0)

    @classmethod
    def blue(self):
        return Color(0, 0, 1)

    def __repr__(self):
        return (self.x, self.y, self.z).__repr__()

if __name__ == "__main__":
    print(Color().white())
    print(Color().black())
    print(Color().red())
    print(Color().green())
    print(Color().blue())