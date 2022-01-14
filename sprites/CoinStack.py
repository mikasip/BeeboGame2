# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 18:43:24 2020

@author: Mika Sipilä
"""
import pygame as pg
vec = pg.math.Vector2

class CoinStack(pg.sprite.Sprite):
    def __init__(self, game, x, y, amount):
        pg.sprite.Sprite.__init__(self, game.items)
        self.amount = amount
        self.pos = vec(x,y)
        self.image = game.gold_img
        self.rect = self.image.get_rect(left = x, top = y)
        self.type = "gold"