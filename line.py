from vector import Vec3

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def project(self, plane_normal):
        return Line(
            start=self.start.plane_projection(plane_normal), 
            end=self.end.plane_projection(plane_normal))

    def __repr__(self):
        return f"Line( s: {self.start} e: {self.end} )"

