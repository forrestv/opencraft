from unit import *

Build = 0 # building, cost (min,gas), prerequisits
Attack = 1 # weapon, range, reload
Upgrade = 2 # name, cost
Spell = 3 # energy, function

#def Build(cost,prereq): pass

"""
class BuildingName(Building):
    def __init__(self):
        Building.__init__(self)
        self.health
        self.id
        self.canlift
        self.circle = (146,6)
        self.food/self.hunger
        self.abilitys/upgrades
"""

# Buildings

class CommandCenter(Building):
    maxhealth = 1500
    def __init__(self):
        Building.__init__(self)
        self.abilities = [
            (Build,SCV,(50,0,20),None),
            (Build,ComsatStation,(50,50,50),(Academy,)),
            (Build,NuclearSilo,(100,100,70),(CovertOps,))
        ]
        self.canlift = True
        self.size = 146
        self.vert = 6
        self.bound = v(4,3)*32
        self.food = (0,10,0)
        self.id = 106
    def action2(self,key,pos,view):
        build = SCV()
        build.player = self.player
        build.pos = place_unit(self.pos, build.bound, view.units)
        view.units.append(build)
        
class ComsatStation(Addon):
    def __init__(self):
        Building.__init__(self)
        self.health = 750.0
        self.abilities = [
            (Spell,50.0,self.ScannerSweep)
        ]
    def ScannerSweep(self,pos):
        reveal_map_temp(pos, 10, 5.0) #rad,time
        
class NuclearSilo(Addon):
    def __init__(self):
        Building.__init__(self)
        self.health = 600.0
        self.abilities = [
            (Build,Nuke,(200,200),40,None)
        ]
        
class SupplyDepot(Building):
    def __init__(self):
        Building.__init__(self)
        self.health = 500.0
        self.food = (0,8,0)
        
class Refinery(Building):
    def __init__(self):
        Building.__init__(self)
        self.health = 750.0
        
class Barracks(Building):
    def __init__(self):
        Building.__init__(self)
        self.health = 1000.0
        self.abilitys = [
            (Build,Marine,(50,50,360),())
        ]
        
class EngineeringBay(Building):
    def __init__(self):
        Building.__init__(self)
        self.health = 850.0
        self.abilities = [
            (Upgrade,"InfantryArmor",(150,150))
        ]
        self.liftable = True
        
class MissileTurret(Building):
    def __init__(self):
        Building.__init__(self)
        self.health = 200.0
        self.projectile = LongboltMissile
        
class Academy(Building):
    def __init__(self):
        Building.__init__(self)
        self.health = 600.0
        
class Bunker(Building):
    def __init__(self):
        Building.__init__(self)
        self.health = 350.0
        
class Factory(Building):
    def __init__(self):
        Building.__init__(self)
        self.projectile = Tank
        self.recharge_time = 5.0
        self.size = 122
        self.vert = 12
        self.health = 1000.0
        self.abilities = [
            (Build,Tank,(100,50),None)
            ]
        self.liftable = True
    def update(self,dt,view):
        Building.update(self,dt,view)
        
class MachineShop(Addon): pass

class Starport(Building):
    def __init__(self):
        Building.__init__(self)
        5
        
        
class ControlTower(Building): pass

class ScienceFacility(Building): pass
class CovertOps(Building): pass
class Armory(Building):
    def __init__(self):
        Building.__init__(self)
        self.health = 750
        self.id = 123
        self.upgrades = [VehicleWeapons, VehiclePlating, ShipWeapons, ShipArmor]
        
        
class SCV(LandUnit):
    def __init__(self): # repair costs 1/3 original cost
        LandUnit.__init__(self)
        self.health = 60.0
        self.speed = 80
        self.ang_speed = 30.0
        self.size = 22
        self.vert = 11
        self.hunger = (0,1,0)
        self.bound = v(23,23)
        self.abilities = [
            (Attack,FusionCutter,1,2),
            (Build,CommandCenter,(400,0))
            ]
        self.id = 7
    def action2(self,key,pos,view):
        build = Factory()
        build.player = self.player
        build.pos = pos
        view.units.append(build)
        
        
class Marine(LandUnit):
    def __init__(self):
        LandUnit.__init__(self)
        self.health = 40.0
        self.speed = 100
        self.ang_speed = 30.0
        self.size = 22
        self.vert = 9
        self.time = 0
        self.walkt = 0
        self.id = 0
        self.abilities = [
            (Attack,GaussRifle,30,1),
            (Spell,self.Stimpack)
        ]
        self.hunger = (0,1,0)
        self.bound = (17,20)
    def Stimpack(self):
        self.stimtime = 10.0
        self.speed = 150
    def update(self,dt,view):
        LandUnit.update(self,dt,view)
        if self.moving:
            self.time += dt*25
            self.time = (self.time - 4) % 8 + 4
        else:
            self.time = 0
    def get_frame(self,dt,view):
        if self.attacking:
            self.attkt += 1
            self.attkt = (self.attkt+1) % 2
        elif self.moving:
            self.walkt += 1
            if self.walkt > 0:
                pass
        elif self.state == "idle":
            self.walkt = 1
            
class GaussRifle(Projectile): pass

class Firebat(LandUnit):
    def __init__(self):
        LandUnit.__init__(self)
        self.health = 40.0
        self.speed = .4
        self.ang_speed = 30.0
        self.recharge_time = 2
        self.range = 1
        self.projectile = GaussRifle
        self.size = .05
        self.time = 0
        
class Ghost(LandUnit):
    maxhealth = 40
    sight = property(lambda: 11 if self.player.upgrades["OpticImplants"] else 9)
    def __init__(self):
        LandUnit.__init__(self)
        self.health = 40.0
        self.speed = .4
        self.ang_speed = 30.0
        self.recharge_time = 2
        self.range = 1
        self.projectile = GaussRifle
        self.size = .05
        self.time = 0
        self.id = 1
        
class Medic(LandUnit):
    def __init__(self):
        LandUnit.__init__(self)
        self.health = 40.0
        self.speed = .4
        self.ang_speed = 30.0
        self.recharge_time = 2
        self.range = 1
        self.size = .05
        self.time = 0
class Vulture(LandUnit): pass

class Tank(LandUnit):
    def __init__(self):
        LandUnit.__init__(self)
        self.speed = 150.0
        self.ang_speed = 10.0
        self.health = 75.0
        self.recharge_time = 1.5
        self.range = 800
        self.projectile = SeigeBullet
        self.size = 62
        self.vert = 5
        self.time = 0
        self.hunger = (0,4,0)
        self.abilities = [
            (Spell,0,self.seige)
            ]
        self.seiged = False
        self.id = 5 # and 30
    def update(self,dt,view):
        LandUnit.update(self,dt,view)
        if self.moving: self.time += dt*6
        self.time = self.time % 3
    def seige(self):
        self.seige = not self.seige
        
class SeigeBullet(Projectile):
    def __init__(self):
        Projectile.__init__(self)
        self.speed = 100.0
        self.damage = 20.0
        self.sdir = 0
        
class Goliath(LandUnit): pass

class Wraith(AirUnit):
    def __init__(self):
        AirUnit.__init__(self)
        self.speed = 200.0
        self.ang_speed = 20.0
        self.health = 50.0
        self.recharge_time = 1.1
        self.range = 400
        self.size = 32
        self.vert = 12
        self.hunger = (0,2,0)
        self.projectile = Laser
        self.id = 8
        
class Laser(Projectile):
    def __init__(self):
        Projectile.__init__(self)
        self.speed = 2.0
        self.damage = 10.0
        
class Dropship(AirUnit):
    def __init__(self):
        AirUnit.__init__(self)
        self.speed = 200.0
        self.ang_speed = 20.0
        self.health = 50.0
        self.recharge_time = 1.1
        self.range = 10
        self.size = 48
        self.vert = 13
        self.hunger = (0,2,0)
        self.units = []
        self.id = 11
    def update(self,dt,view):
        AirUnit.update(self,dt,view)
        if self.dest != None and type(self.dest) != type(v(())) and type(self.dest) != type([]):
            diff = v(self.dest.pos) - self.pos
            diff = sqrt(dot(diff,diff))
            if diff <= self.range:
                view.units.remove(self.dest)
                self.units.append(self.dest)
                self.dest.dest = None
    def action2(self,key,pos,view):
        for unit in self.units: unit.pos = self.pos.copy()
        view.units.extend(self.units)
        self.units = []
        
class ScienceVessel(AirUnit): pass
class Battlecruiser(AirUnit): pass
class Valkyrie(AirUnit): pass

class FusionCutter(Projectile):
    def __init__(self):
        self.damage = 5.0
        self.speed = 1.0
        
class Nuke(Projectile): pass


class LongboltMissile(Projectile):
    def __init__(self):
        Projectile.__init__(self)
        self.damage = 20.0
