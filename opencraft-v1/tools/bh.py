import random

p = 5


heap = [-1] * (2**p-1)

last = 0

def g(num): # num can be index
  return num

def up(num):
  return int((num-1)/2)

def down(num):
  return 2*num+1, 2*num + 2

def swap(a,b):
  heap[a], heap[b] = heap[b], heap[a]

def add(num):
  global last
  heap[last] = num
  cur = last
  while cur != 0:
    upper = up(cur)
    if heap[cur] < heap[upper]:
      swap(cur,upper)
    else: break
    cur = upper
  last += 1

def get_top():
  global last
  res = heap[0]
  last -= 1
  heap[0], heap[last] = heap[last], -1
  cur = 0
  while cur < last:
    downer = down(cur)
    if downer[0] >= len(heap): break
    m = min(downer, key=lambda x: heap[x])
    if heap[cur] > heap[m] and heap[m] != -1:
      swap(cur,m)
      cur = m
    else:
      break
  return res

def change(): pass

def printh():
  l = len(heap) + 1
  l = l / 2
  j = 1
  while j != l*2:
    print heap[j-1:j-1+j]
    j = j * 2

count = 10 # less than 32
print
for i in range(count):
  add(int(random.random()*500))

printh()
print
l = []
for i in range(count):
  l.append(get_top())

print l
m = list(l)
m.sort()
if l != m:
  print "BAD ORDER in",
  for i, (a,b) in enumerate(zip(l,m)):
    if a != b: print i,
