from settings import *
from helpers import *
import pygame as pg
from os import path
from sprites.Player import *

class GuiItem:
    def __init__(self, width, height, image):
        self.width = width
        self.height = height
        self.image = image
    
    def blit_item(self, container, pos):
        x = pos[0]
        y = pos[1]
        if pos == "center":
            x = (WIDTH-self.width)/2
            y = (HEIGHT-self.height)/2
        elif pos == "bottomright":
            x = WIDTH-self.width
            y = HEIGHT-self.height
        elif pos == "bottomleft":
            x = 0
            y = HEIGHT-self.height
        elif pos == "topleft":
            x = WIDTH-self.width
            y = 0
        elif pos == "topright":
            x = 0
            y = 0

        container.blit(self.image, (x,y))

class GuiText(GuiItem):
    def __init__(self, text, size, color, width, height):
        image = pg.font.SysFont('calibri', size).render(text, True, color)
        text_width = image.get_rect().width
        if text_width >= width:
            image = pg.Surface((width, height), pg.SRCALPHA)
            image.convert_alpha()
            blit_text(image, text, (0,0), width, height, pg.font.SysFont('calibri', size))
        else:
            width = text_width
        GuiItem.__init__(self,width,height,image)

class GuiObject:
    def __init__(self, text, action):
        self.text = text
        self.action = action

class GuiGrid(GuiItem):
    def __init__(self, width_multiplier, height_multiplier, title, cancel_text, ok_text, ncol, nrow, margin, items, close_action = None, space = 30):
        self.width = width_multiplier * WIDTH
        self.height = height_multiplier * HEIGHT
        self.ncol = ncol
        self.nrow = nrow
        self.selected_item = None
        self.title = title
        self.cancel_text = cancel_text
        self.ok_text = ok_text
        self.margin = margin
        self.items = items
        self.active_index = 0
        self.close_action = close_action
        self.img_folder = path.join(path.dirname(__file__), 'img')
        self.menu_box_img = pg.image.load(resource_path('img/' + MENU_BOX)).convert_alpha()
        self.menu_box_img = pg.transform.scale(self.menu_box_img, (round(self.width), round(self.height)))
        self.image = None
        self.space = space
        self.update_image()
        self.image_rect = self.image.get_rect(left = (WIDTH - self.width)/2, top = (HEIGHT - self.height)/2)
        GuiItem.__init__(self, self.width, self.height, self.image)

    def get_image(self):
        return self.image
    
    def get_rect(self):
        return self.image_rect
        
    def update_image(self):
        self.image = pg.Surface((self.width, self.height))
        self.image.blit(self.menu_box_img, (0,0))
        title_size = 32
        text_size = 20

        if self.title != None:
            title = GuiText(self.title, title_size, BLACK, 0.8*self.width, 0.3*self.height)
            title.blit_item(self.image, ((self.width - title.width)/2, self.margin))
        else:
            title_size = 0
                
        if self.cancel_text != None:
            col = BLACK
            if self.active_index == len(self.items):
                col = RED
            cancel = GuiText(self.cancel_text, text_size, col, 0.35*self.width, 0.35*self.height)
            cancel.blit_item(self.image, (self.width - cancel.width - self.margin, self.height - self.margin))

        #if self.ok_text != None:
        #    ok = GuiText(self.ok_text, text_size, BLACK, 0.35*self.width, 0.35*self.height)
        #    ok.blit_item(self.image, (self.margin, self.height - self.margin))

        col_width = (self.width - 2*self.margin)/self.ncol
        row_height = (self.height - 2*self.margin - title_size - text_size)/self.nrow
        
        gui_items = []
        for i, item in enumerate(self.items):
            col = BLACK
            if i == self.active_index:
                col = RED
            gui_items.append(GuiText(item.text, 20, col, col_width, row_height))
    

        index = 0
        for i in range(self.nrow):
            for j in range(self.ncol):
                if index >= len(gui_items):
                    break
                gui_items[index].blit_item(self.image, (self.margin + (j)*col_width  + (col_width - gui_items[index].width)/2, self.margin + title_size + i*row_height + self.space))        
                index += 1

    def handle_key_pressed(self, key):
        nitems = len(self.items) - 1
        if self.cancel_text != None:
            nitems = len(self.items) 
        if key in [pg.K_UP, pg.K_DOWN]:
            self.active_index = move_in_matrix(self.ncol, self.nrow, self.active_index, nitems, key)
        elif key == pg.K_DOWN:
            self.active_index = move_in_matrix(self.ncol, self.nrow, self.active_index, nitems, key)
        elif key == pg.K_SPACE:
            if self.active_index == len(self.items) or len(self.items) == 0:
                self.close_action()
            else:
                self.items[self.active_index].action()
        self.update_image()

class CustomGuiItem:
    def make_image(self):
        raise NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))
    def space_pressed(self):
        raise NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))
    def change_active(self, key):
        raise NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))
    def get_image(self):
        raise NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))
    def get_rect(self):
        raise NotImplementedError("Class %s doesn't implement aMethod()" % (self.__class__.__name__))

class EquippedGearGui(CustomGuiItem):

    def __init__(self, background_image, player, close_action, add_to_backpack):
        self.background_image = background_image
        self.equipped_image_rect = background_image.get_rect()
        self.equipped = []
        self.player:Player = player
        self.dialog_index_active = 0
        self.unequip_dialog_open = False
        self.active_equipped_index = 8
        self.equipped_cols = 4
        self.equipped_rows = 2
        self.equipped_indicators = [0,0,0,0,0,0,0,0]
        self.equipped_image = self.make_image()
        self.close_action = close_action
        self.add_to_backpack = add_to_backpack

    def get_image(self):
        return self.equipped_image
    
    def get_rect(self):
        return self.equipped_image_rect

    def make_image(self):
        self.equipped_indicators = [0,0,0,0,0,0,0,0]
        image = pg.Surface(self.equipped_image_rect.size)
        image.blit(self.background_image, (0,0))
        head_line_image = HEADER_FONT.render("Equipped Gear", True, BLACK)
        head_line_rect = head_line_image.get_rect(left = 50, top = 50)
        image.blit(head_line_image, head_line_rect)
        next_item_pos = vec(50, 100)
        item_types = ["Helmet", "Cloak", "Weapon", "Ring", "Gloves", "Chain", "Pants", "Boots"]
        index = 0
        col_size = (WIDTH - 100) / 4
        items = []
        for i, item_type in enumerate(item_types):
            for item in self.equipped:
                if item.type == item_type.lower():
                    items.append(item)
                    self.equipped_indicators[i] = 1
            text_image = BODY_FONT_SMALL.render(item_type, True, BLACK)
            text_rect1 = text_image.get_rect()
            text_rect2 = text_image.get_rect(left = (col_size - text_rect1.width)/2 + next_item_pos.x, top = next_item_pos.y)
            image.blit(text_image, text_rect2)
            item_pos_x = (col_size - 70) / 2 + next_item_pos.x
            item_pos_y = next_item_pos.y + 20
            for item in items:
                if item.type == item_type.lower():
                    bg_image, bg_image_rect = create_item_with_rect(item.image, 70, 70, item_pos_x, item_pos_y, (self.active_equipped_index == index))
                    image.blit(bg_image, bg_image_rect)
            index += 1
            if next_item_pos.x < col_size * 3:
                next_item_pos.x += col_size
            else:
                next_item_pos.x = 50
                next_item_pos.y += 100

        padding = 0
        if self.active_equipped_index < 8:
            active_index = self.get_active_index()
            for i, stat in enumerate(items[active_index].stats):
                stat_img = BODY_FONT_SMALL.render(stat, True, BLACK)
                stat_rect = stat_img.get_rect(left = WIDTH - 200, top = HEIGHT - 150 + padding)
                image.blit(stat_img, stat_rect)
                padding += 25
        quit_img = BODY_FONT_SMALL.render("BACK", True, BLACK)
        bg_image, bg_image_rect = create_item_with_rect(quit_img, 70, 40, 40, HEIGHT - 80, (self.active_equipped_index == 8))
        image.blit(bg_image, bg_image_rect)
        gold_text_img = BODY_FONT_SMALL.render("Your gold: " + str(self.player.gold), True, BLACK)
        gold_text_rect = gold_text_img.get_rect()
        gold_text_rect2 = gold_text_img.get_rect(left = WIDTH - gold_text_rect.width - 100, top = 50)
        image.blit(gold_text_img, gold_text_rect2)
        gold_icon_rect = GOLD_IMG.get_rect(left = WIDTH - 100 + 3, top = 50)
        image.blit(GOLD_IMG, gold_icon_rect)
        if self.unequip_dialog_open:
            self.create_equip_dialog(image)
        return image

    def change_active(self,key):
        if self.unequip_dialog_open:
            if key == pg.K_RIGHT:
                self.dialog_index_active = 1
            if key == pg.K_LEFT:
                self.dialog_index_active = 0
        else:
            new_index = move_in_matrix(self.equipped_cols, self.equipped_rows, self.active_equipped_index, 8, key)
            if new_index == 8 or self.equipped_indicators[new_index] == 1:
                self.active_equipped_index = new_index
            else:
                index = 8
                if key in [pg.K_LEFT, pg.K_UP]:
                    index = self.active_equipped_index
                    for i, item_type in enumerate(["helmet", "cloak", "weapon", "ring", "gloves", "chestplate", "pants", "boots"]):
                        for item in self.equipped:
                            if item.type == item_type:
                                if self.equipped_indicators[i] == 1:
                                    if i < new_index:
                                        index = i
                else:
                    for i, item_type in enumerate(["helmet", "cloak", "weapon", "ring", "gloves", "chestplate", "pants", "boots"]):
                        for item in self.equipped:
                            if item.type == item_type:
                                if self.equipped_indicators[i] == 1:
                                    if i > new_index:
                                        index = i
                                        break
                        else:
                            continue
                        break
                self.active_equipped_index = index
        self.equipped_image = self.make_image()

    def get_active_index(self):
        active_index = 0
        for i in range(0,self.active_equipped_index):
            if self.equipped_indicators[i] == 1:
                active_index += 1
        return active_index

    def create_equip_dialog(self, image):
        surface, rect = create_dialog(image, self.background_image, self.equipped_image_rect.size, "Unequip", "Cancel", self.dialog_index_active, HEADER_FONT)
        image.blit(surface, rect)
        
    def space_pressed(self):
        if self.unequip_dialog_open:
            if self.dialog_index_active == 0:
                item_type = None
                for i, type in enumerate(["helmet", "cloak", "weapon", "ring", "gloves", "chestplate", "pants", "boots"]):
                    if i == self.active_equipped_index:
                        item_type = type
                item = list(filter(lambda item: item.type == item_type, self.equipped))[0]
                self.equipped.remove(item)
                self.add_to_backpack(item)
                self.unequip_dialog_open = False
                self.active_equipped_index = 8
            else:
                self.unequip_dialog_open = False
            self.equipped_image = self.make_image()
        else:
            if self.active_equipped_index == 8:
                self.close_action()
            else:
                if not self.unequip_dialog_open:
                    self.unequip_dialog_open = True
                    self.equipped_image = self.make_image()
