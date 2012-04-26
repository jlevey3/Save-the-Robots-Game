import pygame
from pygame import Surface
from pygame.sprite import Sprite, Group #sprites and groups!
from random import randrange
from robots import *
from utils import *
from resource import *
from random import randint

def collide_meteor_shield(meteor, shield):
    return collide_rect_circle(meteor.rect, shield.rect.center, shield.rect.width/2)
    
def distance (self, other):
    return math.sqrt((other.x-self.x)**2 + (other.y-self.y)**2)

class ImpactGroup(Group):
    impacts = Group()

class FallingGroup(Group):
    fallings = Group()
        

        
class Meteor (Sprite):
    coord_x = 0
    coord_y = 0
    size = (5,5)
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
        
        
        FallingGroup.fallings.add(FallingMeteor (self))
        #self.original_image = image.convert()
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
        if self.kind == "rock":
            ImpactGroup.impacts.add(Impact (self.rect.center, self.bounds, 4, self.kind))
        if self.kind == "ice":
            ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 0))
            ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 1))
            ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 2))
            ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 3))

            
        Sprite.kill(self)

class IceMeteor(Meteor):
    size = 5,5
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
        ImpactGroup.impacts.add(RockImpact (self.rect.center, self.bounds, 4, self.kind))
        Sprite.kill(self)
    
class RockMeteor(Meteor):
    COLOR = 255,165,0
    size = 5,5
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
    COLOR = 255,255,255
    size = 7,7
    
    
    def update(self):
        self.duration -= 1
        self.checkshield()
        if self.duration <= 0:
            self.coord_x, self.coord_y = self.rect.center
            self.kill()
#class Meteor_Fall(Sprite):
    

class RadiationMeteor(Meteor):
    COLOR = 255,255,255
    size = 7,7
    
    
    def update(self):
        self.duration -= 1
        self.checkshield()
        if self.duration <= 0:
            self.coord_x, self.coord_y = self.rect.center
            self.kill()
    
    def kill(self):
        ImpactGroup.impacts.add(RadiationImpact (self.rect.center, self.bounds, 4, self.kind))
        Sprite.kill(self)





        
class Impact(Meteor):
    size = (100,100)
    COLOR = 0,140,0
    duration = 5
    def __init__(self,loc, bounds, duration, kind):
        
        #print "explosion!"
        
        # Ice should have moving impacts
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.image.fill(self.COLOR)
        self.bounds = bounds
        self.duration = duration
        self.kind = kind
        if kind == "rock":
            self.duration = 10
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
    COLOR = 40,130,40
    kind = "radiation"
    duration = 60
    size = (100,100)

class IceImpact (Meteor):
    COLOR = 0,50,160
    duration = 30
    size = (30,30)
    def update(self):
        self.duration -= 1
        if self.dir == 0:
            self.rect.x -= 5
        if self.dir == 1:
            self.rect.y -= 5
        if self.dir == 2:
            self.rect.y += 5
        if self.dir == 3:
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

# make impact group itself a Group().  Group is an object.  Make a new class for each element
# of meteor
#



class FallingMeteor(Sprite):
    COLOR = 0,0,0
    size = 40,40
    height = 1000
    def __init__(self, parent):
        print "Falling Meteor Created!"
        Sprite.__init__(self)
        self.parent = parent
        self.kind = parent.kind
        self.COLOR = parent.COLOR
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.parent.rect.centerx
        self.rect.centery = self.parent.rect.centery - self.height
        self.dir = dir
        
        
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
