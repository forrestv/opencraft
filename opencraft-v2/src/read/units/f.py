import struct
import sys

t = []
for l in open(sys.argv[1]).read().split('\n'):
 if l:
  t.append(l.split())

d = open(sys.argv[2]).read()
for i in t:
  for ty in 'bBhHiI':
    try:
      f = struct.pack(ty*(len(i)-1), *map(int,i[1:]))
    except struct.error:
      pass
    else:
      c = 0
      while True:
        c = d.find(f, c+1)
        if c == -1: break
        print i[0], ty, c, c+228*struct.calcsize(ty)
