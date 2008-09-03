class Player(object):
    def step(self):
        raise NotImplementedError

class LocalPlayer(Player): pass
class ComputerPlayer(Player): pass
class NetworkPlayer(Player): pass

class OrderGetter(object):
    def __init__(self, lp, ):
    def step(self):
        # get network ones
        # get 
