# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 18:35:26 2019

@author: Mika Sipilä
"""

import pygame as pg
from os import path
from settings import *
from helpers import *
from sprites.obstacles import *
from SpriteSheet import *
from discussion import *
from Message import Message
import math
vec = pg.math.Vector2
import numpy
from time import sleep

class Fighter(pg.sprite.Sprite):
    def __init__(self, groups, game, x, y, image, rect, is_player, hp = 20, dmg = 1):
        pg.sprite.Sprite.__init__(self, groups)
        self.is_player = is_player
        self.game = game
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.way = vec(0,1)
        self.image = image
        self.rect = self.image.get_rect()
        self.hit_rect = rect
        self.hit_rect.center = self.rect.center
        self.current_image = self.image
        self.wait = False
        self.hit_period = 0
        self.last_hit = 0
        self.hit_points = hp
        self.max_hit_points = hp
        self.hp_reg_time_total = 7
        self.hp_reg_time_left = 7
        self.hp_reg_time = self.hp_reg_time_total
        self.damage = dmg
        self.defence = 0
        self.crit_ratio = 1
        self.crit_chance = 0
        self.hit_font = BODY_FONT_SMALL
        self.dieing = False
        self.attack_speed = 1
        self.dieing_time = 1
        self.hp_bar_img_bg = pg.Surface((50, 8))
        self.hp_bar_img_bg.fill(LIGHTGREY)
        self.hp_bar_rect = self.hp_bar_img_bg.get_rect(left = (self.rect.width - 50)/2, top = (self.rect.height - self.hit_rect.height)/2 - 10)
        line = pg.Surface((50, 1))
        line_rect1 = line.get_rect()
        line_rect2 = line.get_rect(left = 0, top = 7)
        line2 = pg.Surface((1, 8))
        line2_rect1 = line.get_rect()
        line2_rect2 = line.get_rect(left = 49, top = 0)
        line2.fill(BLACK)
        line.fill(BLACK)
        self.hp_bar_img_bg.blit(line, line_rect1)
        self.hp_bar_img_bg.blit(line, line_rect2)
        self.hp_bar_img_bg.blit(line2, line2_rect1)
        self.hp_bar_img_bg.blit(line2, line2_rect2)
        self.hp_bar = self.hp_bar_img_bg.copy()
        hp = make_hp_bar(48, 6, self.max_hit_points, self.hit_points)
        hp_rect = hp.get_rect(top = 1, left = 1)
        self.hp_bar.blit(hp, hp_rect)
        self.killed_by_self = False
        
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.current_map.collisions, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    hit = list(filter(lambda x: x.rect.left <= self.hit_rect.right, hits))
                    if len(hit) > 0:
                        if hit[0].rect.left - self.hit_rect.centerx > hit[0].rect.top - self.hit_rect.centery and hit[0].rect.left - self.hit_rect.centerx > self.hit_rect.centery - hit[0].rect.bottom:
                            self.pos.x = hit[0].rect.left - self.hit_rect.width / 2.0
                            self.hit_rect.centerx = self.pos.x
                            self.vel.x = 0
                if self.vel.x < 0:
                    hit = list(filter(lambda x: x.rect.right >= self.hit_rect.left, hits))
                    if len(hit) > 0:
                        if self.hit_rect.centerx - hit[0].rect.right > hit[0].rect.top - self.hit_rect.centery and self.hit_rect.centerx - hit[0].rect.right > self.hit_rect.centery - hit[0].rect.bottom:
                            self.pos.x = hit[0].rect.right + self.hit_rect.width / 2.0
                            self.hit_rect.centerx = self.pos.x
                            self.vel.x = 0
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.current_map.collisions, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    hit = list(filter(lambda x: x.rect.top <= self.hit_rect.bottom, hits))
                    if len(hit) > 0 and self.hit_rect.centery < hit[0].rect.top:
                        self.pos.y = hit[0].rect.top - self.hit_rect.height / 2.0
                        self.hit_rect.centery = self.pos.y
                        self.vel.y = 0
                if self.vel.y < 0:
                    hit = list(filter(lambda x: x.rect.bottom >= self.hit_rect.top, hits))
                    if len(hit) > 0 and self.hit_rect.centery > hit[0].rect.bottom:
                        self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2.0
                        self.hit_rect.centery = self.pos.y
                        self.vel.y = 0
    
    def make_hit(self, target):
        damage = numpy.random.normal(self.damage, self.damage*0.1)
        damage = damage - target.defence
        crit = numpy.random.binomial(1, self.crit_chance)
        if crit == 1:
            damage *= self.crit_ratio
        if damage < 0:
            damage = 0
        target.take_hit(round(damage))
        self.game.add_to_send_list(target.create_message_to_server())
        if target.hit_points < 0:
            if self.is_player:
                self.add_exp(target.gives_exp)
        
    def take_hit(self, damage):
        self.update_hit_points(damage)
        if damage > 0:
            self.update_hp_bar()
        if self.hit_points < 0:
            self.dieing = True
            self.killed_by_self = True
        Message(self.game, "-" + str(damage), 2, self)
        
    def update_hit_points(self, damage):
        self.hit_points -= damage
    
    def update_hp_bar(self):
        self.hp_bar = self.hp_bar_img_bg.copy()
        hp = make_hp_bar(48, 6, self.hit_points, self.max_hit_points)
        hp_rect = hp.get_rect(top = 1, left = 1)
        self.hp_bar.blit(hp, hp_rect)
    
    def die_animation(self):
        angle = angle_between(vec(1,0), self.way)
        temp_image, temp_rect = rotate(self.current_image, angle, vec(0,0))
        self.image = temp_image
        change_alpha(self.image, round(255 - 255*(1 - self.dieing_time)))
        self.dieing_time -= self.game.dt
        if self.dieing_time <= 0:
            self.kill()
            self.remove()
            
    def remove(self):
        return
        
        