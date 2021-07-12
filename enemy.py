
from random import random, randrange

import pyxel

from blood import Blood
from drop import Drop
from global_lists import bloods_list, drops_list


class Enemy:
    def __init__(self, parent):
        self.parent = parent
        self.anime_count = 0
        self.posx = random()*(pyxel.width-64-10)+32+5
        self.posy = -self.parent.scroll_y+0
        self.alive = True

    def update(self):
        self.anime_count += 1
        self.anime_count %= 12
        self.posy += 1
        if self.posy > pyxel.height+self.parent.scroll_y+11:
            self.alive = False
        elif self.posx-10 < self.parent.player.posx < self.posx+10 and self.posy-2 < self.parent.player.posy < self.posy+8:
            pyxel.play(1, 5)
            self.parent.gameover()

    def draw(self):
        tilex = 0
        if self.anime_count in [0, 1, 2, 3, 7, 8]:
            tilex = 0
        elif self.anime_count in [4, 6, 9, 11]:
            tilex = 16
        else:
            tilex = 32
        pyxel.blt(self.posx-5, self.posy-11 +
                  self.parent.scroll_y, 0, tilex, 0, 16, 11, 14)

    def killed(self):
        self.parent.killcount += 1
        if random() > 0.7:
            drops_list.append(Drop(self))
        self.alive = False
        for i in range(20):
            bloods_list.append(Blood(self))
