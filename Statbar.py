# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 18:35:09 2019

@author: Mika Sipilä
"""

import pygame as pg
from settings import *
from helpers import *

class Statbar:
    def __init__(self, player):
        self.player = player
        self.bgsurface = pg.Surface((WIDTH,30))
        self.bgsurface.fill(LIGHTGREY)
        self.font = BODY_FONT
        self.hp_font = BODY_FONT_SMALL
        hp_bar_img = pg.Surface((200, 24))
        hp_bar_rect = hp_bar_img.get_rect(left = 20, top = 2)
        line = pg.Surface((200, 2))
        line_rect1 = line.get_rect()
        line_rect2 = line.get_rect(left = 0, top = 22)
        line2 = pg.Surface((2, 26))
        line2_rect1 = line.get_rect()
        line2_rect2 = line.get_rect(left = 198, top = 0)
        line2.fill(BLACK)
        line.fill(BLACK)
        line3 = pg.Surface((WIDTH, 2))
        line3.fill(BLACK)
        line3_rect = line3.get_rect(left = 0, top = 28)
        hp_bar_img.blit(line, line_rect1)
        hp_bar_img.blit(line, line_rect2)
        hp_bar_img.blit(line2, line2_rect1)
        hp_bar_img.blit(line2, line2_rect2)
        self.bgsurface.blit(line3, line3_rect)
        self.bgsurface.blit(hp_bar_img, hp_bar_rect)
        self.image = self.draw_statbar()
        self.rect = self.image.get_rect()
        
    def draw_statbar(self):
        surface = self.bgsurface.copy()
        gold_text_img = self.font.render(str(self.player.gold), True, BLACK)
        gold_text_rect = gold_text_img.get_rect()
        gold_text_rect2 = gold_text_img.get_rect(left = WIDTH - gold_text_rect.width - 20, top = 4)
        surface.blit(gold_text_img, gold_text_rect2)
        gold_icon_rect = self.player.game.gold_img.get_rect(left = WIDTH - 20 + 3, top = 4)
        surface.blit(self.player.game.gold_img, gold_icon_rect)
        strength_rect = STRENGHT_IMG.get_rect(left = WIDTH - 220, top = 4)
        surface.blit(STRENGHT_IMG, strength_rect)
        strength_amount_img = self.font.render(str(self.player.total_strength), True, BLACK)
        strength_amount_rect = strength_amount_img.get_rect(left = WIDTH - 220 + 18, top = 4)
        surface.blit(strength_amount_img, strength_amount_rect)
        agility_rect = AGILITY_IMG.get_rect(left = WIDTH - 180, top = 4)
        surface.blit(AGILITY_IMG, agility_rect)
        agility_amount_img = self.font.render(str(self.player.total_agility), True, BLACK)
        agility_amount_rect = agility_amount_img.get_rect(left = WIDTH - 180 + 18, top = 4)
        surface.blit(agility_amount_img, agility_amount_rect)
        fortune_rect = FORTUNE_IMG.get_rect(left = WIDTH - 140, top = 4)
        surface.blit(FORTUNE_IMG, fortune_rect)
        fortune_amount_img = self.font.render(str(self.player.total_fortune), True, BLACK)
        fortune_amount_rect = fortune_amount_img.get_rect(left = WIDTH - 140 + 18, top = 4)
        surface.blit(fortune_amount_img, fortune_amount_rect)
        hp_bar = make_hp_bar(196, 20, self.player.hit_points, self.player.max_hit_points)
        hp_bar_rect = hp_bar.get_rect(left=22, top=4)
        hp_text = self.hp_font.render(str(self.player.hit_points) + " / " + str(self.player.max_hit_points), True, WHITE)
        hp_text_rect = hp_text.get_rect(top = (20 - hp_text.get_height())/2 + 4, left = (196 - hp_text.get_width())/2 + 20)
        surface.blit(hp_bar, hp_bar_rect)
        surface.blit(hp_text, hp_text_rect)
        lvl_text = self.hp_font.render("Lvl. " + str(self.player.level), True, BLACK)
        lvl_rect = lvl_text.get_rect(left = 230, top = 2)
        exp_text = self.hp_font.render(str(self.player.exp) + " / " + str(self.player.next_lvl_exp), True, BLACK)
        exp_rect = lvl_text.get_rect(left = 230, top = 4 + lvl_rect.height)
        surface.blit(lvl_text, lvl_rect)
        surface.blit(exp_text, exp_rect)
        return surface
    
    def update(self):
        self.image = self.draw_statbar()
        
        