import struct
import pygame

def init(palette):
    f = open("star.spk","rb")
    header = struct.unpack("<H",f.read(2))[0]
    header = struct.unpack("<"+str(header)+"H",f.read(header*2))
    
    star = []
    for x in range(len(header)):
        img = pygame.surface.Surface((640,480),pygame.SRCALPHA,32)
        layer = []
        for y in range(header[x]):
            posx, posy, posfile = struct.unpack("<3H2x",f.read(8))
            
            pos = f.tell() ; f.seek(posfile)
            sizex, sizey = struct.unpack("<2H",f.read(4))
            data = f.read(sizex*sizey)
            f.seek(pos)
            surf = pygame.image.fromstring(data,(sizex,sizey),"P")
            surf.set_palette(palette)
            surf.set_colorkey(0)
            for xadd in (-640,0,640):
                for yadd in (-480,0,480):
                    img.blit(surf,(posx-sizex/2+xadd,posy-sizex/2+yadd))
        star.append(img)
    return star
    
def draw(view):
    pos = -view.pos
    for num in range(len(view.star)):
        p = pos/(num+4)
        p = p % (640,480)
        view.screen.blit(view.star[num],p)
        view.screen.blit(view.star[num],p-(640,0))
        view.screen.blit(view.star[num],p-(640,480))
        view.screen.blit(view.star[num],p-(0,480))
        
