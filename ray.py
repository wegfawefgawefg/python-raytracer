class Ray:
    def __init__(self, origin, dir):
        self.origin = origin
        self.dir = dir.norm()