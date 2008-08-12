import struct
import tbl

f = open("weapons.dat")
t = tbl.read(open("stat_txt.tbl"))
def g(s):
  s = "<130"+s
  l = struct.calcsize(s)
  r= f.read(l)
  assert len(r) == l
  return struct.unpack(s, r)

s = "HIBHIIBBBBBHHHHHBBHHHH"
assert struct.calcsize("<"+s) == 42, struct.calcsize("<"+s)
l = map(g,s)

print '<meta http-equiv="refresh" content="1"/><table border=2>'
desc = "ID label sprite spell flag min max upgrade type mbehavior mtype explosion inner middle outer dmg bonus cool factor p1 p2 msg icon"
desc = desc.split(" ")
print '<tr><td>'+'</td><td>'.join(desc)+'</td></tr>'
for i, x in enumerate(zip(*l)):
  x = (t[x[0]-1],)+x[1:-2]+(t[x[-2]-1],)+x[-1:]
  print '<tr><td>'+str(i)+'</td><td>'+'</td><td>'.join(map(str,x))+'</td></tr>'
print '</table>'
