import os
import sys

import pygame as pg

import vars as vr
import config as cf
import tools as t

def path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def Text(msg, coord, size, color):  # blit to the screen a text
    TextColor = pg.Color(color) # set the color of the text
    font = pg.font.Font(path("rsc/pixel.ttf"), size)  # set the font
    return vr.window.blit(font.render(msg, True, TextColor), coord)  # return and blit the text on the screen

def getInputs():
    keys = pg.key.get_pressed()
    vr.inputs["SPACE"] = True if keys[pg.K_SPACE] else False

    vr.inputs["UP"] = True if keys[pg.K_UP] else False
    vr.inputs["DOWN"] = True if keys[pg.K_DOWN] else False
    vr.inputs["RIGHT"] = True if keys[pg.K_RIGHT] else False
    vr.inputs["LEFT"] = True if keys[pg.K_LEFT] else False

def isInWindow(coord):
    if 0 <= coord[0] <= vr.win_width:
        if 0 <= coord[1] <= vr.win_height:
            return True
    return False

def is_in_border(coord, delta=(cf.worldborder[0], cf.worldborder[0], cf.worldborder[1], cf.worldborder[1])):
    x, y = coord
    wx, wy = cf.world_size
    return delta[0] < x < wx - (delta[0] + delta[1]), delta[2] < y < wy - (delta[2] + delta[3])

def keep_in_border(coord, delta=(cf.worldborder[0], cf.worldborder[0], cf.worldborder[1], cf.worldborder[1])):
    x, y = coord
    wx, wy = cf.world_size
    return min(max(delta[0], x), wx - (delta[0] + delta[1])), min(max(delta[2], y), wy - (delta[2] + delta[3]))

def drawSeg(seg):
    pg.draw.line(vr.window, (20, 20, 100), seg(0), seg(1), 4)

def getNewId():
    vr.id += 1
    return vr.id

def adapt_to_view(coord):
    return t.Vdiff(coord, vr.camera_coord)

def get_view_center_coord():
    return t.Vcl(1, vr.camera_coord, 0.5, vr.window_size)

def min_distance_to_border(coord, border=cf.worldborder):
    x, y = coord
    return min(x - border[0], cf.world_size[0] - x - border[0], y - border[1], cf.world_size[1] - y - border[1])

def distance_to_borders(coord, border=cf.worldborder):
    x, y = coord
    return x - border[0], cf.world_size[0] - x - border[0], y - border[1], cf.world_size[1] - y - border[1]

def draw_worldborder():
    if min_distance_to_border(get_view_center_coord()) < max(vr.win_half_width, vr.win_half_height):
        anchor = adapt_to_view(t.Vadd((0, 0), (vr.win_half_width, vr.win_half_height)))
        pg.draw.rect(vr.window, 'red', [anchor[0], anchor[1], cf.world_size[0] - vr.win_width, cf.world_size[1] - vr.win_height], 2)

def distance_to_speed_per_updt(distance):
    return distance * t.inv(vr.dt_update)

def distance_to_acc_per_updt(distance):
    return distance * (t.inv(vr.dt_update) ** 2)
