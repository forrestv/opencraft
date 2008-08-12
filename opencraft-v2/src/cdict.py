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
