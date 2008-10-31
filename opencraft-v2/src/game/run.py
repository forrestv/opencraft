import pygame

import GameState, UI

map = None
game = GameState.GameState(map)
order_collector = GameState.OrderCollector()

game_time = 0
ui = UI.UI()

clock = pygame.time.Clock()
while True:
    dt = clock.tick()/1000.
    game_time += dt
    while game_time > .1:
        a
        orders = order_collector.pop()
        gamestate.step(orders)
        game_time -= .1
    ui.step(game)
