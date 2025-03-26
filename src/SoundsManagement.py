import random
import pygame
from random import shuffle, randint
import sound_config as scf

def PlayMusic(playlist, volume=scf.music_volume):  # play music
    pygame.mixer.music.fadeout(2)  # stop music which is playing
    pygame.mixer.music.unload()
    shuffle(scf.musics[playlist])
    for path in scf.musics[playlist]:
        pygame.mixer.music.load(path)
    if scf.sound_musics_mode:
        pygame.mixer.music.set_volume(volume/100)  # set the volume of the music (50% default)
    else:
        pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(-1)  # Play it indefinitely (loop)
    return

def PlayEffect(effect, volume=scf.fx_volume):
    if scf.sound_effects_mode:
        effect = pygame.mixer.Sound(scf.fx[effect])
        effect.set_volume(volume/100)
        effect.play()
    return

def updateVolume(music=True, volume=scf.music_volume):
    if music is False:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(scf.music_volume / 100)

