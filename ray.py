class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.dir = direction.norm()