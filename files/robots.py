import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface
from player import Player
from app import *

class Shield(Sprite):
    color = 255,255,255
    size = 10,10
    parent = 0
    
    def __init__(self, parent):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = parent.center
        self.image.fill(self.color)
    
class Robot(Sprite):
    color = 255,255,0
    size = 10,10
    health = 1
    weight = 2
    def __init__(self,loc,bounds):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.image.fill(self.color)
        self.makeshield()
        
#    def update(self):

    def makeshield(self):
        return
    def update(self):
        keys = pygame.key.get_pressed()
        self.rect.clamp_ip(self.bounds)
    
    def damage (self, source):
        if not self.immunitycheck(source):
            self.health -= 1
            print "robot hit"
            if self.health <= 0:
                print "Robot killed"
                #  Player.drop()  Ask Alec
                self.kill()
    
    def immunitycheck(self, source):
        return False
            

class Fatherbot(Robot):
    color = 255,122,0
    size = 20,20
    health = 2
    weight = 4
    
class Motherbot(Robot):
    color = 0,122,255
    size = 15,15
    health = 2
    weight = 3

class Brotherbot(Robot):
    color = 30,250,250
    size = 10,10
    health = 3
    weight = 3
    
    #def makeshield(self):
        
    
    def immunitycheck(self, source):
        if source.kind == "rock":
            pygame.draw.line(pygame.display.get_surface(), (255,0,0), self.rect.center, source.rect.center, 3)
            return True

class Sisterbot(Robot):
    color = 238,130,238
    size = 10,10
    health = 3
    weight = 2
    