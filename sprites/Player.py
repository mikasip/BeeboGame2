# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 17:51:18 2019

@author: Mika Sipilä
"""

import pygame as pg
from os import path
from settings import *
from helpers import *
from tilemap import *
from sprites.obstacles import *
from SpriteSheet import *
from discussion import *
from Backpack import *
from Equipment import *
from sprites.Fighter import *
from Statbar import *
from GUI import *
from QuestsObject import *
from sprites.OtherItem import * 
from SkillsGUI import *
from Message import *
from Buyer import Buyer
import math
import numpy
vec = pg.math.Vector2
from time import sleep

class Player(Fighter):
    def __init__(self, game, x, y):
        Fighter.__init__(self, game.players, game, x, y, game.hero_img_standing, PLAYER_HIT_RECT, True)
        self.id = 0
        self.last_updated = 0
        self.hit_door_timer = 0
        self.gold = 200
        self.level = 1
        self.exp = 0
        self.next_lvl_exp = 100
        self.strength = 1
        self.agility = 1
        self.fortune = 1
        self.total_strength = self.strength
        self.total_agility = self.agility
        self.total_fortune = self.fortune
        self.crit_chance = 0
        self.crit_ratio = 1
        self.backpack = Backpack(game, self)
        self.background = self.game.menu_box_img
        self.equipped_gear = EquippedGearGui(self.background, self, self.close_all_dialogs, self.add_to_backpack)
        self.quests = Quests(self.background, self.close_all_dialogs)
        self.door_locked_dialog = GuiGrid(0.5, 0.2, "Door locked!", None, None, 1,1, 40, [])
        self.img_standing = game.hero_img_standing
        self.img_walking1 = game.hero_img_walking1
        self.img_walking2 = game.hero_img_walking2
        self.hit_frames = game.hero_hit_frames
        self.open_dialog = None
        self.statbar = Statbar(self)
        self.skillsGUI = SkillsGUI(self)
        self.run_multiplier = 1.2
        self.active_quests = []
        self.completed_quests = []
        attribute_items = [GuiObject("Get Strength", lambda: self.update_stats("strength")), GuiObject("Get Agility", lambda: self.update_stats("agility")), GuiObject("Get Fortune", lambda: self.update_stats("fortune"))]
        self.attribute_selection = GuiGrid(0.7, 0.7, "Level up!", None, None, 1, 3, 70, attribute_items)
        self.die_dialog = GuiGrid(0.7, 0.7, "Game over...", None, None, 1, 3, 70, [GuiObject("Try again",self.load_game)])
        self.spells = []
        self.spell_objs = []
        self.spell_cast_cooldown = HIT_COOLDOWN
        self.spell_cast_timer = 0
        self.hit_cooldown = HIT_COOLDOWN
        self.hit_points = 60
        self.image_index = 0
        self.max_spells = 0
        self.effects:list[PlayerEffect] = []
        self.quick_use = []
        self.quick_use_max_space = 2
        self.quick_use_cd = 0
        
    def load_data(self, data):
        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])
        self.statbar.update()
        for item in data['equipped_items']:
            new_item = None
            if item["type"] == "weapon":
                new_item = Weapon(self.game, item)
                self.img_standing = new_item.standing_image
                self.img_walking1 = new_item.walking_image1
                self.img_walking2 = new_item.walking_image2
                self.hit_frames = new_item.hit_frames
            elif item["type"] in ["cloak", "helmet", "boots", "chestplate", "ring", "pants", "gloves"]:
                new_item = Armor(self.game, item)
            self.equipped_gear.equipped.append(new_item)
        self.equipped_gear.equipped_image = self.equipped_gear.make_image()
        for quest in self.active_quests:
            self.quests.quests.append(quest)
            self.quests.items.append(GuiObject(str(QUESTS[quest]['name']), lambda: self.quests.open_quest(QUESTS[quest])))
        self.effects = []
        for effect in data['effects']:
            new_effect = PlayerEffect(effect['effect'], effect['time'], effect['amount'], effect['item_name'])
            self.effects.append(new_effect)
            Message(self.game, new_effect.message, new_effect.time, self, BLUE)
        for item in data['quick_use']:
            item = list(filter(lambda i: i.name == item, self.backpack.items))
            if len(item) > 0:
                self.quick_use.append(item[0])
        self.quests.update_image()
        self.update_stats(None, True)
        self.make_spells()

    def update_stats(self, new_attribute = None, load_data = False):
        self.prev_strength = self.total_strength
        if new_attribute == "strength":
            self.strength += 1
        elif new_attribute == "agility":
            self.agility += 1
        elif new_attribute == "fortune":
            self.fortune += 1
        self.total_strength = self.strength
        self.total_agility = self.agility
        self.total_fortune = self.fortune
        self.defence = 0
        no_weapon = True
        for item in self.equipped_gear.equipped:
            if isinstance(item, Weapon):
                self.damage = item.damage
                self.attack_speed = item.speed
                self.total_agility += item.agility
                self.total_strength += item.strength
                self.total_fortune += item.fortune
                self.img_standing = item.standing_image
                self.img_walking1 = item.walking_image1
                self.img_walking2 = item.walking_image2
                self.hit_frames = item.hit_frames
                no_weapon = False
            elif isinstance(item, Armor):
                self.defence += item.defence
                self.total_agility += item.agility
                self.total_strength += item.strength
                self.total_fortune += item.fortune
        self.defence += self.total_strength
        self.damage += self.level
        for effect in self.effects:
            if effect.effect == "strength":
                self.total_strength += effect.amount
            elif effect.effect == "agility":
                self.total_agility += effect.amount
            elif effect.effect == "fortune":
                self.total_fortune += effect.amount
            elif effect.effect == "defence":
                self.defence += effect.amount
            elif effect.effect == "damage":
                self.damage += effect.amount
        self.max_hit_points = 40 + 20*self.total_strength
        self.crit_chance = 1 - 30/(30 + self.total_fortune)
        self.crit_ratio = math.pow(1.05, self.total_fortune)
        self.run_multiplier = 1.2 + 0.05*self.total_agility
        self.attack_speed *= math.pow(0.97, self.total_agility)
        if not load_data:
            strength_diff = self.total_strength - self.prev_strength
            self.hit_points += strength_diff*20
            if self.hit_points <= 0:
                self.hit_points = 1
        if no_weapon:
            self.img_standing = self.game.hero_img_standing
            self.img_walking1 = self.game.hero_img_walking1
            self.img_walking2 = self.game.hero_img_walking2
            self.hit_frames = self.game.hero_hit_frames
        self.statbar.update()
        if self.open_dialog == self.attribute_selection:
            self.open_dialog = None
            self.wait = False
        for level in MAX_SPELLS_PER_LEVEL.keys():
            if self.game.player.level >= level:
                self.max_spells = MAX_SPELLS_PER_LEVEL[level]
        
    def update_hit_points(self, damage):
        if damage > 0:
            self.hit_points -= damage
            self.statbar.update()
      
    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.next_lvl_exp:
            self.exp -= self.next_lvl_exp
            self.level_up()
        self.statbar.update()
        
    def level_up(self):
        self.level += 1
        self.next_lvl_exp = int(round(numpy.power(self.level, 1.5)*100, -2))
        self.open_dialog = self.attribute_selection
        self.wait = True
        
    def get_keys(self):
        self.vel = vec(0, 0)
        if self.hit_door_timer <= 0:
            keys = pg.key.get_pressed()
            if len(keys) > 0:
                self.game.add_to_send_list(self.create_message_to_server())
            if keys[pg.K_RCTRL]:
                self.speed_multiplier = self.run_multiplier
            else:
                self.speed_multiplier = 1
            if keys[pg.K_w]:
                self.cast_spell("W")
            elif keys[pg.K_e]:
                self.cast_spell("E")
            elif keys[pg.K_r]:
                self.cast_spell("R")
            elif keys[pg.K_a]:
                self.cast_spell("A")
            elif keys[pg.K_s]:
                self.cast_spell("S")
            elif keys[pg.K_d]:
                self.cast_spell("D")
            elif keys[pg.K_z]:
                self.quick_use_consumable(0)
            elif keys[pg.K_x]:
                self.quick_use_consumable(1)
            if keys[pg.K_LEFT]:
                self.vel.x = -PLAYER_SPEED
            elif keys[pg.K_RIGHT]:
                self.vel.x = PLAYER_SPEED
            if keys[pg.K_UP]:
                self.vel.y = -PLAYER_SPEED
            if keys[pg.K_DOWN]:
                self.vel.y = PLAYER_SPEED
            if self.hit_period <= 0:
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
        else:
            self.hit_door_timer -= 1
    
    def cast_spell(self, key):
        if self.spell_cast_timer <= 0:
            spells = list(filter(lambda spell: spell.key == key, self. spell_objs))
            if len(spells) > 0:
                spell = spells[0]
                if spell.current_cooldown <= 0:
                    items_needed = []
                    castable = True
                    for item_needed in spell.needed:
                        items = list(filter(lambda x: x.name == item_needed["name"], self.backpack.items))
                        if len(items) > 0:
                            if items[0].amount < item_needed["amount"]:
                                castable = False
                                items_needed.append(item_needed["name"])
                        else:
                            castable = False
                            items_needed.append(item_needed["name"])
                    if castable:
                        spell_hash = HIT_SPELLS[spell.id]
                        SpellSprite(self.game, spell_hash, self.pos.x, self.pos.y, self.way)
                        self.spell_cast_timer = self.spell_cast_cooldown*self.attack_speed
                        spell.current_cooldown = spell.cooldown*self.attack_speed
                        for item_needed in spell.needed:
                            items = list(filter(lambda x: x.name == item_needed["name"], self.backpack.items))
                            if len(items) > 0:
                                self.change_item_count(items[0], -item_needed["amount"])
                    else:
                        message = "Items needed: "
                        for item in items_needed:
                            message += item + ", "
                        message = message[:-2]
                        if len(list(filter(lambda x: x.message == message, self.game.messages))) == 0:
                            Message(self.game, message, 2, self)
    
    def quick_use_consumable(self, index):
        if self.quick_use_cd <= 0:
            if len(self.quick_use) > index:
                item = self.quick_use[index]
                backpack_items = list(filter(lambda i: i.name == item.name, self.backpack.items))
                if len(backpack_items) > 0:
                    self.quick_use_cd = 1
                    self.change_item_count(backpack_items[0], -1)
                    self.use_consumable(item)
    
    def make_spells(self):
        keys = ["W", "E", "R", "A", "S", "D"]
        self.spell_objs = []
        for i,spell in enumerate(self.spells):
            spell_obj = CastableSpell(HIT_SPELLS[spell], keys[i])
            self.spell_objs.append(spell_obj)
        self.skillsGUI.update_skills(self)
        
    def take_hit(self, damage):
        if not self.wait:
            super().take_hit(damage)
            self.game.add_to_send_list(self.create_message_to_server())

    def create_message_to_server(self):
        weapon = "none"
        weapons = list(filter(lambda item: item.type == "weapon", self.equipped_gear.equipped))
        if len(weapons) > 0:
            weapon = weapons[0].file
        return self.game.current_map.name + "," +  "player" + "," + str(self.id) + "," + str(round(self.pos.x)) + "," + str(round(self.pos.y)) + "," + str(self.hit_points) + "," + str(self.max_hit_points) + "," + str(self.way.x) + "," + str(self.way.y) + "," + str(self.image_index) + "," + weapon

    def pick_item(self, item):
        if self.append_item(item):
            self.game.current_map.items.remove(item)
            item.kill()
        else:
            self.game.error_message.create_error_dialog("Backpack is full!")
            
    def collide_with_beebo(self):
        hits = pg.sprite.spritecollide(self, self.game.current_map.beebos, False, collide_hit_rect)
        if len(hits) >= 1:
            return(hits[0])
        return False

    def collide_with_item(self):
        hits = pg.sprite.spritecollide(self, self.game.current_map.items, False, collide_hit_rect)
        if len(hits) >= 1:
            return(hits[0])
        return False

    def collide_with_doorway(self):
        hits = pg.sprite.spritecollide(self, self.game.current_map.doorways, False, collide_hit_rect)
        if len(hits) >= 1:    
            hit_vec = vec(hits[0].x, hits[0].y)
            for doorway in self.game.current_map.doorways:
                if doorway.x == hit_vec.x and doorway.y == hit_vec.y:
                    if doorway.locked:
                        if len(list(filter(lambda item: item.name == doorway.key_needed, self.backpack.items))) <= 0:
                            self.open_dialog = self.door_locked_dialog
                            break
                    map_exists = False
                    self.game.add_to_send_list("remove," + self.game.current_map.name + "," + str(self.id))
                    for tile_map in self.game.maps:
                        if tile_map.name == doorway.name:
                            self.game.current_map = tile_map
                            map_exists = True
                    if not map_exists or self.game.current_map.needs_update:
                        new_map = TiledMap(resource_path('maps/' + doorway.name + '.tmx'), doorway.name)
                        self.game.current_map = new_map
                    self.game.map_img_under, self.game.map_img_over = self.game.current_map.make_map()
                    self.game.map_rect = self.game.map_img_under.get_rect()
                    self.pos = doorway.player_pos * TILESIZE
                    self.rect.center = self.pos
                    self.hit_rect.center = self.pos
                    self.hit_door_timer = 20
                    self.game.new()
                    return True
        else:
            if self.open_dialog == self.door_locked_dialog:
                self.open_dialog = None
        return False
                
    def collide_with_mobs(self):
        for mob in self.game.current_map.mobs:
            if abs(self.pos.x - mob.pos.x) < 40 and abs(self.pos.y - mob.pos.y) < 40:
                if (self.way.x == 1 and abs(self.pos.x + 40 - mob.pos.x) < 20) or (self.way.x == -1 and abs(self.pos.x - 40 - mob.pos.x) < 20):
                    self.vel.x = 0
                if (self.way.y == 1 and abs(self.pos.y + 40 - mob.pos.y) < 20) or (self.way.y == -1 and abs(self.pos.y - mob.pos.y - 40) < 20):
                    self.vel.y = 0
    
    def collide_with_friendly_mob(self):
        for mob in self.game.current_map.mobs:
            if mob.friendly_mob:
                if abs(self.pos.x - mob.pos.x) < 40 and abs(self.pos.y - mob.pos.y) < 40:
                    return mob
        return False
                
                    
    def collide_with_treasure(self):
        hits = pg.sprite.spritecollide(self, self.game.current_map.treasures, False, collide_hit_rect)
        if len(hits) >= 1:
            return(hits[0])
        return False        
    
    def chance_gold_amount(self, amount):
        self.gold += amount
        self.gold = round(self.gold)
        self.statbar.update()
        
    def update_image(self):
        
        if self.vel.x != 0 or self.vel.y != 0:
            if self.current_image == self.img_walking1:
                self.image_index = 2
                self.current_image = self.img_walking2
            else:
                self.image_index = 1
                self.current_image = self.img_walking1
        else:
            self.current_image = self.img_standing
            self.image_index = 0
    
    def hit(self):
        if self.last_hit <= 0:
            self.hit_period = (HIT_COOLDOWN/3)*self.attack_speed
            self.last_hit = self.hit_cooldown*self.attack_speed
            for mob in self.game.current_map.mobs:
                if abs(numpy.linalg.norm(vec(self.pos.x+(self.way.x*mob.hit_rect.width), self.pos.y+(self.way.y*mob.hit_rect.height)) - mob.pos)) < 20:
                    self.make_hit(mob)
    
    def update(self):
        if not self.wait:
            if self.dieing:
                self.die_animation()
                if self.dieing_time <= 0:
                    self.open_dialog = self.die_dialog
            else:
                if self.spell_cast_timer >= 0:
                    self.spell_cast_timer -= self.game.dt
                if self.quick_use_cd > 0:
                    self.quick_use_cd -= self.game.dt
                for spell in self.spell_objs:
                    if spell.current_cooldown > 0:
                        spell.current_cooldown -= self.game.dt
                for effect in self.effects:
                    if effect.time <= 0:
                        self.effects.remove(effect)
                        self.update_stats()
                    effect.time -= self.game.dt
                self.get_keys()
                if self.last_updated <= 0 and self.hit_period <= 0:
                    self.update_image()
                    self.last_updated = IMAGE_UPDATE_FREQUENCY/self.speed_multiplier
                elif self.hit_period > 0:
                    frame = math.floor(((HIT_COOLDOWN/3)*self.attack_speed - self.hit_period) / ((HIT_COOLDOWN*self.attack_speed/(3*4))))
                    self.image_index = 3 + frame
                    self.current_image = self.hit_frames.get_image(frame * 100, 0, 100, 100)
                else:
                    self.last_updated = self.last_updated - 1
                angle = angle_between(vec(1,0), self.way)
                self.image, self.rect = rotate(self.current_image, angle, vec(0,0))
                self.collide_with_mobs()
                if self.hit_points < self.max_hit_points:
                    if self.hp_reg_time <= 0:
                        self.hit_points += 1
                        Message(self.game, "+1", 2, self, GREEN)
                        self.statbar.update()
                        self.hp_reg_time = self.hp_reg_time_total
                    else:
                        self.hp_reg_time -= self.game.dt
                else:
                    self.hp_reg_time = self.hp_reg_time_total
                if self.hit_period <= 0:
                    self.pos += self.vel * self.game.dt
                else:
                    self.hit_period -= self.game.dt
                self.last_hit -= self.game.dt
                hit_door = self.collide_with_doorway()
                if not hit_door:
                    self.hit_rect.centerx = self.pos.x
                    self.collide_with_walls('x')
                    self.hit_rect.centery = self.pos.y
                    self.collide_with_walls('y')
                    self.rect.center = self.hit_rect.center
                self.skillsGUI.update_cooldowns(self)

    def open_equipped(self):
        if self.open_dialog != self.attribute_selection:
            self.open_dialog = self.equipped_gear
            self.wait = True
            self.game.menu_open = False
    
    def open_backpack(self):
        if self.open_dialog != self.attribute_selection:
            self.open_dialog = self.backpack
            self.wait = True
            self.game.menu_open = False
    
    def open_sell_dialog(self, dialog):
        if isinstance(dialog, Buyer):
            dialog.items = list(filter(lambda item: item.is_sellable, self.backpack.items))
            dialog.image = dialog.make_backpack_image()
            self.open_dialog = dialog
            self.wait = True
    
    def open_quests(self):
        if self.open_dialog != self.attribute_selection:
            self.open_dialog = self.quests
            self.wait = True
            self.game.menu_open = False

    def handle_key_pressed(self, key):
        if self.open_dialog in [self.door_locked_dialog, self.attribute_selection, self.die_dialog]:
            self.open_dialog.handle_key_pressed(key)
        elif self.open_dialog != None:
            if key == pg.K_SPACE:
                self.open_dialog.space_pressed()
            else:
                self.open_dialog.change_active(key)
    
    def close_all_dialogs(self):
        self.open_dialog = None
        self.wait = False

    def add_to_backpack(self, item):
        existing_items = list(filter(lambda x: item.name == x.name, self.backpack.items))
        for existing_item in existing_items:
            if existing_item.max_stacks <= existing_item.amount + item.amount:
                existing_item.amount += item.amount
                self.backpack.image = self.backpack.make_backpack_image()
                return True
        if self.backpack.max_space > len(self.backpack.items):
            self.backpack.items.append(item)
            self.update_stats()
            self.backpack.image = self.backpack.make_backpack_image()
            return True
        self.game.error_message.create_error_dialog("Backpack is full!")
        return False

    def reward(self, reward):
        for item_reward in reward['items']:
            item = ITEMS[item_reward]
            item_to_add = None
            if item['type'] == "weapon":
                item_to_add = Weapon(self.game, item)
            elif item['type'] in [""]:
                item_to_add = Armor(self.game, item)
            elif item['type'] == "other_item":
                item_to_add = OtherItem(self.game, item)
            
            if not self.append_item(DropSprite(None, 0, 0, item_to_add)):
                return False
            else: 
                Message(self.game, item["name"] + " obtained!", 4, self, GREEN)
        if reward["gold"] > 0:
            Message(self.game, str(reward["gold"]) + " gold obtained!", 4, self, GREEN)
        if reward["exp"] > 0:
            Message(self.game, str(reward['exp']) + " exp obtained!", 4, self, GREEN)

        self.chance_gold_amount(reward['gold'])
        self.add_exp(reward['exp'])
        return True

    def change_item_count(self, item, amount):
        item.amount += amount
        if item.amount <= 0:
            self.backpack.items.remove(item)
        self.backpack.image = self.backpack.make_backpack_image()

    def append_item(self, item):
        if item.type == "gold":
            self.gold += round(item.amount)
            self.statbar.update()
        elif item.type == "other_item":
            items = list(filter(lambda x: x.name == item.name, self.backpack.items))
            if len(items) > 0:
                items[0].amount += 1
            else:
                added = self.add_to_backpack(item.item)
                if not added:
                    return False
            if item.only_once:
                    if item.id != None:
                        self.game.collected_items.append(item.id)
        else:
            added = self.add_to_backpack(item.item)
            if not added:
                return False
        self.backpack.image = self.backpack.make_backpack_image()
        return True

    def load_game(self):
        self.game.load_game_from_file()
        self.game.new()

    def use_consumable(self, consumable):
        if self.hit_points + consumable.hp < self.max_hit_points:
            self.hit_points += consumable.hp
        else:
            self.hit_points = self.max_hit_points
        if consumable.hp > 0:
            Message(self.game, "+" + str(consumable.hp), 1, self, GREEN)
        for effect in consumable.effects:
            self.effects.append(effect)
            Message(self.game, effect.message, effect.time, self, BLUE)
            self.update_stats()
        self.update_hp_bar()
        self.statbar.update()

class CastableSpell:
    def __init__(self, spell, key):
        self.cooldown = spell["cooldown"]
        self.current_cooldown = 0
        self.key = key
        self.id = spell['id']
        self.needed = spell["needed"]
