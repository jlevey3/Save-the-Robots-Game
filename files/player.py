import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface

class Player(Sprite):
    def __init__(self,loc,bounds):
        Sprite.__init__(self)
        self.image, self.rect = load_image('robotzim.bmp', -1)
        self.rect.center = loc
        
    
    def update(self):
        self.rect.clamp_ip(self.bounds) #stays within bounds

    def carry(self):
        if not self.alive():
            return

   
    
        
