import os
import pygame
import time

from .. import ui
from .. import read

class Video(ui.UI):
    def __init__(self, name):
        ui.UI.__init__(self)
        self.name = name
        self.add_call(self.
    def work(self):
        smk = read.read_smk(self.name)
        wide_size = (2*smk.video.get_width(), smk.video.get_height())
        self.display.fill((0, 0, 0))
        smk.audio[0].play()
        while self.run:
            start = time.time()
            self.update()
            try:
                smk.next()
            except StopIteration:
                break
            video = pygame.transform.smoothscale(smk.video, wide_size)
            self.display.blit(video, ui.get_center_coords(video.get_size(), self.display.get_size()))
            time.sleep(1/smk.fps-(time.time()-start))
        smk.audio[0].stop()
    def mousebuttondown(self, **kwargs):
        self.run = False
    keydown = mousebuttondown
