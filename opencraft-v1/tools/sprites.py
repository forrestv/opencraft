import struct
import sys

import tbl

t = tbl.read("data/broodat.mpq/arr/images.tbl")
sp = open("data/broodat.mpq/arr/images.dat")

def main(self, file):
  file = open(file)
  
  image = struct.unpack("<517H", file.read(517*2))
  length = (-1,)*130 + struct.unpack("<387B", file.read(387*1))
  unk1 = struct.unpack("<517B", file.read(517*1))
  unk2 = struct.unpack("<517B", file.read(517*1))
  circ = (-1,)*130 + struct.unpack("<387B", file.read(387*1))
  vert = (-1,)*130 + struct.unpack("<387B", file.read(387*1))
  image2 = []
  for x in image:
    sp.seek(x*4)
    y = struct.unpack("<I", sp.read(4))[0]
    y = t[y-1]
    image2.append(y)
  circ2 = []
  for x in circ:
    sp.seek((x+561)*4)
    y = struct.unpack("<I", sp.read(4))[0]
    y = t[y-1]
    circ2.append(y)
  out = zip(image2, length, unk1, unk2, circ2, vert)
  for x in enumerate(out):
    print x

main(*sys.argv)
