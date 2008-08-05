import struct
import sys
wpe = open(sys.argv[1])

import pygame

find = [
(75,79,111),
(99,107,147),
]

if 1:
  palette = wpe.read()
  palette = struct.unpack(str(len(palette))+"B",palette)
  palette = [palette[4*x:4*x+3] for x in range(len(palette)/4)]

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
