# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 19:33:46 2019

@author: Mika Sipilä
"""

import pygame as pg
from settings import *
from helpers import *

class ErrorMessageHandler(object):
    def __init__(self, bg):
        self.open = False
        self.background = pg.transform.scale(bg, (360, 110))
        self.image = self.background
        self.rect = self.background.get_rect(top = (HEIGHT - 110) / 2, left = (WIDTH - 360) / 2)
        self.font = BODY_FONT
    
    def create_error_dialog(self, message):
        image = pg.Surface(self.rect.size)
        image.blit(self.background, (0,0))
        blit_text(image, message, (40,40), 300, 100, self.font)
        self.image = image
        self.open = True