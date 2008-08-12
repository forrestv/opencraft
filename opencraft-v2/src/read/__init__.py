import os
import mpq

from .. import Config

def read_bin(f):
    import bin
    return bin.Node(files[f].fakefile)
    
def read_smk(f):
    import pysmk
    return pysmk.SMKReader(files[f].offsetfile)
    
def read_exe_icon(f):
    import exe_icon
    return exe_icon.read_icon(files[f].string)
    
def read_pcx(f):
    import pygame
    return pygame.image.load(files[f].fakefile)
    
def read_font(f):
    import font
    return font.read_font(files[f].fakefile)
    
def read_font_palette(f):
    import font
    return font.read_font_palette(files[f].fakefile)
    
def read_wav(f):
    import wav
    return wav.read_wav(files[f].file)

def read_music(f):
    return files[f].file

class FileWrapper(object):
    def __init__(self,file):
        self._file = file
    @property
    def file(self):
        return iter(self._file)
    @property
    def offsetfile(self):
        assert not self._file.encrypted and not self._file.compressed and not self._file.imploded
        f = open(self._file._archive.filename, 'rb')
        f.seek(self._file._archive.offset + self._file.offset)
        return f
    @property
    def fakefile(self):
        import cStringIO
        return cStringIO.StringIO(self.string)
    @property
    def string(self):
        return str(self._file)
        
class FileFinder:
    def __init__(self, path):
        self.archives = []
        a = mpq.Archive(os.path.join(path, "BroodWar.mpq"))
        self.archives.append(mpq.Archive(a["files\\broodat.mpq"]))
        self.archives.append(a)
        a = mpq.Archive(os.path.join(path, "StarCraft.mpq"))
        self.archives.append(mpq.Archive(a["files\\stardat.mpq"]))
        self.archives.append(a)
    def __getitem__(self, item):
        for a in self.archives:
            try:
                f = a[item]
            except IndexError:
                pass
            else:
                return FileWrapper(f)
        raise KeyError, item
        
files = FileFinder(os.path.join(Config.path, "archives"))
