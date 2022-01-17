
from settings import BODY_FONT_SMALL
from Backpack import Backpack
from GUI import *

class Buyer(Backpack):
    def __init__(self, game, player):
        self.items = player.backpack.items
        super().__init__(game, player)
        self.font = self.stat_font = BODY_FONT_SMALL

    def make_action_text(self):
        return "Sell for " + str(round(self.items[self.active_index].price*0.7)) + " gold"

    def create_equip_dialog(self):
        active_item = self.items[self.active_index]
        items = []
        items.append(GuiObject(self.make_action_text(), self.sell_item))
        items.append(GuiObject("Cancel", self.close_selection_menu))
        self.selection_menu = GuiGrid(0.3, 0.4, None, None, None, 1, len(items), 40, items, 10)
        self.selection_menu.blit_item(self.image, "center")
    
    def sell_item(self):
        item = self.items[self.active_index]
        self.player.chance_gold_amount(item.price*0.7)
        backpack_item = list(filter(lambda i: i == item, self.player.backpack.items))
        if len(backpack_item) > 0:
            self.player.change_item_count(backpack_item[0], -1)
            if item.amount < 1:
                self.items.remove(item)
        self.selection_menu = None
        self.image = self.make_backpack_image()