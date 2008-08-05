"""
Caching dictionary
"""

class cdict(object):
  def __init__(self, getter):
    self.dict = {}
    self.getter = getter
  def __getitem__(self, item):
    if item not in self.dict:
#      try:
      self.dict[item] = self.getter(item)
#      except:
#        raise KeyError
    return self.dict[item]
  def get(self, item, default = None):
    if item not in self.dict:
      try:
        self.dict[item] = self.getter(item)
      except:
        return default
    return self.dict[item]
