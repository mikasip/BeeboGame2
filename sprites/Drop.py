# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:04:46 2020

@author: Mika Sipilä
"""

import pygame as pg
from settings import *
vec = pg.math.Vector2

class Drop(pg.sprite.Sprite):
    def __init__(self, game, x, y, item):
        pg.sprite.Sprite.__init__(self, game.items)
        self.item = item
        self.pos = vec(x,y)
        self.image = pg.transform.scale(item.image, (round(0.7*TILESIZE), round(0.7*TILESIZE)))
        self.rect = self.image.get_rect(left = x, top = y)
        self.type = "item"