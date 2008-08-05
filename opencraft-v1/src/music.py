import pygame
import os
import random

def preinit(view):
    pygame.mixer.pre_init(22050,8,2,2**18)
    
def init(view):
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    play(os.path.join("music", "title.ogg"), view)
    
def fade(view):
    pygame.mixer.music.fadeout(500)
    
last = None

def next(view):
    global last
    r = last
    while r == last:
        r = str(int(random.random()*3)+1)
    last = r
    play(os.path.join("music","terran"+r+".ogg"),view)
    
def play(name,view):
    pygame.mixer.music.load(name)
    pygame.mixer.music.set_volume(view.config.musicVolume)
    pygame.mixer.music.play(1)
