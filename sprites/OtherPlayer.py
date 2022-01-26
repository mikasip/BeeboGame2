from settings import PLAYER_HIT_RECT, LIGHTGREY, BODY_IMAGES, EYE_IMAGES, HAIR_IMAGES
from helpers import rotate, angle_between, make_hp_bar, resource_path
from SpriteSheet import SpriteSheet
import pygame as pg
from os import path

vec = pg.math.Vector2

class OtherPlayer(pg.sprite.Sprite):
    def __init__(self, game, x, y, id):
        self.ready = False
        pg.sprite.Sprite.__init__(self, game.other_players)
        self.id = id
        self.game = game
        self.pos = vec(x, y)
        self.way = vec(0,1)
        self.image = game.hero_img_standing
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.current_image = self.image
        self.image_index = 0
        self.weapon = None
        self.is_killed = False
        self.hp_bar_img_bg = pg.Surface((50, 8))
        self.hp_bar_img_bg.fill(LIGHTGREY)
        self.hp_bar = None
        self.hp_bar_rect = self.hp_bar_img_bg.get_rect(left = (self.rect.width - 50)/2, top = (self.rect.height - self.hit_rect.height)/2 - 10)
        self.body = BODY_IMAGES[1]
        self.eyes = EYE_IMAGES[1]
        self.hair = HAIR_IMAGES[1]
        self.feet = "black"
        self.hands = ""
        self.hit_points = 60
        self.max_hit_points = 60
        self.img_standing = None
        self.img_walking1 = None
        self.img_walking2 = None
        self.hit_frames = None
        self.sprite_sheet:SpriteSheet = SpriteSheet()
        self.update_images()
        self.update_hp_bar()

    def update(self):
        if self.ready:
            if self.is_killed:
                self.kill()
                return
            angle = angle_between(vec(1,0), self.way)
            self.current_image = self.sprite_sheet.get_image(self.image_index*150, 0, 150, 150)
            self.image, self.rect = rotate(self.current_image, angle, vec(0,0))
            self.rect.center = (self.pos.x, self.pos.y)
            rect = self.hp_bar.get_rect(left = (self.rect.width - 50)/2, top = (self.rect.height - self.hit_rect.height)/2 - 10)
            self.image.blit(self.hp_bar, rect)

    def update_images(self):
        surface = pg.Surface((1050, 150), pg.SRCALPHA)
        surface.blit(pg.image.load(resource_path('img/' + "feet_" + self.feet + '.png')).convert_alpha(), (0,0))
        if self.weapon != None:
            surface.blit(pg.image.load(resource_path('img/' + "weapon_" + self.weapon + ".png")).convert_alpha(), (0,0))
        surface.blit(pg.image.load(resource_path('img/' + self.body + ".png")).convert_alpha(), (0,0))
        if self.hands != "":
            surface.blit(pg.image.load(resource_path('img/' + "hands_" + self.hands + ".png")).convert_alpha(), (0,0))
        surface.blit(pg.image.load(resource_path('img/' + self.eyes + ".png")).convert_alpha(), (0,0))
        if self.hair != None:
            surface.blit(pg.image.load(resource_path('img/' + self.hair + ".png")).convert_alpha(), (0,0))
        surface.blit(pg.image.load(resource_path('img/' + "backpack_gray" + ".png")).convert_alpha(), (0,0))
        self.sprite_sheet.sprite_sheet = surface
    
    def update_hp_bar(self):
        self.hp_bar = self.hp_bar_img_bg.copy()
        hp = make_hp_bar(48, 6, self.hit_points, self.max_hit_points)
        hp_rect = hp.get_rect(top = 1, left = 1)
        self.hp_bar.blit(hp, hp_rect)
    
