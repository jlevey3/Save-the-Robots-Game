import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface

class Player(Sprite):
    color = 255,255,255
    size = 20,20
    speed = 7
    speedmod_rad = 0 # default -2
    speedmod_carrying = 0 #default -2

    def __init__(self,loc,bounds):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
       # self.image, self.rect = load_image('robotzim.bmp', -1)
        self.rect.center = loc
        self.bounds = bounds
        
        self.image.fill(self.color)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_DOWN] or keys[K_s]:
            self.rect.y += (self.speed + self.speedmod_rad + self.speedmod_carrying)
        if keys[K_UP] or keys[K_w]:
            self.rect.y += -self.speed
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x += -self.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += self.speed

        self.rect.clamp_ip(self.bounds) #stays within bounds
