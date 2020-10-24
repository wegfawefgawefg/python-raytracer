from .color import Color

class Light:
    def __init__(self, pos, color=Color().white()):
        self.pos = pos
        self.color = color