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
    def __init__(self, coord, size, msg, color="white", callback=None, text_size=None, shiftx=0.3, shifty=0.1, framed=False, transparent=False, font='pixel'):
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

        self.transparent, self.font = transparent, font
        self.framed, self.frame = framed, None
        if self.framed:
            self.visuals['RELEASED FRAMED'] = img("gui/PressButton/frame/released.png", resize=self.size)
            self.visuals['PRESSED FRAMED'] = img("gui/PressButton/frame/pressed.png", resize=self.size)
            self.visuals['HOVERED FRAMED'] = img("gui/PressButton/frame/hovered.png", resize=self.size)

    def update(self):
        if t.intersect_box(vr.cursor, (t.Vcl(1, self.coord, -0.5, self.size), t.Vcl(1, self.coord, 0.5, self.size))):
            if vr.inputs['CLICK']:
                sm.PlayEffect('click_selected')
                self.visual_state = "PRESSED"
                self.pressed = True
                self.visual = self.visuals[self.visual_state]
                if self.callback is not None:
                    self.callback()
            elif self.visual_state != "HOVERED":
                sm.PlayEffect('button_hovered')
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
        if not self.transparent:
            vr.game_window.blit(self.visual, draw_coord)
        if self.framed:
            vr.game_window.blit(self.visuals[self.visual_state + " FRAMED"], draw_coord)
        u.Text(self.message, t.Vadd(draw_coord, t.VxV(self.size, self.shift)), self.text_size, self.color, font_type=self.font)
        return

class SwitchButton:
    def __init__(self, coord, size, msg, color="white", callback=None, text_size=None, shiftx=0.3, shifty=0.1, switch_on=True):
        self.type, self.id = "switch button", u.getNewId()
        self.coord = coord
        self.size, self.text_size = size, text_size if text_size is not None else size[0]//5
        self.shift = (shiftx, shifty)
        self.message, self.color = str(msg), color
        self.visuals, self.visual_state = {'ON': img("gui/SwitchButton/on.png", resize=self.size),
                                           'ON HOVERED': img("gui/SwitchButton/on_hovered.png", resize=self.size),
                                           'OFF': img("gui/SwitchButton/off.png", resize=self.size),
                                           'OFF HOVERED': img("gui/SwitchButton/off_hovered.png", resize=self.size)}, "ON" if switch_on else "OFF"
        self.visual = pg.transform.scale(self.visuals[self.visual_state], self.size)
        self.switch_on = switch_on
        self.callback = callback

    def update(self):
        if t.intersect_box(vr.cursor, (t.Vcl(1, self.coord, -0.5, self.size), t.Vcl(1, self.coord, 0.5, self.size))):
            if vr.inputs['CLICK']:
                if self.switch_on:
                    sm.PlayEffect('switch_off')
                    self.switch_on = False
                    self.visual_state = 'OFF HOVERED'
                else:
                    sm.PlayEffect('switch_on')
                    self.switch_on = True
                    self.visual_state = 'ON HOVERED'
                if self.callback is not None:
                    self.callback(self.switch_on)
            elif self.visual_state != "ON HOVERED" and self.visual_state != "OFF HOVERED":
                sm.PlayEffect('button_hovered')
                self.visual_state = "ON HOVERED" if self.switch_on else "OFF HOVERED"
        elif self.visual_state == "ON HOVERED" or self.visual_state == "OFF HOVERED":
            self.visual_state = "ON" if self.switch_on else "OFF"
        return

    def draw(self):
        self.visual = self.visuals[self.visual_state]
        draw_coord = t.Vcl(1, self.coord, -0.5, self.size)
        vr.game_window.blit(self.visual, draw_coord)
        u.Text(self.message, t.Vadd(draw_coord, t.VxV(self.size, self.shift)), self.text_size, self.color)
        return

class SlidingValue:
    def __init__(self, coord, size, msg='', color="white", value=0, value_color="white", value_range=(0, 100), callback=None, text_size=None, value_size=None, shiftx=0.3, shifty=0.1, val_shiftx=0.3, val_shifty=0.1, val_unit=""):
        self.type, self.id = "switch button", u.getNewId()
        self.coord = coord
        self.size, self.text_size, self.value_size = size, text_size if text_size is not None else size[0]//5, value_size if value_size is not None else size[0]//5
        self.shift, self.val_shift = (shiftx, shifty), (val_shiftx, val_shifty)
        self.message, self.msg_color = str(msg), color
        self.value, self.value_color, self.value_range, self.val_unit = value, value_color, value_range, val_unit
        self.visuals, self.visual_state = {'ACTIVE': img("gui/frame_hovered.png", resize=self.size),
                                           'PASSIVE': img("gui/frame.png", resize=self.size)}, "PASSIVE"
        self.visual = self.visuals[self.visual_state]
        self.selected, self.start_coord, self.value_on_click = False, None, None
        self.callback = callback

    def update(self):
        if not self.selected:
            if t.intersect_box(vr.cursor, (t.Vcl(1, self.coord, -0.5, self.size), t.Vcl(1, self.coord, 0.5, self.size))):
                if self.visual_state != 'ACTIVE':
                    sm.PlayEffect('button_hovered')
                    self.visual_state = 'ACTIVE'
                if vr.inputs['CLICK_PRESSED']:
                    self.selected = True
                    self.start_coord = vr.cursor
                    self.value_on_click = self.value
            else:
                self.visual_state = 'PASSIVE'
        else:
            if vr.inputs['CLICK_PRESSED']:
                distance = t.distance(self.start_coord, vr.cursor) * t.s(self.start_coord[1] - vr.cursor[1])
                self.value = int(max(min(self.value_range), min(max(self.value_range), self.value_on_click + (self.value_range[1] - self.value_range[0]) * distance / (vr.win_height * 0.25))))
                self.callback(self.value)
            else:
                self.selected = False
        return

    def draw(self):
        self.visual = self.visuals[self.visual_state]
        draw_coord = t.Vcl(1, self.coord, -0.5, self.size)
        vr.game_window.blit(self.visual, draw_coord)
        u.Text(self.message, t.Vadd(draw_coord, t.VxV(self.size, self.shift)), self.text_size, self.msg_color)
        u.Text(str(self.value) + self.val_unit, t.Vadd(draw_coord, t.VxV(self.size, self.val_shift)), self.value_size, self.value_color)
        return
