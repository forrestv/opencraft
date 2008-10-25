import pefile
import cStringIO
import struct
import pygame

def read_struct(f, s):
    l = struct.calcsize(s)
    d = f.read(l)
    return struct.unpack(s, d)

def process(f):
    size, width, height, planes, bitcount, compression, sizeimage, \
        xpelspermeter, ypelspermeter, clrused, clrimportant = read_struct(f, "IIIHHIIIIII")
    height /= 2
    palette = [list(reversed(read_struct(f, "BBBx"))) for i in range(16)]
    xor_img2 = f.read(width*height/2)
    xor_img = []
    for c in xor_img2:
        c = ord(c)
        xor_img.append(chr(((c&0x0F)>>0)*17))
        xor_img.append(chr(((c&0xF0)>>4)*17))
    xor_img = pygame.image.fromstring(''.join(xor_img), (width, height), "P", True)
    xor_img.set_palette([x for i in xrange(16) for x in palette])
    new_xor = pygame.Surface(xor_img.get_size(), pygame.SRCALPHA, 32)
    new_xor.blit(xor_img, (0, 0))
    xor_img = new_xor
    xor_pix = pygame.surfarray.pixels_alpha(xor_img)
    and_img2 = f.read(width*height/8)
    and_img = []
    for c in and_img2:
        c = ord(c)
        for i in reversed(xrange(8)):
            and_img.append(0 if c & (1<<i) else 255)
    and_img = pygame.image.fromstring(''.join(map(chr,and_img)), (width, height), "P", True)
    and_pix = pygame.surfarray.pixels2d(and_img)
    xor_pix[:,:] = and_pix
    return xor_img
    
def read_icon(string):
    pe = pefile.PE(data=string)
    rt_string_idx = [entry.id for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries].index(pefile.RESOURCE_TYPE['RT_ICON'])
    rt_string_directory = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_string_idx]
    rt_string_directory = [e for e in pe.DIRECTORY_ENTRY_RESOURCE.entries if e.id == pefile.RESOURCE_TYPE['RT_ICON']][0]
    entry = rt_string_directory.directory.entries[1] # XXX
    offset = entry.directory.entries[0].data.struct.OffsetToData
    size = entry.directory.entries[0].data.struct.Size
    data = pe.get_memory_mapped_image()[offset:offset+size]
    f = cStringIO.StringIO(data)
    return process(f)
