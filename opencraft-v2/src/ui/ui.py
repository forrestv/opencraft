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
        self.display2 = pygame.Surface((640,480))
        self.updateflag = PipeEvent.PipeEvent()
        event_threadt = threading.Thread(target=self.event_thread)
        display_threadt = threading.Thread(target=self.display_thread)
        event_threadt.setDaemon(True)
        display_threadt.setDaemon(True)
        self.pause = False
        self.run = True
        event_threadt.start()
        display_threadt.start()
        self.work()
        self.run = False
        event_threadt.join()
        display_threadt.join()
        
    def event_thread(self):
        while self.run:
            if not self.pause:
                for event in pygame.event.get():
                    self.handle_event(event)
            x11events.wait(.5)
    
    def update(self):
        self.display2, self.display = self.display, self.display2
        self.updateflag.set()
    
    def display_thread(self):
        from .. import ui
        while self.run:
            if not self.pause:
                ui.display.blit(self.display2, (0,0))
                pygame.display.update()
            self.updateflag.wait(.5)
            self.updateflag.clear()
            
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
