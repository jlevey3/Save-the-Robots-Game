#!/usr/bin/env python
# ROCKS AND ROBOTS
import pygame, math, random
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide
from random import randrange
from player import Player



SCREEN_SIZE = 800,600
BG_COLOR = 0,0,0

def main():

    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect()
    
    #initialize game
    player = Player(bounds.center, bounds) #sets starting position fir player
    player_grp = GroupSingle(player)

    #game loop
    done = False
    clock = pygame.time.Clock()
    print "Loop Started"
    while not done:

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                done = True
	
	


    #input


    #update
        player.update()

    #collisions


    #draw
        screen.fill(BG_COLOR)
        player_grp.draw(screen)
        pygame.display.flip()
    
        clock.tick(30)
    


if __name__ == "__main__":
    main()
    print "Game Over"
	
    
