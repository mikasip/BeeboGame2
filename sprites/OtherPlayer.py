from settings import PLAYER_HIT_RECT, LIGHTGREY
from helpers import rotate, angle_between, make_hp_bar, resource_path
from SpriteSheet import SpriteSheet
import pygame as pg
from os import path

vec = pg.math.Vector2

class OtherPlayer(pg.sprite.Sprite):
    def __init__(self, game, x, y, id):
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
        hit_frames = SpriteSheet(resource_path('img/' + 'hero_hit' + '.png'))
        self.original_images = [game.hero_img_standing, game.hero_img_walking1, game.hero_img_walking2, hit_frames.get_image(0 * 100, 0, 100, 100), hit_frames.get_image(1 * 100, 0, 100, 100), hit_frames.get_image(2 * 100, 0, 100, 100), hit_frames.get_image(3 * 100, 0, 100, 100)]
        self.images = self.original_images
        self.is_killed = False
        self.hp_bar_img_bg = pg.Surface((50, 8))
        self.hp_bar_img_bg.fill(LIGHTGREY)
        self.hp_bar_rect = self.hp_bar_img_bg.get_rect(left = (self.rect.width - 50)/2, top = (self.rect.height - self.hit_rect.height)/2 - 10)

    def update(self):
        if self.is_killed:
            self.kill()
            return
        angle = angle_between(vec(1,0), self.way)
        self.current_image = self.images[self.image_index]
        self.image, self.rect = rotate(self.current_image, angle, vec(0,0))
        self.rect.center = (self.pos.x, self.pos.y)
        rect = self.hp_bar.get_rect(left = (self.rect.width - 50)/2, top = (self.rect.height - self.hit_rect.height)/2 - 10)
        self.image.blit(self.hp_bar, rect)

    def update_images(self):
        if self.weapon != None:
            hit_frames = SpriteSheet(resource_path('img/' + 'hero_hit_with_' + self.weapon + '.png'))
            self.images = [pg.image.load(resource_path('img/' + 'standing_hero_with_' + self.weapon + '.png')).convert_alpha(),
                pg.image.load(resource_path('img/' + 'standing_hero_with_' + self.weapon + '.png')).convert_alpha(),
                pg.image.load(resource_path('img/' + 'walking_hero1_with_' + self.weapon + '.png')).convert_alpha(),
                pg.image.load(resource_path('img/' + 'walking_hero2_with_' + self.weapon + '.png')).convert_alpha(),
                hit_frames.get_image(0 * 100, 0, 100, 100),
                hit_frames.get_image(1 * 100, 0, 100, 100), 
                hit_frames.get_image(2 * 100, 0, 100, 100), 
                hit_frames.get_image(3 * 100, 0, 100, 100)
            ]
        else:
            self.images = self.original_images
    
    def update_hp_bar(self):
        self.hp_bar = self.hp_bar_img_bg.copy()
        hp = make_hp_bar(48, 6, self.hit_points, self.max_hit_points)
        hp_rect = hp.get_rect(top = 1, left = 1)
        self.hp_bar.blit(hp, hp_rect)

    
