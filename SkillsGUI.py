
from math import pi
import pygame as pg
from settings import *
from helpers import *

class SkillsGUI:
    def __init__(self, player):
        self.player = player
        self.width, self.height = (400, 50)
        self.bgsurface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        #self.bgsurface.fill(LIGHTGREY)
        self.font = BODY_FONT
        self.hp_font = BODY_FONT_SMALL
        pg.draw.circle(self.bgsurface, LIGHTERGREY, (25,25), 20)
        self.bgsurface.blit(pg.image.load(resource_path('img/' + 'steel_sword_drop.png')).convert_alpha(), (9, 9))
        q_img = self.hp_font.render("Q", True, BLACK)
        self.bgsurface.blit(q_img, (30,10))
        pg.draw.arc(self.bgsurface, (0,0,0), [5,5,40,40], 0, 2*pi, 2)
        #pg.draw.line(self.bgsurface, BLACK, [0, 0], [self.width,0], 2)
        #pg.draw.line(self.bgsurface, BLACK, [self.width - 2, 0], [self.width - 2, self.height], 2)
        self.image = self.bgsurface
        self.transparent_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - self.height
        
    def update_cooldowns(self, player):
        surface = self.bgsurface.copy()
        transparent_surface = self.transparent_surface.copy()
        if player.last_hit > 0:
            cooldown = player.last_hit/(player.hit_cooldown*player.attack_speed)
            cooldown_as_rad = cooldown*2*pi
            pg.draw.arc(transparent_surface, (0,0,0,100), [5,5,40,40], pi/2, pi/2 + cooldown_as_rad, 20)
        padding = 55
        for skill in player.spell_objs:
            cooldown = skill.current_cooldown/(skill.cooldown*player.attack_speed)
            if player.spell_cast_timer > 0 and skill.current_cooldown < player.spell_cast_timer:
                cooldown = player.spell_cast_timer/(player.spell_cast_cooldown*player.attack_speed)
            if cooldown > 0:
                cooldown_as_rad = cooldown*2*pi
                pg.draw.arc(transparent_surface, (0,0,0,100), [padding,5,40,40], pi/2, pi/2 + cooldown_as_rad, 20)
            padding += 50
        
        surface.blit(transparent_surface, (0,0))
        self.image = surface

    
    def update_skills(self, player):
        surface = self.bgsurface.copy()
        keys = ["W", "E", "R", "A", "S", "D"]
        padding = 75
        for i, skill in enumerate(player.spells):
            pg.draw.circle(surface, LIGHTERGREY, (padding,25), 20)
            surface.blit(pg.image.load(resource_path('img/' + HIT_SPELLS[skill]["file"]) + ".png").convert_alpha(), (padding - 25 + 9, 9))
            q_img = self.hp_font.render(keys[i], True, BLACK)
            surface.blit(q_img, (padding + 5,10))
            pg.draw.arc(surface, (0,0,0), [padding - 20, 5,40,40], 0, 2*pi, 2)
            padding += 50
        self.bgsurface = surface
        self.image = self.bgsurface
        keys = ["Z", "X"]
        for i, item in enumerate(player.quick_use):
            pg.draw.circle(surface, LIGHTERGREY, (padding,25), 20)
            surface.blit(pg.image.load(resource_path('img/' + item.file) + ".png").convert_alpha(), (padding - 25 + 9, 9))
            q_img = self.hp_font.render(keys[i], True, BLACK)
            surface.blit(q_img, (padding + 5,10))
            pg.draw.arc(surface, (0,0,0), [padding - 20, 5,40,40], 0, 2*pi, 2)
            padding += 50
