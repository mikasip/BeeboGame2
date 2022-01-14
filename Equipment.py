# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 19:22:08 2019

@author: Mika Sipilä
"""

import pygame as pg
from os import path
from settings import *
from helpers import *
from tilemap import *
from sprites.obstacles import *
from SpriteSheet import *

class Item(object):
    def __init__(self, game, item, amount, requirements, max_stacks):
        self.name = item["name"]
        self.file = item["file"]
        self.price = item["price"]
        self.level = item["level"]
        self.type = item["type"]
        self.is_sellable = item["is_sellable"]
        self.amount = amount
        self.image = pg.image.load(resource_path('img/' + self.file + '.png')).convert_alpha()
        self.drop_image = pg.image.load(resource_path('img/' + self.file + '_drop.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.requirements = requirements
        self.stats = [str(self.name)]
        self.shop_stats = []
        self.max_stacks = max_stacks
        price_text = "Price"
        if len(self.requirements) > 0:
            reqs = "Ingredients: "
            for req in self.requirements:
                item = req["name"]
                if req["count"] > 1:
                    item += "s"
                reqs += str(req["count"]) + " " + item + ", "
            self.shop_stats.append(reqs[:-2])
            price_text = "Cost"
        self.shop_stats.append(price_text + ": " + str(self.price))


class Weapon(Item):
    def __init__(self, game, item, random_stats = False):
        Item.__init__(self, game, item, 1, item["requirements"], 1)
        self.damage = item["damage"]
        self.speed = item["speed"]
        self.strength = item["strength"]
        self.fortune = item["fortune"]
        self.agility = item["agility"]
        if random_stats:
            self.damage += round(np.random.normal(0, self.damage**(3/2)/10))
            self.strength += round(np.random.normal(0, self.strength**(3/2)/10))
            self.agility += round(np.random.normal(0, self.strength**(3/2)/10))
            self.fortune += round(np.random.normal(0, self.strength**(3/2)/10))
        self.hit_frames = SpriteSheet(resource_path('img/' + 'hero_hit_with_' + self.file + '.png'))
        self.standing_image = pg.image.load(resource_path('img/' + 'standing_hero_with_' + self.file + '.png')).convert_alpha()
        self.walking_image1 = pg.image.load(resource_path('img/' + 'walking_hero1_with_' + self.file + '.png')).convert_alpha()
        self.walking_image2 = pg.image.load(resource_path('img/' + 'walking_hero2_with_' + self.file + '.png')).convert_alpha()
        self.stats = [str(self.name), "Damage: " + str(self.damage), "Speed: " + str(self.speed), "Level needed: " + str(self.level)]
        if self.strength > 0:
            self.stats.append("Strength: " + str(self.strength))
        if self.agility > 0:
            self.stats.append("Agility: " + str(self.agility))
        if self.fortune > 0:
            self.stats.append("Fortune: " + str(self.fortune))
        
        
class Armor(Item):
    def __init__(self, game, item, random_stats = False):
        self.defence = item["defence"]
        Item.__init__(self, game, item,  1, item["requirements"], 1)
        self.strength = item["strength"]
        self.fortune = item["fortune"]
        self.agility = item["agility"]
        if random_stats:
            self.defence += round(np.random.normal(0, self.defence**(3/2)/10))
            self.strength += round(np.random.normal(0, self.strength**(3/2)/10))
            self.agility += round(np.random.normal(0, self.strength**(3/2)/10))
            self.fortune += round(np.random.normal(0, self.strength**(3/2)/10))
        self.stats = [str(self.name), "Defence: " + str(self.defence),  "Level needed: " + str(self.level)]
        if self.strength > 0:
            self.stats.append("Strength: " + str(self.strength))
        if self.agility > 0:
            self.stats.append("Agility: " + str(self.agility))
        if self.fortune > 0:
            self.stats.append("Fortune: " + str(self.fortune))
        
class Consumable(Item):
    def __init__(self, game, item):
        self.amount = 1
        Item.__init__(self, game, item,  1, item["requirements"], 10)
        self.hp = item["hp"]
        gives = ""
        self.effects = []
        try:
            if len(item["effects"]) > 0:
                gives = "Gives "
                for effect in item["effects"]:
                    self.effects.append(PlayerEffect(effect["effect"], round(effect["time"]), effect["amount"], item["name"]))
                    gives += str(effect["amount"]) + " " + effect["effect"] + " for " + str(round(effect["time"])) + " seconds, "
                gives = gives[:-2]
            else:
                gives = "Gives " + str(item["hp"]) + " hp"    
        except:
            gives = "Gives " + str(item["hp"]) + " hp"
        self.stats = [str(self.name), gives, "Level needed: " + str(self.level)]

class PlayerEffect:
    def __init__(self, effect, time, amount, item_name):
        self.effect = effect
        self.time = time
        self.amount = amount
        self.item_name = item_name
        self.message = "Affected by " + item_name
        
    def to_hash(self):
        return { 'effect': self.effect, 'time': round(self.time), 'amount': self.amount, 'item_name': self.item_name}

class OtherItem(Item):
    def __init__(self, game, item):
        Item.__init__(self, game, item,  item["amount"], item["requirements"], 99)
        self.stats = [str(self.name)]

class Spell(Item):
    def __init__(self, game, item):
        super().__init__(game, item, 1, [])
        self.damage = item["damage"]
        self.id = item["id"]
        self.strength_needed = item["strength_needed"]
        self.agility_needed = item["agility_needed"]
        self.fortune_needed = item["fortune_needed"]
        self.stats = [str(self.name), "Damage: " + str(self.damage), "Effect: " + item["effect"], "Level needed: " + str(self.level)]
        needed = "Per cast: "
        for cast_item in item["needed"]:
            needed += str(cast_item["amount"]) + " " + cast_item["name"]
            if cast_item["amount"] > 1:
                needed += "s"
            needed += ", "
        needed = needed[:-2]
        self.stats.append(needed)
        if self.strength_needed > 0:
            self.stats.append("Strength needed: " + str(self.strength_needed))
        if self.agility_needed > 0:
            self.stats.append("Agility needed: " + str(self.agility_needed))
        if self.fortune_needed > 0:
            self.stats.append("Fortune needed: " + str(self.fortune_needed))
        self.shop_stats = ["Price: " + str(self.price)]

spellId = 0   
class SpellSprite(pg.sprite.Sprite):
    def __init__(self, game, spell, x, y, way):
        global spellId
        pg.sprite.Sprite.__init__(self, game.spells)
        angle = angle_between(vec(1,0), way)
        self.file_name = spell["file"]
        self.image, self.rect = rotate(pg.image.load(resource_path('img/' + self.file_name + '.png')).convert_alpha(), angle, vec(0,0))
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0,0,32,32)
        self.current_image = self.image
        self.rect.center = (x,y)
        self.hit_rect.center = self.rect.center
        self.way = vec(way.x, way.y)
        self.damage = spell["damage"]
        self.slow = spell['slow']
        self.effect_time = spell['effect_time']
        self.dot = spell['dot']
        self.game:Game = game
        self.speed = 500
        self.time = 0.35
        self.id = spellId
        spellId += 1

    def update(self):
        self.rect.center += self.way * self.speed * self.game.dt
        self.hit_rect.center = self.rect.center
        self.time -= self.game.dt
        if self.time <= 0:
            self.kill()
        wall_hits = pg.sprite.spritecollide(self, self.game.current_map.collisions, False, collide_hit_rect)
        if len(wall_hits) > 0:
            self.kill()
            self.game.add_to_send_list('remove_spell,' + self.game.current_map.name + "," + str(self.game.player.id) + "," + str(self.id))
            return
        hits = pg.sprite.spritecollide(self, self.game.current_map.mobs, False, collide_hit_rect_center)
        for hit in hits:
            hit.take_hit(self.damage)
            self.game.add_to_send_list(hit.create_message_to_server())
            hit.apply_effect(self.dot, self.slow, self.effect_time)
            SpellHitSprite(self.game, hit.pos.x, hit.pos.y, self.file_name, self.id)
        if len(hits) > 0:
            self.kill()
            self.game.add_to_send_list(self.game.current_map.name + ",spell," + str(self.game.player.id) + "," + str(self.id) + "," + str(self.rect.centerx) + "," + str(self.rect.centery) + "," + str(self.way.x) + "," + str(self.way.y) + ',True' + "," + self.file_name)
            return
        self.game.add_to_send_list(self.game.current_map.name + ",spell," + str(self.game.player.id) + "," + str(self.id) + "," + str(self.rect.centerx) + "," + str(self.rect.centery) + "," + str(self.way.x) + "," + str(self.way.y) + ',False' + "," + self.file_name)
        

class SpellHitSprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, file_name,id):
        self.id = id
        self.time = 0.2
        pg.sprite.Sprite.__init__(self, game.spells)

        self.image = pg.image.load(resource_path('img/' + file_name + '_hit.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.center = (x,y)
        
    def update(self):
        self.time -= self.game.dt
        if self.time <= 0:
            self.kill()
            self.game.add_to_send_list('remove_spell,' + self.game.current_map.name + "," + str(self.game.player.id) + "," + str(self.id))

class OtherSpell(pg.sprite.Sprite):
    def __init__(self, game, x, y, way_x, way_y, file_name, id, player_id):
        pg.sprite.Sprite.__init__(self, game.other_spells)
        self.player_id = player_id
        self.id = id
        self.pos = vec(x,y)
        angle = angle_between(vec(1,0), vec(way_x,way_y))
        self.file_name = file_name
        self.image, self.rect = rotate(pg.image.load(resource_path('img/' + self.file_name + '.png')).convert_alpha(), angle, vec(0,0))