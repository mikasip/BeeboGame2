# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 14:49:11 2020

@author: Mika Sipilä
"""

import pygame as pg
import numpy
from helpers import *
from settings import *
from sprites.CoinStack import *
from sprites.Drop import *
from sprites.OtherItem import *
from Equipment import *
vec = pg.math.Vector2

class Treasure(pg.sprite.Sprite):
    def __init__(self, game, name, width, heigth, x, y, way_x, way_y, drop, tier):
        pg.sprite.Sprite.__init__(self, game.treasures)
        self.game = game
        self.name = name
        self.pos = vec(x,y)
        self.way = vec(way_x, way_y)
        self.rect = pg.Rect(x - 5,y - 5,width + 10,heigth + 10)
        self.drop = drop
        self.opened = False
        self.tier = tier
    
    def open_treasure(self):
        if not self.opened:
            if len(self.drop) == 0:
                coins = CoinStack(self.game, self.pos.x + self.way.x*TILESIZE, self.pos.y + self.way.y*TILESIZE, round(numpy.random.normal(6, 1)))
                self.opened = True
                for item in LOOTS[self.tier]:
                    p = np.random.uniform()
                    if p < item['prob']:
                        item = self.game.make_item(item['item'])
                        drop = DropSprite(self.game, self.pos.x + self.way.x*TILESIZE, self.pos.y + self.way.y*TILESIZE, item)
                        self.game.current_map.items.append(drop)
                self.game.current_map.items.append(coins)
            if not self.name in CONTINUING_TREASURES:
                self.game.opened_treasures.append(self.name)
            for item in self.drop:
                sprite = DropSprite(self.game, self.pos.x + self.way.x*TILESIZE, self.pos.y + self.way.y*TILESIZE, item)
                self.game.current_map.items.append(sprite)
            self.opened = True
