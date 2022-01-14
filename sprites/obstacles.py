# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:56:45 2019

@author: Mika Sipilä
"""

import pygame as pg
from settings import *
from helpers import *
from GUI import *
vec = pg.math.Vector2
import pytmx

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.collisionals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
class Doorway(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, name, pos_x, pos_y, locked, key_needed):
        self.groups = game.doorways
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.player_pos = vec(pos_x, pos_y)
        self.locked = locked
        self.key_needed = key_needed



