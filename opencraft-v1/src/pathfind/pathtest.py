import time
import sys
import pygame
import path

c = 10

map = pygame.image.load(sys.argv[1])

size = map.get_size()

d = pygame.display.set_mode(size)
d.blit(map,(0,0))
pygame.display.update()

pathf = path.path(size)

pathf.set_map(0, map)

s = time.time()
for i in xrange(c):
  q = pathf.get_path((0,0),0,(size[0]-1,size[1]-1))
e = time.time()
print (e-s)/c


l = None
for i in q:
  if l != None:
    pygame.draw.line(d,(255,0,0),l,i)
  l = i

while True: pygame.display.update()
