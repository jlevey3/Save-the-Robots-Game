import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from pygame import Surface
from resource import *
import glob
import math

class PlayerSprite(Group):
    sprite = Group()



    
        
class Player(Sprite):
    color = 255,255,255
    lives = 5
    size = 40,40
    speed = 10
    health = 100
    # Endurance:
    max = 500
    value = 500
    recoveryrate = 5
    
    
    anim_counter = 1
    anim_frame = 0
    sprite = 0
    dir = 0
    anim_array = []
    speedmod_rad = 0 # default -2
    speedmod_carrying = 0 #default -2
    speedmods = [0,0,0] #element 0 is carried, element 1-X is environment.
    

    def __init__(self,loc,bounds):
        Sprite.__init__(self)
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        #self.image = load_image('archie')
        #self.image.fill(self.color)
        self.rect.center = loc
        self.bounds = bounds
        self.carrying = None
        self.sprite = PlayerSprite.sprite.add(Animation(self))
        #self.image.fill((255,255,255,.5))
        self.death_sfx = load_sfx("archiestrike")
        
       
    
    def grab(self, robot):
        if not self.carrying:
            self.carrying = robot
            self.speedmods[0] = -robot.weight

    def drop(self):
        self.carrying = None
        self.speedmods[0] = 0

    def update(self):
        if self.carrying != None:
            if not self.carrying.alive():
                self.carrying = None
        if self.carrying == None:
            self.speedmods[0] = 0
            self.recover()
        else:
            self.decay()
        self.speedmods[2] = -self.tired()
        print str(self.value) + " " + str(self.tired())
        speedtotal = 0
        for element in self.speedmods[:]:
            speedtotal += element
        if self.speed + speedtotal <= 0:
            speedtotal = -self.speed + 1
        keys = pygame.key.get_pressed()
        
        #For testing.
        
        if keys[K_y]:
            self.lives -=1
            self.health -= 100
        
        if keys[K_DOWN] or keys[K_s]:
            self.dir = 2
            self.rect.y += (self.speed + speedtotal)
        
        if keys[K_UP] or keys[K_w]:
            self.dir = 0
            self.rect.y += -(self.speed + speedtotal)
            
        if keys[K_LEFT] or keys[K_a]:
            self.dir = 3
            self.rect.x += -(self.speed + speedtotal)
           
        if keys[K_RIGHT] or keys[K_d]:
            self.dir = 1
            self.rect.x += (self.speed + speedtotal)
           

        if keys [K_DOWN] or keys[K_s] or keys[K_LEFT] or keys[K_a] or keys[K_RIGHT] or keys[K_d] or keys[K_UP] or keys[K_w]:
            self.anim_counter += 1
        else:
            self.anim_counter = 1
            self.anim_frame = 0
            
        if self.anim_counter % 3 == 0:
            self.anim_frame +=1
        
        if self.anim_frame >= 3:
            self.anim_frame = 0
        self.speedmods[1] = 0

        self.rect.clamp_ip(self.bounds) #stays within bounds


        if self.carrying:
            self.carrying.rect.center = self.rect.center #clamps robot to player
        
        #self.image = self.animation[self.carrying][self.direction][self.anim_frame]
    
    def damage (self, source):
        self.death_sfx.stop()
        self.death_sfx.play()
        "Applies damage effect unique to the robot.  source is the object, source.kind is the damage type"
        if source.kind != "radiation":  
            print "player hit: ", source, " ", source.kind
        if source.kind == "ice":
            self.health -=20
        if source.kind == "fire":
            self.health -= 5
        if source.kind == "rock":
            print "Player was hit by a rock!"
            self.health -= 10
        if self.health <= 0 and self.lives > 0:
            self.lives -= 1
            self.health = 100
        if source.kind == "radiation":
            self.speedmods[1] = -4
            
            
            
    def recover(self):
        if self.value < self.max:
            if (self.max - self.value) <= self.recoveryrate:
                self.value = self.max
            else: self.value += self.recoveryrate
    
    def decay(self):
        if self.value > 0:
            self.value -= 1
    
    def tired(self):
        return math.floor(7 - (self.value / (self.max/7)))

   # forward=[(load_image("forward_"+str(self.iscarrying)+"_"+str(self.frame))]

   
            

# [0 or 1 to denote carrying][0-4 to denote direction][0-6 for frame]

class Animation(Sprite):
    anim_array = []
    size = (80,100)
    def __init__(self, parent):
        Sprite.__init__(self)
        self.parent = parent
        self.color = parent.color
        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.parent.rect.centerx
        self.rect.centery = self.parent.rect.centery
        self.dir = dir
        self.get_anims()

    #    try:
     #       self.image = load_image(self.anim_array)
      #  except:
       #     //self.image.fill(self.color)
    


    def update(self):
        self.image = self.anim_array[0][self.parent.dir][self.parent.anim_frame]
        self.image = pygame.transform.scale(self.image, self.size)
        self.image.set_colorkey((255,255,255))
        self.rect.center = self.parent.rect.center
        
        if not self.parent.alive():
            self.kill()

    def get_anims(self):
        self.anim_array = [[],[]]
        self.anim_array[0].append([]) 

        for i in range (0,5):
            self.anim_array[0][0].append(load_image("Archie/back_"+str(i)))
            print self.anim_array
        self.anim_array[0].append([])
        for i in range(0,5):
            self.anim_array[0][1].append(load_image("Archie/right_"+str(i)))
        self.anim_array[0].append([])
        for i in range(0,5):
            self.anim_array[0][2].append(load_image("Archie/forward_"+str(i)))  
        self.anim_array[0].append([])
        for i in range(0,5):
            self.anim_array[0][3].append(load_image("Archie/left_"+str(i)))
        self.anim_array[0].append([])

        for i in range(0,5):
            self.anim_array[0][0].append(load_image("Archie/carry_back_"+str(i)))
        self.anim_array[0].append([])
        for i in range(0,5):
            self.anim_array[0][1].append(load_image("Archie/carry_right_"+str(i)))
        self.anim_array[0].append([])
        for i in range(0,5):
            self.anim_array[0][2].append(load_image("Archie/carry_forward_"+str(i)))
        self.anim_array[0].append([]) 
        for i in range(0,5):
            self.anim_array[0][3].append(load_image("Archie/carry_left_"+str(i)))
        self.anim_array[0].append([])

    

        