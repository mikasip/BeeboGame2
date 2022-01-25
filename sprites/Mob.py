# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 20:07:51 2019

@author: Mika Sipilä
"""


import pygame as pg
from os import path
from settings import *
from helpers import *
from sprites.obstacles import *
from SpriteSheet import *
from discussion import *
from sprites.Fighter import *
from sprites.CoinStack import *
from sprites.OtherItem import DropSprite
from Message import Message
import math
vec = pg.math.Vector2
import numpy

class Mob(Fighter):
    def __init__(self, game, x, y, player, stand_frames, walk_frames, hit_frames, exp, drop, hp, dmg, defence, gold, no_hit, hit_rect, name, walk_speed, hit_speed, id):
        self.stand_frames = stand_frames
        self.hit_frames = hit_frames
        self.current_frame = 0
        self.drop = drop
        self.gold = gold
        self.name = name
        self.walk_frames = walk_frames
        Fighter.__init__(self, game.mobs, game, x, y, self.stand_frames.get_image(0,0,100,100), hit_rect, False, hp, dmg)
        self.last_updated = numpy.random.uniform(0,0.5)
        self.player:Player = player
        self.dropped = False
        self.gives_exp = exp
        self.defence = defence
        self.exp = 0
        self.no_hit = no_hit
        self.friendly_mob = False
        self.hit_rect = hit_rect
        self.effects = []
        self.walk_speed = walk_speed
        self.hit_speed = hit_speed
        self.id = id
        self.image_index = 0
        self.others_to_update = False
        self.images = [self.stand_frames.get_image(0,0,100,100), self.stand_frames.get_image(100,0,100,100), self.walk_frames.get_image(0,0,100,100), self.walk_frames.get_image(100,0,100,100), self.hit_frames.get_image(0 * 100, 0, 100, 100), self.hit_frames.get_image(1 * 100, 0, 100, 100), self.hit_frames.get_image(2 * 100, 0, 100, 100)]
        self.total_hit_period = (HIT_COOLDOWN/3)*self.hit_speed
        self.total_slow = 1
        self.max_slow = 2

    def create_message_to_server(self):
        return self.game.current_map.name + "," +  "mob" + "," + str(self.id) + "," + str(self.max_hit_points) + "," + str(round(self.pos.x)) + "," + str(round(self.pos.y)) + "," + str(self.way.x) + "," + str(self.way.y) + "," + str(self.image_index)
        
    def update_way(self):
        closest_player = self.player
        min_dist = distance(self.player.pos, self.pos)
        for player in self.game.other_players:
            dist = distance(player.pos, self.pos)
            if dist < min_dist:
                min_dist = dist
                closest_player = player
        total_slow = self.total_slow
        self.others_to_update = False
        if closest_player != self.player:
            self.others_to_update = True
            return
        if min_dist < 200 and min_dist >= 40:
            self.vel = way_to_pos(self.pos, self.player.pos) * self.walk_speed / total_slow
        elif min_dist < 40 or min_dist > 200:
            self.vel = vec(0,0)
            if self.last_hit <= 0 and min_dist < 40 and not self.no_hit:
                self.hit(total_slow)
        self.way = way_to_pos(self.pos, self.player.pos)
        self.vel = self.vel/numpy.sqrt(numpy.abs(self.way.x) + numpy.abs(self.way.y))
                
    def update_image_index(self):
        if self.vel.x == 0 and self.vel.y == 0:
            if self.image_index == 1:
                self.image_index = 0
            else:
                self.image_index = 1
        else:
            if self.image_index == 3:
                self.image_index = 2
            else:
                self.image_index = 3
    
    def hit(self, slow):
        if self.last_hit <= 0:
            self.total_hit_period = (HIT_COOLDOWN/3)*slow/self.hit_speed
            self.hit_period = (HIT_COOLDOWN/3)*slow/self.hit_speed
            self.last_hit = HIT_COOLDOWN*slow/self.hit_speed
            self.make_hit(self.player)
    
    def remove(self):
        self.game.current_map.mobs.remove(self)
        
    def drop_coins(self):
        if self.gold > 0:
            amount = numpy.random.normal(self.gold, self.gold/4)
            coins = CoinStack(self.game, self.pos.x, self.pos.y, amount)
            self.game.current_map.items.append(coins)
    
    def drop_items(self):
        for item in self.drop:
            self.game.current_map.items.append(DropSprite(self.game, self.pos.x, self.pos.y, item))
    
    def update(self):
        if not self.wait:
            if self.dieing:
                if not self.dropped and self.killed_by_self:
                    self.drop_coins()
                    self.drop_items()
                    self.dropped = True
                self.die_animation()
            else:
                self.update_way()
                for effect in self.effects:
                    if effect.effect_time > 0:
                        effect.effect_time -= self.game.dt
                        if effect.dot_timer <= 0:
                            self.take_hit(effect.dot)
                            effect.dot_timer = effect.total_dot_timer
                    else:
                        self.effects.remove(effect)
                        self.total_slow *= (1/effect.slow)
                        self.game.add_to_send_list('damage,' + self.game.current_map.name + "," + str(self.id) + "," + str(0) + "," + str(1/effect.slow))

                if self.others_to_update:
                    self.current_image = self.images[self.image_index]
                    angle = angle_between(vec(1,0), self.way)
                    self.image, self.rect = rotate(self.current_image, angle, vec(0,0))
                    rect = self.hp_bar.get_rect(left = (self.rect.width - 50)/2, top = (self.rect.height - self.hit_rect.height)/2 - 10)
                    self.image.blit(self.hp_bar, rect)
                    self.update_hp_bar()
                    self.hit_rect.center = self.pos
                    self.rect.center = self.pos
                    return
                if self.last_updated <= 0 and self.hit_period <= 0:
                    self.update_image_index()
                    self.current_image = self.images[self.image_index]
                    self.last_updated = 0.24
                elif self.hit_period > 0 and self.hit_period < self.total_hit_period:
                    frame = math.floor((self.total_hit_period - self.hit_period) / ((self.total_hit_period/3)))
                    self.image_index = frame + 4
                    self.current_image = self.images[self.image_index]
                else:
                    self.last_updated -= self.game.dt/self.total_slow
                angle = angle_between(vec(1,0), self.way)
                self.image, self.rect = rotate(self.current_image, angle, vec(0,0))
                rect = self.hp_bar.get_rect(left = (self.rect.width - 50)/2, top = (self.rect.height - self.hit_rect.height)/2 - 10)
                self.image.blit(self.hp_bar, rect)
                #if self.hit_points < self.max_hit_points:
                #    if self.hp_reg_time <= 0:
                #        self.hit_points += 1
                #        self.hit_labels.append("+" + str(1))
                #        self.hit_label_times.append(60)
                #        self.update_hp_bar()
                #        self.hp_reg_time = self.hp_reg_time_total
                #    else:
                #        self.hp_reg_time -= 1
                #else:
                #    self.hp_reg_time = self.hp_reg_time_total
                if self.hit_period <= 0:
                    self.pos += self.vel * self.game.dt
                else:
                    self.hit_period -= self.game.dt
                self.last_hit -= self.game.dt
                self.hit_rect.center = self.pos
                self.collide_with_walls('x')
                self.collide_with_walls('y')
                self.rect.center = self.hit_rect.center
                self.game.add_to_send_list(self.create_message_to_server())

    def take_hit(self, damage, slow = 1):
        super().take_hit(damage)
        self.game.add_to_send_list('damage,' + self.game.current_map.name + "," + str(self.id) + "," + str(damage) + "," + str(slow))

    def apply_effect(self, dot, slow, effect_time):
        self.effects.append(Effect(HIT_COOLDOWN, slow, dot, effect_time))
        self.total_slow *= slow
        if self.total_slow > 2:
            self.total_slow = 2

class FriendlyMob(Mob):
    def __init__(self, game, x, y, player, stand_frames, walk_frames, exp, drop, hp, defence, gold, action, hit_rect, follows, name, walk_speed, id):
        super().__init__(game,x,y, player, stand_frames, walk_frames, walk_frames, exp, drop, hp, 0, defence, gold, True, hit_rect, name, walk_speed, 1, id)
        self.action = action
        self.action_done = False
        self.friendly_mob = True
        self.last_way_update = 0
        self.follows = follows

    def space_action(self):
        if self.action != None and not self.action_done:
            if self.action["item_needed"] == None or self.action["item_needed"] in list(map(lambda item: item.name, self.player.backpack.items)):
                item = self.game.make_item(self.action["drop"], True)
                self.game.current_map.items.append(DropSprite(self.game, self.pos.x, self.pos.y, item))
                self.action_done = True
            else:
                Message(self.game, "You need " + self.action["item_needed"] + " to " + self.action["name"], 4, self.player)
    
    def update_way(self):
        if self.follows:
            return super().update_way()
        closest_player = self.player
        min_dist = distance(self.player.pos, self.pos)
        for player in self.game.other_players:
            dist = distance(player.pos, self.pos)
            if dist < min_dist:
                min_dist = dist
                closest_player = player
        self.others_to_update = False
        if closest_player != self.player:
            self.others_to_update = True
            return
        total_slow = self.total_slow
        if self.last_way_update <= 0:
            self.last_way_update = 4
            num = numpy.random.uniform()
            if num > 0.5:
                x = numpy.random.randint(-1,2)
                y = numpy.random.randint(-1,2)
                if x == 0 and y == 0:
                    new_way = 1
                    if numpy.random.uniform() > 0.5:
                        new_way = -1
                    if numpy.random.uniform() > 0.5:
                        x = new_way
                    else:
                        y = new_way
                mult = 1
                if numpy.abs(x) + numpy.abs(y) == 2:
                    mult = 0.7071
                self.way = vec(x,y)
                self.vel = mult*self.walk_speed/total_slow*vec(x, y)
            else:
                self.vel = vec(0,0)
        else:
            self.last_way_update -= self.game.dt
            
class Effect:
    def __init__(self, dot_timer, slow, dot, effect_time):
        self.total_dot_timer = dot_timer
        self.dot_timer = dot_timer
        self.slow = slow
        self.dot = dot
        self.effect_time = effect_time   
