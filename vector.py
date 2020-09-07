import math

class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def mag(self):
        return math.sqrt(
            self.x**2 +
            self.y**2 + 
            self.z**2)

    def norm(self):
        mag = self.mag()
        self.x = self.x / mag
        self.y = self.y / mag
        self.z = self.z / mag
        return self

    def __add__(self, other):
        return Vec3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z)

    def __sub__(self, other):
        return Vec3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z)

    def __mul__(self, other):
        assert not isinstance(other, Vec3)
        return Vec3(
            self.x * other,
            self.y * other,
            self.z * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        assert not isinstance(other, Vec3)
        return Vec3(
            self.x / other, 
            self.y / other, 
            self.x / other)

    def dot(self, vec2):
        return self.x * vec2.x + \
               self.y * vec2.y + \
               self.z * vec2.z

    def __repr__(self):
        return (self.x, self.y, self.z).__repr__()

if __name__ == "__main__":
    vec = Vec3(1,2,3) 
    vec2 = Vec3(4,5,6)
    print(vec, vec2)

    print("vec.mag(): {}".format(vec.mag()))
    print("vec + vec2: {} + {} = {}".format(vec, vec2, vec + vec2))
    print("vec - vec2: {} - {} = {}".format(vec, vec2, vec - vec2))
    print("vec.dot(vec2): {}.dot({}) = {}".format(vec, vec2, vec.dot(vec2)))
    print("vec * num: {} * {} = {}".format(vec, 5.0, vec * 5.0))
    print("vec / num: {} / {} = {}".format(vec, 5.0, vec / 5.0))
    print("vec.norm(): {}".format(vec.norm()))
    print("vec.mag(): {}".format(vec.mag()))
