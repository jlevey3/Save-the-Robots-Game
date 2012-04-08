import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface

class Robot(Sprite):
    color = 255,255,0
    size = 20,20
    
    def __init__(self,loc,bounds):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = loc
        self.image.fill(self.color)
        
#    def update(self):

    def update(self):
        keys = pygame.key.get_pressed()
        
        
        self.rect.clamp_ip(self.bounds)


    def grabbed(self, loc):
        self
