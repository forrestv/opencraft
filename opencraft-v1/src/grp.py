import struct
import pygame

def load(path,palette,compressed = False):
    compressed = (path.split(".")[-1] != "grc")
    
    f = open(path,"rb")
    flen = len(f.read())
    f.seek(0)
    
    frames = []
    framecount = struct.unpack("<H",f.read(2))[0]
    size = struct.unpack("<2H",f.read(4))
    for framenum in range(framecount):
        offset = struct.unpack("<2B",f.read(2))
        unknown = struct.unpack("<2B",f.read(2))
        pointer = struct.unpack("<L",f.read(4))[0]
        frames.append([offset,unknown,pointer])
        
    spointers = list(set([x[2] for x in frames]))
    spointers.sort()
    final = []
    for framenum in range(framecount):
        framepointer = frames[framenum][2]
        f.seek(framepointer)
        if compressed:
            linecount = frames[framenum][1][1]
            linepointers = struct.unpack("<"+str(linecount)+"H",f.read(2*linecount))
            lines = []
            for linenum in range(linecount):
                f.seek(framepointer+linepointers[linenum])
                if linenum == linecount-1:
                    if spointers.index(framepointer)+1 == len(spointers):
                        length = flen-linepointers[linenum]-frames[framenum][2]
                    else:
                        length = spointers[spointers.index(framepointer)+1] - frames[framenum][2]-linepointers[linenum]
                else:
                    length = linepointers[linenum+1]-linepointers[linenum]
                line = struct.unpack("<"+str(length)+"B",f.read(length))
                c = 0
                result = [0]*frames[framenum][1][0]
                xpos = 0
                
                while 1:
                    try: v = line[c]
                    except IndexError: break
                    if v == 0x80 or v==0x40 or v==0x00: raise ValueError, "invalid grp"
                    if v > 0x80:
                        xpos += v - 0x80
                    elif v > 0x40:
                        loop = v - 0x40
                        c += 1
                        for x in range(loop):
                            result[xpos] = line[c]
                            xpos += 1
                    elif v <= 0x40:
                        loop = v
                        for x in range(loop):
                            c += 1
                            result[xpos] = line[c]
                            xpos += 1
                    c += 1
                lines.append(result)
                
            s= ""
            for x in lines:
                s = s + struct.pack(str(frames[framenum][1][0])+"B", *x)
                #print x
        else:
            s = f.read(frames[framenum][1][0]*frames[framenum][1][1])
            
        surf = pygame.surface.Surface(size, 0, 8)
        a = pygame.image.fromstring(s, frames[framenum][1], "P")
        
        a.set_palette(palette)
        surf.set_palette(palette)
        
        surf.blit(a, frames[framenum][0])
        surf.set_colorkey(0)
        
        final.append(surf)
    return final
