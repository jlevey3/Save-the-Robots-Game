#!/usr/bin/env python
# ROCKS AND ROBOTS
import pygame, math, random
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide
from random import randrange
from player import Player
from robots import Robot


SCREEN_SIZE = 800,600
BG_COLOR = 0,0,0

def main():

    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect()
    
    #initialize game
    player = Player(bounds.center, bounds) #sets starting position fir player
    robot = Robot(bounds.bottomleft, bounds)
    player_grp = GroupSingle(player)
    robot_grp = GroupSingle(robot)
    score = 0
    font = pygame.font.Font(None,35)

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

            
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if player.carrying:
                    player.drop()
                else:
                    for robot in groupcollide(robot_grp, player_grp, False, False):
                        player.grab(robot)
                        score += 5
                        print "robot picked up"
                        break
                
	


    #input


    #update
        player.update()

    #collisions


    #draw
        screen.fill(BG_COLOR)
        player_grp.draw(screen)
        robot_grp.draw(screen)
     
    
        clock.tick(30)
        score_text = font.render("Score: %05d"%score, False, (255,255,255))
        screen.blit(score_text, (5,5))
        pygame.display.flip()


if __name__ == "__main__":
    main()
    print "Game Over"
	
    
