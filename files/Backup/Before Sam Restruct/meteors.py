import pygame
from pygame import Surface
from pygame.sprite import Sprite, Group #sprites and groups!
from random import randrange

class ImpactGroup(Group):
    impacts = Group()
        

class Hazard (Sprite):
    coord_x = 0
    coord_y = 0
    size = (2,2)
    duration = 60
    COLOR = 255,0,0
    def __init__(self,loc, bounds, falltime, kind):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.image.fill(self.COLOR)
        self.bounds = bounds
        self.duration = duration
        self.kind = kind
        
class Meteor (Sprite):
    coord_x = 0
    coord_y = 0
    size = (5,5)
    duration = 60
    COLOR = 255,0,0
    def __init__(self,loc, bounds, falltime, kind, dir=0):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.dir = dir
        self.bounds = bounds
        self.falltime = falltime
        self.kind = kind
        
        if self.kind == "ice":
            print "Recoloring for ice"
            self.COLOR = 0, 50, 155
        self.image.fill(self.COLOR)
        #self.original_image = image.convert()
    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.coord_x, self.coord_y = self.rect.center
            self.kill()
        #if self.duration < 30:
        #    if self.duration%2 == 0:
        #        self.image.fill(self.image.get_colorkey())
        #        self.image.blit(self.original_image,(0,0))
                
    
    def kill(self):
        #self.explode = Surface(self.size)
        if self.kind == "rock":
            ImpactGroup.impacts.add(Impact (self.rect.center, self.bounds, 4, self.kind))
        if self.kind == "ice":
            ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 0))
            ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 1))
            ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 2))
            ImpactGroup.impacts.add(IceImpact (self.rect.center, self.bounds, 30, self.kind, 3))

            print "ICE"
        Sprite.kill(self)
     
#class Meteor_Fall(Sprite):
    
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
        if self.duration <= 0:
            
            
            self.coord_x, self.coord_y = self.rect.center
            self.kill()
    def kill(self):    
        Sprite.kill(self)
        
        
class Impact(Meteor):
    size = (100,100)
    COLOR = 0,140,0
    duration = 5
    def __init__(self,loc, bounds, duration, kind):
        
        print "explosion!"
        
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



# make impact group itself a Group().  Group is an object.  Make a new class for each element
# of meteor



