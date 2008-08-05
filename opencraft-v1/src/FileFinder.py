import mpq

class FileFinder:
    def __init__(self, path):
        names = [
            ("BroodWar.mpq", "files\\broodat.mpq",),
            ("BroodWar.mpq",),
            ("StarCraft.mpq", "files\\stardat.mpq",),
            ("StarCraft.mpq",),
        ]
        
        for i, x in enumerate(names):
            names[i] = (path + "/" + x[0],) + x[1:]
            
        archives = []
        for x in names:
            a = mpq.Archive(x[0])
            for y in x[1:]:
                a = mpq.Archive(a[y])
            archives.append(a)
            
        self.archives = archives
    def __getitem__(self, item):
        for a in self.archives:
            try:
                f = a[item]
            except KeyError:
                pass
            else:
                return f
        raise KeyError
