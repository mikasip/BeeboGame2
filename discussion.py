# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 10:59:02 2019

@author: Mika Sipilä
"""

import pygame as pg
from os import path
from settings import *
from helpers import *
from tilemap import *
from quests import *
from sprites.obstacles import *
from Quest import *
import math

class DiscussionHandler(object):
    def __init__(self):
        self.discussion_open = False
        self.comment = None
    
    def set_comment(self, comment):
        self.comment = comment
        if comment != None:
            self.discussion_open = True
    
    def space_pressed(self, player):
        self.comment.space_pressed(self, player)

class Comment(object):
    def __init__(self, game, comment, beebo):
        self.background = pg.image.load(resource_path('img/' + DISCUSSION_BOX)).convert_alpha()
        self.rect = self.background.get_rect()
        self.beebo = beebo
        self.comment = comment
        self.font = BODY_FONT
        self.image = self.make_comment_box_image()
        self.pos_x = WIDTH - self.rect.width
        self.pos_y = HEIGHT - self.rect.height
        self.pos = (self.pos_x, self.pos_y)
        self.game = game
    
    def make_comment_box_image(self):
        image = pg.Surface(self.rect.size)
        image.blit(self.background, (0,0))
        comment_image = self.font.render(self.comment, True, BLACK)
        comment_rect = comment_image.get_rect(left = 50, top = 50)
        image.blit(comment_image, comment_rect)
        return image
    
    def space_pressed(self, handler):
        handler.discussion_open = False
        self.game.player.wait = False
    
class Store(object):
    def __init__(self, game, beebo, items, head_line):
        self.background = game.menu_box_img
        self.rect = self.background.get_rect()
        self.beebo = beebo
        self.font = HEADER_FONT
        self.stat_font = BODY_FONT
        self.pos = (0, 0)
        self.items = items
        self.head_line = head_line
        self.active_index = 0
        self.purchase_index_active = 0
        self.purchase_dialog_open = False
        self.rows = 1
        self.can_change = True
        self.game = game
        if len(items) >= math.floor((WIDTH - MARGIN*2) / 70):
            self.cols = math.floor((WIDTH - MARGIN*2) / 70)
        else:
            self.cols = len(items)
        self.image = self.make_store_box_image()
        
    def make_store_box_image(self):
        image = pg.Surface(self.rect.size)
        image.blit(self.background, (0,0))
        head_line_image = self.font.render(self.head_line, True, BLACK)
        head_line_rect = head_line_image.get_rect(left = MARGIN, top = MARGIN)
        image.blit(head_line_image, head_line_rect)
        next_item_pos = vec(MARGIN, 50 + MARGIN)
        self.rows = 1
        for i, item in enumerate(self.items):
            bg_image, bg_image_rect = create_item_with_rect(item.image, 70, 70, next_item_pos.x, next_item_pos.y, (self.active_index == i))
            image.blit(bg_image, bg_image_rect)
            if next_item_pos.x + 170 >= WIDTH:
                next_item_pos.x = MARGIN
                next_item_pos.y += 70
                self.rows += 1
            else:
                next_item_pos.x += 70
            if next_item_pos.y + 170 >= HEIGHT:
                break
        y = 0
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
            for i, stat in enumerate(self.items[self.active_index].shop_stats):
                y, line_end_x = blit_text(stat_bg, stat, (10, y), stat_w - 20, stat_h - 20, self.stat_font)
                if len(self.items[self.active_index].shop_stats) - 1 == i:
                    price_img = self.game.gold_img
                    price_rect = price_img.get_rect(left = line_end_x + 5, top = y - 18)
                    stat_bg.blit(price_img, price_rect)
            stat_rect = stat_bg.get_rect(left = WIDTH - stat_w - MARGIN_LEFT, top = HEIGHT - stat_h - MARGIN_BOT)
            image.blit(stat_bg, stat_rect)
        quit_img = self.stat_font.render("QUIT", True, BLACK)
        bg_image, bg_image_rect = create_item_with_rect(quit_img, 70, 40, MARGIN_LEFT, HEIGHT - MARGIN_BOT - 40, (self.active_index == len(self.items)))
        image.blit(bg_image, bg_image_rect)
        gold_text_img = self.stat_font.render("Your gold: " + str(self.game.player.gold), True, BLACK)
        gold_text_rect = gold_text_img.get_rect()
        gold_text_rect2 = gold_text_img.get_rect(left = WIDTH - gold_text_rect.width - MARGIN_LEFT - 25, top = MARGIN_BOT)
        image.blit(gold_text_img, gold_text_rect2)
        gold_icon_rect = self.game.gold_img.get_rect(left = WIDTH - MARGIN_LEFT - 22, top = MARGIN_BOT)
        image.blit(self.game.gold_img, gold_icon_rect)
        if self.purchase_dialog_open:
            self.create_purchase_dialog(image)
            
        return image
    
    def change_active(self, key):
        if self.purchase_dialog_open:
            if key == pg.K_RIGHT:
                self.purchase_index_active = 1
            if key == pg.K_LEFT:
                self.purchase_index_active = 0
        else: 
            self.active_index = move_in_matrix(self.cols, self.rows, self.active_index, len(self.items), key)
        self.image = self.make_store_box_image()
        
        
    def space_pressed(self, handler):
        if self.active_index == len(self.items):
            handler.discussion_open = False
            self.game.player.wait = False
        else:
            requirements_met = None
            if len(self.items[self.active_index].requirements) > 0:
                requirements_met = True
            for req in self.items[self.active_index].requirements:
                items = list(filter(lambda item: item.name == req["name"], self.game.player.backpack.items))
                
                if len(items) > 0 and items[0].type == "other_item":
                    if items[0].amount < req["count"]:
                        requirements_met = False 
                elif len(items) < req["count"]:
                    requirements_met = False
            
            if self.game.player.level < self.items[self.active_index].level:
                message = "Level needed: " + str(self.items[self.active_index].level)
                self.game.error_message.create_error_dialog(message)
            elif requirements_met == False:
                message = "Ingredients missing"
                self.game.error_message.create_error_dialog(message)
            elif requirements_met == None and self.game.player.gold < self.items[self.active_index].price:
                message = "Not enough gold"
                self.game.error_message.create_error_dialog(message)
            elif self.items[self.active_index].type == "spell" and self.items[self.active_index].id in self.game.player.spells:
                message = "Spell already learned"
                self.game.error_message.create_error_dialog(message)
            elif self.items[self.active_index].type == "spell" and len(self.game.player.spells) >= self.game.player.max_spells:
                next_level = 0
                for level in MAX_SPELLS_PER_LEVEL.keys():
                    if self.game.player.level < level:
                        next_level = level
                        break
                message = "You have maximum amount of spells, you can get another spell at level " + str(next_level)
                self.game.error_message.create_error_dialog(message)
            elif self.items[self.active_index].type == "spell"  and self.game.player.strength < self.items[self.active_index].strength_needed:
                message = "Not enough strength"
                self.game.error_message.create_error_dialog(message)
            elif self.items[self.active_index].type == "spell" and self.game.player.agility < self.items[self.active_index].agility_needed:
                message = "Not enough agility"
                self.game.error_message.create_error_dialog(message)
            elif self.items[self.active_index].type == "spell" and self.game.player.fortune < self.items[self.active_index].fortune_needed:
                message = "Not enough fortune"
                self.game.error_message.create_error_dialog(message)
            elif not self.purchase_dialog_open:
                self.create_purchase_dialog(self.image)
                self.purchase_dialog_open = True
            else:
                if self.purchase_dialog_open:
                    self.purchase_dialog_open = False
                    if self.purchase_index_active == 1:
                        self.image = self.make_store_box_image()
                    if self.purchase_index_active == 0:
                        self.purchase_item()

    def create_purchase_dialog(self, image):
        
        bg_surface = pg.Surface(self.rect.size)
        bg_surface.blit(self.background, (0,0))
        purchase_surface = pg.transform.scale(bg_surface, (360, 110))
        purchase_text = self.font.render("Purchase", True, BLACK)
        purchase_image, purchase_rect = create_item_with_rect(purchase_text, 150, 50, 30, 30, (self.purchase_index_active == 0))
        cancel_text = self.font.render("Cancel", True, BLACK)
        cancel_image, cancel_rect = create_item_with_rect(cancel_text, 150, 50, 180, 30, (self.purchase_index_active == 1))
        purchase_surface.blit(purchase_image, purchase_rect)
        purchase_surface.blit(cancel_image, cancel_rect)
        purchase_surface_rect = purchase_surface.get_rect(top = (HEIGHT - 110) / 2, left = (WIDTH - 360) / 2)
        image.blit(purchase_surface, purchase_surface_rect)
        
    def purchase_item(self):
        if self.items[self.active_index].type == "spell":
            self.game.player.spells.append(self.items[self.active_index].id)
            self.game.player.make_spells()
            self.game.player.chance_gold_amount(-self.items[self.active_index].price)
            self.image = self.make_store_box_image()
            self.game.player.backpack.image = self.game.player.backpack.make_backpack_image()
            return
        added = self.game.player.add_to_backpack(self.items[self.active_index])
        if added:
            self.game.player.chance_gold_amount(-self.items[self.active_index].price)
            for req in self.items[self.active_index].requirements:
                    items = list(filter(lambda item: item.name == req["name"], self.game.player.backpack.items))
                    if len(items) > 0 and items[0].type == "other_item":
                        self.game.player.change_item_count(items[0], -req["count"])
                    else:
                        for i in range(0, req["count"]):
                            self.game.player.backpack.items.remove(items[i])
        self.image = self.make_store_box_image()
        self.game.player.backpack.image = self.game.player.backpack.make_backpack_image()
        return

class QuestDialog(object):
    def __init__(self, game, host, quest):
        self.game = game
        self.host = host
        self.quest = quest
        self.background = pg.image.load(resource_path('img/' + DISCUSSION_BOX)).convert_alpha()
        self.background = pg.transform.scale(self.background, (int(WIDTH), int(HEIGHT/2)))
        self.rect = self.background.get_rect()
        self.font = BODY_FONT
        self.pos_x = WIDTH - self.rect.width
        self.pos_y = HEIGHT - self.rect.height
        self.pos = (self.pos_x, self.pos_y)
        self.active_index = 0
        self.state = 0
        self.image = self.make_quest_dialog()

    
    def make_quest_dialog(self):
        image = pg.Surface(self.rect.size)
        image.blit(self.background, (0,0))
        dialog = QUESTS[self.quest]['dialog']
        self.state = 0
        if self.quest in self.game.player.active_quests:
            dialog = QUESTS[self.quest]['not_done_dialog']
            self.state = 1
            completed = False
            mission = QUESTS[self.quest]['mission']
            if mission['type'] == "collect":
                for i, item in enumerate(mission['item']):
                    items = list(filter(lambda x: x.name == item, self.game.player.backpack.items))
                    if len(items) > 0:
                        if items[0].amount >= mission['amount'][i]:
                            completed = True
            elif mission['type'] == "bring":
                done_count = 0
                for mob in self.game.current_map.mobs:
                    if mob.name == mission['mob']:
                        if mission['start_x'] <= mob.rect.centerx and mission['end_x'] >= mob.rect.centerx and mission['start_y'] <= mob.rect.centery and mission['end_y'] >= mob.rect.centery:
                            done_count += 1
                if done_count >= mission['amount']:
                    completed = True
            if completed:
                dialog = QUESTS[self.quest]['done_dialog']
                self.state = 2

        blit_text(image, str(dialog), (30,30), image.get_rect().width - 30, 200, self.font, BLACK)
        accept_text = self.font.render("Accept", True, BLACK)
        cancel_string = "Cancel"
        if self.state == 1:
            cancel_string = "Ok"
            self.active_index = 0
        accept_image, accept_rect = create_item_with_rect(accept_text, 100, 30, (image.get_rect().width)/2 - 100 - 15, int(HEIGHT/2) - 50, (self.active_index == 0))
        cancel_text = self.font.render(cancel_string, True, BLACK)
        cancel_image, cancel_rect = create_item_with_rect(cancel_text, 100, 30, (image.get_rect().width)/2 + 15, int(HEIGHT/2) - 50, (self.active_index == 1))
        if self.state != 1:
            image.blit(accept_image, accept_rect)
        image.blit(cancel_image, cancel_rect)

        return image
    
    def change_active(self, key):
        if self.state != 1:
            if key == pg.K_RIGHT:
                self.active_index = 1
            if key == pg.K_LEFT:
                self.active_index = 0
            self.image = self.make_quest_dialog()
    
    def space_pressed(self, handler):
        if self.active_index == 0:
            if self.state == 0:
                self.game.player.quests.add_quest(self.quest)
                self.game.player.active_quests.append(self.quest)
            elif self.state == 2:
                if not self.game.player.reward(QUESTS[self.quest]['reward']):
                    return
                self.game.player.quests.remove_quest(self.quest)
                self.game.player.active_quests.remove(self.quest)

                if QUESTS[self.quest]['only_once'] == 'true':
                    self.host.quest = None
                    self.game.player.completed_quests.append(self.quest)
                if QUESTS[self.quest]['mission']['type'] == "collect":
                    for i, item in enumerate(QUESTS[self.quest]['mission']['item']):
                        backpack_item = list(filter(lambda x: x.name == item, self.game.player.backpack.items))[0]
                        amount = QUESTS[self.quest]['mission']['amount'][i]
                        self.game.player.change_item_count(backpack_item, -amount)
                if QUESTS[self.quest]['mission']['type'] == "bring":
                    self.game.current_map.needs_update = True
        self.image = self.make_quest_dialog()
        self.game.player.quests.update_items()
        handler.discussion_open = False
        if self.game.player.open_dialog != self.game.player.attribute_selection:
            self.game.player.wait = False