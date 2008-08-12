import struct
import pygame
import palettes

class open:
    def __init__(self, f, palette):
        layers = struct.unpack("<H",f.read(2))[0]
        header = struct.unpack("<"+str(header)+"H",f.read(layers*2))
        stars = []
        for x in header:
            img = pygame.surface.Surface((640,480),pygame.SRCALPHA,32)
            layer = []
            for y in range(x):
                posx, posy, posfile = struct.unpack("<3H2x",f.read(8))
                
                pos = f.tell() ; f.seek(posfile)
                sizex, sizey = struct.unpack("<2H",f.read(4))
                data = f.read(sizex*sizey)
                f.seek(pos)
                surf = pygame.image.fromstring(data,(sizex,sizey),"P")
                surf.set_palette(palettes.get('unit')
                surf.set_colorkey(0)
                for xadd in (-640,0,640):
                    for yadd in (-480,0,480):
                        img.blit(surf,(posx+xadd,posy+yadd))
            star.append(img)
        self.stars = star
    def draw(self, display, pos):
        for num, star in enumerate(self.stars):
            p = -pos/(num+4)
            p = p % (640,480)
            for xadd in (-640,0):
                for yadd in (-480,0):
                    img.blit(surf, p + (xadd, yadd))
