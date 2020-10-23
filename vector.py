import math
import random

class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def mag(self):
        return math.sqrt(
            self.x**2 +
            self.y**2 + 
            self.z**2) 

    def norm(self):
        mag = self.mag()
        if mag > 0:
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

    def __neg__(self):
        return self.clone() * -1

    def dot(self, vec2):
        return self.x * vec2.x + \
               self.y * vec2.y + \
               self.z * vec2.z

    def cross(self, vec2):
        return Vec3(
            self.y * vec2.z - self.z * vec2.y, 
            self.z * vec2.x - self.x * vec2.z, 
            self.x * vec2.y - self.y * vec2.x)

    def rotate_x(self, xrot):
        c = math.cos(xrot)
        s = math.sin(xrot)
        return Vec3(
            self.x, 
            self.y * c - self.z * s, 
            self.y * s + self.z * c)

    def rotate_y(self, yrot):
        c = math.cos(yrot)
        s = math.sin(yrot)
        return Vec3(
            self.x * c + self.z * s, 
            self.y, 
            -self.x * s + self.z * c)

    def rotate_z(self, zrot):
        c = math.cos(zrot)
        s = math.sin(zrot)
        return Vec3(
            self.x * c - self.y * s, 
            self.x * s + self.y * c, 
            self.z)

    def rotate(self, xrot, yrot, zrot):
        rot_vec = self.rotate_x(xrot)
        rot_vec = rot_vec.rotate_y(yrot)
        rot_vec = rot_vec.rotate_z(zrot)
        return rot_vec

    def plane_projection(self, plane_normal):
        orth_component = (
            self.dot(plane_normal) 
            / plane_normal.mag() ** 2
            * plane_normal
        )
        projection = self - orth_component
        return projection

    @classmethod
    def random(self, max_val=1.0):
        random_vec=Vec3(
            random.random() - 0.5, 
            random.random() - 0.5, 
            random.random() - 0.5)
        random_vec = random_vec * 2.0 * max_val
        return random_vec

    @classmethod
    def random_in_unit_sphere(self):
        while True:
            random_vec = Vec3.random()        
            if random_vec.mag() < 1:
                return random_vec

    @classmethod
    def random_unit_vector(self):
        a = random.random() * math.pi * 2
        z = (random.random() - 0.5) * 2
        r = math.sqrt(1 - z*z)
        return Vec3(r * math.cos(a), r * math.sin(a), z)

    def __repr__(self):
        return f"({self.x:5.3}, {self.y:5.3}, {self.z:5.3})"

    def clone(self):
        return Vec3(self.x, self.y, self.z)

if __name__ == "__main__":
    vec = Vec3(1,2,3) 
    vec2 = Vec3(4,5,6)
    print(vec, vec2)

    print("vec.mag(): {}".format(vec.mag()))
    print("vec + vec2: {} + {} = {}".format(vec, vec2, vec + vec2))
    print("vec - vec2: {} - {} = {}".format(vec, vec2, vec - vec2))
    print("vec.dot(vec2): {}.dot({}) = {}".format(vec, vec2, vec.dot(vec2)))
    print("vec.cross(): {}.cross({}) = {}".format(vec, vec2, vec.cross(vec2)))
    print("vec * num: {} * {} = {}".format(vec, 5.0, vec * 5.0))
    print("vec / num: {} / {} = {}".format(vec, 5.0, vec / 5.0))
    print("vec.norm(): {}".format(vec.norm()))
    print("vec.mag(): {}".format(vec.mag()))

    for i in range(10):
        print(Vec3.random_in_unit_sphere())