
import math
from urllib.parse import quote_plus
from webbrowser import open as openw

import pyxel
from bresenham import bresenham

from background import Background
from blood import Blood
from bullet import Bullet
from drop import Drop
from enemy import Enemy
from global_lists import bloods_list, bullets_list, drops_list, enemys_list
from player import Player

SCENE_TITLE = 0
SCENE_TITLE_TO_GAME = 1
SCENE_GAME = 2
SCENE_GAME_TO_GAMEOVER = 3


class App:
    def __init__(self):
        pyxel.init(184, 192)
        self.killcount = 0
        self.scroll_y = 0
        self.scene = SCENE_TITLE
        self.background = Background(self)
        self.counts = {}
        self.dif = 1
        self.kushis = 99
        self.clickcount = 0
        pyxel.load("assets/main.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.scene == SCENE_TITLE:
            self.scroll_y += 1
            if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                pyxel.play(0, 3)
                self.scene = SCENE_TITLE_TO_GAME
                self.counts["ttg_count_1"] = 0
                self.counts["ttg_count_2"] = 0
                self.counts["ttg_count_3"] = 0
                self.counts["ttg_count_4"] = 0
                self.start_count = pyxel.frame_count+0
        elif self.scene == SCENE_TITLE_TO_GAME:
            self.scroll_y += 1
            if self.counts["ttg_count_1"]**1.8 > 16:
                self.counts["ttg_count_2"] += 1
            if self.counts["ttg_count_1"]**1.8 > 32:
                self.counts["ttg_count_3"] += 1
            if self.counts["ttg_count_1"]**1.8 > 48:
                self.counts["ttg_count_4"] += 1
                if pyxel.height <= self.counts["ttg_count_4"]**2-7-32:
                    self.scene = SCENE_GAME
                    self.killcount = 0
                    self.dif = 1
                    self.player = Player(self)
            self.counts["ttg_count_1"] += 1
        elif self.scene == SCENE_GAME:
            if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                self.clickcount += 1
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                self.clickcount = 0

            self.scroll_y += self.dif
            if pyxel.frame_count % (math.floor(20/self.dif)) == 0:
                enemys_list.append(Enemy(self))
            for i in enemys_list:
                if i.alive:
                    i.update()
                else:
                    enemys_list.remove(i)
            for i in bullets_list:
                if i.alive:
                    i.update()
                else:
                    bullets_list.remove(i)
            for i in bloods_list:
                if i.alive:
                    i.update()
                else:
                    bloods_list.remove(i)
            for i in drops_list:
                if i.alive:
                    i.update()
                else:
                    drops_list.remove(i)
            self.dif += 0.001
            self.player.update()

    def draw(self):
        self.background.draw()
        if self.scene == SCENE_TITLE:
            pyxel.blt(pyxel.width/2-32, pyxel.height /
                      2-8-32, 0, 0, 32, 64, 16, 7)
            pyxel.blt(pyxel.width/2-32+8, pyxel.height /
                      2-8-32, 0, 0, 16, 16, 16, 0)
            pyxel.blt(pyxel.width/2-32+8+16, pyxel.height /
                      2-8-32, 0, 16, 16, 16, 16, 0)
            pyxel.blt(pyxel.width/2-32+8+32, pyxel.height /
                      2-8-32, 0, 32, 16, 16, 16, 0)
            pyxel.text(pyxel.width/2-len("- CLICK START -")*2,
                       pyxel.height/2-2, "- CLICK START -", 7)
        elif self.scene == SCENE_TITLE_TO_GAME:
            pyxel.blt(self.counts["ttg_count_1"]**1.8+pyxel.width /
                      2-32, pyxel.height/2-8-32, 0, 0, 32, 64, 16, 7)
            pyxel.blt(pyxel.width/2-32+8,
                      self.counts["ttg_count_2"]**2+pyxel.height/2-8-32, 0, 0, 16, 16, 16, 0)
            pyxel.blt(pyxel.width/2-32+8+16,
                      self.counts["ttg_count_3"]**2+pyxel.height/2-8-32, 0, 16, 16, 16, 16, 0)
            pyxel.blt(pyxel.width/2-32+8+32,
                      self.counts["ttg_count_4"]**2+pyxel.height/2-8-32, 0, 32, 16, 16, 16, 0)
        elif self.scene == SCENE_GAME:
            for i in list(bresenham(pyxel.mouse_x, pyxel.mouse_y, math.floor(self.player.posx), math.floor(self.player.posy+self.scroll_y-11)))[::3]:
                pyxel.pset(i[0], i[1], 7)
            self.player.draw()
            crosser = []
            for i in range(5):
                crosser.append((pyxel.mouse_x+2-i, pyxel.mouse_y+0))
            for i in range(5):
                crosser.append((pyxel.mouse_x+0, pyxel.mouse_y+2-i))
            for i in range(16):
                pyxel.pal(i, (i+7) % 16)
            for i in crosser:
                pyxel.pset(i[0], i[1], pyxel.pget(i[0], i[1]))
            pyxel.pal()
            pyxel.text(5, 5, str(self.kushis), 7)
            for i in bloods_list:
                i.draw()
            for i in enemys_list:
                i.draw()
            for i in drops_list:
                i.draw()
            for i in bullets_list:
                i.draw()
        elif self.scene == SCENE_GAME_TO_GAMEOVER:
            pyxel.rect(16, 0, 123, self.counts["gtg_count"]*4, 7)
            pyxel.rect(16, 0, 20, self.counts["gtg_count"]*4, 4)
            pyxel.rect(139, 0, 20, self.counts["gtg_count"]*4, 4)
            pyxel.line(16, 0, 16, self.counts["gtg_count"]*4, 0)
            pyxel.line(159, 0, 159, self.counts["gtg_count"]*4, 0)
            if self.counts["gtg_count"] < pyxel.height/4:
                pyxel.blt(0, self.counts["gtg_count"]
                          * 4-32, 1, 0, 0, 186, 32, 12)
            else:
                pyxel.blt(0, pyxel.height-32, 1, 0, 0, 186, 32, 12)
                if self.counts["gtg_count"] > pyxel.height/4+20:
                    pyxel.text(37, 33, "SCORE ".upper() +
                               str(self.stop_count - self.start_count), 0)
                    if self.counts["gtg_count"] > pyxel.height/4+40:
                        pyxel.text(37, 40, "KILL  ".upper() +
                                   str(self.killcount), 0)
                    if self.counts["gtg_count"] > pyxel.height/4+60:
                        if 37 <= pyxel.mouse_x <= 37+64 and 47 <= pyxel.mouse_y <= 47+64:
                            pyxel.pal(12, 8)
                            pyxel.pal(7, 12)
                            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                                openw(
                                    "https://twitter.com/intent/tweet?text=" + quote_plus("SCORE:".upper()+str(self.stop_count - self.start_count)+"\nKILL:".upper()+str(self.killcount)+"\n#Bakumatu_Harisenbon\nhttps://github.com/AlageZ/Harisenbon/releases/"))
                        pyxel.blt(37, 47, 0, 32, 64, 64, 64, 0)
                        pyxel.pal()
                        pyxel.mouse(True)
            self.counts["gtg_count"] += 1

    def gameover(self):
        self.stop_count = pyxel.frame_count+0
        self.counts["gtg_count"] = 0
        self.scene = SCENE_GAME_TO_GAMEOVER
