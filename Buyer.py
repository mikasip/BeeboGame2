
from settings import BODY_FONT_SMALL
from Backpack import Backpack

class Buyer(Backpack):
    def __init__(self, game, player):
        self.items = player.backpack.items
        super().__init__(game, player)
        self.font = self.stat_font = BODY_FONT_SMALL

    def make_action_text(self):
        return "Sell for " + str(round(self.items[self.active_index].price*0.7)) + " gold"

    def space_pressed(self):
        if self.active_index == len(self.items) and not self.equip_dialog_open:
            self.player.open_dialog = None
            self.player.wait = False
        else:
            if not self.equip_dialog_open:
                self.create_equip_dialog(self.image)
                self.equip_dialog_open = True
            else:
                if self.equip_dialog_open:
                    if self.equip_index_active == 0:
                        item = self.items[self.active_index]
                        self.player.chance_gold_amount(item.price*0.7)
                        if item.type == "other_item":
                            self.player.change_item_count(item, -1)
                            if item.amount > 1:
                                item.amount -= 1
                            else:
                                self.items.remove(item)
                        else:
                            self.player.backpack.items.remove(item)
                            self.items.remove(item)
                        self.equip_dialog_open = False
                    else:
                        self.equip_dialog_open = False
                    self.image = self.make_backpack_image()