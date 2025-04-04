import config as cf
import vars as vr
import tools as t
import utils as u
from visuals import img, load_folder

import pygame as pg
import SoundsManagement as sm

class Displayer:
    def __init__(self, coord, size, msg, color="white", text_size=None, shiftx=0.3, shifty=0.1):
        self.type, self.id = "press button", u.getNewId()
        self.coord = coord
        self.size, self.text_size = size, text_size if text_size is not None else size[0]//5
        self.shift = (shiftx, shifty)
        self.message, self.color = "", color
        self.visual = img("gui/displayer.png", resize=self.size)

        self.update_msg(msg)

    def update(self, msg_updated=None, rounding=None, unit=""):
        if msg_updated is not None:
            self.update_msg(msg_updated, rounding=rounding, unit=unit)
        return

    def update_msg(self, msg_updated, rounding=None, unit=None):
        self.message = str(msg_updated if rounding is None else round(msg_updated, rounding)) + ("" if unit is None else " " + unit)

    def draw(self):
        draw_coord = t.Vcl(1, self.coord, -0.5, self.size)
        vr.game_window.blit(self.visual, draw_coord)
        u.Text(self.message, t.Vadd(draw_coord, t.VxV(self.size, self.shift)), self.text_size, self.color)
        return

class PressButton:
    def __init__(self, coord, size, msg, color="white", callback=None, text_size=None, shiftx=0.3, shifty=0.1):
        self.type, self.id = "press button", u.getNewId()
        self.coord = coord
        self.size, self.text_size = size, text_size if text_size is not None else size[0]//5
        self.shift = (shiftx, shifty)
        self.message, self.color = str(msg), color
        self.visuals, self.visual_state = {'RELEASED': img("gui/PressButton/released.png", resize=self.size),
                                           'PRESSED': img("gui/PressButton/pressed.png", resize=self.size),
                                           'HOVERED': img("gui/PressButton/hovered.png", resize=self.size)}, "RELEASED"
        self.visual = pg.transform.scale(self.visuals[self.visual_state], self.size)
        self.pressed = False
        self.callback = callback

    def update(self):
        if t.intersect_box(vr.cursor, (t.Vcl(1, self.coord, -0.5, self.size), t.Vcl(1, self.coord, 0.5, self.size))):
            if vr.inputs['CLICK']:
                self.visual_state = "PRESSED"
                self.pressed = True
                self.visual = self.visuals[self.visual_state]
                if self.callback is not None:
                    self.callback()
            elif self.visual_state != "HOVERED":
                #sm.PlayEffect("button hovered")
                self.visual_state = "HOVERED"
                self.visual = self.visuals[self.visual_state]
        else:
            self.pressed = False
            if self.visual_state != "RELEASED":
                self.visual_state = "RELEASED"
                self.visual = self.visuals[self.visual_state]
        return

    def draw(self):
        draw_coord = t.Vcl(1, self.coord, -0.5, self.size)
        vr.game_window.blit(self.visual, draw_coord)
        u.Text(self.message, t.Vadd(draw_coord, t.VxV(self.size, self.shift)), self.text_size, self.color)
        return

"""
class SwitchButton:
    def __init__(self, coord, size, msg, color="white", on=True):
        self.type, self.id = "switch button", u.getNewId()
        self.coord = coord
        self.size = size
        self.message, self.color = msg, color
        self.is_on, self.t_treshold = on, vr.t
        self.visuals, self.visual_state = cf.gui_visuals["SwitchButton"], "ON" if self.is_on else "OFF"
        self.visual = transform.scale(self.visuals[self.visual_state], self.size)

    def update(self):
        if t.IsInside(vr.cursor, [t.Vmult_sum(self.coord, 1, self.size, -1/2), t.Vmult_sum(self.coord, 1, self.size, 1/2)]):
            if vr.inputs['CLICK'] and time.time() - self.t_treshold > 0.3:
                self.t_treshold = time.time()
                if self.visual_state == "ON HOVERED":
                    self.visual_state = "OFF HOVERED"
                    self.is_on = False
                else:
                    self.visual_state = "ON HOVERED"
                    self.is_on = True
                self.visual = transform.scale(self.visuals[self.visual_state], self.size)
            elif self.visual_state != "ON HOVERED" or self.visual_state != "OFF HOVERED":
                if self.visual_state == "ON":
                    sm.PlayEffect("button hovered")
                    self.visual_state = "ON HOVERED"
                if self.visual_state == "OFF":
                    sm.PlayEffect("button hovered")
                    self.visual_state = "OFF HOVERED"
                self.visual = transform.scale(self.visuals[self.visual_state], self.size)
        else:
            if self.visual_state == "ON HOVERED":
                self.visual_state = "ON"
                self.visual = transform.scale(self.visuals[self.visual_state], self.size)
            elif self.visual_state == "OFF HOVERED":
                self.visual_state = "OFF"
                self.visual = transform.scale(self.visuals[self.visual_state], self.size)
        return

    def draw(self):
        draw_coord = t.Vmult_sum(self.coord, 1, self.size, -1 / 2)
        vr.screen.blit(self.visual, draw_coord)
        u.Text(self.message, t.Vsum(draw_coord, [self.size[0]/5, self.size[1]/5]), self.size[0]//5, self.color, vr.screen)
        return

    def destroy(self):
        try:
            vr.gui.remove(self)
        except:
            pass
        return
"""
