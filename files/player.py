import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface

class Player(Sprite):
    color = 255,255,255
    lives = 5
    size = 20,20
    speed = 7
    speedmod_rad = 0 # default -2
    speedmod_carrying = 0 #default -2
    speedmods = [0,0] #element 0 is carried, element 1-X is environment.

    def __init__(self,loc,bounds):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
       # self.image, self.rect = load_image('robotzim.bmp', -1)
        self.rect.center = loc
        self.bounds = bounds
        
        self.image.fill(self.color)
        
        self.carrying = None
    
    def grab(self, robot):
        if not self.carrying:
            self.carrying = robot
            self.speedmods[0] = -robot.weight

    def drop(self):
        self.carrying = None
        self.speedmods[0] = 0

    def update(self):
        speedtotal = 0
        for element in self.speedmods[:]:
            speedtotal += element
        if self.speed + speedtotal < 0:
            speedtotal = self.speed
        keys = pygame.key.get_pressed()
        if keys[K_DOWN] or keys[K_s]:
            self.rect.y += (self.speed + speedtotal)
        if keys[K_UP] or keys[K_w]:
            self.rect.y += -(self.speed + speedtotal)
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x += -(self.speed + speedtotal)
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += (self.speed + speedtotal)

        self.rect.clamp_ip(self.bounds) #stays within bounds


        if self.carrying:
            self.carrying.rect.center = self.rect.center #clamps robot to player
    
        if self.color[1]<255:
            self.color = self.color[0], self.color[1]+1, self.color[2]+1 
            self.image.fill(self.color)
    
    
    def damage (self, source):
        "Applies damage effect unique to the robot.  source is the object, source_element is the damage type"
        if source.kind != "radiation":  
            print "player hit: ", source, " ", source.kind
            #self.kill()
            if self.color[1]-10 < 0: #ensures a legal color
                self.kill()
            else:
                self.color = self.color[0], self.color[1]-10, self.color[2]-10  # NEED BETTER WAY TO DO THIS
                self.image.fill(self.color)
        if source.kind == "rock":
            print "Player was hit by a rock!"
