import sys
import struct

def main(self, file):
  file = open(file)
  x = 0
  while True:
    s = file.read(4)
    if len(s) != 4: break
    print x, struct.unpack("4B",s), struct.unpack("I",s)[0]
    x += 4

main(*sys.argv)
