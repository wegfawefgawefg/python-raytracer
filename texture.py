from .color import Color

from PIL import Image

class ColorTexture:
    def __init__(self, texture_file):
        im = Image.open(texture_file)
        self.width, self.height = im.size
        
        im_pixels = im.load()
        pixels = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                pix = im_pixels[x, y]
                row.append(Color(r=pix[0], g=pix[1], b=pix[2]))
            pixels.append(row)
        self.pixels = pixels


    def color_at(self, u, v):
        x = int((u % 1.0) * (self.width - 1))
        y = int((v % 1.0) * (self.height - 1))
        return self.pixels[y][x]
    