# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 14:14:18 2019

@author: Mika Sipilä
"""
import pygame as pg
from settings import *
from helpers import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.hero_img_standing
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.way = vec(0,1)
        self.current_image = game.hero_img_standing
        self.last_updated = 0
        
    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_RCTRL]:
            self.speed_multiplier = 2
        else:
            self.speed_multiplier = 1
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        if self.vel.x != 0 or self.vel.y != 0:
            if self.vel.x > 0:
                self.way.x = 1
            elif self.vel.x < 0:
                self.way.x = -1
            else:
                self.way.x = 0
            if self.vel.y > 0:
                self.way.y = 1
            elif self.vel.y < 0:
                self.way.y = -1
            else:
                self.way.y = 0
        self.vel *= self.speed_multiplier
        

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                
    def update_image(self):
        if self.vel.x != 0 or self.vel.y != 0:
            if self.current_image == self.game.hero_img_walking1:
                self.current_image = self.game.hero_img_walking2
            else:
                self.current_image = self.game.hero_img_walking1
        else:
            self.current_image = self.game.hero_img_standing
        
    def update(self):
        self.get_keys()
        if self.last_updated <= 0:
            self.update_image()
            self.last_updated = IMAGE_UPDATE_FREQUENCY/self.speed_multiplier
        else:
            self.last_updated = self.last_updated - 1
        if self.way.x == 0:
            if self.way.y == 1:
                self.image = pg.transform.rotate(self.current_image, -90)
            if self.way.y == -1:
                self.image = pg.transform.rotate(self.current_image, 90)
        elif self.way.y == 0:
            if self.way.x == -1:
                self.image = pg.transform.rotate(self.current_image, -180)
            if self.way.x == 1:
                self.image = self.current_image
        elif self.way.y == 1 and self.way.x == 1:
            self.image = pg.transform.rotate(self.current_image, -45)
        elif self.way.y == -1 and self.way.x == 1:
            self.image = pg.transform.rotate(self.current_image, 45)
        elif self.way.y == 1 and self.way.x == -1:
            self.image = pg.transform.rotate(self.current_image, -135)
        elif self.way.y == -1 and self.way.x == -1:
            self.image = pg.transform.rotate(self.current_image, 135)
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
