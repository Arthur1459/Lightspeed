import config as cf
import tools as t
from utils import path
import pygame.image as pgi
import pygame.transform as pgt
from glob import glob

def img(filepath, resize=None, full_path=False, flip=(False, False)):
    img_raw = pgt.flip(pgi.load(filepath if full_path else path(f"rsc/visuals/{filepath}")), flip[0], flip[1])
    if resize is None:
        return img_raw
    else:
        return pgt.scale(img_raw, resize)

def load_folder(folderpath, resize=None, files_type="*.png", flip=(False, False)):
    files_paths = glob(path(f"rsc/visuals/{folderpath}/{files_type}"))
    return [img(filepath, full_path=True, resize=resize, flip=flip) for filepath in sorted(files_paths)]

empty = img("empty.png")

player_visuals = {'stand': {'duration': 0.125, 'frames': load_folder("player/stand", resize=cf.player_size)},
                  'run_right': {'duration': 0.05, 'frames': load_folder("player/run", resize=cf.player_size, flip=(False, False))},
                  'run_left': {'duration': 0.05, 'frames': load_folder("player/run", resize=cf.player_size, flip=(True, False))},
                  'jump_right': {'duration': 1, 'frames': load_folder("player/jumpside", resize=cf.player_size, flip=(False, False))},
                  'jump_left': {'duration': 1, 'frames': load_folder("player/jumpside", resize=cf.player_size, flip=(True, False))},
                  'fall': {'duration': 1, 'frames': load_folder("player/fall", resize=cf.player_size, flip=(False, False))},
                  'slide_right': {'duration': 0.05, 'frames': load_folder("player/slide", resize=cf.player_size, flip=(False, False))},
                  'slide_left': {'duration': 0.05, 'frames': load_folder("player/slide", resize=cf.player_size, flip=(True, False))},
                  'dead': {'duration': 0, 'frames': [img('empty.png')]},
                  'grapple': {'duration': 0, 'frames':  [img('player/grapple/grapple_0.png', resize=cf.player_grapple_size)]}}

blocks_visuals = {'metal': load_folder("blocks/metal_blocks")}
spike_visuals = {'frames': load_folder("blocks/fire_blocks"), 'duration': 0.15}
particles_visuals = {'default': {'frames': load_folder("particles/default"), 'duration': 0.2},
             'fire': {'frames': load_folder("particles/fire"), 'duration': 0.1},
             'void': {'frames': load_folder("particles/void"), 'duration': 0.2},
             'star': {'frames': load_folder("particles/star"), 'duration': 1.}}
creatures_visuals = {'bat': {'frames': load_folder("creatures/bat", resize=t.duo(cf.bat['size'])), 'duration': 0.05}}

sync_animations_cycles = [('spike', spike_visuals)]
