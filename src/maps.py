import vars as vr
import config as cf
import tools as t
import utils as u
import geometry as geo
from ambient import Particle
import pickle

import pygame as pg

class Map:
    def __init__(self, name='default'):
        self.name = name

        self.start_coord = cf.start_camera_coord
        self.geobjects = []
        self.content = {'geobjects': set()}

        self.ambient_elts = []
        self.old_ambient_elts = []

    def update(self):
        for animation in vr.animation_cycles:
            if vr.t - vr.animation_cycles[animation]['t'] > vr.animation_cycles[animation]['dt_threshold']:
                vr.animation_cycles[animation]['t'] = vr.t
                vr.animation_cycles[animation]['index'] = (vr.animation_cycles[animation]['index'] + 1) % vr.animation_cycles[animation]['max_index']

        for ambient_elt in self.old_ambient_elts:
            if ambient_elt in self.ambient_elts: self.ambient_elts.remove(ambient_elt)
        self.old_ambient_elts = []

        void_particle_max_speed = u.distance_to_speed_per_updt(2)
        rnd_anchor = t.Vadd(vr.camera_coord, (t.rndInt(0, vr.win_width), t.rndInt(0, vr.win_height)))
        self.ambient_elts.append(Particle('void', rnd_anchor, persistence=2., size=4, speed=(t.rndInt(-1 * void_particle_max_speed, 1 * void_particle_max_speed), void_particle_max_speed)))
        if u.proba(2):
            self.ambient_elts.append(Particle('star', rnd_anchor, friction=0.99, spawn_on_death=(8,), alpha=250, persistence=1., size=4, speed=(t.rndS() * t.rndInt(2 * void_particle_max_speed, 4 * void_particle_max_speed), t.rndInt(-4 * void_particle_max_speed, 4 * void_particle_max_speed))))

        if vr.player.states == 'dead' and vr.t - vr.player.actions_timers['respawn'] > cf.respawn_time:
            self.reload_map()
            vr.player.respawn()

    def add_block(self, anchor, size, update=False):
        geo_type, geo_data = 'block', (anchor, size)
        self.content['geobjects'].add((geo_type, geo_data))
        if update: self.reload_obj(geo_type, geo_data)
    def add_geobject(self, anchor, points, update=False):
        geo_type, geo_date = 'geobject', (anchor, points)
        self.content['geobjects'].add((geo_type, geo_date))
        if update: self.reload_obj(geo_type, geo_date)
    def add(self, geo_type, geo_data, update=False):
        self.content['geobjects'].add((geo_type, geo_data))
        if update: self.reload_obj(geo_type, geo_data)
    def remove(self, obj, obj_type='geobject'):
        if obj_type == 'geobject':
            self.geobjects.remove(obj)
            self.content['geobjects'].remove((obj.get_type(), obj.get_data()))
        else:
            pass
    def reload_map(self):
        self.geobjects = []
        for geo_type, geo_data in self.content['geobjects']:
            self.reload_obj(geo_type, geo_data)
        vr.camera_coord = self.start_coord

    def reload_obj(self, geo_type, geo_data):
        if geo_type == 'block':
            anchor, size = geo_data
            self.geobjects.append(geo.Block(anchor, size))
        elif geo_type == 'geobject':
            anchor, points = geo_data
            self.geobjects.append(geo.Geobject(anchor, points))
        elif geo_type == 'spike':
            anchor, size = geo_data
            self.geobjects.append(geo.Spike(anchor, size))

    def save_map(self):
        with open(u.path(f"rsc/maps/{self.name}.pkl"), 'wb') as file:
            self.start_coord = vr.camera_coord
            datas = (self.start_coord, self.content)
            pickle.dump(datas, file, pickle.HIGHEST_PROTOCOL)

    def load_map(self, name='default'):
        with open(u.path(f"rsc/maps/{name}.pkl"), 'rb') as file:
            self.start_coord, self.content = pickle.load(file)
        self.reload_map()

