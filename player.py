
import math
import pyxel
from blood import Blood
from bullet import Bullet
from global_lists import bullets_list, bloods_list


class Player:
    def __init__(self, parent):
        self.parent = parent
        self.posy = self.parent.scroll_y+pyxel.height-32
        self.posx = pyxel.width/2
        self.bloodflag = 0

    def update(self):
        self.posy -= self.parent.dif
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.posx += 2*pyxel.width/100
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.posx -= 2*pyxel.width/100
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.posy -= 2*pyxel.height/100
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.posy += 2*pyxel.height/100
        if self.posy > pyxel.height-self.parent.scroll_y:
            self.posy = pyxel.height-self.parent.scroll_y
        if self.posy < 0-self.parent.scroll_y+16:
            self.posy = 0-self.parent.scroll_y+16
        if self.posx > pyxel.width-32-5:
            self.posx = pyxel.width-32-5
        if self.posx < 32+5:
            self.posx = 32+5
        for i in bloods_list:
            if math.floor(i.posx) == math.floor(self.posx):
                if math.floor(i.posy) == math.floor(self.posy):
                    if i.p != self:
                        self.bloodflag = 10
        if pyxel.frame_count % 5 == 0 and self.bloodflag > 0:
            self.bloodflag -= 1
            bloods_list.append(Blood(self))
            bloods_list[-1].posx = self.posx
            bloods_list[-1].posy = self.posy
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            if self.parent.kushis > 0:
                pyxel.play(0, 0)
                self.parent.kushis -= 1
                bullets_list.append(Bullet(self.parent))
        if pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON):
            if self.parent.clickcount > 30:
                pyxel.play(0, 0)
                for i in range(min(5, self.parent.kushis)):
                    self.parent.kushis -= 1
                    bullets_list.append(Bullet(self.parent))
                    bullets_list[-1].at = math.radians(
                        math.degrees(bullets_list[-1].at)+(i-2)*20)

    def draw(self):
        pyxel.blt(self.posx-5, self.posy-11 +
                  self.parent.scroll_y, 0, 0, 48, 16, 11, 14)
