import pygame
import numpy

pygame.surfarray.use_arraytype("numpy")

def convert_to_greyscale(s):
    s = pygame.surfarray.pixels3d(s)
    
    numpy.divide(s[:,:,0], 3, s[:,:,0])
    numpy.divide(s[:,:,1], 3, s[:,:,1])
    numpy.divide(s[:,:,2], 3, s[:,:,2])
    numpy.add(s[:,:,0], s[:,:,1], s[:,:,0])
    numpy.add(s[:,:,0], s[:,:,2], s[:,:,0])
    s[:,:,1] = s[:,:,0]
    s[:,:,2] = s[:,:,0]

if __name__ == "__main__":
    import time, sys
    d = pygame.display.set_mode((640, 480))
    d.blit(pygame.image.load(sys.argv[1]), (0, 0))
    pygame.display.update()
    s = time.time()
    for i in xrange(100):
      convert_to_greyscale(d)
    print (time.time()-s)/100
    while True: pygame.display.update()
