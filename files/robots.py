import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface
from player import Player
from app import *
from resource import *
from debris import *

class ShieldGroup(Group):
    shields = Group()

class RoboGroup(Group):
    robots = Group()
    robosprites = Group()

class Shield(Sprite):
    color = 255,255,255
    transparent = 0,0,0
    size = 120,120
    kind = "null"
    
    def __init__(self, parent, kind):
        self.parent=parent
        Sprite.__init__(self)
        self.kind = kind
        self.hiss_sfx = load_sfx("hiss")
        if kind == "baseball":
            self.color = 0,90,90
        elif kind == "cigar":
            self.color = 255,100,0
        elif kind == "health":
            self.color = 180, 200, 180
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.center = self.parent.rect.center
        self.image.fill(self.transparent)
        self.image.set_colorkey(self.transparent)
        pygame.draw.ellipse(self.image, (self.color), self.image.get_rect())
        pygame.draw.ellipse(self.image, self.transparent, self.image.get_rect().inflate(-10, -10))
        #pygame.draw.ellispe(self.image, (30,255,30), self.rect.center, ((self.rect.width)/2))
            
    def update(self):
        
        if not self.parent.alive():
            self.kill()
        
        self.rect.center = self.parent.rect.center
   
   
    
class Robot(Sprite):
    color = 255,255,0
    size = 20,20
    health = 1
    weight = 2
    iscarried = False
    childshield = 0
    name = "empty"
    
   

    def __init__(self,loc,bounds):
        Sprite.__init__(self)
        self.bounds = bounds
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()

        self.rect.bottomleft = loc
        self.image.fill(self.color)
        self.makeshield()
        self.sprite = RoboGroup.robosprites.add(RoboImages (self))
        self.get_sound()
#def update(self):

    def get_sound(self):
        self.death_sfx = load_sfx("brotherbotdeath")
        self.hiss_sfx = load_sfx("hiss")

    def makeshield(self):
        return
    def update(self):
        keys = pygame.key.get_pressed()
        self.rect.clamp_ip(self.bounds)
        childsprite.update
    def damage (self, source):
        if not self.immunitycheck(source):
            self.health -= source.damage
            print "robot hit"
            if source.kind == "fire":
                DebrisGroup.debris.add(Spark(self))
                self.hiss_sfx.stop()
                self.hiss_sfx.play()
                
            else:
                DebrisGroup.debris.add(Gear(self))
            if self.health <= 0:
                print "Robot killed"
                self.death_sfx.stop()
                self.death_sfx.play()
                self.kill()
    
    def immunitycheck(self, source):
        if source.kind =="radiation":
            return True
        else:
            return False
            

class Babybot(Robot):
    size = 10,10
    health = 70
    weight = 0
    name = "baby"



class Fatherbot(Robot):
    #color = 255,122,0
    size = 20,20
    health = 100
    weight = 4
    name = "father"
    
    def makeshield(self):
        self.childshield = Shield(self, "cigar")
        ShieldGroup.shields.add(self.childshield)
        
    
    def immunitycheck(self, source):
        if source.kind == "ice" or source.kind == "fire":
            pygame.draw.line(pygame.display.get_surface(), (255,0,0), self.rect.center, source.rect.center, 3)
            
            
            return True
            
        elif source.kind == "radiation":
            return True
        else:
            return False
    
    def get_sound(self):
        self.death_sfx = load_sfx("fatherbotdeath")
        
class Motherbot(Robot):
    #color = 0,122,255
    size = 20,20
    health = 120
    weight = 3
    name = "mother"
    
    def makeshield(self):
        self.childshield = Shield(self, "health")
        ShieldGroup.shields.add(self.childshield)
        

    def get_sound(self):
        self.death_sfx = load_sfx("motherbotdeath")

class Brotherbot(Robot):
    #color = 30,250,250
    size = 20,20
    health = 90
    weight = 3
    name = "brother"
    
    def get_sound(self):
        self.death_sfx = load_sfx("brotherbotdeath")
        self.bathit_sfx = load_sfx("bathit")
    def makeshield(self):
        self.childshield = Shield(self, "baseball")
        ShieldGroup.shields.add(self.childshield)
        
        
        
    
    def immunitycheck(self, source):
        if source.kind == "rock":
            pygame.draw.line(pygame.display.get_surface(), (255,0,0), self.rect.center, source.rect.center, 3)
            self.bathit_sfx.stop()
            self.bathit_sfx.play()
            return True
        elif source.kind == "radiation":
            return True
        else:
            return False

class Sisterbot(Robot):
   # color = 238,130,238
    size = 20,20
    health = 90
    weight = 2
    name = "sister"
    
    def immunitycheck(self, source):
        if True:
            self.rect.x -= 50
        self.rect.clamp_ip(self.bounds)

    def get_sound(self):
        self.death_sfx = load_sfx("sisterbotdeath")


class RoboImages(Sprite):
    color = 0,0,0
    size = 60,60
    def __init__(self, parent):
        Sprite.__init__(self)
        self.parent = parent
        self.name = parent.name
        if parent.name == "baby":
            self.size = 40,40
        self.color = parent.color
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.parent.rect.centerx
        self.rect.centery = self.parent.rect.centery
        self.dir = dir
        
    

        try:
            self.image = load_image(self.name+'bot')
            print "found family sprite"
        except:
            self.image.fill(self.color)
            print "failed to load family image"
        
        
        self.image = pygame.transform.scale(self.image, self.size)
        self.image.set_colorkey((255,255,255))
        
   
    def update(self):
        self.rect.center = self.parent.rect.center
        if not self.parent.alive():
            self.kill()
