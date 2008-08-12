import struct

def read_struct(f, s):
    l = struct.calcsize(s)
    d = f.read(l)
    return struct.unpack(s, d)
