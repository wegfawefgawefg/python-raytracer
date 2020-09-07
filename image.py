from color import Color

class Image:
    def __init__(self, width=320, height=200):
        self.width = width
        self.height = height
        self.pixels = [[Color() for col in range(width)] for row in range(height)] 

    def randomize(self):
        for row in self.pixels:
            for col in row:
                col.randomize()

    def write_as_ppm(self, file_name):
        file_name_with_ext = file_name + ".ppm"
        with open(file_name_with_ext, "w") as img:
            img.write("P3 {} {}\n".format(self.width, self.height))
            img.write("255\n")
            for row in self.pixels:
                for pixel in row:
                    img.write("{} {} {}\t".format(
                        pixel.x, pixel.y, pixel.z))
                img.write("\n")
            img.close()

if __name__ == "__main__":
    img = Image()
    img.randomize()
    img.write_as_ppm("pic")