import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface

class Robot(Sprite):
    color = 255,255,0
    size = 10,20
    
    def __init__(self,loc):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect
        self.rect.right = loc
        self.image.fill(self.color)
        
#    def update(self):
        
