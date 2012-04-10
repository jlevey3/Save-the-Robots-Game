#!/usr/bin/env python
# ROCKS AND ROBOTS
import pygame, math, random
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide
from random import randrange
from player import Player
from meteors import * # Meteor, Impact


SCREEN_SIZE = 800,600
BG_COLOR = 0,0,0

def main():
    spawntime = 60
    spawnticker = 0
    score = 0
    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect()
    font = pygame.font.Font(None,35)
    meteors = Group()
    impacts = Group()
    
    #initialize game
    player = Player(bounds.center, bounds) #sets starting position for player
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
	    elif event.type == KEYDOWN and event.key == K_y:
		print ImpactGroup.impacts


    #input


#spawn meteors
	spawnticker += 1
	if spawnticker >= spawntime:
            #print "spawned!"
	    meteors.add(Meteor((randrange(0,400),randrange(0,200)),bounds, 90, "rock"))
	    spawnticker = 0
    #update
        player.update()
	meteors.update()
	ImpactGroup.impacts.update()

    #collisions
	coll = groupcollide(player_grp, ImpactGroup.impacts, False, False)
	for robot in coll:
	    robot.damage(coll[robot][0], coll[robot][0].kind)  #ASK ABOUT EASIER WAY TO WRITE THIS
	    #robot.damage(robot[0], robot[0].kind)
	#for robot in coll: #groupcollide(player_grp, ImpactGroup.impacts, False, False):
	#    for meteor in robot:
	#	print meteor
		#robot.damage(meteor, meteor.kind)
	    #print robot
	    #print "Impact List:", groupcollide(player_grp, ImpactGroup.impacts, False, False)
        #    robot.damage(robot{)
            
	    

    #draw
        screen.fill(BG_COLOR)
        
	meteors.draw(screen)
	ImpactGroup.impacts.draw(screen)
	player_grp.draw(screen)
	score_text = font.render("Score: %05d"%score, False, (255,255,255))
        screen.blit(score_text, (5,5))

        pygame.display.flip()
	
        clock.tick(30)
	
    


if __name__ == "__main__":
    main()
    print "Game Over"
	
    
