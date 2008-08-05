import struct
import sys

def main(self, file):
  file = open(file)
  
  image = struct.unpack("<999I", file.read(999*4))
  print image
  return
  gfx = struct.unpack("<999B", file.read(999*1))
  shadow = struct.unpack("<999B", file.read(999*1))
  unknown = struct.unpack("<999B", file.read(999*1))
  floats = struct.unpack("<999B", file.read(999*1))

main(*sys.argv)
