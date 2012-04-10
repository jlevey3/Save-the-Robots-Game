import pygame
from pygame import Surface
from pygame.sprite import Sprite, Group #sprites and groups!
from random import randrange

class Meteor (Sprite):
    coord_x = 0
    coord_y = 0
    size = (1,1)
    falltime = 60
    COLOR = 255,0,0
    def __init__(self,loc, bounds, falltime):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.image.fill(self.color)
        self.bounds = bounds
        self.falltime = falltime
    def update():
        self.falltime -= 1
        if falltime <= 0:
            self.coord_x, self.coord_y = self.rect.center
            self.impact()

            self.kill()
    
    def impact():
        #self.explode = Surface(self.size)
        print "impact!"