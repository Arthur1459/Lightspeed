import vars as vr
import config as cf
import tools as t
import utils as u
from visuals import particles_visuals

import pygame as pg


class AmbientElt:
    def __init__(self, anchori):
        self.id = u.getNewId()
        self.tags = {'default'}
        self.world_anchor = anchori

    def get_type(self):
        return 'ambient'
    def get_data(self):
        return self.world_anchor

    def update(self):
        pass

    def draw(self):
        pg.draw.circle(vr.window, 'yellow', u.adapt_to_view(self.world_anchor), 5)

class Particle(AmbientElt):
    def __init__(self, particle_name, anchori, persistence=1., size=32, alpha=250, speed=(0, 0), gravity=True, friction=0.9, spawn_on_death=(0,)):
        super().__init__(anchori)

        self.name = particle_name
        self.speed, self.gravity, self.friction = speed, gravity, friction
        self.size = (size, size)
        self.on_death = spawn_on_death
        self.persistence, self.creation_time = persistence, vr.t
        self.alpha, self.alpha_0 = alpha, alpha

        self.visuals, self.frames_duration = [pg.transform.scale(frame, self.size).convert_alpha() for frame in particles_visuals[self.name]['frames']], particles_visuals[self.name]['duration']
        self.visual, self.visual_index, self.visual_time = self.visuals[0], 0, vr.t

        self.alive = True
    def draw(self):
        if self.alive:
            self.world_anchor = t.Vcl(1, self.world_anchor, vr.dt_update, self.speed)
            self.speed = t.Vcl(self.friction, self.speed, vr.dt_update, (0, vr.gravity if self.gravity else 0))
            if vr.t - self.creation_time > self.persistence:
                self.alive = False
                for i in range(self.on_death[0]):
                    vr.map.ambient_elts.append(Particle(self.name, self.world_anchor, alpha=self.alpha_0//2, persistence=self.persistence/2, speed=(t.rndS() * self.speed[0] * t.rnd(1., 1.5), t.rndS() * self.speed[1] * t.rnd(1., 1.5)), size=self.size[0]//2, gravity=self.gravity))

            if vr.t - self.visual_time > self.frames_duration:
                self.visual_index = (self.visual_index + 1) % len(self.visuals)
                self.visual = self.visuals[self.visual_index]
                self.visual_time = vr.t

            self.alpha = max(0, self.alpha_0 * (1 - (vr.t - self.creation_time) / self.persistence))
            self.visual.set_alpha(self.alpha)

            vr.window.blit(self.visual, u.adapt_to_view(t.Vcl(1, self.world_anchor, -0.5, self.size)))
