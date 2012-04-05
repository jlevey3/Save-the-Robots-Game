import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface

class Player(Sprite):
    color = 255,255,255
    size = 20,20

    def __init__(self,loc,bounds):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
       # self.image, self.rect = load_image('robotzim.bmp', -1)
        self.rect.center = loc
        self.bounds = bounds
        
        self.image.fill(self.color)
    
    def update(self):
        self.rect.clamp_ip(self.bounds) #stays within bounds

   # def carry(self):
    #    if not self.alive():
     #       return

    def walk (self, direction):
        print "walking"
        if direction == 0:
            self.rect.move(0,1)
        
