import math
import pygame
import os, sys
from pygame.locals import *
from vector import *
import cPickle
import struct
import PIL.Image
import re

class Order(object): pass

class Null(object): pass

from world import *

import music
import star
import grp
import tile
import mapreader
import pathfind
import ui
import font

debug = True

class Sprite(object):
    def __init__(self,name,pos,speed=1):
        self.name = name
        self.pos = pos
        self.time = 0
        self.speed = speed
    def draw(self,view):
        sprite = view.sprites[self.name]
        new = sprite[int(self.time)]
        pos = self.pos-view.pos
        if int(self.time) >= len(sprite) - 1:
            view.uisprites.remove(self)
        view.screen.blit(new,pos-v(new.get_size())/2)
    def update(self):
        self.time = self.time + self.speed
        
from unit import *

def init(args,view):
    music.preinit(view)
    
    pygame.init()
    pygame.display.set_caption("OpenCraft")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))
    pygame.mouse.set_visible(False)
    view.screen = pygame.display.set_mode([640,480])
    view.screen.blit(pygame.image.load("images/title.png"),(0,0))
    pygame.display.update()
    
    music.init(view)
    
    print "Loading palettes"
    view.palettes = {}
    for path in os.listdir("palettes"):
        if path[0] == ".":
            continue
        pal = open(os.path.join("palettes", path),"rb").read()
        palette = []
        for i in range(0, len(pal), 3):
            palette.append((ord(pal[i]), ord(pal[i+1]), ord(pal[i+2])))
        view.palettes[path] = palette
    view.palettes["shadow"] = [(0,0,0)]*256
    
    
    print "Reading map"
    filename = "maps/BroodWar/(2)Astral Balance.scm"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    view.mapdim, view.tileset, view.map, view.doodads, view.starts, view.resources = mapreader.load(filename)
    
    print "Loading tileset:", view.tileset
    view.tile = tile.tiles["tileset/"+view.tileset+"/"+view.tileset]
    view.tilepalette = view.tile.palette
    print "Loading sprites"
    for datum in os.walk("images"):
        for path in [os.path.join(datum[0],x) for x in datum[2]]:
            if path.find("/.") != -1:
                continue
            name = '.'.join('/'.join(path.split("/")[1:]).split(".")[:-1]) # remove images/ and extension
            ext = path.split(".")[-1]
            if ext == "grp":
                sprite = grp.load(path, view.palettes["unit"])
            if ext == "grc":
                sprite = grp.load(path, view.palettes["unit"], True)
            if ext == "gro":
                sprite = grp.load(path, view.palettes["orange"])
            if ext == "grt":
                sprite = grp.load(path, view.tilepalette)
            if ext == "grs":
                sprite = grp.load(path, view.palettes["shadow"])
            if ext == "png":
                sprite = pygame.image.load(path)
            if ext == "pcx":
                sprite = pygame.image.load(path)
                sprite.set_colorkey(0)
            view.sprites[name] = sprite
            
    print "Loading doodads"
    for path in os.listdir("tileset/"+view.tileset):
        if path == ".svn": continue
        if path.split(".")[-1] != "grp": continue
        view.sprites["tileset/"+view.tileset+"/"+path] = grp.load("tileset/"+view.tileset+"/"+path, view.tilepalette)
        
    print "Loading fonts"
    font.load()
    
    print "Loading team colors"
    colors = pygame.image.load("images/colors.pcx")
    view.colors = []
    for team in range(15):
        view.colors.append([colors.get_at((x+team*8,0))[0:3] for x in range(7)])
    colors = pygame.image.load("images/colorsm.pcx")
    view.colorsm = []
    for team in range(16):
        view.colorsm.append(colors.get_at((team,0)))
        
    if view.tileset == "platform":
        print "Reading stars"
        view.star = star.init(view.palettes["unit"])
        
    print "Making map surface"
    make_map(view)
    
    print "Generating minimap"
    s = pygame.image.tostring(view.map_surf,"RGBX")
    temp = PIL.Image.fromstring ("RGBX", view.map_surf.get_size (), s)
    temp.thumbnail ((128,128), PIL.Image.ANTIALIAS)
    view.minimap = pygame.image.fromstring (temp.tostring(), temp.size, temp.mode) 
    
    for doodad in view.doodads:
        if type(doodad[0]) == int:
            view.sprites["tileset/"+str(doodad[0])] = [view.font.render(str(doodad[0]),True,(255,255,255))]
            doodad = [str(doodad[0]),doodad[1],doodad[2]]
        view.units.append(Doodad(doodad))
    view.mapw = [[all(pygame.surfarray.pixels2d(view.tile[m][1])) for m in y] for y in view.map]
    #view.mapw = [[True for m in y] for y in view.map]
    #print view.mapw
    #print mapw[5][5], mapw[10][10]
    view.pathfind = pathfind.path(view.mapdim)
    
    view.movie = []
    for path in sorted(os.listdir("movie")):
        if path[0] == ".":
            continue
        view.movie.append(pygame.image.load(os.path.join("movie",path)))
        
    print "Loading units"
    load(view)
    print "Loaded! Took", pygame.time.get_ticks()/1000.0
    music.fade(view)
    
def convertnum(string):
    y = 0
    for x in reversed(string):
        y = y << 8
        y += ord(x)
        
    return y
    
def load(view):
    for res in view.resources:
        if res[0] in ("min1","min2","min3"):
            unit = MineralField(int(res[0][-1]))
        elif res[0] == "gas":
            unit = VespeneGeyser()
        else:
            print "invalid resource"
        unit.pos = v(res[1],res[2])
        unit.amt = res[3]
        view.units.append(unit)
        
    view.takencolors = [False]*8
    for start in enumerate(view.starts):
        player = Player()
        testcolor = int(random()*8)
        while view.takencolors[testcolor]:
            testcolor = int(random()*8)
        view.takencolors[testcolor] = True
        player.color = testcolor
        view.players.append(player)
        unit = CommandCenter()
        unit.pos = v(start[1])
        unit.player = player
        unit.finished = 1
        view.units.append(unit)
        for i in range(4):
            unit = SCV()
            unit.player = player
            unit.pos = v(start[1]) + (i*35-64,2*32)
            unit.pos = place_unit(start[1], unit.bound, view.units)
            unit.angle = random()*2*3.14159
            view.units.append(unit)
            
    view.pos = v(view.starts[0]) - v(640,13*32)/2
    
    return
    view.units.append(Tank())
    view.units.append(SCV())
    for x in range(2):
        view.units.append(Dropship())
    view.units.append(Factory())
    view.units.append(Marine())
    #view.units[-1].dest = view.path2
    view.units.append(Wraith())
    for unit in view.units:
        if unit.tangible: unit.pos = random(2)*500
        unit.player = view.players[0]
        
def handle_event(event, view):
    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
        return True
        
    elif event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            if pygame.rect.Rect(6,348,128,128).collidepoint(*event.pos): #minimap
                pos = (v(event.pos)-(6,348))*32+(16,16)
                view.pos = pos-v((640,480))/2
            elif pygame.rect.Rect(413,410,60,56).collidepoint(*event.pos):
                view.followselection = True
            else:
                view.begin_pos = event.pos
                
        elif event.button == 2:
            view.scroll_start = event.pos
            view.scroll_center = view.pos
            
        elif event.button == 3:
            target = default_action(view.pos+event.pos,view)
            for unit in view.selection:
                unit.action(target,view)
            view.uisprites.append(Sprite("Acquired",view.pos+event.pos))
            
    elif event.type == MOUSEBUTTONUP:
        if event.button == 1:
            if view.followselection:
                view.followselection = False
            elif view.begin_pos:
                wpos = view.pos+event.pos
                if event.pos == view.begin_pos:
                    table = []
                    for unit in [x for x in view.units if x.selectable]:
                        df = wpos-unit.pos
                        dist = sqrt(dot(df,df))
                        table.append((dist,unit))
                    table.sort()
                    view.selection = [table[0][1]]
                else:
                    view.selarea = pygame.Rect(view.begin_pos,v(event.pos)-view.begin_pos)
                    view.selarea.normalize()
                    new = []
                    for unit in view.units:
                        area = pygame.Rect(unit.pos-unit.bound/2-view.pos,unit.pos+unit.bound/2-view.pos)
                        if area.colliderect(view.selarea) and unit.selectable:
                            new.append(unit)
                    if new: view.selection = new
                view.selarea = None
                view.begin_pos = None
                
        if event.button == 2:
            view.scroll_start = None
            
    elif event.type == MOUSEMOTION:
        if view.begin_pos:
            view.selarea = pygame.Rect(view.begin_pos,v(event.pos)-view.begin_pos)
            view.selarea.normalize()
        if view.scroll_start:
            view.pos = v(view.scroll_start)-event.pos+view.scroll_center
            #view.scroll_start = event.pos
    elif event.type == KEYDOWN:
        if pygame.key.name(event.key) == "b":
            for unit in view.selection:
                pos = view.pos+pygame.mouse.get_pos()
                unit.action2(pygame.key.name(event.key),pos,view)
        if event.key == pygame.K_LEFT: view.scrollleft = True
        if event.key == pygame.K_RIGHT: view.scrollright = True
        if event.key == pygame.K_UP: view.scrollup = True
        if event.key == pygame.K_DOWN: view.scrolldown = True
    elif event.type == KEYUP:
        if event.key == pygame.K_LEFT: view.scrollleft = False
        if event.key == pygame.K_RIGHT: view.scrollright = False
        if event.key == pygame.K_UP: view.scrollup = False
        if event.key == pygame.K_DOWN: view.scrolldown = False
    elif event.type == USEREVENT:
        music.next(view)
        
def default_action(target,view):
    for unit in [x for x in view.units if x.tangible]:
        df = unit.pos-target
        diff = sqrt(dot(df,df))
        if diff < unit.size/2:
            target = unit
            break
    return target
    
if 0:
    type = "move"
    for unit in [x for x in view.units if x.tangible]:
        df = unit.pos-target
        diff = sqrt(dot(df,df))
        if diff < unit.size:
            target = unit
            type = "attack"
            break
    order = Order()
    order.type = type
    order.pos = target
    return order
    
def get_unit_at_point(pos,view):
    table = []
    for unit in [x for x in view.units if x.selectable]:
        df = pos-unit.pos
        dist = sqrt(dot(df,df))
        if dist <= unit.size/2: table.append((dist,unit))
    table.sort()
    if table == []: return None
    return table[0][1]
    
def main():
    config = Null()
    config.keyScrollSpeed = 2000.0
    config.musicVolume = .5
    
    view = Null()
    view.pos = v((0,0))
    view.sprites = {}
    view.cursor = {}
    view.units = []
    view.selarea = None
    view.begin_pos = None
    view.scroll_start = None
    view.selection = []
    view.players = []
    view.ct = 0.0
    view.scrollleft = False
    view.scrollright = False
    view.scrollup = False
    view.scrolldown = False
    view.uisprites = []
    view.config = config
    view.tilepalcount = 0
    view.followselection = False
    
    init(sys.argv, view)
    
    dt = .001
    mp = 0
    #view.pathfind.set_map(chr(0)*view.mapdim[0]*view.mapdim[1])
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if handle_event(event, view): return
            
            
            
        #view.path = pathf(view.occu)
        view.occu = list([list(x) for x in view.mapw])
        
        for player in view.players:
            player.food = v(0,0,0)
            player.hunger = v(0,0,0)
        for unit in view.units:
            unit.update(dt, view)
            
        if view.scrollleft: view.pos = view.pos + v(-1.0,0.0)*config.keyScrollSpeed*dt
        if view.scrollright: view.pos = view.pos + v(1.0,0.0)*config.keyScrollSpeed*dt
        if view.scrollup: view.pos = view.pos + v(0.0,-1.0)*config.keyScrollSpeed*dt
        if view.scrolldown: view.pos = view.pos + v(0.0,1.0)*config.keyScrollSpeed*dt
        
        if view.followselection and view.selection != []:
            poss = [x.pos for x in view.selection]
            poss = sum(poss)/len(poss)
            view.pos = poss - v(640,480)/2
            
        if view.pos[0] < 0: view.pos[0] = 0
        if view.pos[1] < 0: view.pos[1] = 0
        maxx = view.mapdim[0]*32 - view.screen.get_width()
        maxy = (view.mapdim[1]-12)*32
        if view.pos[0] > maxx: view.pos[0] = maxx
        if view.pos[1] > maxy: view.pos[1] = maxy
        view.pos = v([int(x) for x in view.pos])
        
        view.screen.fill((0,0,0))
        if view.tileset == "platform":
            star.draw(view)
        draw_tiles(view)
        
        tempunits = []
        for unit in view.units:
            tempunits.append((unit.level,unit.pos[1],unit))
        tempunits.sort()
        view.minimapover = pygame.surface.Surface((128,128),pygame.SRCALPHA,32)
        for unit in tempunits:
            unit[2].draw(view)
            
        for sprite in view.uisprites:
            sprite.draw(view)
            sprite.update()
            
        if view.selarea: pygame.draw.rect(view.screen, (16,252,24), view.selarea, 1)
        
        #68 w 3 down
        player = view.players[0]
        player.raceindex = 1
        player.minerals = 50
        player.gas = 0
        #print player.food, player.hunger
        icons = [
            (0, player.minerals, (16, 252, 24)),
            (player.raceindex+1, player.gas, (16, 252, 24)),
        ]
        for raceindex in range(3):
            food = player.food[raceindex]
            hunger = player.hunger[raceindex]
            if not food and not hunger: # heh
                continue
            if food >= hunger:
                color = (16, 252, 24)
            else:
                color = (200,24,24)
            icons.append((raceindex+4, str(hunger)+"/"+str(food), color))
            
        sprite = view.sprites["icons"]
        x = 640
        icons.reverse()
        for icon in icons:
            x -= 68
            view.screen.blit(sprite[icon[0]],(x,3))
            text = font.render(10, str(icon[1]), "game5")
            view.screen.blit(text, (x+16, 3))
            
        view.screen.blit(view.sprites['ConsoleTerran'],(0,0))
        
        view.screen.blit(view.minimap, v(6,348)+(64,64)-v(view.minimap.get_size())/2)
        view.screen.blit(view.minimapover, v(6,348)+(64,64)-v(view.minimap.get_size())/2)
        topleft = v(6,348)+(64,64)-v(view.minimap.get_size())/2
        pygame.draw.line(view.screen, (204,204,208), topleft+(0,-1), topleft+(128,-1))
        bottomright = v(6,348)+(64,64)+v(view.minimap.get_size())/2
        pygame.draw.line(view.screen, (172,152,148), bottomright, bottomright+(-128,0))
        
        pygame.draw.rect(view.screen,(255,255,255), (v(6,348)+(64,64)-v(view.minimap.get_size())/2+view.pos/32,(20,13)),1)
        #print view.mapdim
        
        
        (173,389)
        if len(view.selection) == 0:
            pass
        elif len(view.selection) == 1:
            u = view.selection[0]
            if u.id:
                w = view.sprites["Wireframe"][u.id]
                w.set_palette(get_wpalette(u))
                view.screen.blit(w, (168,388))
            if u.health != None:
                s = str(int(u.health))+"/"+str(u.maxhealth)
                t = font.render(8, s, "game5", True)
                view.screen.blit(t,v(199,457)-v(t.get_size())/2)
            s = u.name
            t = font.render(10, u.name, "game0", True)
            view.screen.blit(t,v(315,394)-v(t.get_size())/2)
        else:
            pass #multiple grpwire.grp
        #buttons
        
        view.screen.blit(view.sprites["TerranButtons"][4], (3,320))
        view.screen.blit(view.sprites["TerranButtons"][0], (416,388))
        
        view.screen.blit(font.render(8,"MENU", "game1"),(435,394))
        mp += .5
        mp = mp % 10
        view.screen.blit(view.movie[int(mp)], (413,410))
        #pygame.draw.rect(view.screen, (128,128,128), ((413,410),(60,56)))
        view.screen.blit(view.sprites["TerranOverlay"], (413, 410))
        
        if debug:
            surf = font.render(8, str(int(clock.get_fps()+.5)), "game0")
            view.screen.blit(surf,(0,0))
            
        if pygame.mouse.get_focused():
            view.ct += dt * 8
            cursor = 'CursorArrow'
            u = get_unit_at_point(pygame.mouse.get_pos()+view.pos,view)
            if u:
                if u.player == view.players[0]: cursor = 'CursorTarget2Green'
                elif u.player == -1: cursor = 'CursorTarget2Yellow'
                else: cursor = 'CursorTarget2Red'
            if view.selarea: cursor = 'CursorDrag'
            if view.scroll_start: cursor = None
            if view.sprites['ConsoleTerran'].get_at(pygame.mouse.get_pos()) != (0,0,0,255):
                cursor = "CursorArrow"
            if cursor == "CursorArrow": view.ct = view.ct % 4.0
            elif cursor in ("CursorTarget2Green","CursorTarget2Yellow","CursorTarget2Red"): view.ct = view.ct % 14.0
            else: view.ct = 0
            
            if cursor:
                sprite = view.sprites[cursor][int(view.ct)]
                view.screen.blit(sprite, v(pygame.mouse.get_pos())-v(sprite.get_size())/2)
        try: a
        except NameError: a = 0.
        a += dt
        a = a % 5
        view.screen.blit(ui.progress_bar(a/5,view),(281,426))
        pygame.display.update()
        pygame.mixer.music.set_volume(view.config.musicVolume)
        #sendp(cPickle.dumps(view.units),view)
        #try:
        # while True:
        #  view.units = cPickle.loads(view.socket.recvfrom(2**20)[0])
        #except socket.error: pass
        if debug:
            clock.tick()
        else:
            clock.tick(30)
        dt = clock.get_time()/1000.0
        
