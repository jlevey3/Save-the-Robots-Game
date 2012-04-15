#!/usr/bin/env python
# ROCKS AND ROBOTS
import pygame, math, random
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide
from random import randrange
from player import Player
from robots import Robot
from meteors import * # Meteor, Impact


SCREEN_SIZE = 800,600
BG_COLOR = 0,0,0

def main():

    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect()
    
    #initialize game
    player = Player(bounds.center, bounds) #sets starting position fir player
    robot = Robot((randrange(0,800),randrange(0,600)), bounds)
    player_grp = GroupSingle(player)
    #robot_grp = GroupSingle(robot)
    robot_grp = Group()
    robot_grp.add(Robot((randrange(0,800),randrange(0,600)), bounds))
    robot_grp.add(Robot((randrange(0,800),randrange(0,600)), bounds))
    robot_grp.add(Robot((randrange(0,800),randrange(0,600)), bounds))
    meteors = Group()
    impacts = Group()
    score = 0
    spawntime = 10
    spawnticker = 0
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

    #spawn meteors
	spawnticker += 1
	if spawnticker >= spawntime:
	    #print "spawned!"
	    meteors.add(Meteor((randrange(0,800),randrange(0,600)),bounds, 90, "rock"))
	    spawnticker = 0
	    
    #update
	meteors.update()
	ImpactGroup.impacts.update()
        player.update()

    #collisions
	coll = groupcollide(player_grp, ImpactGroup.impacts, False, False)
	for robot in coll:
	    robot.damage(coll[robot][0])
	
	coll = groupcollide(robot_grp, ImpactGroup.impacts, False, False)
	for robot in coll:
	    robot.damage(coll[robot][0])
    #draw
        screen.fill(BG_COLOR)
        
        robot_grp.draw(screen)
	
	ImpactGroup.impacts.draw(screen)
	meteors.draw(screen)
	player_grp.draw(screen)
	robot_grp.draw(screen)
        clock.tick(30)
        score_text = font.render("Score: %05d"%score, False, (255,255,255))
        screen.blit(score_text, (5,5))
        pygame.display.flip()


if __name__ == "__main__":
    main()
    print "Game Over"
	
    
