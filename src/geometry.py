import vars as vr
import config as cf
import tools as t
import utils as u
from visuals import player_visuals

import pygame as pg

class Geobject:
    def __init__(self, anchori=(1000, 800), relative_points=((-100, -50), (100, -50), (100, 50), (-100, 50)), frozen=False):
        self.id = u.getNewId()

        self.frozen = False
        self.world_anchor = anchori
        self.points_relative = relative_points
        self.points_absolute = [t.Vadd(self.world_anchor, point) for point in self.points_relative]

        self.radius = max([t.norm(point) for point in self.points_relative])

    def update(self):
        self.points_absolute = [u.adapt_to_view(t.Vadd(self.world_anchor, point)) for point in self.points_relative]

    def draw(self):
        pg.draw.polygon(vr.window, 'yellow', self.points_absolute, 4)
