import pygame
import ctypes
import select

libX11 = ctypes.CDLL("libX11.so")

def get_display():
    w = pygame.display.get_wm_info()
    w = w['display']
    n = id(w)
    n = ctypes.cast(n+8, ctypes.POINTER(ctypes.c_int)).contents.value
    return n

def get_fd():
    n = get_display()
    n = ctypes.cast(n+8, ctypes.POINTER(ctypes.c_int)).contents.value
    return n

fd = None

def wait(timeout=None):
    global fd
    if fd == None:
        fd = get_fd()
    select.select([fd], [], [], timeout)

def set_cursor():
    d = get_display()
    libX11.XFlush(d)

pygame.init()
print get_fd()
set_cursor()
