class cdict(object):
    def __init__(self, getter):
        self.getter = getter
        self._dict = {}
    def __getitem__(self, item):
        try:
            return self._dict[item]
        except KeyError:
            self._dict[item] = result = self.getter(item)
            return result

class edict(dict):
    def __init__(self, getter, timeout):
        self.getter = getter
        self.timeout = timeout
        self._dict = {}
    def __getitem__(self, item):
        try:
            result = self._dict[item]
        except KeyError:
            self._dict[item] = [None, self.getter(item)]
            result = self._dict[item]
        now = time.time()
        result[0] = now
        oldest = now + self.timeout
        for key in self._dict.keys():
            if self._dict[key][0] > oldest:
                del self._dict[key]
        return result[1]

def expire_memoize(timeout):
    def func(userfunc):
        results = edict(lambda x: userfunc(*x), timeout)
        def func2(*args):
            return results[args]
        return func2
    return func
