import pygame
from pygame import Surface
from pygame.sprite import Sprite, Group #sprites and groups!
from random import randrange
#from robots import *
from utils import *
from resource import *
from random import randint
import math

class DebrisGroup(Group):
    debris = Group()

class Debris (Sprite):
    image = 0
    size = (20,20)
    x = 0
    y = 0
    vx = 0
    vy = -20
    def __init__(self, source, vx = 30, vy = -10):
        self.vx = randrange(-30,30)
        self.vy = vy
        Sprite.__init__(self)
        self.size = source.size
        self.image = Surface(self.size)
        self.image = source.image
        #self.image.fill((200,200,200))
        self.rect = self.image.get_rect()
        self.rect.center = source.rect.center
        print "debris created"
        
    def update(self):
        
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += 1
        
        if self.rect.y >= 700 or self.rect.x >= 800 or self.rect.x <= -100:
            self.kill()
        
        