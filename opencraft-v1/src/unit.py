from vector import *
import pygame
from world import *

def fix_rad_angle(rad):
    return (rad+math.pi) % (math.pi*2.0)-math.pi
    
class Object(object):
    maxhealth = None
    def __init__(self):
        self.angle = math.pi*1.5
        self.orders = []
        self.name = str(self.__class__).split("'")[1].split(".")[-1]
        self.recharge = 0.0
        self.tangible = True
        self.selectable = True
        self.level = 0
        self.time = 0
        self.abilities = []
        self.sdir = 0
        self.dest = None
        self.bound = v(5,5)
        self.vert = 0
        self.food = (0,0,0)
        self.hunger = (0,0,0)
        self.hover = 0
        self.health = self.maxhealth
        self.id = None
    def update(self, dt, view):
        if self.orders:
            if self.do_order(self.orders[0], dt, view):
                self.orders.pop[0]
                
        if self.health <= 0:
            view.units.remove(self)
            del self
    def update(self,dt,view):
        self.player.food = self.player.food + self.food
        self.player.hunger = self.player.hunger + self.hunger
        
    def action(self,target,view):
        self.orders.append(target)
        self.dest = target
    def do_order(self, order, dt, view): # return True if complete
        if order.type == "move":
            pos = order.pos
            range = 0
            type = "move"
        elif order.type == "attack":
            pos = order.pos
            range = self.range*.9
        elif order.type == None:
            pass
    def get_frame(self, view): #(frame,reflect=False)
        angle = (self.angle+math.pi/2) % (math.pi*2)
        angle = angle/math.pi/2
        angle = int(angle*32+.5)
        angle = angle % 32
        reflect = angle > 16
        if angle > 16:
            angle = 32-angle
        b = int(self.time)
        return (angle+b*17,reflect)
    def get_sprite_name(self, view):
        return self.name
    def draw(self, view):
        pos = self.pos-view.pos
        if self in view.selection:
            circle = view.sprites["o"+str(self.size).zfill(3)][0]
            circle.set_palette(get_circle_palette(36,152,36))
            view.screen.blit(circle,pos-v(circle.get_size())/2+v(0,self.vert))
            if self.health and 0:
                surf = view.font.render(str(self.health), True, (255,0,0))
                view.screen.blit(surf, pos-v(surf.get_size())/2+(0.0,self.size*.6))
        name = self.get_sprite_name(view)
        sprite = view.sprites[name]
        frame,reflect = self.get_frame(view)
        new = sprite[frame]
        if name + "Shadow" in view.sprites:
            shad = view.sprites[name+"Shadow"][frame]
            shadchange = 0
        else:
            shad = new.copy()
            shadchange = 35*self.level+5
            shad.set_palette([(0,0,0)]*300)
        if self.player:
            new.set_palette(get_palette(self,view))
        if reflect:
            new = pygame.transform.flip(new,True,False)
            shad = pygame.transform.flip(shad,True,False)
            
        shad.set_alpha(128)
        shadpos = pos - v(shad.get_size()) / 2 + v(0, shadchange)
        mainpos = pos- v(new.get_size()) / 2 + v(0, self.hover)
        if pygame.Rect((shadpos,shad.get_size())).colliderect(((0,0),(640,32*14))):
            view.screen.blit(shad, shadpos)
        if pygame.Rect((mainpos,new.get_size())).colliderect(((0,0),(640,32*14))):
            view.screen.blit(new, mainpos)
            
        if self.player:
            color = view.colorsm[self.player.color]
        else:
            color = view.colorsm[-1]
        size = self.bound/32
        for x in range(2):
            if size[x] <= 2: size[x] = 2
        mpos = self.pos/32.+(.5,.5)-size/2
        pygame.draw.rect(view.minimapover, color, (mpos,size))
        
        try:
            if type(self.dest) == list:
                pygame.draw.lines(view.minimapover,(255,0,0),False,self.dest)
        except: pass
        
class Unit(Object):
    def __init__(self):
        Object.__init__(self)
        self.angspeed = 30.0
        self.curspeed = 0.0
        self.accel = 50.0
    def update(self,dt,view):
        Object.update(self, dt, view)
        self.moving = False
        if type(self.dest) == type(v(())) and self.level == 0:
            self.dest = view.pathfind.get_path([int(x) for x in self.pos/32],0,[int(x) for x in self.dest/32])
            try:
                self.dest.pop(0)
            except:
                pass
            print self.dest
        if type(self.dest) != type([]) and type(self.dest) != type(v(())) and self.dest != None: #dest is unit
            if self.dest not in view.units or self.dest is self:
                self.dest = None
        if type(self.dest) == type([]):
            dest = v(self.dest[0])*32+(16,16)
        elif type(self.dest) != type(v(())) and self.dest != None:
            dest = self.dest.pos
        elif self.dest == None: dest = self.pos
        else: dest = self.dest
        diff = v(dest)-self.pos
        diff_polar = (sqrt(dot(diff,diff)),arctan2(diff[1],diff[0]))
        #diff_polar = (diff_polar[0],int(diff_polar[1]/2/math.pi*32+.5)*1.0/32.0*2*math.pi)
        angle_error = fix_rad_angle(self.angle - diff_polar[1])
        
        ang_vel = angle_error
        if abs(ang_vel) > self.ang_speed*dt:
            ang_vel = dt*self.ang_speed*sign(ang_vel)
            
        speed = diff_polar[0]
        if type(self.dest) == type([]):
            speed = self.speed*dt
        if speed > self.speed*dt:
            speed = self.speed*dt
            
        if speed > self.curspeed*dt:
            self.curspeed += self.accel*dt
            if self.curspeed > self.speed:
                self.curspeed = self.speed
                
        if speed > self.curspeed*dt:
            speed = self.curspeed*dt
            
        min_error = 1
        
        if type(self.dest) != type([]) and type(self.dest) != type(v(())) and self.dest != None:
            min_error = self.range*.9
            print "bad attack"
            
        if diff_polar[0] > min_error:
            self.angle -= ang_vel
            self.moving = True
        oldpos = v(self.pos)
        if abs(angle_error) < 0.01 and diff_polar[0] > min_error:
            self.moving = True
            newpos = self.pos + v((cos(diff_polar[1]),sin(diff_polar[1])))*speed
            bad = False
            if self.tangible:
                myrect = pygame.rect.Rect(self.pos - v(self.bound)/2,self.bound)
                for unit in view.units:
                    if unit is not self and unit.tangible and unit.level == self.level:
                        unitrect = pygame.rect.Rect(unit.pos - v(unit.bound)/2,unit.bound)
                        if myrect.colliderect(unitrect):
                            bad = True
                            break
            if not bad: self.pos = newpos
            
        if (diff_polar[0] < min_error or speed > diff_polar[0]) and type(self.dest) == type([]):
            self.dest.pop(0)
            if not self.dest: self.dest = None
            self.moving = True
            
            
        self.curspeed = self.curspeed*.9+speed/dt*.1
        #print self,speed
        
        self.recharge += dt
        try: self.projectile
        except AttributeError: pass
        else:
            if type(self.dest) != type(v()) and self.dest != None and type(self.dest) != type([]):
                if self.recharge > self.recharge_time and diff_polar[0] <= self.range:
                    projectile = self.projectile()
                    projectile.pos = self.pos.copy()
                    projectile.dest = self.dest
                    projectile.player = self.player
                    view.units.append(projectile)
                    self.recharge = 0.0
                    
        if self.health <= 0.0:
            view.units.remove(self)
            view.uisprites.append(Sprite("MechExplode",self.pos))
            
class LandUnit(Unit): pass

class AirUnit(Unit):
    def __init__(self):
        Unit.__init__(self)
        self.level = 1
        self.hovercount = 1
    def update(self,dt,view):
        Unit.update(self,dt,view)
        self.hovercount += .025+.05*random(1)[0]
        self.hovercount = self.hovercount % 4
        self.hover = [0,1,0,-1][int(self.hovercount)]
        
def get_circle_palette(*color):
    return [(x/18.*color[0]+.5*color[0],x/18.*color[1]+.5*color[1],x/18.*color[2]+.5*color[2]) for x in range(9)]
    
class Resource(Object):
    def __init__(self):
        Object.__init__(self)
        self.player = None
        
class MineralField(Resource):
    def __init__(self, type):
        Resource.__init__(self)
        self.size = 72
        self.bound = v(2,2)*32
        self.type = type
        self.name = self.name+str(type)
    def update(self, dt, view):
        if self.amt <= 0: view.units.remove(self)
    def get_sprite(self):
        return self.name + str(self.type)
    def get_frame(self, view):
        if self.amt >= 750: frame = 0
        elif self.amt >= 500: frame = 1
        elif self.amt >= 250: frame = 2
        elif self.amt >= 0: frame = 3
        return (frame, False)
        
geyser_index = {
    "badlands": 0,
    "platform": 1,
#  "install": 0,
    "ashworld": 3,
    "jungle": 0,
    "desert": 0,
    "ice": 0,
    "twilight": 0,
}

class VespeneGeyser(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.smoke = [(11, -19), (-40, -13), (34, 2)]
        self.size = 146
        self.bound = v(4,2)*32
    def update(self,dt,view):
        if int(random(1)[0]*50) == 23:
            pos = self.smoke[int(random()*3)]
            view.uisprites.append(Sprite("GeyserSmoke",self.pos+pos,1./2))
    def get_frame(self, view):
        return (geyser_index[view.tileset], False)
        
class Building(Object):
    def __init__(self):
        Object.__init__(self)
        self.canlift = False
        self.speed = 0
        self.ang_speed = 0
        self.angle = math.pi*1.5
        self.finished = 0.0
    def update(self,dt,view):
        Object.update(self,dt,view)
        if type(self.dest) != type(v(())) and self.dest != None:
            if self.dest not in view.units or self.dest is self:
                self.dest = None
                
        dest = self.dest
        if type(dest) != type(v(())) and dest != None:
            dest = self.dest.pos
            
        if dest != None:
            self.recharge += dt
            self.moving = True
            if self.recharge > self.recharge_time:
                projectile = self.projectile()
                projectile.pos = place_unit(self.pos, projectile.bound, view.units)
                projectile.dest = v(self.dest)
                projectile.player = self.player
                view.units.append(projectile)
                self.recharge = 0.0
        else:
            self.recharge = 0.0
            self.moving = False
            
        if self.health <= 0.0:
            view.units.remove(self)
            view.uisprites.append(Sprite("MechExplode",self.pos))
        self.finished += .003
        if self.finished > 1: self.finished = 1
    def get_frame(self, view):
        if self.finished < .2:
            frame = 0
        elif self.finished < .4:
            frame = 1
        elif self.finished < .6:
            frame = 2
        elif self.finished < .8:
            frame = 1
        else:
            frame = 0
        return (frame, False)
    def get_sprite_name(self, view):
        if self.finished < .6:
            return "TerranBuildLarge"
        else:
            return self.name
            
class Addon(Building): pass

class Projectile(Object):
    def __init__(self):
        Object.__init__(self)
        self.selectable = False
        self.tangible = False
    def update(self,dt, view):
        if self.dest not in view.units:
            view.units.remove(self)
            view.uisprites.append(Sprite("Explode", self.pos))
            return
        diff = self.dest.pos-self.pos
        diff_polar = (sqrt(dot(diff,diff)),arctan2(diff[1],diff[0]))
        self.angle = diff_polar[1]
        self.pos = self.pos + v((cos(self.angle),sin(self.angle)))*self.speed*dt
        if diff_polar[0] < self.dest.size/2:
            self.dest.health -= self.damage
            view.units.remove(self)
            view.uisprites.append(Sprite("Explode", self.pos))
            
class Doodad(Object):
    def __init__(self,datum):
        Object.__init__(self)
        self.sdir = 0
        self.selectable = False
        self.angle = math.pi*1.5
        self.name = "tileset/"+datum[0]
        self.pos = v(datum[1],datum[2])
        self.level = .5
        self.time = 0
        self.tangible = False
    def update(self,dt,view): self.time += .5
    def draw(self,view):
        #self.time = self.time % 1.0
        pos = self.pos - view.pos
        sprite = view.sprites[self.name]
        sprite = sprite[int(self.time%len(sprite))]
        shadowname = self.name.replace("0","").replace(".grp","sha.grp")
        shadow = view.sprites.get(shadowname, None)
        if shadow:
            shadow = shadow[int(self.time%len(shadow))]
            shadow.set_palette([(0,0,0)]*256)
            view.screen.blit(shadow, pos - v(shadow.get_size())/2)
        view.screen.blit(sprite,pos-v(sprite.get_size())/2)
        
from units import *
from main import Sprite
