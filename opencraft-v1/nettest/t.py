import subprocess
while True:
  subprocess.call(''.join(map(chr,[67, 58, 92, 80, 114, 111, 103, 114, 97, 109, 32, 70, 105, 108, 101, 115, 92, 83, 116, 97, 114, 
99, 114, 97, 102, 116, 92, 83, 116, 97, 114, 99, 114, 97, 102, 116, 46, 101, 120, 101])))

import sys,math
import pygame
import network

network.init(int(sys.argv[1]))

selection = []

def get_my_orders(units):
  global selection
  o = []
  for e in pygame.event.get():
    if e.type == pygame.MOUSEBUTTONDOWN:
     if e.button == 1:
      ma = 10000000
      for u in [u for u in units if u.owner == me and u.type == 1]:
        v = (e.pos[0] - u.pos[0], e.pos[1] - u.pos[1])
        m = math.sqrt(v[0]**2+v[1]**2)
        if m < ma:
          de = u
          ma = m
      selection = [de]
     elif e.button == 3:
       for u in selection:
         o.append((units.index(u), map(float,e.pos)))
    
  return o
  return [(0,(1,1))]

class Unit:
  type = 1
  pos = None
  dest = None
  cool = 0
  @property
  def speed(self):
    return .5+(2-self.type)*.5
  owner = None

def logic(units, o): # completely deterministic
  for order in o:
    units[order[0]].dest = order[1]
  for u in units:
    u.cool += 1
    if u.type == 1 and u.cool > 2000:
      u.cool = 0
      n = Unit()
      n.type = 2
      n.pos = u.pos
      n.dest = u.pos
      n.owner = u.owner
      units.append(n)
    elif u.type == 2:
      de = u
      for n in units:
        ma = 10000000
        for x in [u for u in units if u.owner != me and u.type == 1]:
          v = (u.pos[0] - x.pos[0], u.pos[1] - x.pos[1])
          m = math.sqrt(v[0]**2+v[1]**2)
          if m < ma:
            de = x
            ma = m
      if ma < 10:
        units.remove(de)
        units.remove(u)
        if de in selection: selection.remove(de)
      u.dest = de.pos
    v = (u.dest[0] - u.pos[0], u.dest[1] - u.pos[1])
    m = math.sqrt(v[0]**2+v[1]**2)
    if m > u.speed:
      m = m/u.speed
      v = (v[0]/m,v[1]/m)
    #m *= 50.
    #m *= 4 #0 pixels per second
    u.pos = (u.pos[0]+v[0],u.pos[1] + v[1])

d = pygame.display.set_mode((400,400))
units = []
me = int(sys.argv[3])
for x in range(6):
  u = Unit()
  u.pos = (x*20.,x*20.)
  u.dest = u.pos
  u.owner = x%2
  units.append(u)
raw_input()
while True:
  orders = get_my_orders(units)
  network.send(int(sys.argv[2]),repr(orders))
  i = eval(network.get())
  all_orders = []
  all_orders.extend(orders)
  all_orders.extend(i)
  # magic
  logic(units, all_orders)
  d.fill((0,0,0))
  for u in units:
    f = 1
    if u in selection:
      f = 0
    pygame.draw.circle(d, (255*(u.owner!=me),255*(u.owner==me),0), u.pos, 16 if u.type==1 else 4,f)
  pygame.display.update()
  #print "cycle"
  #pygame.time.wait(10)
