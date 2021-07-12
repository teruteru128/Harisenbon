
import math
import pyxel

from global_lists import enemys_list


class Bullet:
    def __init__(self, parent):
        self.parent = parent
        self.alive = True
        self.posx = self.parent.player.posx
        self.posy = self.parent.player.posy+self.parent.scroll_y-8
        xx = pyxel.mouse_x-self.posx
        yy = pyxel.mouse_y-self.posy
        self.at = math.atan2(yy, xx)

    def update(self):
        poses = []
        for i in range(1, 8):
            poses.append((math.cos(self.at)*i+self.posx,
                         math.sin(self.at)*i+self.posy))
        for a in enemys_list:
            for b in poses:
                if a.posx-5 < b[0] < a.posx+5 and a.posy-11 < b[1]-self.parent.scroll_y < a.posy:
                    pyxel.play(1, 5)
                    a.killed()
                    break
            else:
                continue
            break
        self.posx = poses[6][0]
        self.posy = poses[6][1]

        if not (0 < poses[-1][1] < pyxel.height):
            self.alive = False
        elif not (32 < poses[-1][0] < pyxel.width-32):
            self.alive = False
            pyxel.play(2, 4)

    def draw(self):
        pyxel.line(self.posx, self.posy,
                   self.posx+math.cos(self.at)*5, self.posy+math.sin(self.at)*5, 0)
