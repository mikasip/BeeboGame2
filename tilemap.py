# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 16:22:10 2019

@author: Mika Sipilä
"""

import pygame as pg
from settings import *
vec = pg.math.Vector2
import pytmx

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_hit_rect_center(one, two):
    rect = pg.Rect(0,0,1,1)
    rect.center = two.rect.center
    return one.hit_rect.colliderect(rect)

class Map:
    def __init__(self, filenames_under, filenames_over, starting_pos, indoor):
        self.layers_under = []
        self.layers_over = []
        self.doorways = {}
        for filename in filenames_under:
            with open(filename, 'rt') as f:
                data = []
                for line in f:
                    data.append(line.strip())
                self.layers_under.append(data)
        for filename in filenames_over:
            with open(filename, 'rt') as f:
                data = []
                for line in f:
                    data.append(line.strip())
                self.layers_over.append(data)
        self.indoor = indoor            
        self.tilewidth = len(self.layers_under[0][0])
        self.tileheight = len(self.layers_under[0])
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        self.starting_pos = starting_pos

class TiledMap:
    def __init__(self, filename, name):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.name = name
        self.needs_update = False

    def render(self, surface_under, surface_over):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if layer.name[0] == "U":
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid, in layer:
                        tile = ti(gid)
                        if tile:
                            surface_under.blit(tile, (x * self.tmxdata.tilewidth + layer.offsetx,
                                                y * self.tmxdata.tileheight + layer.offsety))
            if layer.name[0] == "T":
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid, in layer:
                        tile = ti(gid)
                        if tile:
                            surface_over.blit(tile, (x * self.tmxdata.tilewidth + layer.offsetx,
                                                y * self.tmxdata.tileheight + layer.offsety))
    def make_map(self):
        temp_surface_under = pg.Surface((self.width, self.height))
        temp_surface_over = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.render(temp_surface_under, temp_surface_over)
        return temp_surface_under, temp_surface_over

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.center[0] + int(WIDTH / 2)
        y = -target.rect.center[1] + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        if self.width < WIDTH:
            x = (WIDTH - self.width)/2
        if self.height < HEIGHT:
            y = (HEIGHT - self.height)/2
        self.camera = pg.Rect(x, y, self.width, self.height)