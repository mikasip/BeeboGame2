import pygame as pg
from os import path
from settings import *
from helpers import *
from tilemap import *

class Message(pg.sprite.Sprite):
    def __init__(self, game, message, time, unit, col = RED):
        self.time = time
        self.game = game
        pg.sprite.Sprite.__init__(self, game.messages)
        self.image = BODY_FONT_SMALL.render(message, True, col)
        self.rect = self.image.get_rect()
        self.message = message
        self.unit = unit
        self.rect.center = (unit.pos.x, unit.pos.y - 20)
        
    def update(self):
        i = 0
        for message in self.game.messages:
            if message.unit == self.unit:
                i += 1
            if message == self:
                break
        self.rect.center = (self.unit.pos.x, self.unit.pos.y - i*20)
        self.time -= self.game.dt
        if self.time <= 0:
            self.kill()
