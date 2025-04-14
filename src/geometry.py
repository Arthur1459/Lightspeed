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

    def intersect(self, absolute_coord):
        xm, ym = cf.world_size
        xM, yM = 0, 0
        for x, y in self.points_absolute:
            xm, ym = min(xm, x), min(ym, y)
            xM, yM = max(xM, x), max(yM, y)
        xt, yt = absolute_coord
        return xm < xt < xM and ym < yt < yM

class Block(Geobject):
    def __init__(self, anchori=(1200, 1000), size=(100, 100), visual_type='blocks'):
        self.size = size
        self.radius = t.norm(self.size)
        super().__init__(anchori, ((0, 0), (self.sizex(), 0), (self.sizex(), self.sizey()), (0, self.sizey())))

        self.tags.add('solid')

        self.visual_type = visual_type
        self.visuals = {visual: blocks_visuals[visual]['frames'] for visual in blocks_visuals}
        self.visual = self.visuals[self.visual_type][t.rndInt(0, len(self.visuals[self.visual_type]))]

    def update(self):
        super().update()
    def update_visual(self):
        self.visual = self.visuals[self.visual_type][t.rndInt(0, len(self.visuals[self.visual_type]))]

    def get_type(self):
        return 'block'
    def get_data(self):
        return (self.world_anchor, self.size, self.visual_type)
    def sizex(self):
        return self.size[0]
    def sizey(self):
        return self.size[1]
    def get_size(self):
        return self.sizex(), self.sizey()
    def draw(self):
        vr.game_window.blit(self.visual, u.adapt_to_view(self.world_anchor))

class Slope(Geobject):
    def __init__(self, anchori=(1200, 1000), size=(100, 100), visual_type='blocks', direction='topright'):
        self.size = size
        self.radius = t.norm(self.size)
        super().__init__(anchori, ((0, 0), (self.sizex(), 0), (self.sizex(), self.sizey()), (0, self.sizey())))

        self.tags.add('solid')

        self.direction = direction
        self.triangle_relative_coord = ((0, self.sizey()), (self.sizex(), 0), self.get_size())
        if direction == 'topright': self.triangle_relative_coord = ((0, self.sizey()), (self.sizex(), 0), self.get_size())
        if direction == 'topleft': self.triangle_relative_coord = ((self.sizex(), self.sizey()), (0, 0), (0, self.sizey()))
        if direction == 'botright': self.triangle_relative_coord = ((0, 0), (self.sizex(), self.sizey()), (self.sizex(), 0))
        if direction == 'botleft': self.triangle_relative_coord = ((self.sizex(), 0), (0, self.sizey()), (0, 0))

        self.visual_type = visual_type
        self.visuals = {visual: [frame for frame in blocks_visuals[visual]['frames']] for visual in blocks_visuals}
        self.visual = self.convert_triangle(self.visuals[self.visual_type][t.rndInt(0, len(self.visuals[self.visual_type]))])

    def convert_triangle(self, texture):
        visual = pg.transform.scale(texture.convert_alpha(), self.size)
        triangle_surface = pg.Surface(self.size, pg.SRCALPHA)
        pg.draw.polygon(triangle_surface, (255, 255, 255, 255), self.triangle_relative_coord)

        masked_texture = visual.copy()
        masked_texture.blit(triangle_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        return masked_texture

    def intersect(self, world_coord):
        """Return True if coord (x, y) is inside the triangle."""
        world_coords = [t.Vadd(self.world_anchor, relative_coord) for relative_coord in self.triangle_relative_coord]
        a, b, c = world_coords

        # Compute vectors
        v0 = t.Vdiff(c, a) #c - a
        v1 = t.Vdiff(b, a) #b - a
        v2 = t.Vdiff(world_coord, a) #p - a

        # Compute dot products
        dot00 = t.dot(v0, v0)
        dot01 = t.dot(v0, v1)
        dot02 = t.dot(v0, v2)
        dot11 = t.dot(v1, v1)
        dot12 = t.dot(v1, v2)

        # Compute barycentric coordinates
        denom = dot00 * dot11 - dot01 * dot01
        if denom == 0:
            return False  # Degenerate triangle

        inv_denom = 1 / denom
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom

        # Check if point is in triangle
        return (u >= 0) and (v >= 0) and (u + v <= 1)

    def update(self):
        super().update()
    def update_visual(self):
        self.visual = self.convert_triangle(self.visuals[self.visual_type][t.rndInt(0, len(self.visuals[self.visual_type]))])

    def get_type(self):
        return 'slope'
    def get_data(self):
        return (self.world_anchor, self.size, self.visual_type, self.direction)
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
