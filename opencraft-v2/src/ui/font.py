# available fonts: "8", "10", "12", "14", "16", "16x", "32", "50"

import struct
import pygame

from .. import util
from .. import read

spacelen = {"10": 5, "16x": 12}

fonts = util.cdict(read.read_font)
palettes = util.cdict(read.read_font_palette)

def render(size,palette,text,tight=False):
    font = fonts["files\\font\\font%s.fnt" % size]
    palette = palettes[palette]
    text = str(text)
    curpal = 0
    for mode in range(2):
        p = 0
        h = 0
        for index, c in enumerate(text):
            c = ord(c)
            if c < 7: # 4 -> 2, 1 -> 1
                if c == 4: curpal = 2
                elif c == 1: curpal = 1
                else: curpal = c
                continue
            else:
                c = c - 33
            if c == -1:
                p += spacelen[size]
                continue
            i = font[c]
            if mode == 1:
                i.set_palette(palette[curpal])
                s.blit(i, (p,0))
            p += i.get_width()
            h = max(h,i.get_height())
            if not tight and index < len(text) - 1:
                p += 1
        if mode == 0:
            s = pygame.surface.Surface((p,h),pygame.SRCALPHA)
    return s
