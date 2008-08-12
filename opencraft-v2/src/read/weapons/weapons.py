import struct

class WeaponType:
    def __init__(self, data):
        assert len(data) == 22
        self.label = data[0]
        self.sprite = data[1]
        self.spell = data[2]
        self.flag = data[3]
        self.range = data[4:6]
        self.upgrade_type = data[6]
        self.type = ["unknown","explosive","concussive","normal","spell"][data[7]]
        self.mbehavior = data[8]
        self.mtype = data[9]
        self.explosion = data[10]
        self.splash = data[11:14]
        self.damage = data[14]
        self.bonus = data[15]
        self.cool = data[16]
        self.factor = data[17]
        self.pos1 = data[18]
        self.pos2 = data[19]
        self.msg = data[20]
        self.icon = data[21]

def g(s):
  s = "<130"+s
  l = struct.calcsize(s)
  r = f.read(l)
  assert len(r) == l
  return struct.unpack(s, r)

s = "HIBHIIBBBBBHHHHHBBHHHH"
assert struct.calcsize("<"+s) == 42

f = open("weapons.dat")

l = map(g, s)

l = zip(*l)

l = map(WeaponType, l)
