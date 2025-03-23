import vars as vr
import config as cf
import tools as t
import utils as u
import geometry as geo
import pickle

import pygame as pg

class Map:
    def __init__(self, name='default'):
        self.name = name

        self.geobjects = []
        self.content = {'geobjects': set()}

    def add_block(self, anchor, size, update=False):
        geo_type, geo_data = 'block', (anchor, size)
        self.content['geobjects'].add((geo_type, geo_data))
        if update: self.reload_obj(geo_type, geo_data)
    def add_geobject(self, anchor, points, update=False):
        geo_type, geo_date = 'geobject', (anchor, points)
        self.content['geobjects'].add((geo_type, geo_date))
        if update: self.reload_obj(geo_type, geo_date)
    def remove(self, obj, obj_type='geobject'):
        if obj_type == 'geobject':
            self.geobjects.remove(obj)
            self.content['geobjects'].remove((obj.get_type(), obj.get_data()))
        else:
            pass
    def reload_map(self):
        for geo_type, geo_data in self.content['geobjects']:
            self.reload_obj(geo_type, geo_data)

    def reload_obj(self, geo_type, geo_data):
        if geo_type == 'block':
            anchor, size = geo_data
            self.geobjects.append(geo.Block(anchor, size))
        if geo_type == 'geobject':
            anchor, points = geo_data
            self.geobjects.append(geo.Geobject(anchor, points))

    def save_map(self):
        with open(u.path(f"rsc/maps/{self.name}.pkl"), 'wb') as file:
            pickle.dump(self.content, file, pickle.HIGHEST_PROTOCOL)

    def load_map(self, name='default'):
        with open(u.path(f"rsc/maps/{name}.pkl"), 'rb') as file:
            self.content = pickle.load(file)
        self.reload_map()

