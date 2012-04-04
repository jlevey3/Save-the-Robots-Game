#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide
from random import randrange



SCREEN_SIZE = 800,800
BG_COLOR = 100,100,100

def main():
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect()

    #initialize game


    #game loop
    done = False
    clock = pygame.time.Clock()

    while not done:

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                done = True



    #input


    #update


    #collisions


    #draw
    screen.fill(BG_COLOR)

    pygame.display.flip()
    
    clock.tick(30)
    


if __name__ == "__main__":
    main()
    print "Game Over"
    
