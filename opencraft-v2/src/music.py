import pygame.mixer
import read

def start(f):
    f = read.read_music(f)
    pygame.mixer.music.load(f)
    pygame.mixer.music.play()
