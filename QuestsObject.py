from Quest import Quest
from GUI import *
from quests import *

class Quests(GuiGrid, CustomGuiItem):
    def __init__(self, background_image, close_action):
        self.background_image = background_image
        self.rect = background_image.get_rect()
        self.quests = []
        self.active_index = 0
        gui_items = []
        self.quest_open = None
        for quest in self.quests:
            quest = QUESTS[quest]
            gui_items.append(GuiObject(quest['name'], lambda: self.open_quest(quest)))
        GuiGrid.__init__(self, 1, 1, "Active quests", "Return", None, 1, 10, 80, gui_items, close_action)
    
    def get_image(self):
        return self.image
    
    def get_rect(self):
        return self.rect
    
    def space_pressed(self):
        self.handle_key_pressed(pg.K_SPACE)
    
    def change_active(self, key):
        self.active_index = move_in_matrix(self.ncol, self.nrow, self.active_index, len(self.items), key)
        self.update_image()

    def add_quest(self, quest):
        if quest not in self.quests:
            self.quests.append(quest)
            self.update_items()
            self.update_image()
    
    def remove_quest(self, quest):
        if quest in self.quests:
            self.quests.remove(quest)
            self.update_items()
    
    def update_items(self):
        self.items = []
        for quest in self.quests:
            quest = QUESTS[quest]
            self.items.append(GuiObject(quest['name'], lambda: self.open_quest(quest)))
        self.update_image()

    def open_quest(self, quest):
        self.quest_open = quest
        self.update_image()

    def update_image(self):
        super().update_image()

        if self.quest_open != None:
            items = [GuiObject(str(self.quest_open['description']), None), GuiObject(str(self.quest_open['mission']['text']), None)]
            gui = GuiGrid(1,1, str(self.quest_open['name']), "Back", None, 1, 5, 80, items, None)
            gui.update_image()
            self.image.blit(gui.image, (0,0))

    def handle_key_pressed(self, event):
        if self.quest_open != None:
            if event == pg.K_SPACE:
                self.quest_open = None
                self.update_image()
        else:
            super().handle_key_pressed(event)



