import sys
import pygame
import time
import pysmk

def open(f):
    if ":" in f:
        import mpq
        f = f.split(":")
        return iter(mpq.Archive(f[0])[f[1]])
    else:
        return __builtins__.open(f)

if sys.argv[2] == "time":
    import timeit
    
    rep = 10
    count = 10
    res = 1000000.
    for i in xrange(rep):
      start = time.time()
      for x in xrange(count):
        smk = pysmk.SMKReader(open(sys.argv[1]))
      end = time.time()
      res = min(res, (end-start)/count)
    print "%f ms/start" % (res*1000)
    
    count = smk.frames-1
    start = time.time()
    for x in xrange(count):
        print "%i/%i" % (x,count)
        smk.next()
    end = time.time()
    print "%f ms/frame" % ((end-start)/count*1000)
    
elif sys.argv[2] == "save":
    smk = pysmk.SMKReader(open(sys.argv[1]))
    from PIL import Image
    temp = Image.fromstring("RGBA", smk.video.get_size(), pygame.image.tostring(smk.video, "RGBA"))
    temp.save("x.png")
    
elif sys.argv[2] == "play":
    pygame.init()
    smk = pysmk.SMKReader(open(sys.argv[1]))
    size = smk.video.get_size()
    display = pygame.display.set_mode(smk.video.get_size())
    clock = pygame.time.Clock()
    playing = False
    while True:
        display.fill((0,0,0))
        display.blit(smk.video, (0,0))
        pygame.display.update()
        try:
            smk.next()
        except StopIteration:
            break
        if smk.audio[0]:
            if not playing:
                smk.audio[0].play()
                playing = True
        clock.tick(smk.fps)
    file('audio','wr').write(smk.audio[0].get_buffer().raw)
