class GameState(object):
    def step(self, orders):
        self.units.apply(orders)
        self.units.update()
