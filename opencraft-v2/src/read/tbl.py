import struct
import ff
import StringIO

def read(file):
    if isinstance(file, str):
        file = open(file)
    file.seek(0,2)
    flen = file.tell()
    file.seek(0)
    
    length = struct.unpack("<H", file.read(2))[0]
    offsets = struct.unpack("<%iH" % length, file.read(2*length))
    
    offsetslist = list(set(offsets))
    offsetslist.sort()
    
    final = []
    for index in range(len(offsets)):
        offset = offsetslist[index]
        listoffset = offsetslist.index(offset)
        try:
            end = offsetslist[listoffset+1]
        except IndexError:
            end = flen
        file.seek(offset)
        final.append(file.read(end-offset-1))
    return final
    
if __name__ == "__main__":
    import sys
    ff.init("archives")
    print read(sys.argv[1])
