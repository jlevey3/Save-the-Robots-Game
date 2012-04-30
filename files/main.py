#!/usr/bin/env python
# ROCKS AND ROBOTS
import pygame, math, random
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide
from random import randrange
from player import *
from robots import *
from meteors import * # Meteor, Impact
from app import ApplicationState, Application
from text import TextBlock
import share
import os, sys
from resource import *
import addrobots
import meteorspawn
from meteorspawn import MeteorGroup
from debris import DebrisGroup

SCREEN_SIZE = 800,600
BG_COLOR = 0,0,0
pygame.init()

class Instruction(ApplicationState):
    fg_color = 25,255,55
    bg_color = 0,0,0
    song = "menumusic"
    
    def setup(self):
	pygame.mixer.music.set_volume(0.50)
        play_song(self.song)
	font = pygame.font.Font(None, 30)
        
        tb = TextBlock(font, justify=TextBlock.LEFT)
        self.text = tb.render("""
Archibald the Robot lived a happy existence with his robo-family, 
until one day their planet was bombarded by meteors! 
Navigate Archie around the screen to help rescue his family members
from falling meteors. 
Move quickly to avoid the meteors.
When Archie is carrying a family member, he will be significantly slowed.

Controls: 
 * Move around with W A S D keys.
 * Space picks up family members. 
 * ESC pauses the game.
 * ESC + q brings you back to the menu screen.

Hit <SPACE> to continue.

Good luck!
""".strip().split("\n"), True, self.fg_color, self.bg_color)

                
    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.app.quit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            self.app.set_state(MainMenu)

    def draw(self, screen):
        bounds = screen.get_rect()

        screen.fill(self.bg_color)
        
        rect = self.text.get_rect()
        rect.center = bounds.center
        screen.blit(self.text, rect)
        
        
class MainMenu(ApplicationState):
    fg_color = 25,255,55

    flash_rate = 500

    def setup(self):
	#self.titleimage = load_image("logo")
	#self.titleimage.set_colorkey((255,255,255))
        font = pygame.font.Font(None, 70)
        self.BG_IMAGE = load_image("Menuscreen")
        font.set_italic(True)
        font.set_underline(False)
        font = pygame.font.Font(None,30)
        self.inst = font.render("Press <SPACE> to Start", True, self.fg_color)

    def resume(self):
        self.clock = pygame.time.Clock()
        self.time = 0

    def handle_event(self, event):
        if event.type == KEYDOWN and (event.key == K_q or event.key == K_ESCAPE):
            self.app.quit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            self.app.set_state(Game)

    def update(self):
        self.time += self.clock.tick()
        self.time %= 2 * self.flash_rate
        self.draw_inst = self.time < self.flash_rate


    def draw(self, screen):
        bounds = screen.get_rect()
        screen.blit(self.BG_IMAGE, (0,0))
        if self.draw_inst:
            rect = self.inst.get_rect()
            rect.center = bounds.centerx, bounds.centery + bounds.height / 4
            screen.blit(self.inst, rect)


class PauseMenu(ApplicationState):
    def resume(self):
        self.game = self.app.state

        screen = pygame.display.get_surface()
        frame = screen.convert_alpha()
        frame.fill((0,0,0,128))
        screen.blit(frame, (0,0))


    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_q:
            self.app.set_state(MainMenu)
        elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_ESCAPE):
            self.app.set_state(self.game)

class Game(ApplicationState):
    foo = "foo"
    
    def setup (self, level_num = 1):
        print "STARTING LEVEL"
	pygame.mixer.music.stop
	self.timer = 0
	self.SCREEN_SIZE = SCREEN_SIZE
	self.BG_COLOR = BG_COLOR
	self.score = 0
	self.spawntime = 10
	self.spawnticker = 0
	self.robot_grp = RoboGroup.robots
	self.level_num = level_num
	self.BG_IMAGE = load_image("background1")
	
	self.bounds = self.app.screen.get_rect()
        self.font = pygame.font.Font(None,35)
	
	ImpactGroup.impacts.empty()
	ShieldGroup.shields.empty()
	MeteorGroup.meteors.empty()
        RoboGroup.robosprites.empty()
        PlayerSprite.sprite.empty()
        self.robot_grp.empty()
        
	
	#creates a new meteor spawner
	self.MeteorSpawner = meteorspawn.MeteorSpawner()
	self.MeteorSpawner.bounds = self.bounds

	
        
    
	self.player = Player(self.bounds.center, self.bounds) #sets starting position fir player
	
	
	self.player_grp = GroupSingle(self.player)
	setattr(share, "player", self.player_grp)

    
	#THIS FILE CONTROLS WHAT ROBOTS APPEAR AT GAME START
	import addrobots
	addrobots.addrobots(self.bounds)
	#----------------------
	
	
	
	self.meteors = MeteorGroup.meteors
	self.impacts = Group()
	setattr(share, "family", self.robot_grp)  # HAcky solution.
    
	

    #game loop
    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.app.set_state(PauseMenu)
        elif event.type == KEYDOWN and event.key == K_SPACE:
            if self.player.carrying:
                self.player.drop()
            else:
                for robot in groupcollide(self.robot_grp, self.player_grp, False, False):
                    self.player.grab(robot)
                    self.score += 50
                    print "robot picked up"
        if self.player.lives <= 0 and self.player.health <=0:
            self.app.set_state(GameOver)

    def load_image(name, colorkey=None):
        fullname = os.path.join('resources', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print "Cant load yo image:", name
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    def resume(self):    
	self.clock = pygame.time.Clock()
	print "Loop Started"
	
    def update(self):
        

	
	self.spawnticker += 1
	
	
        
        """
        if self.spawnticker >= self.spawntime:
            #print "ICE SPAWNED"
            self.meteors.add(RadiationMeteor((randrange(0,800),randrange(0,600)),self.bounds, 90, "radiation"))
	    self.meteors.add(IronMeteor((randrange(0,800),randrange(0,600)),self.bounds, 300, "iron"))
	    
	    
        if self.spawnticker >= self.spawntime:
            #print "spawned!"
            self.meteors.add(RockMeteor((randrange(0,800),randrange(0,600)),self.bounds, 90, "rock"))
            self.spawnticker = 0
	"""	
	#update
	self.MeteorSpawner.spawn()
        self.meteors.update()
        ImpactGroup.impacts.update()
        self.player.update()
	ShieldGroup.shields.update()
	FallingGroup.fallings.update()
	RoboGroup.robosprites.update()
        PlayerSprite.sprite.update()
	DebrisGroup.debris.update()
	self.timer += 1

	#collisions
        coll = groupcollide(self.player_grp, ImpactGroup.impacts, False, False)
        for robot in coll:
            robot.damage(coll[robot][0])
	    
        coll = groupcollide(self.robot_grp, ImpactGroup.impacts, False, False)
        for robot in coll:
            robot.damage(coll[robot][0])
            

    def draw(self, screen):
	screen.fill(BG_COLOR)
    
	screen.blit(self.BG_IMAGE,(0,0))
	self.robot_grp.draw(screen)	

	ImpactGroup.impacts.draw(screen)
	ShieldGroup.shields.draw(screen)
	self.meteors.draw(screen)
	self.player_grp.draw(screen)
	self.robot_grp.draw(screen)
	FallingGroup.fallings.draw(screen)
	RoboGroup.robosprites.draw(screen)
	PlayerSprite.sprite.draw(screen)
	DebrisGroup.debris.draw(screen)
	
	self.clock.tick(30)
	
	    
        lives_text = self.font.render("Lives: %01d"%self.player.lives, False, (255,255,255))
	timer_text = self.font.render("Score: %03d"%(self.timer/30), False, (255,255,255))
        health_text = self.font.render("Health: %03d"%self.player.health, False, (255,255,255))
	screen.blit(lives_text, (200,5))
	screen.blit(timer_text, (5,5))
        screen.blit(health_text, (400,5))

   

class GameOver(ApplicationState):
    fg_color = 25,255,55
    bg_color = 0,0,0
	
    def setup(self):
        font = pygame.font.Font(None, 50)
        
        tb = TextBlock(font, justify=TextBlock.CENTER)
        self.text = tb.render(("""
GAME OVER! 
Your score is: %d

Hit ESC to quit

or <space> to return to the Main Menu!
""" % self.app.state.timer).strip().split("\n"), True, self.fg_color, self.bg_color)

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.app.quit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            self.app.set_state(MainMenu)
        
    def draw(self, screen):
        bounds = screen.get_rect()
        
        screen.fill(self.bg_color)

        rect = self.text.get_rect()
        rect.center = bounds.center
        screen.blit(self.text, rect)
