import struct
import sys
import pygame

find = [
(75,79,111),
(99,107,147),
]

if 1:
  palette = open('jungle.wpe').read()
  palette = struct.unpack(str(len(palette))+"B",palette)
  palette = [palette[4*x:4*x+3] for x in range(len(palette)/4)]

image1 = pygame.image.load('a.png')
image2 = pygame.image.load('b.png')

def get_palette(color):
  good = []
  if 1:
    for i in range(256):
      c = palette[i]
      if c == color:
        good.append(i)
  return good

for x in range(250):
  for y in range(250):
    p1 = image1.get_at((x,y))[:3]
    p2 = image2.get_at((x,y))[:3]
    p1 = get_palette(p1)
    p2 = get_palette(p2)
    if p1 != p2 or len(p1) != len(p2): print (p1,p2)


sys.exit()
for x in range(len(palette)):
  if palette[x] in find:
    print x, palette[x], "next", palette[x+1]

pygame.init()
d = pygame.display.set_mode((160,160))
for x in range(256):
  c = palette[x]
  y = x % 16
  z = (x-y)/16
  for a in range(10):
   for b in range(10):
    d.set_at((y*10+a,z*10+b),c)
while 1: pygame.display.update()
