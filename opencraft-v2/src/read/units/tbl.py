import struct

def read(file):
  file.seek(0,2)
  flen = file.tell()
  file.seek(0)
  
  length = struct.unpack("<H", file.read(2))[0]
  offsets = struct.unpack("<%iH" % length, file.read(2*length))
  
  offsetslist = list(set(offsets))
  offsetslist.sort()
  
  final = []
  for index in range(len(offsets)):
    offset = offsets[index]
    listoffset = offsetslist.index(offset)
    try:
      end = offsetslist[listoffset+1]
    except IndexError:
      end = flen
    file.seek(offset)
    final.append(file.read(end-offset-1))
  return final
