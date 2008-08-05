"""

World drawing

make fog

blit it with MAX to Player.fog


three tile states:

  in tmpfog and playerfog:
    units & ground visible
  in playerfog:
    ground visible, but darkened
  none:
    black

draw ground
draw tmpfog
draw selection circles/hit bars/debug info
draw units
draw Player.fog


"""


import pygame
import math

import cdict


def get_overlay(radius):
    k = 3 # feather radius
    s = pygame.Surface((radius*4, radius*4), pygame.SRCALPHA, 32)
    for x in xrange(s.get_width()):
        for y in xrange(s.get_height()):
            d = math.sqrt((x-radius*2)**2+(y-radius*2)**2)
            c = radius - d
            c = 255*c/k
            c = int(c)
            if c < 0:
                c = 0
            elif c > 255:
                c = 255
            s.set_at((x,y), (c, c, c))
    return s

def make_fog(size, views):
    s = pygame.Surface(size)
    for pos, radius in views:
        o = overlays[radius]
        pos = (pos[0]-o.get_width()/2, pos[1]-o.get_height()/2)
        s.blit(o, pos, None, pygame.BLEND_MAX)
    return s

overlays = cdict.cdict(get_overlay)

if __name__ == "__main__":
    import random, time
    d = pygame.display.set_mode((256,256))
    while True:
        x = [((int(random.random()*256), int(random.random()*256)), int(random.random()*30)) for i in xrange(20)]
        f = make_fog((256,256), x)
        d.fill((0,0,0))
        d.blit(f, (0, 0))
        pygame.display.update()
        time.sleep(1)
