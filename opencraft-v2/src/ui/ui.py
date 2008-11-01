import threading
import os
import pygame

import x11events
import PipeEvent

def get_center_coords(inner, outer):
    x = outer[0]/2 - inner[0]/2
    y = outer[1]/2 - inner[1]/2
    return x, y
    
class UI(object):
    def __init__(self):
        self.display = pygame.Surface((640,480))
        self.calls = []
    def add_call(self, func, delay):
        "delay of 0 means until next event"
        self.calls.append((func, delay))
    
    def execute(self):
        time = 0.
        clock = pygame.time.Clock()
        calls = [[c[0], c[1], None] for c in self.calls]
        for call in calls:
            call[0]()
            call[2] = 0
        while True:
            x11events.wait(min(x[2]+x[1]-time for x in calls if x[1] is not None))
            time += clock.tick()/1000.
            self.handle_events()
            for call in calls:
                if call[1] is None:
                    call[0]()
                else:
                    while time > call[2] + call[1]:
                        call[2] += call[1]
                        call[0]()
    
    def update(self):
        pygame.display.update()
        
    def handle_events(self):
        for event in pygame.event.get():
            self.handle_event(event)
    
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
    
def init():
    pass
