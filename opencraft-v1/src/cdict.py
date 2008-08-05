"""
Caching dictionary
"""

class cdict(object):
    def __init__(self, getter):
        self.dict = {}
        self.getter = getter
    def __getitem__(self, item):
        if item not in self.dict:
            self.dict[item] = self.getter(item)
        return self.dict[item]
    def get(self, item, default = None):
        if item not in self.dict:
            try:
                self.dict[item] = self.getter(item)
            except:
                return default
        return self.dict[item]
        
del cdict

class cdict(dict):
    def __init__(self, getter):
        dict.__init__(self)
        self.getter = getter
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            self[item] = self.getter(item)
            return dict.__getitem__(self, item)
