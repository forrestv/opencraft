import struct
import tbl

t = tbl.read("data/broodat.mpq/arr/images.tbl")
for i in range(520):
 x = i
 sp = open("data/broodat.mpq/arr/sprites.dat")
 sp.seek(x*2)
 x = struct.unpack("<H", sp.read(2))[0]
 
 sp = open("data/broodat.mpq/arr/images.dat")
 sp.seek(x*4)
 x = struct.unpack("<I", sp.read(4))[0]
 
 x = t[x-1]
 
 x = x.replace("\\","/").lower()
 x = '/'.join(x.split("/")[2:])
 if x:
   print "  %i: \"%s\"," % (i, x)
