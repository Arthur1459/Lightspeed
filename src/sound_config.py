from glob import glob
from utils import path

def soundpath(filepath, full_path=False):
    return filepath if full_path else path(f"rsc/sounds/{filepath}")

def load_soundfolder(folderpath, files_type="*.mp3"):
    files_paths = glob(path(f"rsc/sounds/{folderpath}/{files_type}"))
    return [soundpath(filepath, full_path=True) for filepath in sorted(files_paths)]

music_volume = 50
sound_musics_mode = False

fx_volume = 50
sound_effects_mode = False

musics = {'ingame': load_soundfolder('musics/ingame')}
print(musics)
fx = {}
