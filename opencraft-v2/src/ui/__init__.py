import os
import pygame

import x11events

def get_center_coords(inner, outer):
    x = outer[0]/2 - inner[0]/2
    y = outer[1]/2 - inner[1]/2
    return x, y

class UI(object):
    def __init__(self):
        self.calls = []
    def add_call(self, func, delay):
        "delay of 0 means until next event"
        self.calls.append((func, delay))
    
    def execute(self):
        time = 0.
        self.clock = pygame.time.Clock()
        calls = [[c[0], c[1], None] for c in self.calls]
        for call in calls:
            call[0]()
            call[2] = 0
        while True:
            x11events.wait(min(x[2]+x[1]-time for x in calls if x[1] is not None))
            time += self.clock.tick()/1000.
            if self.handle_events():
                return
            for call in calls:
                if call[1] is None:
                    if call[0]():
                        return
                else:
                    while time >= call[2] + call[1]:
                        call[2] += call[1]
                        if call[0]():
                            return
    
    def update(self):
        pygame.display.update()
    
    def handle_events(self):
        res = False
        for event in pygame.event.get():
            res = res or self.handle_event(event)
        return res
    
    def handle_event(self, event):
        name = pygame.event.event_name(event.type).lower()
        try:
            handler = getattr(self, name)
        except AttributeError:
            return
        handler(**event.dict)
    
    def quit(self):
        os._exit(0)    

def CursorUI(UI):
    def __init__(self, cursor=None): pass

display = None
def init():
    global display
    display = pygame.display.set_mode((640, 480))
