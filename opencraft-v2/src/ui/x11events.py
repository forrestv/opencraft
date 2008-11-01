import pygame
import ctypes
import select

def get_fd():
    w = pygame.display.get_wm_info()
    w = w['display']
    n = int(str(w)[23:-1], 16)
    n = ctypes.cast(n+8, ctypes.POINTER(ctypes.c_int)).contents.value
    n = ctypes.cast(n+8, ctypes.POINTER(ctypes.c_int)).contents.value
    return n

fd = None

def wait(timeout=None):
    global fd
    if fd == None:
        fd = get_fd()
    select.select([fd], [], [], timeout)
