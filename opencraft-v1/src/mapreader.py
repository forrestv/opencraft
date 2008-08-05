import struct
import mpq
import StringIO
from doodads import doodad_types

tilesets = {
    0: "badlands",
    1: "platform",
    2: "install",
    3: "ashworld",
    4: "jungle",
    5: "desert",
    6: "ice",
    7: "twilight",
}

def load(filename):
    if filename.split(".")[-1].lower() in ("scm", "scx"):
        mf = StringIO.StringIO(mpq.Archive(filename)[0])
    else:
        mf = open(filename)
        
    maps = {}
    while True:
        title = mf.read(4)
        if title == "": break
        data = mf.read(struct.unpack("<L",mf.read(4))[0])
        maps[title.strip(" ")] = data
        
    mapdim = struct.unpack("<2H", maps["DIM"])
    
    tileset = tilesets[struct.unpack("<H",maps["ERA"])[0]]
    
    
    tiles = struct.unpack("<"+str(len(maps["MTXM"])/2)+"H",maps["MTXM"])
    tiles = [tiles[x::mapdim[0]] for x in range(0,mapdim[0])]
    
    doodads = []
    thingy = StringIO.StringIO(maps["THG2"])
    while 1:
        raw = thingy.read(10)
        if raw == "": break
        number, x, y, owner, unknown, flag = struct.unpack("<HHHBBH", raw)
        try:
            name = doodad_types[number]
        except KeyError:
            print number,x,y,owner,unknown,flag
            doodads.append((number,x,y))
            continue
        doodads.append((name,x,y))
        
    unit = StringIO.StringIO(maps["UNIT"])
    starts = []
    resources = []
    while 1:
        raw = unit.read(36)
        if raw == "": break
        serial, x, y, type, unknown, flag, validflag, owner, hp, shield, energy, resource, hanger, state, unknown2, unknown3 = struct.unpack("<LHHHHHHBBBBLHHLL", raw)
        if type in (176, 177, 178): resources.append(("min"+str(type-175),x,y,resource))
        elif type in (188,): resources.append(("gas",x,y,resource))
        elif type in (214,): starts.append((x,y))
        elif type in (89,90,93,94,95,96): print "unfinished critter"
        else: print "unknown", type
    return mapdim, tileset, tiles, doodads, starts, resources
    
