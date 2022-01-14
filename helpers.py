# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 19:32:40 2019

@author: Mika Sipilä
"""

import pygame as pg
from settings import *
import numpy as np
import math
vec = pg.math.Vector2
import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):

    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    atanA = np.arctan2(v1_u.x, v1_u.y)
    atanB = np.arctan2(v2_u.x, v2_u.y)
    radians = atanA - atanB
    return(radians * (180/math.pi))
    
def rotate(surface, angle, offset):
    rotated_image = pg.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(top=rotated_offset.y, left=rotated_offset.x)
    return rotated_image, rect  # Return the rotated image and shifted rect.

def create_item_with_rect(image, width, height, pos_x, pos_y, active, amount = 1):
    image_to_return = image        
    image_rect = image.get_rect() 
    image_pos_x = (width - image_rect.width) / 2
    image_pos_y = (height - image_rect.height) / 2
    image_to_return = pg.Surface((width, height), pg.SRCALPHA)
    if active:
        image_to_return.fill(LIGHTGREY)
    image_rect = image.get_rect(left = image_pos_x, top = image_pos_y)
    image_to_return.blit(image, image_rect)
    image_rect = image_to_return.get_rect(left = pos_x, top = pos_y)
    if amount > 1:
        text = BODY_FONT_SMALL.render(str(amount), True, BLACK)
        image_to_return.blit(text, text.get_rect(left = width - 20, top = height - 20))
    return image_to_return, image_rect

def move_in_matrix(cols, rows, active_index, max_index, key):
    new_index = active_index
    if max_index > 0:
        active_col = (active_index + 1) % cols
        active_row = math.floor(active_index / cols) + 1
        if key == pg.K_UP:
            if active_index == max_index:
                new_index -= 1
            elif active_row > 1:
                new_index -= cols
        if key == pg.K_DOWN:
            if active_row < rows:
                if active_index + cols >= max_index:
                    new_index = max_index
                else:
                    new_index += cols
            elif active_row == rows:
                new_index = max_index
        if key == pg.K_RIGHT:
            if active_index < max_index:
                new_index += 1
        if key == pg.K_LEFT:
            if active_index > 0:
                new_index -= 1
    return new_index

def distance(pos1, pos2):
    return math.sqrt(math.pow((pos1.x - pos2.x),2) + math.pow((pos1.y - pos2.y),2))

def way_to_pos(pos1, pos2):
    way = vec(0,0)
    if pos1.x < pos2.x - 5:
        way.x = 1
    elif pos1.x > pos2.x + 5:
        way.x = -1
    if pos1.y < pos2.y - 5:
        way.y = 1
    elif pos1.y > pos2.y + 5:
        way.y = -1
    return way

def create_dialog(image, bg, size, text1, text2, active_index, font):
     bg_surface = pg.Surface(size)
     bg_surface.blit(bg, (0,0))
     surface = pg.transform.scale(bg_surface, (360, 110))
     text1_image = font.render(text1, True, BLACK)
     image1, rect1 = create_item_with_rect(text1_image, 150, 50, 30, 30, (active_index == 0))
     text2_image = font.render(text2, True, BLACK)
     image2, rect2 = create_item_with_rect(text2_image, 150, 50, 180, 30, (active_index == 1))
     surface.blit(image1, rect1)
     surface.blit(image2, rect2)
     surface_rect = surface.get_rect(top = (HEIGHT - 110) / 2, left = (WIDTH - 360) / 2)
     return surface, surface_rect
 
def change_alpha(img, alpha=255):
    chan = pg.surfarray.pixels_alpha(img)
    chan2 = np.minimum(chan, np.ones(chan.shape, dtype=chan.dtype)) * alpha
    np.copyto(chan, chan2)
    del chan
    
def make_hp_bar(width, height, hp, max_hp):
    color = GREEN
    hp_left = float(hp/max_hp)
    length = round(hp_left * width)
    if hp_left < 0.66:
        if hp_left < 0.33:
            color = RED
        else:
            color = YELLOW
    if length <= 0:
        return pg.Surface((1, height))
    hp_bar = pg.Surface((length, height))
    hp_bar.fill(color)
    return hp_bar

def blit_text(surface, text, pos, width, heigth, font, color=pg.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width = pos[0] + width
    max_heigth = pos[1] + heigth
    x, y = pos
    line_end_x = x
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
            line_end_x = x
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
    return (y, line_end_x)
    