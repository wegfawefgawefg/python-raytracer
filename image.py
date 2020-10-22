from color import Color
from PIL import Image as PImage

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

    def to_pimage(self):
        file_image = PImage.new('RGB', (self.width, self.height), color = 'black')
        pixels = file_image.load()
        for y in range(self.height):
            for x in range(self.width):
                pixels[x, y] = (
                    int(min(self.pixels[y][x].x, 255)), 
                    int(min(self.pixels[y][x].y, 255)), 
                    int(min(self.pixels[y][x].z, 255)))

        return file_image

    def write_as_png(self, file_name, show_when_done=False):
        file_image = self.to_pimage()
        file_image.save(file_name + ".png")
        if show_when_done:
            file_image.show()

    def show(self):
        file_image = self.to_pimage()
        file_image.show()

if __name__ == "__main__":
    img = Image()
    img.randomize()
    img.write_as_ppm("pic")