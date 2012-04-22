"""
This file is for the stuff that loads images and sounds to the game
"""

import os
from os.path import abspath, dirname

import pygame

ROOT_DIR = dirname(abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "resources")
IMG_DIR = os.path.join(DATA_DIR, "images")

_images = {}
def load_image(name):
    if name not in _images:
        path = os.path.join(IMG_DIR, name + ".bmp")
        _images[name] = pygame.image.load(path)
        
    return _images[name].convert()
    