# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 17:52:08 2019

@author: Mika Sipilä
"""
import pygame as pg
from settings import *
from helpers import *
vec = pg.math.Vector2

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.background_sprite_sheet.get_image(0, 18*32, 32, 32)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE