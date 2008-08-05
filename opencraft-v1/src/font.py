import sys
import struct
import pygame

badpalette = [(x,x,x) for x in range(256)]

palettes = {}

def load_palette_group(filename, name):
    i = pygame.image.load(filename)
    for t in range(i.get_width()/8):
        r = []
        for c in range(8):
            color = i.get_at((t*8+c,0))
            r.append(color[:3])
        palettes[name+str(t)] = r
        
def render(size,text,palette="game5",tight=False):
    size = str(size)
    text = str(text)
    if size not in fonts: raise ValueError, "invalid size"
    font = fonts[size]
    p = 0
    h = 0
    for c in text:
        c = ord(c) - 33
        if c == -1:
            p += 8
            continue
        i = font[c]
        h = max(i.get_height(),h)
        p += i.get_width()
        if not tight:
            p += 1
    s = pygame.surface.Surface((p,h),0,8)
    s.set_colorkey(0)
    s.set_palette(badpalette)
    p = 0
    for c in text:
        c = ord(c) - 33
        if c == -1:
            p += 8
            continue
        i = font[c]
        s.blit(i, (p,0))
        p += i.get_width()
        if not tight:
            p += 1
    # 0 (1 2 3 4 5 6) 7
    s.set_palette(palettes[palette])
    return s
    
def load():
    global fonts
    fonts = {}
    for name in ("8", "10", "12", "14", "16", "16x", "32", "50"):
        name2 = "font/font%s.fnt" % name
        fonts[name] = readfont(name2)
    load_palette_group("images/gamefont.pcx","game")
    
def readfont(path):
    file = open(path)
    file.seek(0,2)
    flen = file.tell()
    file.seek(0)
    
    magic = file.read(5)
    if magic != "FONT ": raise ValueError, "invalid magic"
    
    info = file.read(3)
    info = struct.unpack("3B", info)
    length = info[0] - 32
    max_width = info[1]
    max_height = info[2]
    
    pad = file.read(4)
    pad = struct.unpack("4B", pad)
    if pad != (0,0,0,0): raise ValueError, "invalid padding"
    
    offsets = struct.unpack("%iI" % length, file.read(4*length))
    
    offsetlist = list(offsets)
    offsetlist.sort()
    
    final = []
    for (index,offset) in enumerate(offsets):
        if index + 1 == len(offsets):
            end = flen
        else:
            end = offsets[index+1]
        file.seek(offset)
        s = file.read(end-offset)
        if s == "": continue
        s = struct.unpack(str(len(s))+"B", s)
        width = s[0]
        height = s[1]
        xoffset = s[2]
        yoffset = s[3]
        r = pygame.surface.Surface((width+xoffset,height+yoffset),0,8)
        r.set_colorkey(0)
        r.set_palette(badpalette)
        p = 0
        for x in s[4:]:
            p += (x >> 3) & 0x1F
            z = width
            r.set_at((xoffset+p%z,yoffset+p//z), (x & 0x07))
            p += 1
        #if index >= len(characters):
        #  final["un"+str(index)] = r
        #else:
        #  char = characters[index]
        #  final[char] = r
        final.append(r)
    return final
    
if __name__ == "__main__":
    pygame.init()
    d = pygame.display.set_mode((30*16,30*16))
    load()
    #s = render(50,"All rights reserved.")
    #size = s.get_size()
    #s = pygame.transform.scale(s,(size[0]*8,size[1]*8))
    #d.blit(s,(0,0))
    #s = pygame.surfarray.pixels2d(s)
    #for (x,l) in enumerate(s):
    # for (y,m) in enumerate(l):
    #   if m in (0,8): continue
    #   #d.blit(render(8,m),(x*8,y*8))
    p = 0
    for x in map(chr,range(256)):
        x = render("16x",x)
    #  #if len(x) == 1: continue
        d.blit(x, (p%16*30,p//16*30))
        print x, "at", p
        p += 1
    while True:
        pygame.display.update()
