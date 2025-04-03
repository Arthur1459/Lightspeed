import vars as vr
import config as cf
import tools as t
import utils as u
from visuals import creatures_visuals, empty
from ambient import Particle

import pygame as pg

class Creature:
    def __init__(self, anchori, size):
        self.id = u.getNewId()
        self.tags = {'creature',}

        self.world_anchor = anchori
        self.size = (size, size)
        self.radius = t.norm(self.size)

        self.visuals = [empty]
        self.visual, self.visual_index, self.frame_time, self.frame_duration = self.visuals[0], 0, vr.t, 1.

    def update(self):
        self.update_visual()

    def update_visual(self, force=False):
        if vr.t - self.frame_time > self.frame_duration or force:
            self.frame_time = vr.t
            self.visual_index = (self.visual_index + 1) % len(self.visuals)
            self.visual = self.visuals[self.visual_index]
    def draw(self):
        vr.game_window.blit(self.visual, u.adapt_to_view(self.world_anchor))

    def get_type(self):
        return 'creature'
    def get_data(self):
        return (self.world_anchor, self.size)
    def remove_tag(self, tag):
        if tag in self.tags: self.tags.remove(tag)
    def get_center(self):
        return t.Vadd(self.world_anchor, t.Vmul(self.size, 0.5))
    def sizex(self):
        return self.size[0]
    def sizey(self):
        return self.size[0]
    def get_size(self):
        return self.size
    def intersect(self, absolute_coord, poly_type='rectangle'):
        if poly_type == 'rectangle':
            xm, ym = self.world_anchor
            xM, yM = t.Vadd(self.world_anchor, self.get_size())
            xt, yt = absolute_coord
            return xm < xt < xM and ym < yt < yM
        else:
            return False


class Bat(Creature):
    def __init__(self, anchori):
        super().__init__(anchori, cf.bat['size'])

        self.tags.add('bat')

        self.world_anchor_base = self.world_anchor[:]
        self.speed = [0, 0]
        self.state = 'default'

        self.visuals, self.frame_duration = creatures_visuals['bat']['frames'], creatures_visuals['bat']['duration']
        self.update_visual(force=True)

    def get_type(self):
        return 'bat'
    def get_data(self):
        return self.world_anchor_base
    def update_visual(self, force=False):

        speed_factor = max(1, (50 * t.norm(self.speed) / u.distance_to_speed_per_updt(self.sizex()))**2) if self.state == 'attack' else 1
        if vr.t - self.frame_time > self.frame_duration / speed_factor or force:
            self.frame_time = vr.t
            self.visual_index = (self.visual_index + 1) % len(self.visuals)
            self.visual = self.visuals[self.visual_index]

        if self.visual_index == 0:
            vr.map.ambient_elts.append(Particle('fire', t.Vcl(1, self.world_anchor, 0.5, self.get_size()), persistence=0.5, alpha=250, size=2, gravity=True, speed=u.rnd_speed(4)))
    def update(self):
        super().update()

        if t.distance(self.world_anchor, vr.player.get_world_anchor_centered()) < cf.bat['action_radius']:
            self.state = 'attack'
        else:
            self.state = 'default'

        if self.state == 'default':
            self.speed = t.Vcl(0.9, self.speed, 1, t.Vmul((t.rnd(-1, 1), t.rnd(-1, 1)), u.distance_to_speed_per_updt(cf.bat['speed_default'])))
            if t.distance(self.world_anchor, self.world_anchor_base) > cf.bat['moving_radius']:
                self.speed = t.Vadd(self.speed, t.Vmul(t.Vdir(self.world_anchor, self.world_anchor_base), t.inv(vr.dt_update) * cf.bat['come_back_speed']))
        elif self.state == 'attack':
            self.speed = t.Vmul(t.Vdir(self.get_center(), vr.player.get_world_anchor_centered()), u.distance_to_speed_per_updt(cf.bat['speed_attack']))

        self.world_anchor = t.Vcl(1, self.world_anchor, vr.dt_update, self.speed)
