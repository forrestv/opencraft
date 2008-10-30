import Order
'''
class Player
  def game_loop
  def draw_loop?
  def get_orders(cycle): return list or None
'''
class OrderCollector(object):
    def insert(self, cycle, orders):
        self.orders[cycle] = orders
    def orders(self, cycle):
        if cycle in self.orders:
            return self.orders[cycle]
        else:
            return None

class Player(OrderCollector):
    def game_step(game):
        pass
    def draw_step():
        pass
    def pop_orders(cycle):
        pass

class LocalPlayer(Player):
    def __init__(self):
        Player.__init__(self)
        self.queued_orders = []
    def draw_step():
        pass
    def pop_orders(cycle):
        return 

class RemotePlayer(Player):
    def __init__(self):
        Player.__init__(self)
    def receive_orders(self):
        for msg in self.conn.receive:
            a
    def orders(self, cycle):
        self.receive_orders()
        return Player.orders(self, cycle)

class AIPlayer(Player):
    def game_step(gamestate):
        self.insert(gamestate.cycle, ai.step(gamestate))

class PlayerContainer(object):
    def __init__(self, players):
       pass
    def remove(self, index): pass

class GameState(object):
    def __init__(self, map):
        self.units = []
        self.map = map
        self.cycle = 0
    def step(self, orders):
        for order in orders:
            unit = self.units[order.unit]
            unit.apply_order(order)
        for unit in self.units:
            unit.update()

class Game(object): # GameState ?
    def __init__(self, map, players):
        self.state = GameState(map)
        self.players = players
        self.ordercollector = OrderCollector()
    def game_step():
        for player in self.players:
            player.step()
        if self.pending():
            return
        orders = self.get_orders()
        self.state.step(orders)
