import sys

sys.path.insert(0, ".")

from src import path

map = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
[1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

p = path.path((10,10))
p.set_map(map)
for t in xrange(1000):
  q=p.get_path((0,0),0,(9,9))

for y in range(len(map)):
  for x in range(len(map[0])):
    if not map[x][y]: print "#",
    elif (x,y) in q: print "X",
    else: print " ",
  print
