import time
import sys
import pygame
import path

c = 2

map = pygame.image.load(sys.argv[1])

d = map.get_size()
pathf = path.path(d)

pathf.set_map(0, map)

s = time.time()
for c in xrange(c):
  q = pathf.get_path((0,0),0,(d[0]-1,d[1]-1))
e = time.time()
print (e-s)/c

d = pygame.display.set_mode(d)
d.blit(map,(0,0))

l = None
for i in q:
  if l != None:
    pygame.draw.line(d,(255,0,0),l,i)
  l = i

while True: pygame.display.update()
