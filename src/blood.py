
from random import random, randrange
import pyxel


class Blood:
    def __init__(self, p):
        self.p = p
        self.parent = p.parent
        self.alive = True
        self.posx = p.posx+randrange(-5, 5)
        self.posy = p.posy+randrange(-5, 5)

    def update(self):
        if self.posy > pyxel.height+self.parent.scroll_y+11:
            self.alive = False

    def draw(self):
        pyxel.pset(self.posx, self.posy+self.parent.scroll_y, 8)
