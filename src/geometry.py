import vars as vr
import config as cf
import tools as t
import utils as u
from visuals import blocks_visuals, spike_visuals, sync_animations_cycles
from ambient import Particle

import pygame as pg

class Geobject:
    def __init__(self, anchori=(1000, 800), relative_points=((-100, -50), (100, -50), (100, 50), (-100, 50))):
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
    def get_size(self):
        return 2 * self.radius, 2 * self.radius
    def __getitem__(self, item):
        return self.get_type()
    def update(self):
        for i, point in enumerate(self.points_relative):
            self.points_absolute[i] = t.Vadd(self.world_anchor, point)
            self.points_win[i] = u.adapt_to_view(t.Vadd(self.world_anchor, point))

    def draw(self):
        pg.draw.polygon(vr.game_window, 'yellow', self.points_absolute, 4)

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
    def __init__(self, anchori=(1200, 1000), size=(100, 100), visual_type='default'):
        self.size = size
        self.radius = t.norm(self.size)
        super().__init__(anchori, ((0, 0), (self.sizex(), 0), (self.sizex(), self.sizey()), (0, self.sizey())))

        self.tags.add('solid')

        self.visual_type = visual_type
        self.visuals = {'default': blocks_visuals['blocks']['frames'], 'top': blocks_visuals['blocks_top']['frames']}
        self.visual = self.visuals[self.visual_type][t.rndInt(0, len(self.visuals[self.visual_type]))]

    def update(self):
        super().update()
    def update_visual(self):
        self.visual = self.visuals[self.visual_type][t.rndInt(0, len(self.visuals[self.visual_type]))]

    def get_type(self):
        return 'block'
    def get_data(self):
        return (self.world_anchor, self.size, self.visual_type)
    def player_skin(self):
        self.visual = self.visuals[1]
    def base_skin(self):
        self.visual = self.visuals[0]

    def sizex(self):
        return self.size[0]
    def sizey(self):
        return self.size[1]
    def get_size(self):
        return self.sizex(), self.sizey()
    def draw(self):
        vr.game_window.blit(self.visual, u.adapt_to_view(self.world_anchor))

class Spike(Block):
    def __init__(self, anchori=(1200, 1000), size=(50, 50)):
        self.size = size
        super().__init__(anchori, self.get_size())

        self.tags.add('solid')
        self.tags.add('spike')

        self.visuals = [pg.transform.scale(frame, self.size) for frame in spike_visuals['frames']]
        self.visual = self.visuals[vr.animation_cycles['spike']['index']]

    def get_type(self):
        return 'spike'
    def get_data(self):
        return (self.world_anchor, self.size)

    def draw(self):
        self.visual = self.visuals[vr.animation_cycles['spike']['index']]
        vr.game_window.blit(self.visual, u.adapt_to_view(self.world_anchor))

        if u.proba(20):
            anchor = t.Vadd(self.world_anchor, (self.sizex()/2 + t.rndInt(-0.2 * self.sizex(), 0.2 * self.sizex()), self.sizey()/2 + t.rndInt(- 0.4 * self.sizey(), 0.4 * self.sizey())))
            max_speed = u.distance_to_speed_per_updt(10)
            speed = (t.rndInt(-max_speed, max_speed), t.rndInt(-max_speed, max_speed))
            vr.map.ambient_elts.append(Particle('fire', anchor, size=4, speed=speed, gravity=True))
