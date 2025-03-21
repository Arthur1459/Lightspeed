import config as cf
from utils import path
import pygame.image as pgi
import pygame.transform as pgt

def img(filepath, size=None):
    if size is None:
        return pgi.load(path(f"rsc/visuals/{filepath}"))
    else:
        return pgt.scale(pgi.load(path(f"rsc/visuals/{filepath}")), size)

player_visuals = {'default': [img('player/default.png', cf.player_size)]}
