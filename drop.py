
import math
from random import random, randrange
import pyxel


class Drop:
    def __init__(self, p):
        self.p = p
        self.parent = p.parent
        self.alive = True
        self.posx = p.posx
        self.posy = p.posy

    def update(self):
        if self.posy > pyxel.height+self.parent.scroll_y+11:
            self.alive = False
        elif self.posx-10 < self.parent.player.posx < self.posx+10 and self.posy-10 < self.parent.player.posy < self.posy+10:
            self.alive = False
            pyxel.play(3, 6)
            self.parent.kushis += 1
            self.parent.kushis = min(99, self.parent.kushis)

    def draw(self):
        pyxel.blt(self.posx-5, self.posy +
                  self.parent.scroll_y-5, 0, 0, 128, 10, 10, 6)
