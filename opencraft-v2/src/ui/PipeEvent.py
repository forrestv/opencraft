import os
import select

class PipeEvent(object):
    def __init__(self):
        self.read, self.write = os.pipe()
    def isSet(self):
        return select.select([self.read], [], [], 0)[0] != []
    def set(self):
        os.write(self.write, "\x00")
    def clear(self):
        while self.isSet():
            os.read(self.read, 2**16)
    def wait(self, timeout=None):
        select.select([self.read], [], [], timeout)
