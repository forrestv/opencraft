from vector import *
import pygame

def get_palette(unit, view):
    pal = list(view.palettes["unit"])
    pal[8:15] = view.colors[unit.player.color]
    return pal
    
def get_wpalette(unit):
    return [(0,0,0)]*208+[(0,255,0)]*4
    
class Player(object):
    def __init__(self):
        self.color = 0
        
def get_tile(num):
    return v((num%16,num/16))
    
def make_map(view):
    s = pygame.surface.Surface(v(view.mapdim)*32,0,8)
    s.set_palette(view.tilepalette)
    s.set_colorkey(0)
    for x in range(view.mapdim[0]):
        for y in range(view.mapdim[1]):
            m = view.map[x][y]
            row = view.tile[m][0]
            s.blit(row,v(x,y)*32)
    view.map_surf = s
    
def draw_tiles(view):
    #wpos = map(int,(v(pygame.mouse.get_pos())+view.pos)/32)
    #print wpos, view.mapv[wpos[0]][wpos[1]]
    g = v([int(-x/32) for x in view.pos])
    q = -view.pos % 32
    for x in range(-1,640/32+1):
        for y in range(-1,480/32+1):
            X, Y = (x,y)-g
            if X < 0 or Y < 0: continue
            if X >= view.mapdim[0] or Y >= view.mapdim[1]: continue
            #if [X,Y] == wpos: continue
            #if (X,Y) in view.path2: continue
            #view.screen.blit(view.tile,v((x,y))*32+q,(get_tile(view.map[X][Y])*32,(32,32)))
            #continue
            m = view.map[X][Y]
            row = view.tile[m>>4][m&15]
            try:
                view.screen.blit(row,v((x,y))*32+q)
            except: pass
            
def draw_tiles(view):
    #print view.map_surf.map_rgb(view.map_surf.get_at(v(view.pos)+pygame.mouse.get_pos()))
    
    view.tilepalcount += .5
    view.tilepalcount = view.tilepalcount % 42
    #print int(view.tilepalcount)
    pal0 = view.tilepalette[1:7]
    pal1 = view.tilepalette[7:14]
    pal2 = view.tilepalette[248:255]
    for x in range(int(view.tilepalcount% 6)):
        pal0.insert(0,pal0.pop())
    for x in range(int(view.tilepalcount % 7)):
        pal1.insert(0,pal1.pop())
        pal2.insert(0,pal2.pop())
    #pal2 = [(0,0,0)]*7
    pal = view.tilepalette[:1] + pal0 + pal1 + view.tilepalette[14:248] + pal2 + view.tilepalette[255:]
    #print len(pal)
    view.map_surf.set_palette(pal)
    view.screen.blit(view.map_surf,(0,0),(view.pos,(640,32*14)))
    
def place_unit(pos, size, units):
    s = pygame.surface.Surface((600,600))
    for u in units:
        top = v(u.pos) - v(pos) - v(u.bound)/2+ v(600,600)/2-v(size)/2-(1,1)
        pygame.draw.rect(s, (255,255,255), (top,v(u.bound)+v(size)+(2,2)))
    s = pygame.surfarray.pixels3d(s)
    
    sides = [v(-1,1),v(1,1),v(1,-1),v(-1,-1)]
    sidev = [v(1,0),v(0,-1),v(-1,0),v(0,1)]
    side = 0
    distance = 0
    radius = 32+16 #32*1.5
    while True:
        x, y = sides[side]*radius+sidev[side]*distance+(300,300)
        #print x, y
        if s[x][y][0] == 0: break
        distance += 2
        if distance >= radius*2+1:
            side += 1
            if side == 4:
                radius += 2
                if radius >= 300:
                    return None
                side = 0
            distance = 0
    return v(x,y)+pos-(300,300)
    #d = pygame.display.set_mode((600,600))
    #d.blit(s,(0,0))
    #pygame.display.update()
    #while 1: pass
