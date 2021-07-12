
from random import random, randrange

import pyxel

BACK_DOT_COUNT = 300


class Background:
    def __init__(self, parent):
        self.parent = parent
        self.dot_list = []
        self.bg_color = 9
        self.dot_color = 4
        for i in range(BACK_DOT_COUNT):
            self.dot_list.append(
                (random() * pyxel.width, random() * pyxel.height, 1)
            )

    def draw(self):
        pyxel.cls(self.bg_color)
        for (x, y, speed) in self.dot_list:
            pyxel.pset(x, (y+self.parent.scroll_y) %
                       pyxel.height, self.dot_color)
        for i in range(32):
            l = self.parent.scroll_y % 128 * 2 * (((64-i)/64))+i*1.5
            c = [i, 64+i, 1, 64-i]
            cc = l
            while cc > 0:
                cc -= 128-i*2
            while cc-i*2 <= pyxel.height:

                pyxel.blt(c[0], cc, 0, c[0], c[1], c[2], c[3], 8)
                pyxel.blt(c[0], cc+64-i, 0, c[0], c[1], c[2], c[3]*-1, 8)
                pyxel.blt(pyxel.width-c[0], cc, 0, c[0], c[1], c[2], c[3], 8)
                pyxel.blt(pyxel.width-c[0], cc+64-i, 0,
                          c[0], c[1], c[2], c[3]*-1, 8)
                cc += 128-i*2-2
