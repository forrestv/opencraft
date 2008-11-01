import pickle
import os

default_config = {
    "scroll_speed_keyboard": 2000,
    "scroll_speed_mouse": 0,
    "music_volume": 1.,
    "introduction_played": False,
}

class Config(object):
    def __init__(self, path):
        self._path = path
        self._data = self._read()
    def _read(self):
        try:
            f = open(self._path)
        except IOError:
            d = dict(default_config)
        else:
            d = pickle.load(f)
        return d
    def __getattr__(self, key):
        return self._data[key]
    def __setattr__(self, key, value):
        if key[0] == '_':
            return object.__setattr__(self, key, value)
        if key not in self._data:
            raise KeyError, "bad config entry name"
        self._data[key] = value
        self._write()
    def _write(self):
        f = open(self._path, "w")
        pickle.dump(self._data, f)

path = os.path.join(os.environ['HOME'], ".opencraft")

config = Config(os.path.join(path, "config.pkl"))

if __name__ == "__main__":
    for k, v in config._data.items():
        print k, v
