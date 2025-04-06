from glob import glob
from utils import path

def soundpath(filepath, full_path=False):
    return filepath if full_path else path(f"rsc/sounds/{filepath}")

def load_soundfolder(folderpath, files_type="*.mp3"):
    files_paths = glob(path(f"rsc/sounds/{folderpath}/{files_type}"))
    return [soundpath(filepath, full_path=True) for filepath in sorted(files_paths)]

def load_sfx():
    files_paths = glob(path(f"rsc/sounds/sfx/*.mp3"))
    return {filepath.split('rsc/sounds/sfx/')[1].replace('.mp3', ''): soundpath(filepath, full_path=True) for filepath in sorted(files_paths)}

music_volume = 50
sound_musics_mode = True

sfx_volume = 40
sound_effects_mode = True

musics = {'ingame': load_soundfolder('musics/ingame'),
          'menu': load_soundfolder('musics/menu')}
sfx = load_sfx()
print(sfx)
