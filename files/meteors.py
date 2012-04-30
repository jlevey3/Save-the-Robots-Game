import pygame
from pygame import Surface
from pygame.sprite import Sprite, Group #sprites and groups!
from random import randrange
from robots import *
from utils import *
from resource import *
from random import randint
import math


def collide_meteor_shield(meteor, shield):
    return collide_rect_circle(meteor.rect, shield.rect.center, shield.rect.width/2)
    
def distance (self, other):
    return math.sqrt((other.rect.x-self.rect.x)**2 + (other.rect.y-self.rect.y)**2)

class ImpactGroup(Group):
    impacts = Group()

class FallingGroup(Group):
    fallings = Group()
    

        
class Meteor (Sprite):
    coord_x = 0
    coord_y = 0
    size = (60,30)
    duration = 60
    child_effect = 0;
    COLOR = 255,0,0
    
    def __init__(self,loc, bounds, falltime, kind, dir=0):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.dir = dir
        self.bounds = bounds
        self.falltime = falltime
        self.kind = kind
        self.image.fill(self.COLOR)
        self.get_sprite()
        
        
        FallingGroup.fallings.add(FallingMeteor (self))
        #self.original_image = image.convert()
        
    def get_sprite(self):
        #-----------This will attempt to load an image, and fill if it fails.
        try:
            self.image = load_image('crosshair_'+self.kind)
        except:
            self.image.fill(self.COLOR)
        #Scale the image to the proper size
        
        self.image = pygame.transform.scale(self.image, self.size) #temp
        #Anything that's pure white will be transparent
        self.image.set_colorkey((255,255,255))
        #-------
        
    def update(self):
        
       
        self.duration -= 1
        self.checkshield()
        
        if self.duration <= 0:
            self.coord_x, self.coord_y = self.rect.center
            self.kill()
        
        #if self.duration < 30:
        #    if self.duration%2 == 0:
        #        self.image.fill(self.image.get_colorkey())
        #        self.image.blit(self.original_image,(0,0))
                
    
    def checkshield(self):
        if self.duration == 1:
            coll = pygame.sprite.spritecollide(self, ShieldGroup.shields, False, collide_meteor_shield)
            for shield in coll:
                #Turn into objects later on.
                if shield.kind == "baseball" and self.kind == "rock":
                    Sprite.kill(self)
                    pygame.draw.line(pygame.display.get_surface(), (255,0,0), self.rect.center, shield.rect.center, 3)
                if shield.kind == "cigar" and self.kind == "ice":
                    Sprite.kill(self)
                    pygame.draw.line(pygame.display.get_surface(), (255,0,0), self.rect.center, shield.rect.center, 3)
    
    def kill(self):
        #self.explode = Surface(self.size)          
        Sprite.kill(self)

class IceMeteor(Meteor):
    COLOR = 0, 50, 155
    #self.image = load_image('meteor_ice')
    def shieldcheck(self):
        if self.duration == 1:
            coll = pygame.sprite.spritecollide(self, ShieldGroup.shields, False, collide_meteor_shield)
            for shield in coll:
                if shield.kind == "cigar":
                    Sprite.kill(self)
                    pygame.draw.line(pygame.display.get_surface(), (255,0,0), self.rect.center, shield.rect.center, 3)
        
    def kill(self):
        ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 0))
        ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 1))
        ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 2))
        ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 3))
        Sprite.kill(self)
        
    
    
class RockMeteor(Meteor):
    COLOR = 255,165,0

    def shieldcheck(self):
        if self.duration == 1:
            coll = pygame.sprite.spritecollide(self, ShieldGroup.shields, False, collide_meteor_shield)
            for shield in coll:
                if shield.kind == "baseball":
                    Sprite.kill(self)
                    pygame.draw.line(pygame.display.get_surface(), (255,0,0), self.rect.center, shield.rect.center, 3)
        
    def kill(self):
        ImpactGroup.impacts.add(RockImpact (self.rect.center, self.bounds, 4, self.kind))
        Sprite.kill(self)




class IronMeteor(Meteor):
    COLOR = 255,170,170

    target = None
    speed = 1
    tracking_distance = 200
    kind = "iron"
    def __init__(self, *args):
        Meteor.__init__(self, *args)
        import share
        self.robotlist = share.player.sprites() + share.family.sprites()
    
    def update(self):
        self.duration -= 1
        self.checkshield()
        if self.duration <= 0:
            self.coord_x, self.coord_y = self.rect.center
            self.kill()
            
        # Homing!
        if self.target == None:
            distances = []
            #go for a coordinate, not an object
            for robot in self.robotlist:
                distances.append((distance(self,robot), robot))
            distances.sort()
            if distances[0][0] <= self.tracking_distance:
                self.target = distances[0][1]
        else:
            if distance(self, self.target) >=self.tracking_distance :
                self.target = None
            else:
                if self.rect.x > self.target.rect.x:
                    self.rect.x -= self.speed
                elif self.rect.x < self.target.rect.x:
                    self.rect.x += self.speed
                if self.rect.y > self.target.rect.y:
                    self.rect.y -= self.speed
                elif self.rect.y < self.target.rect.y:
                    self.rect.y += self.speed
                    
    def kill(self):
        ImpactGroup.impacts.add(RockImpact (self.rect.center, self.bounds, 4, self.kind))
        Sprite.kill(self)

        

            

class RadiationMeteor(Meteor):
    COLOR = 255,255,255
    kind = "radiation"
    
    def update(self):
        self.duration -= 1
        self.checkshield()
        if self.duration <= 0:
            self.coord_x, self.coord_y = self.rect.center
            self.kill()
    
    def kill(self):
        ImpactGroup.impacts.add(RadiationImpact (self.rect.center, self.bounds, 60, self.kind))
        Sprite.kill(self)



class FireMeteor(Meteor):
    COLOR = 255,255,255
    kind = "fire"
    
    def update(self):
        self.duration -= 1
        self.checkshield()
        if self.duration <= 0:
            self.coord_x, self.coord_y = self.rect.center
            self.kill()
    
    def kill(self):
        ImpactGroup.impacts.add(FireImpact (self.rect.center, self.bounds, 60, self.kind))
        Sprite.kill(self)


        
class Impact(Meteor):
    size = (100,100)
    COLOR = 0,140,0
    duration = 5
    dir = 0
 #   impact_sfx = load_sfx("stockmeteorhit")
    def __init__(self,loc, bounds, duration, kind, dir = 0):
        
        #print "explosion!"
        self.dir = dir
        # Ice should have moving impacts
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.image.fill(self.COLOR)
        self.bounds = bounds
        self.duration = duration
        self.kind = kind
        self.get_sprite()
#        self.imact_sfx.stop()

#        self.imact_sfx.play()
    def get_sprite(self):
        #return

        #-----------This will attempt to load an image, and fill if it fails.
        try:
            self.image = load_image('explosion_'+self.kind)
            print "impact explosion yay"
        except:
            self.image.fill(self.COLOR)
            print "failed to find explosion"
        #Scale the image to the proper size and add random rotation
        #if randint(0,2) == 0:
        #    self.image = pygame.transform.flip(self.image, True, False)
        #self.image = pygame.transform.rotate(self.image, randint(-360,360))
        
        self.image = pygame.transform.scale(self.image, self.size) #temp
        #Anything that's pure white will be transparent
        self.image.set_colorkey((255,255,255))
        #-------
        
        
        
        
    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.coord_x, self.coord_y = self.rect.center
            self.kill()
            
    #def collision(self, robot):
        
        
    def kill (self):
        Sprite.kill(self)


class RockImpact(Impact):
    COLOR = 110,110,110
    kind = "rock"
    

    
class RadiationImpact(Impact):
    COLOR = 60,255,60
    kind = "radiation"
    duration = 60
    size = (100,100)
    
    def get_sprite(self):
        #return

        #-----------This will attempt to load an image, and fill if it fails.
        try:
            self.image = load_image('radiationcloud')
            print "impact explosion yay"
        except:
            self.image.fill(self.COLOR)
            print "failed to find explosion"
        #Scale the image to the proper size and add random rotation
        
        
        self.image = pygame.transform.scale(self.image, self.size) #temp
        #Anything that's pure white will be transparent
        self.image.set_colorkey((255,255,255))
        #-------
    
class FireImpact(Impact):
    COLOR = 60,255,60
    kind = "Fire"
    duration = 60
    size = (160,160)
    
    def get_sprite(self):
        #return

        #-----------This will attempt to load an image, and fill if it fails.
        try:
            self.image = load_image('coals')
            print "impact explosion yay"
        except:
            self.image.fill(self.COLOR)
            print "failed to find explosion"
        #Scale the image to the proper size and add random rotation
        
        
        self.image = pygame.transform.scale(self.image, self.size) #temp
        #Anything that's pure white will be transparent
        self.image.set_colorkey((255,255,255))


class IceImpact (Impact):
    COLOR = 0,50,160
    kind = "ice"
    duration = 30
    size = (30,30)
    def update(self):
        self.duration -= 1
        
        if self.dir == 0: # Left
            self.rect.x -= 5
        if self.dir == 1: # Up
            self.rect.y -= 5
        if self.dir == 3: # Right
            self.rect.y += 5
        if self.dir == 2: # South
            self.rect.x += 5
        # 0 = West, 1 = North, 2 = East, 3 = South
        self.checkshield()
        if self.duration <= 0:
            
            self.coord_x, self.coord_y = self.rect.center
            self.kill()
    def checkshield(self):
        coll = pygame.sprite.spritecollide(self, ShieldGroup.shields, False, collide_meteor_shield)
        for shield in coll:
            for shield in coll:
            #Turn into objects later on.
                if shield.kind == "cigar":
                    Sprite.kill(self)
                    pygame.draw.line(pygame.display.get_surface(), (255,0,0), self.rect.center, shield.rect.center, 3)
                    
    def kill(self):    
        Sprite.kill(self)
    
    def get_sprite(self):
        #-----------This will attempt to load an image, and fill if it fails.
        try:
            self.image = load_image('explosion_ice_'+str(self.dir))
            #print "found sprite"
        except:
            self.image.fill(self.COLOR)
            #print "failed sprite"
        #Scale the image to the proper size
        if self.dir == 0 or self.dir == 2: # Left
            self.size = (30,20)
        if self.dir == 1 or self.dir == 3: # Up
            self.size = (20,30)
        self.image = pygame.transform.scale(self.image, self.size) #temp
        #Anything that's pure white will be transparent
        self.image.set_colorkey((255,255,255))
        #-------

# make impact group itself a Group().  Group is an object.  Make a new class for each element
# of meteor
#





class FallingMeteor(Sprite):
    COLOR = 0,0,0
    size = 40,40
    height = 1000
    def __init__(self, parent):
        Sprite.__init__(self)
        self.parent = parent
        self.kind = parent.kind
        self.COLOR = parent.COLOR
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.parent.rect.centerx
        self.rect.centery = self.parent.rect.centery - self.height
        self.dir = dir
        self.get_sprite()
        
    def get_sprite(self):
        #-----------This will attempt to load an image, and fill if it fails.
        try:
            self.image = load_image('meteor_'+self.kind)
        except:
            self.image.fill(self.COLOR)
        #Scale the image to the proper size and add random rotation
        if randint(0,2) == 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.rotate(self.image, randint(-360,360))
        
        self.image = pygame.transform.scale(self.image, self.size) #temp
        #Anything that's pure white will be transparent
        self.image.set_colorkey((255,255,255))
        #-------
        

    def update(self):
        if not self.parent.alive():
            self.kill()
            
        if self.parent.duration <=20:
            self.rect.centery = self.parent.rect.centery - (self.parent.duration * 20)
            self.rect.centerx = self.parent.rect.centerx

class Crosshair(FallingMeteor):
    height = 0
    size = (60,30)
    
    def update():
        if not self.parent.alive():
            self.kill()
            
    def get_sprite(self):
        #-----------This will attempt to load an image, and fill if it fails.
        try:
            self.image = load_image('crosshair_'+self.kind)
        except:
            self.image.fill(self.COLOR)
        #Scale the image to the proper size and add random rotation
        self.image = pygame.transform.scale(self.image, self.size) #temp
        #Anything that's pure white will be transparent
        self.image.set_colorkey((255,255,255))
        #-------
