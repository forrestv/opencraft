class Unit(object):
    def __init__(self, type, pos, angle):
        self.type = type
        self.pos = pos
        self.angle = angle
    def apply_order(self, order):
        print self, order # :P
