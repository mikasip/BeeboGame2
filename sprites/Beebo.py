# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 20:46:16 2019

@author: Mika Sipilä
"""

import pygame as pg
from settings import *
from discussion import *
from helpers import *
from Equipment import *
from Buyer import *
vec = pg.math.Vector2

class Beebo(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, comment, name, quest):
        self.groups = game.collisionals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.game = game
        self.store = None
        self.quest = None
        self.buying = None
        if quest != None and quest not in self.game.player.completed_quests:
            self.quest = QuestDialog(game, self, quest)
        if comment != None:
            self.basic_comment = Comment(game, comment, self)
        else:
            self.basic_comment = None
        if name in SELLERS:
            self.items = []
            for item in SHOPS[name]:
                item = game.make_item(item)
                if item != None:
                    self.items.append(item)
            self.store = Store(game, self, self.items, HEAD_LINES[name])
        if name in BUYERS:
            self.buying = Buyer(game, game.player)
            
    def get_comment(self):
        if self.quest != None:
            return self.quest
        elif self.store != None:
            return self.store
        elif self.buying != None:
            return self.buying
        return self.basic_comment