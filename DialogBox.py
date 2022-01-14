from settings import *
import pygame as pg

class GuiGrid:
    def __init__(self, width_multiplier, height_multiplier, pos, ncol, nrow, margin, space, items):
        self.width = width_multiplier * WIDTH
        self.height = height_multiplier * HEIGHT
        self.ncol = ncol
        self.nrow = nrow
        self.selected_item = None

        if pos == "center":
            return
        elif pos == "topright":
            return
        elif pos == "topleft":
            return
        elif pos == "bottomright":
            return
        elif pos == "bottomleft":
            return
        
        for item in items:
            if item.action != None and self.selected_item == None:
                self.selected_item = item

                
        


class DialogItem:
    def __init__(self, text, action):
        self.text = text


class GuiItem:
    def __init__(self, width_multiplier, height_multiplier, margin,  text = None, image = None):
        self.width = WIDTH * width_multiplier
        self.height = HEIGHT * height_multiplier
        self.text = text
        self.image = image

    def blit(self, container, pos):

        if pos == "center":
            return
        elif pos == "topright":
            return
        elif pos == "topleft":
            return
        elif pos == "bottomright":
            return
        elif pos == "bottomleft":
            return
