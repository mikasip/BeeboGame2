from settings import *
from sprites.Player import Player
from GUI import GuiGrid

class BeeboCreation:
    def __init__(self, player:Player, finish_action):
        self.player:Player = player
        self.last_stage = 2
        self.current_stage = 0
        self.stage_texts = ["Select body", "Select eyes", "Select hair"]
        self.finish_action = finish_action
        self.gui = None
        self.image = None
        self.update_image()

    def update_image(self):
        next_page_text = "Next"
        next_action = self.next
        if self.current_stage == self.last_stage:
            next_page_text = "Complete"
            next_action = self.finish_action
        gui = GuiGrid(1,1,self.stage_texts[self.current_stage], next_page_text, None, 1, 1, 100, [], next_action)
        player_img = self.player.img_standing
        w,h = player_img.get_size()
        gui.image.blit(self.player.img_standing, ((WIDTH - w)/2, (HEIGHT - h)/2))
        text_left = HEADER_FONT.render("<", True, BLACK)
        text_right = HEADER_FONT.render(">", True, BLACK)
        gui.image.blit(text_left, (100, (HEIGHT - text_left.get_height())/2))
        gui.image.blit(text_right, (WIDTH - text_right.get_width() - 100, (HEIGHT - text_right.get_height())/2))
        self.image = gui.image
        self.gui = gui

    def next(self):
        self.current_stage += 1
        self.update_image()

    def change_style(self, next = True):
        val = self.player.body
        images = BODY_IMAGES
        if self.current_stage == 1:
            val = self.player.eyes
            images = EYE_IMAGES
        elif self.current_stage == 2:
            val = self.player.hair
            images = HAIR_IMAGES
        i = images.index(val)
        if next:
            i += 1
            if i >= len(images):
                i = 0
        else:
            i -= 1
            if i < 0:
                i = len(images) - 1
        if self.current_stage == 0:
            self.player.body = images[i]
        elif self.current_stage == 1:
            self.player.eyes = images[i]
        else:
            self.player.hair = images[i]
        self.player.update_sprites()
        self.update_image()
