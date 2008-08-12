class Order(object): pass

class Move(Order):
    icon = "Move"
    def __init__(self, dest):
        self.dest = dest
        if isinstance(self.dest, Unit):
            self.__class__ = MoveUnit
        else:
            self.__class__ = MoveGround

class MoveGround(Order):
    def step(self, unit):
        if sqrt(dot(unit.pos - self.pos))) < 2:
            self.__class__ = Stop
            self.step(unit)

class MoveUnit(Order, Stop):
    def step(self, unit):
        if sqrt(dot(unit.pos - self.dest.pos))) < 20:
            Stop.step(self, unit)

class Stop(Order):
    def step(self, unit):
        a

class Attack(Order):
    def __init__(self, dest):
        self.dest = dest
        if isinstance(self.dest, Unit):
            self.__class__ = MoveUnit
        else:
            self.__class__ = MoveGround
    class attack(self, unit, dest):
        if sqrt(dot(dest.pos - unit.pos)) > unit.type.attack_range:
            self.move_towards(dest.pos)
        else:
            pass # attack!

class AttackGround(Attack):
    def step(self, unit):
        if sqrt(dot(unit.pos - self.pos))) < 2:
            self.__class__ = Stop
            self.step(unit)
        elif 0: #another unit close 
            Attack.attack(self, unit, close_unit)
        else:
            self.move_towards(self.dest)

class AttackUnit(Attack):
    def step(self, unit):
        if sqrt(dot(unit.pos - self.dest.pos))) < 20:
            Stop.step(self, unit)

class Repair(Order):
    def __init__(self, dest): 
        a

class Gather(Order): pass

class Build(Order): pass

class Hold(Order): pass

class SetRallyPoint(Order): pass

class Liftoff(Order): pass
