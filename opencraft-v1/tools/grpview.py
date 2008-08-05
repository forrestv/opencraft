import sys
sys.path.insert(0,".")

import struct
from src.util import unique
import pygame

import src.grp as grp

class null: pass
pygame.init()
v = null()
pal = file("palettes/unit","rb").read()
#pal = file("out","rb").read()
v.palette = []
for i in range(0,len(pal),3):
  v.palette.append((ord(pal[i]),ord(pal[i+1]),ord(pal[i+2])))
pal = file("palettes/orange","rb").read()
#pal = file("out","rb").read()
v.palette2 = []
for i in range(0,len(pal),3):
  v.palette2.append((ord(pal[i]),ord(pal[i+1]),ord(pal[i+2])))
x = [(x,grp.load(x,v.palette,True)) for x in sys.argv[1:]]
s = x[0][1][0].get_size()
d = pygame.display.set_mode((8*s[0],8*s[1]))
print "\n".join([" ".join((y[0],str(len(y[1])))) for y in x])
print x[0][1][0].get_size()
f = 0
q = pygame.font.SysFont("Times New Roman", 12, False)
while 1:
  d.fill((128,128,128))
  for g in x:
    d.blit(pygame.transform.scale(g[1][f%len(g[1])],(s[0]*8,s[1]*8)),(0,0))
  b = f%len(g[1])
  z = str(int(oct(b)))
  b = ""
  for zz in z:
    b += {"0":"000","1":"001","2":"010","3":"011","4":"100","5":"101","6":"110","7":"111"}[zz]
  r = q.render(b,True,(255,255,255))
  sa = r.get_size()
  sb = d.get_size()
  d.blit(r,(sb[0]-sa[0],sb[1]-sa[1]))
  pygame.display.update()
  pygame.time.wait(1000)
  f += 1
  #if f >= len(g): break
