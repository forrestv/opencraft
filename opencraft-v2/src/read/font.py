import struct
import pygame

def read_font_palette(f):
    i = pygame.image.load(f)
    palette = []
    for t in range(i.get_width()/8):
        r = []
        for c in range(8):
            color = i.get_at((t*8+c,0))
            r.append(color[:3])
        palette.append(r)
    return palette

def read_font(file):
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
