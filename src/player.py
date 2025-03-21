import vars as vr
import config as cf
import tools as t
import utils as u
from visuals import player_visuals

import pygame as pg

class Player:
    def __init__(self, coordi=(200, 600)):
        self.id = u.getNewId()

        self.coord = list(coordi)
        self.speed = [0, 0]
        self.acc = [0, 0]

        self.sizex, self.sizey = cf.player_size

        self.states = 'default'
        self.visuals = player_visuals
        self.visual = self.visuals[self.states][0]

    def update(self):

        self.acc = [0, 9.81]
        self.speed = t.Vcl(0.99, self.speed, vr.dt, self.acc)
        self.coord = u.keep_in_window(t.Vcl(1, self.coord, vr.dt, self.speed))

    def getx(self):
        return self.coord[0]
    def gety(self):
        return self.coord[1]
    def get_size(self):
        return self.sizex, self.sizey
    def get_topleft(self):
        return self.getx() - self.sizex/2, self.gety() - self.sizey/2

    def draw(self):
        vr.window.blit(self.visual, self.get_topleft())
