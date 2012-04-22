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
pygame.init()

class Game(object):
    screen = pygame.display.set_mode(SCREEN_SIZE)
    bounds = screen.get_rect()
    font = pygame.font.Font(None,35)
    def __init__ (self):
	self.SCREEN_SIZE = SCREEN_SIZE
	self.BG_COLOR = BG_COLOR
	self.score = 0
	self.spawntime = 10
	self.spawnticker = 0
	self.robot_grp = Group()
    #initialize pygame
    
    
    
    #initialize game
	
	self.player = Player(self.bounds.center, self.bounds) #sets starting position fir player
	robot = Robot((randrange(0,800),randrange(0,600)), self.bounds)
	self.player_grp = GroupSingle(self.player)
    #robot_grp = GroupSingle(robot)
    
	self.robot_grp.add(Robot((randrange(0,800),randrange(0,600)), self.bounds))
	self.robot_grp.add(Robot((randrange(0,800),randrange(0,600)), self.bounds))
	self.robot_grp.add(Robot((randrange(0,800),randrange(0,600)), self.bounds))
	self.meteors = Group()
	self.impacts = Group()
	self.play()
    
	

    #game loop
    def input(self):
	for event in pygame.event.get():
	    if event.type == QUIT:
	        self.quit()
	    elif event.type == KEYDOWN and event.key == K_ESCAPE:
	        self.quit()

	    
	    elif event.type == KEYDOWN and event.key == K_SPACE:
		if self.player.carrying:
		    self.player.drop()
		else:
		    for robot in groupcollide(self.robot_grp, self.player_grp, False, False):
			self.player.grab(robot)
			self.score += 5
			print "robot picked up"
			break
    def quit(self):
	self.done = True
    
    def play(self):
	 # this line may need moving
	self.done = False
	self.clock = pygame.time.Clock()
	print "Loop Started"
	while not self.done:  # MAIN WHILE LOOP
		    
	    
    
    
	#input
	    self.input()
	#spawn meteors
	    self.spawnticker += 1
	    
	    if self.spawnticker >= self.spawntime:
		print "ICE SPAWNED"
		self.meteors.add(Meteor((randrange(0,800),randrange(0,600)),self.bounds, 90, "ice"))
	    
	    if self.spawnticker >= self.spawntime:
		#print "spawned!"
		self.meteors.add(Meteor((randrange(0,800),randrange(0,600)),self.bounds, 90, "rock"))
		self.spawnticker = 0
		
	#update
	    self.meteors.update()
	    ImpactGroup.impacts.update()
	    self.player.update()
    
	#collisions
	    coll = groupcollide(self.player_grp, ImpactGroup.impacts, False, False)
	    for robot in coll:
		robot.damage(coll[robot][0])
	    
	    coll = groupcollide(self.robot_grp, ImpactGroup.impacts, False, False)
	    for robot in coll:
		robot.damage(coll[robot][0])
	    
	    self.draw()
	#draw
    def draw(self):
	screen = self.screen
	self.screen.fill(BG_COLOR)
	
	self.robot_grp.draw(screen)
	
	ImpactGroup.impacts.draw(screen)
	self.meteors.draw(screen)
	self.player_grp.draw(screen)
	self.robot_grp.draw(screen)
	self.clock.tick(30)
	score_text = self.font.render("Score: %05d"%self.score, False, (255,255,255))
	
	screen.blit(score_text, (5,5))
	pygame.display.flip()


if __name__ == "__main__":
    NewGame = Game()
    NewGame.play()
    print "Game Over"
	
    
