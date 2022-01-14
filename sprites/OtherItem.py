import pygame as pg
from os import path
vec = pg.math.Vector2

class DropSprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, item, only_once = False, id = None):
        if game != None:
            pg.sprite.Sprite.__init__(self, game.items)
        self.amount = 1
        self.pos = vec(x,y)
        self.file = item.file
        self.image = item.drop_image
        self.rect = self.image.get_rect(left = x, top = y)
        self.name = item.name
        self.type = item.type
        self.item = item
        self.amount = item.amount
        self.only_once = only_once
        self.id = id