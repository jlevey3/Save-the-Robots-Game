import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface
from resource import *

class Player(Sprite):
    color = 255,255,255
    lives = 5
    size = 20,20
    speed = 8
    health = 100
    speedmod_rad = 0 # default -2
    speedmod_carrying = 0 #default -2
    speedmods = [0,0] #element 0 is carried, element 1-X is environment.

    def __init__(self,loc,bounds):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        #self.image = load_image('archie')
        self.image.fill(self.color)
        self.rect.center = loc
        self.bounds = bounds
        self.carrying = None
        #self.image.fill((255,255,255,.5))
    
    def grab(self, robot):
        if not self.carrying:
            self.carrying = robot
            self.speedmods[0] = -robot.weight

    def drop(self):
        self.carrying = None
        self.speedmods[0] = 0

    def update(self):
        if self.carrying == None:
            self.speedmods[0] = 0
        speedtotal = 0
        for element in self.speedmods[:]:
            speedtotal += element
        if self.speed + speedtotal <= 0:
            speedtotal = -self.speed + 1
        keys = pygame.key.get_pressed()
        if keys[K_DOWN] or keys[K_s]:
            self.rect.y += (self.speed + speedtotal)
        if keys[K_UP] or keys[K_w]:
            self.rect.y += -(self.speed + speedtotal)
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x += -(self.speed + speedtotal)
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += (self.speed + speedtotal)
        
        self.speedmods[1] = 0

        self.rect.clamp_ip(self.bounds) #stays within bounds


        if self.carrying:
            self.carrying.rect.center = self.rect.center #clamps robot to player
    
    
    def damage (self, source):
        "Applies damage effect unique to the robot.  source is the object, source.kind is the damage type"
        if source.kind != "radiation":  
            print "player hit: ", source, " ", source.kind
            
        if source.kind == "rock":
            print "Player was hit by a rock!"
            self.health -= 25
        if self.health <= 0:
            self.lives -= 1
        if source.kind == "radiation":
            self.speedmods[1] = -4
