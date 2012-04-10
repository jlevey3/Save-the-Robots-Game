import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface
import math

class Player(Sprite):
    color = 255,255,255
    size = 20,20
    speed = 7
    speedmod_rad = 0 # default -2
    speedmod_carrying = 0 #default -2
    maxhealth = 100
    curhealth = 100

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
        """
        if self.curhealth <= self.maxhealth:
            self.color = 255, math.floor((self.curhealth/self.maxhealth)*255), math.floor((self.curhealth/self.maxhealth)*255)
            self.image.fill(self.color)"""
            
        
        if self.color[1]<255:
            self.color = self.color[0], self.color[1]+1, self.color[2]+1 
            self.image.fill(self.color)
    
    
    def damage (self, source, source_element):
        "Applies damage effect unique to the robot.  source is the object, source_element is the damage type"
        if source_element != "radiation":
            
            print "player hit: ", source, " ", source_element
            #self.kill()
            if self.color[1]-10 < 0: #ensures a legal color
                self.kill()
            else:
                self.color = self.color[0], self.color[1]-10, self.color[2]-10  # NEED BETTER WAY TO DO THIS
                self.image.fill(self.color)
        if source_element == "rock":
            print "Player was hit by a rock!"
