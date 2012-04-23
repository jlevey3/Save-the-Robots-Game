"""
level.py

"""

import os

import pygame
from pygame import Rect, Surface
from pygame.sprite import Group, spritecollide

from resource import load_image, play_song

from player import Player
from meteors import Meteor

class Level(object):
    song = "maintheme"

    def __init__(self, size):
        self.bounds = Rect((0,0), size)
        self.bg_tile = load_image("asphault1")

    def draw_background(self, surf):
        tw, th = self.bg_tile.get_size()
        sw, sh = surf.get_size()

        for y in range(0, sh, th):
            for x in range(0, sw, tw):
                surf.blit(self.bg_tile, (x,y))

    def restart(self):
        # start the background music
        play_song(self.song)  
        self.player = Player
    def update(self, dt):
        pass

    def draw(self, surf):
        self.draw_background(surf)
        surf.blit(self.player.image, self.player.rect)
