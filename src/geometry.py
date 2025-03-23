import vars as vr
import config as cf
import tools as t
import utils as u
from visuals import blocks

import pygame as pg

class Geobject:
    def __init__(self, anchori=(1000, 800), relative_points=((-100, -50), (100, -50), (100, 50), (-100, 50)), frozen=False):
        self.id = u.getNewId()
        self.tags = {'default'}

        self.frozen = False
        self.world_anchor = anchori
        self.points_relative = relative_points
        self.points_absolute = [t.Vadd(self.world_anchor, point) for point in self.points_relative]
        self.points_win = [u.adapt_to_view(t.Vadd(self.world_anchor, point)) for point in self.points_relative]

        self.radius = max([t.norm(point) for point in self.points_relative])

    def get_type(self):
        return 'geobject'
    def get_data(self):
        return (self.world_anchor, self.points_relative)

    def update(self):
        for i, point in enumerate(self.points_relative):
            self.points_absolute[i] = t.Vadd(self.world_anchor, point)
            self.points_win[i] = u.adapt_to_view(t.Vadd(self.world_anchor, point))

    def draw(self):
        pg.draw.polygon(vr.window, 'yellow', self.points_absolute, 4)

    def intersect(self, absolute_coord, poly_type='rectangle'):
        if poly_type == 'rectangle':
            xm, ym = cf.world_size
            xM, yM = 0, 0
            for x, y in self.points_absolute:
                xm, ym = min(xm, x), min(ym, y)
                xM, yM = max(xM, x), max(yM, y)
            xt, yt = absolute_coord
            return xm < xt < xM and ym < yt < yM
        else:
            return False

class Block(Geobject):
    def __init__(self, anchori=(1200, 1000), size=(200, 100), frozen=False):
        self.size = size
        super().__init__(anchori, ((0, 0), (self.sizex(), 0), (self.sizex(), self.sizey()), (0, self.sizey())))

        self.tags.add('solid')

        self.visual = pg.transform.scale(t.rnd_choice(blocks['metal']), self.size)

    def get_type(self):
        return 'block'
    def get_data(self):
        return (self.world_anchor, self.size)

    def sizex(self):
        return self.size[0]
    def sizey(self):
        return self.size[1]

    def draw(self):
        vr.window.blit(self.visual, u.adapt_to_view(self.world_anchor))
