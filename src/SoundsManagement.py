import random
import pygame
from random import shuffle, randint
import sound_config as scf

current_playlist = None
playlist_started = False
def PlayMusic(playlist, volume=scf.music_volume):  # play music
    global current_playlist, playlist_started
    if playlist != current_playlist:
        playlist_started = False
        current_playlist = playlist
        pygame.mixer.music.fadeout(2)  # stop music which is playing
        pygame.mixer.music.unload()
        shuffle(scf.musics[playlist])
        for path in scf.musics[playlist]:
            pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume/100)  # set the volume of the music (50% default)
    if scf.sound_musics_mode:
        if playlist_started:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play(-1)  # Play it indefinitely (loop)
            playlist_started = True
    return

def StopMusic():
    global playlist_started
    pygame.mixer.music.pause()

def PlayEffect(effect, volume=None):
    if volume is None: volume = scf.sfx_volume
    if scf.sound_effects_mode:
        effect = pygame.mixer.Sound(scf.sfx[effect])
        effect.set_volume(volume/100)
        effect.play(maxtime=2000)
    return

def updateVolume(volume=scf.music_volume):
    pygame.mixer.music.set_volume(volume / 100)

