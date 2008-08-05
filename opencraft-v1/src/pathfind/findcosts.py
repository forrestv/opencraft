import math

cost = math.sqrt(2**2+1**2)
l = []
for i in range(1,1000):
  c = cost*i
  r = int(c+.5)
  d = abs(c-r)
  l.append((d, i, r))

l.sort()
for j in l:
  print j
