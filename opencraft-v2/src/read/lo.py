import struct

def read_struct(f, s):
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
    for frame in load(open(sys.argv[1])):
        print frame
