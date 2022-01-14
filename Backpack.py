# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:54:23 2019

@author: Mika Sipilä
"""

from sprites.sprites import Player
import pygame as pg
from os import path
from settings import *
from helpers import *
from tilemap import *
from Equipment import *
from sprites.obstacles import *
from GUI import *

class Backpack(object):
    def __init__(self, game, player:Player):
        self.background = game.menu_box_img
        self.background_rect = self.background.get_rect()
        self.font = HEADER_FONT
        self.stat_font = BODY_FONT
        self.items = []
        self.active_index = 0
        self.active_row = 1
        self.active_col = 1
        self.rows = 1
        self.cols = 1
        self.equip_index_active = 0
        self.equip_dialog_open = False
        self.can_not_wear_dialog_open = False
        self.game = game
        self.player:Player = player
        self.can_change = True        
        self.image = self.make_backpack_image()
        self.max_space = 40
        
    def get_image(self):
        return self.image

    def get_rect(self):
        return self.background_rect

    def load_data(self, data):
        for item in data:
            if item["type"] == "weapon":
                new_item = Weapon(self.game, item)
            elif item["type"] in ["cloak", "helmet", "boots", "chestplate", "ring", "pants", "gloves"]:
                new_item = Armor(self.game, item)
            elif item["type"] == "other_item":
                new_item = OtherItem(self.game, item)
            else:
                new_item = Consumable(self.game, item)
            self.items.append(new_item)
        self.image = self.make_backpack_image()
        
    def make_backpack_image(self):
        if len(self.items) >= math.floor((WIDTH - 60) / 70):
            self.cols = math.floor((WIDTH - 60) / 70)
        else:
            self.cols = len(self.items)
        image = pg.Surface(self.background_rect.size)
        image.blit(self.background, (0,0))
        head_line_image = self.font.render("Inventory", True, BLACK)
        head_line_rect = head_line_image.get_rect(left = 50, top = 50)
        image.blit(head_line_image, head_line_rect)
        next_item_pos = vec(30, 80)
        self.rows = 1
        for i, item in enumerate(self.items):
            bg_image, bg_image_rect = create_item_with_rect(item.image, 70, 70, next_item_pos.x, next_item_pos.y, (self.active_index == i))
            image.blit(bg_image, bg_image_rect)
            if next_item_pos.x + 170 >= WIDTH:
                next_item_pos.x = 30
                next_item_pos.y += 70
                self.rows += 1
            else:
                next_item_pos.x += 70
            if next_item_pos.y + 170 >= HEIGHT:
                break
        if self.active_index < len(self.items):
            stat_w, stat_h = (200, 160)
            stat_bg = pg.Surface((stat_w,stat_h), pg.SRCALPHA)
            pg.draw.line(stat_bg, BLACK, (0,0), (stat_w,0))
            pg.draw.line(stat_bg, BLACK, (0,0), (0,stat_h))
            pg.draw.line(stat_bg, BLACK, (0, stat_h - 1), (stat_w, stat_h - 1))
            pg.draw.line(stat_bg, BLACK, (stat_w - 1, 0), (stat_w - 1, stat_h))
            y = 10
            for i, stat in enumerate(self.items[self.active_index].stats):
                y = blit_text(stat_bg, stat, (10, y), stat_w - 20, stat_h - 20, self.stat_font)[0]
            stat_rect = stat_bg.get_rect(left = WIDTH - stat_w - MARGIN_LEFT, top = HEIGHT - stat_h - MARGIN_BOT)
            image.blit(stat_bg, stat_rect)
        quit_img = self.stat_font.render("BACK", True, BLACK)
        bg_image, bg_image_rect = create_item_with_rect(quit_img, 70, 40, MARGIN_LEFT, HEIGHT - 40 - MARGIN_BOT, (self.active_index == len(self.items)))
        image.blit(bg_image, bg_image_rect)
        gold_text_img = self.stat_font.render("Your gold: " + str(self.player.gold), True, BLACK)
        gold_text_rect = gold_text_img.get_rect()
        gold_text_rect2 = gold_text_img.get_rect(left = WIDTH - gold_text_rect.width - MARGIN_LEFT - 25, top = MARGIN_BOT)
        image.blit(gold_text_img, gold_text_rect2)
        gold_icon_rect = self.game.gold_img.get_rect(left = WIDTH - MARGIN_LEFT - 22, top = MARGIN_BOT)
        image.blit(self.game.gold_img, gold_icon_rect)
        if self.equip_dialog_open:
            self.create_equip_dialog(image)
            
        return image
    
    def change_active(self, key):
        if self.equip_dialog_open:
            if key == pg.K_RIGHT:
                self.equip_index_active = 1
            if key == pg.K_LEFT:
                self.equip_index_active = 0
        else:
            self.active_index = move_in_matrix(self.cols, self.rows, self.active_index, len(self.items), key)
        self.image = self.make_backpack_image()
        
        
    def space_pressed(self):
        if self.active_index == len(self.items) and not self.equip_dialog_open:
            self.player.open_dialog = None
            self.player.wait = False
        else:
            if self.items[self.active_index].type == "consumable":
                self.use_consumable()
            elif not self.items[self.active_index].type == "other_item":
                if self.items[self.active_index].type in map(lambda o : o.type, self.player.equipped_gear.equipped):
                    message = "You are already wearing " + str(self.items[self.active_index].type)
                    self.game.error_message.create_error_dialog(message)
                elif self.player.level < self.items[self.active_index].level:
                    message = "Level needed: " + str(self.items[self.active_index].level)
                    self.game.error_message.create_error_dialog(message)
                elif not self.equip_dialog_open:
                    self.create_equip_dialog(self.image)
                    self.equip_dialog_open = True
                else:
                    if self.equip_dialog_open:
                        if self.equip_index_active == 0:
                            self.append_item(self.items[self.active_index])
                            self.equip_dialog_open = False
                        else:
                            self.equip_dialog_open = False
                        self.image = self.make_backpack_image()
                    
    def create_equip_dialog(self, image):
        
        bg_surface = pg.Surface(self.background_rect.size)
        bg_surface.blit(self.background, (0,0))
        purchase_surface = pg.transform.scale(bg_surface, (360, 110))
        purchase_text = self.font.render(self.make_action_text(), True, BLACK)
        purchase_image, purchase_rect = create_item_with_rect(purchase_text, 150, 50, 30, 30, (self.equip_index_active == 0))
        cancel_text = self.font.render("Cancel", True, BLACK)
        cancel_image, cancel_rect = create_item_with_rect(cancel_text, 150, 50, 180, 30, (self.equip_index_active == 1))
        purchase_surface.blit(purchase_image, purchase_rect)
        purchase_surface.blit(cancel_image, cancel_rect)
        purchase_surface_rect = purchase_surface.get_rect(top = (HEIGHT - 110) / 2, left = (WIDTH - 360) / 2)
        image.blit(purchase_surface, purchase_surface_rect)
    
    def make_action_text(self):
        return "Equip"
        
    def append_item(self, item):
        self.items.remove(item)
        self.player.equipped_gear.equipped.append(item)
        self.equip_dialog_open = False
        self.player.update_stats()
        self.image = self.make_backpack_image()
        self.player.equipped_gear.equipped_image = self.player.equipped_gear.make_image()
    
    def close_consumable_dialog(self):
        self.player.open_dialog = None
    
    def use_consumable(self):
        self.player.use_consumable(self.items[self.active_index])
        self.items.remove(self.items[self.active_index])
        self.image = self.make_backpack_image()