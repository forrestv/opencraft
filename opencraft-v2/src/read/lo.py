import struct
from common import read_struct

def g(f, s):
    l = struct.calcsize(s)
    d = f.read(l)
    return struct.unpack(s, d)
    
def load(f):
    frames = read_struct(f,"<I")[0]
    overlays = read_struct(f,"<I")[0]
    offsets = read_struct(f,"<%iI"%frames)
    result = []
    for o in offsets:
        frame = []
        f.seek(o)
        poss = read_struct(f,"<%ib"%(2*overlays))
        for i in range(overlays):
            frame.append((poss[i*2],poss[i*2+1]))
        result.append(frame)
    return result
    
if __name__ == "__main__":
    import sys
    print load(open(sys.argv[1]))
