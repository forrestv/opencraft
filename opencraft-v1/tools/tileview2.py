import psyco
psyco.full()

import struct
import pygame
import os, time

import cdict

def read_minitile(index):
  if index % 2 == 1:
    return pygame.transform.flip(minitiles[index-1], True, False)
  else:
    vr4.seek(index/2*64)
    minitile = vr4.read(64)
    minitile = pygame.image.fromstring(minitile,(8,8),"P")
    minitile.set_palette(palette)
    return minitile

def read_tile(index):
    cv5.seek(52*index)
    row = cv5.read(52)
    row = struct.unpack("26H",row)
    indeces = row[10:]
    row = row[:10]
    frow = []
    for i in indeces:
      #if i == 0: continue
      tile = pygame.surface.Surface((32,32)) # should be 8?
      vx4.seek(i*32)
      minindex = struct.unpack("16H",vx4.read(32))
      vf4.seek(i*32)
      walkable = struct.unpack("16H",vf4.read(32))
      walkable = ''.join(map(chr,walkable))
      w = pygame.image.fromstring(walkable,(4,4),"P")
      w.set_palette([(0,0,0),(255,255,255)]*100)
      for x in range(4):
        for y in range(4):
          tile.blit(minitiles[minindex[x+y*4]],(x*8,y*8))
      frow.append(tile)
    return frow+[row+indeces]

def main():
  global cv5,vx4,vf4,vr4
  global palette,minitiles
  d = pygame.display.set_mode((32*16*2,32*2))
  
  os.chdir("tileset/platform")
  cv5 = open("platform.cv5")
  vx4 = open("platform.vx4")
  vf4 = open("platform.vf4")
  vr4 = open("platform.vr4")
  wpe = open("platform.wpe")
  
  palette = wpe.read()
  palette = struct.unpack(str(len(palette))+"B",palette)
  palette = [palette[4*x:4*x+3] for x in range(len(palette)/4)]
  
  minitiles = cdict.cdict(read_minitile)
  tiles = cdict.cdict(read_tile)
  
  print "start"
  z = time.time()
  for x in range(1513): pass
  #tiles[x]
  print "stop"
  print time.time()-z
  for n, y in enumerate(tiles):
    d.fill((0,0,0))
    for x in range(len(y)-1):
      d.blit(pygame.transform.scale(y[x],(64,64)),(x*64,0))
    print n, y[-1]
    pygame.display.update()
    pygame.time.delay(1000)
main()
