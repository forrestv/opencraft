import pygame.mixer
import read

def start(f):
    f = read.read_music(f)
    pygame.mixer.music.load(f)
    pygame.mixer.music.play(-1)

def fadeout():
    pygame.mixer.music.fadeout(1000)
