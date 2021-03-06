# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 14:13:19 2019

@author: Mika Sipilä
"""

from GameState import GameState
from numpy.lib.shape_base import tile
import pygame as pg
from pygame.locals import *
import sys
import json
import jsonpickle
import pickle
from os import path
import ctypes
from settings import *
from sprites.Player import *
from sprites.obstacles import *
from sprites.Mob import *
from sprites.Treasure import *
from SpriteSheet import *
from tilemap import *
from sprites.Beebo import *
from discussion import *
from ErrorHandler import *
from Buyer import * 
from GUI import *
from network import Network
from BeeboCreation import BeeboCreation
from sprites.OtherPlayer import OtherPlayer
vec = pg.math.Vector2

class Game:
    def __init__(self):
        pg.init()
        
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))#, pg.FULLSCREEN | pg.SCALED)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.img_folder = path.join(path.dirname(__file__), 'img')
        self.menu_box_img = pg.image.load(resource_path('img/' + MENU_BOX)).convert_alpha()
        self.menu_box_img = pg.transform.scale(self.menu_box_img, (WIDTH, HEIGHT))
        self.menu_box_rect = self.menu_box_img.get_rect()
        self.head_line_font = HEADER_FONT
        self.stat_font = BODY_FONT
        self.static_img_dict = self.load_img_dict()
        self.game_dict = None
        self.menu_open = False
        self.network:Network = None
        self.connected = False
        self.game_state:GameState = GameState()
        self.break_update_loop = False
        self.main_menu(game_made = False)
        self.send_list = ""
        self.maps_with_player = []
        self.update_messages = []
        self.count = 0
        self.known_peers = []
    
    def make_item(self, item, random_stats = False):
        new_item = None
        if item["type"] == "weapon":
            new_item = Weapon(self, item, random_stats)
        elif item["type"] in ARMOR_TYPES:
            new_item = Armor(self, item, random_stats)
        elif item["type"] == "consumable":
            new_item = Consumable(self, item)
        elif item["type"] == "other_item":
            new_item = OtherItem(self, item)
        elif item["type"] == "spell":
            new_item = Spell(self, item)
        return new_item

    def main_menu(self, game_made = True):
 
        self.menu_open=True
        selected=0

        def return_menu():
            self.menu_open = False
        
        def new_game():
            self.menu_open = False

        def load_game():
            self.load_game_from_file()
            self.new()
            self.menu_open = False
            
        def quit_menu():
            self.quit()
        
        self.beebo_creation:BeeboCreation = None
        def open_beebo_creation():
            self.load_game_data()
            self.new()
            self.beebo_creation = BeeboCreation(self.player, new_game)

        gui_objects = [GuiObject("New Game", open_beebo_creation), GuiObject("Load Game", load_game), GuiObject("Quit", quit_menu)]
        if game_made: 
            gui_objects = [GuiObject("Return", return_menu), GuiObject("New Game", new_game), GuiObject("Load Game", load_game), GuiObject("Save Game", self.save_game), GuiObject("Inventory", self.player.open_backpack), GuiObject("Equipped gear", self.player.open_equipped), GuiObject("Quests", self.player.open_quests), GuiObject("Quit", quit_menu)]
        menu = GuiGrid(1, 1, "MAIN MENU", None, None, 1, 10, 50, gui_objects)
        menu.update_image()

        while self.menu_open:
            if self.beebo_creation:
                menu.image = self.beebo_creation.image
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
                if event.type==pg.KEYDOWN:
                    if self.beebo_creation:
                        if event.key == pg.K_RIGHT:
                            self.beebo_creation.change_style()
                        elif event.key == pg.K_LEFT:
                            self.beebo_creation.change_style(False)
                        else:
                            self.beebo_creation.gui.handle_key_pressed(event.key)
                    else:
                        menu.handle_key_pressed(event.key)
                        menu.update_image()
     
            # Main Menu UI
            self.screen.fill(BLACK)
            menu.blit_item(self.screen, (0,0))
            pg.display.update()
            self.clock.tick(FPS)
            
    def create_game_dict(self):
        game_dict = {
                'player': {
                        'hit_points': 60,
                        'max_hit_points': 60,
                        'damage': 1,
                        'defence': 0,
                        'level': 1,
                        'strength': 1,
                        'agility': 1,
                        'fortune': 1,
                        'gold': 200,
                        'crit_ratio': 1,
                        'crit_chance': 0,
                        'pos_x': 57 * TILESIZE,
                        'pos_y': 10 * TILESIZE,
                        'equipped_items': [],
                        'equipped_indicators': [0,0,0,0,0,0,0,0],
                        'inventory': [],
                        'next_lvl_exp': 100,
                        'exp': 0,
                        'active_quests': [],
                        'completed_quests': [],
                        'spells': [],
                        'quick_use': [],
                        'effects': [],
                        'body': BODY_IMAGES[0],
                        'eyes': EYE_IMAGES[0],
                        'hair': HAIR_IMAGES[0]
                        },
                'current_map': 'village1',
                'opened_treasures': [],
                'collected_items': [],
                }
        return game_dict
    
    def update_game_dict(self):
        self.game_dict = {
                'player': {
                        'hit_points': self.player.hit_points,
                        'max_hit_points': self.player.max_hit_points,
                        'damage': self.player.damage,
                        'defence': self.player.defence,
                        'level': self.player.level,
                        'strength': self.player.strength,
                        'agility': self.player.agility,
                        'fortune': self.player.fortune,
                        'gold': self.player.gold,
                        'crit_ratio': self.player.crit_ratio,
                        'crit_chance': self.player.crit_chance,
                        'pos_x': self.player.pos.x,
                        'pos_y': self.player.pos.y,
                        'equipped_items': [],
                        'inventory': [],
                        'equipped_indicators': self.player.equipped_gear.equipped_indicators,
                        'next_lvl_exp': self.player.next_lvl_exp,
                        'exp': self.player.exp,
                        'active_quests': self.player.active_quests,
                        'completed_quests': self.player.completed_quests,
                        'spells': self.player.spells,
                        'quick_use': list(map(lambda item: item.name, self.player.quick_use)),
                        'effects': list(map(lambda effect: effect.to_hash(), self.player.effects)),
                        'body': self.player.body,
                        'eyes': self.player.eyes,
                        'hair': self.player.hair,
                    },
                    'current_map': self.current_map.name,
                    'opened_treasures': self.opened_treasures,
                    'collected_items': self.collected_items, 
                }
        for item in self.player.equipped_gear.equipped:
            equipped_item = None
            if item.type == "weapon":
                equipped_item = {
                        "file": item.file,
                        "name": item.name,
                        "damage": item.damage,
                        "speed": item.speed,
                        "price": item.price,
                        "level": item.level,
                        "strength": item.strength,
                        "agility": item.agility,
                        "fortune": item.fortune,
                        "type": item.type,
                        "requirements": item.requirements,
                        "amount": item.amount,
                        "is_sellable": True
                        }
            if item.type in ["cloak", "helmet", "boots", "chestplate", "ring", "pants", "gloves"]:
                equipped_item = {
                        "file": item.file,
                        "name": item.name,
                        "defence": item.defence,
                        "price": item.price,
                        "level": item.level,
                        "strength": item.strength,
                        "agility": item.agility,
                        "fortune": item.fortune,
                        "type": item.type,
                        "requirements": item.requirements,
                        "amount": item.amount,
                        "is_sellable": True
                        }
            self.game_dict['player']['equipped_items'].append(equipped_item)
        for item in self.player.backpack.items:
            equipped_item = None
            if item.type == "weapon":
                equipped_item = {
                        "file": item.file,
                        "name": item.name,
                        "damage": item.damage,
                        "speed": item.speed,
                        "price": item.price,
                        "level": item.level, 
                        "strength": item.strength,
                        "agility": item.agility,
                        "fortune": item.fortune,
                        "type": item.type,
                        "requirements": item.requirements,
                        "amount": item.amount,
                        "is_sellable": True
                        }
            if item.type in ["cloak", "helmet", "boots", "chestplate", "ring", "pants", "gloves"]:
                equipped_item = {
                        "file": item.file,
                        "name": item.name,
                        "defence": item.defence,
                        "price": item.price,
                        "level": item.level,
                        "strength": item.strength,
                        "agility": item.agility,
                        "fortune": item.fortune,
                        "type": item.type,
                        "requirements": item.requirements,
                        "amount": item.amount,
                        "is_sellable": True
                        }
            if item.type == "other_item":
                equipped_item = {
                    "file": item.file,
                    "name": item.name,
                    "amount": item.amount,
                    "type": item.type,
                    "level": item.level,
                    "price": item.price,
                    "requirements": item.requirements,
                    "is_sellable": True
                }
            if item.type == "consumable":
                equipped_item = {
                    "file": item.file,
                    "name": item.name,
                    "hp": item.hp,
                    "amount": item.amount,
                    "type": item.type,
                    "level": item.level,
                    "price": item.price,
                    "requirements": item.requirements,
                    "is_sellable": True,
                    "effects": list(map(lambda effect: effect.to_hash(), item.effects))
                }
            self.game_dict['player']['inventory'].append(equipped_item)
            
    def load_img_dict(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        img_dict = {
                'player':
                    {
                        'standing': pg.image.load(resource_path('img/' + HERO_IMG_STANDING)).convert_alpha(),
                        'walking1': pg.image.load(resource_path('img/' + HERO_IMG_WALKING1)).convert_alpha(),
                        'walking2': pg.image.load(resource_path('img/' + HERO_IMG_WALKING2)).convert_alpha(),
                        'hit_frames': SpriteSheet(resource_path('img/' + 'hero_hit.png'))
                            },
                'green_mob':
                    {
                        'stand_frames': SpriteSheet(resource_path('img/' + 'mob_standing.png')),
                        'walk_frames': SpriteSheet(resource_path('img/' + 'mob_standing.png')),
                        'hit_frames': SpriteSheet(resource_path('img/' + 'mob_hit.png'))
                            },
                'other':
                    {
                        'gold': pg.image.load(resource_path('img/' + 'price.png')).convert_alpha()
                            }}
        return img_dict
            
    def load_game_from_file(self):
        load_game = True
        selected = 0
        with open('data.json') as file:
            jsonData = json.load(file)
            dataAgain = jsonpickle.encode(jsonData)
            data = jsonpickle.decode(dataAgain)
            self.game_dict = data
            self.load_game_data(new = False)
        
        
    def save_game(self):
        self.update_game_dict()
        with open('data.json', 'w') as outfile:
            outfile.write(jsonpickle.encode(self.game_dict))
        
    def load_game_data(self, new = True):
        if new:
            self.game_dict = self.create_game_dict()
        game_folder = path.dirname(__file__)
        self.maps = []
        self.current_map = TiledMap(resource_path('maps/' + self.game_dict['current_map'] + '.tmx'), self.game_dict['current_map'])
        self.maps.append(self.current_map)
        self.map_img_under, self.map_img_over = self.current_map.make_map()
        self.map_rect = self.map_img_under.get_rect()
        self.hero_img_standing = pg.image.load(resource_path('img/' + HERO_IMG_STANDING)).convert_alpha()
        self.hero_img_walking1 = pg.image.load(resource_path('img/' + HERO_IMG_WALKING1)).convert_alpha()
        self.hero_img_walking2 = pg.image.load(resource_path('img/' + HERO_IMG_WALKING2)).convert_alpha()
        self.hero_hit_frames = SpriteSheet(resource_path('img/' + 'hero_hit.png'))
        self.green_mob_hit_frames = SpriteSheet(resource_path('img/' + 'mob_hit.png'))
        self.green_mob_stand_frames = SpriteSheet(resource_path('img/' + 'mob_standing.png'))
        self.spider_hit_frames = SpriteSheet(resource_path('img/' + 'spider_hit.png'))
        self.spider_walk_frames = SpriteSheet(resource_path('img/' + 'spider_walk.png'))
        self.spider_stand_frames = SpriteSheet(resource_path('img/' + 'spider_stand.png'))
        self.gold_img = GOLD_IMG
        self.players = pg.sprite.Group()
        self.other_players = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.collisionals = pg.sprite.Group()
        self.doorways = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.spells = pg.sprite.Group()
        self.other_spells = pg.sprite.Group()
        self.treasures = pg.sprite.Group()
        self.messages = pg.sprite.Group()
        self.opened_treasures = self.game_dict['opened_treasures']
        self.collected_items = self.game_dict['collected_items']
        self.player = Player(self, self.game_dict['player']['pos_x'], self.game_dict['player']['pos_y'])
        self.player.backpack.load_data(self.game_dict['player']['inventory'])
        self.player.load_data(self.game_dict['player'])
        self.discussion_handler = DiscussionHandler()
        self.error_message = ErrorMessageHandler(pg.image.load(resource_path('img/' + MENU_BOX)).convert_alpha())
            
    def new(self):
        self.break_update_loop = True
        self.current_map.doorways = []
        self.current_map.collisions = []
        self.current_map.beebos = []
        self.current_map.mobs = []
        self.current_map.items = []
        self.current_map.treasures = []
        self.mobs.empty()
        self.items.empty()
        self.spells.empty()
        self.other_spells.empty()
        mob_id = 0
        for tile_object in self.current_map.tmxdata.objects:
            if tile_object.type == "beebo":
                comment = None
                quest = None
                if hasattr(tile_object, 'comment'):
                    comment = tile_object.comment
                if hasattr(tile_object, 'quest'):
                    quest = tile_object.quest
                new_beebo = Beebo(self, tile_object.x, tile_object.y, 
                                  tile_object.width, tile_object.height, 
                                  comment, tile_object.name, quest)
                self.current_map.beebos.append(new_beebo)
            elif tile_object.name and tile_object.type not in ["mob", "treasure", "item", "friendly_mob"]:
                locked = False
                key_needed = None
                if tile_object.type == "locked":
                    locked = True
                if locked and hasattr(tile_object, 'key'):
                    key_needed = tile_object.key
                doorway = Doorway(self, tile_object.x, tile_object.y,
                        tile_object.width, tile_object.height, tile_object.name, 
                        tile_object.pos_x, tile_object.pos_y, locked, key_needed)
                self.current_map.doorways.append(doorway)
            elif tile_object.type in ["mob", "friendly_mob"]:
                if hasattr(tile_object, "visible_before"):
                    quest = tile_object.visible_before
                    if quest in self.player.completed_quests:
                        continue
                if hasattr(tile_object, "visible_after"):
                    quest = tile_object.visible_after
                    if quest not in self.player.completed_quests:
                        continue
                mob = MOBS[tile_object.name]
                drop = []
                for quest in mob['quest_drops'].keys():
                    if quest in self.player.active_quests:
                        quest_items = mob['quest_drops'][quest]
                        for quest_item in quest_items:
                            num = np.random.uniform()
                            if num < quest_item['prob']:
                                drop_item = self.make_item(quest_item['item'], True)
                                if drop_item != None:
                                    drop.append(drop_item)
                for item in mob['drops']:
                    num = np.random.uniform()
                    if num < item['prob']:
                        drop_item = self.make_item(item['item'], True)
                        if drop_item != None:
                            drop.append(drop_item)
                new_mob = None
                if tile_object.type == "mob":
                    new_mob = Mob(self, tile_object.x, tile_object.y, self.player, SpriteSheet(resource_path('img/' + mob['stand_frames'])), SpriteSheet(resource_path('img/' + mob['walk_frames'])), 
                                SpriteSheet(resource_path('img/' + mob['hit_frames'])), mob['exp'], drop, mob['hp'], mob['damage'], mob['defence'], mob['gold'], mob['no_hit'], mob['hit_rect'], mob['name'], mob['walk_speed'], mob['hit_speed'], mob_id)
                else:
                    new_mob = FriendlyMob(self, tile_object.x, tile_object.y, self.player, SpriteSheet(resource_path('img/' + mob['stand_frames'])), SpriteSheet(resource_path('img/' + mob['walk_frames'])), 
                                mob['exp'], drop, mob['hp'], mob['defence'], mob['gold'], mob['action'], mob['hit_rect'], mob['follows'], mob['name'], mob['walk_speed'], mob_id)
                self.current_map.mobs.append(new_mob)
                mob_id += 1
            elif tile_object.type == "treasure":
                if tile_object.name not in self.opened_treasures:
                    drop = []
                    if tile_object.name in SPECIAL_TREASURES:
                        items = SPECIAL_TREASURE_DROPS[tile_object.name]
                        for item in items:
                            item_obj = ITEMS[item]
                            drop_item = None
                            if item_obj['type'] == "weapon":
                                drop_item = Weapon(self, item_obj)
                            elif item_obj['type'] in ARMOR_TYPES:
                                drop_item = Armor(self, item_obj)
                            elif item_obj['type'] == "other_item":
                                drop_item = OtherItem(self, item_obj)
                            elif item_obj['type'] == "consumable":
                                drop_item = Consumable(self, item_obj)
                            if drop_item != None:
                                drop.append(drop_item)
                    tier = 'tier1'
                    if hasattr(tile_object, tier):
                        tier = tile_object.tier
                    new_treasure = Treasure(self, tile_object.name, tile_object.height, tile_object.width, 
                                            tile_object.x, tile_object.y, tile_object.way_x, tile_object.way_y, drop, tier)
                    self.current_map.treasures.append(new_treasure)
            elif tile_object.type == "item":
                if tile_object.name not in self.collected_items:
                    item = OtherItem(self, ITEMS[tile_object.item_id])
                    sprite = DropSprite(self, tile_object.x, tile_object.y, item, ITEMS[tile_object.item_id]['only_once'], tile_object.name)
                    self.current_map.items.append(sprite)
            else:
                obstacle = Obstacle(self, tile_object.x, tile_object.y,
                        tile_object.width, tile_object.height)
                self.current_map.collisions.append(obstacle)
        self.camera = Camera(self.current_map.width, self.current_map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.network = Network()
        playerId = self.network.getId()
        if playerId != None:
            self.player.id = int(playerId)
            self.connected = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            for peer_id in list(map(lambda peer: peer.id, self.network.peers)):
                if peer_id not in self.known_peers:
                    self.network.send_to_peer(self.player.create_message_to_server() + "," + str(self.player.pos.x) + "," + str(self.player.pos.y), peer_id)
            if len(self.send_list) > 0:
                self.send_to_server(self.send_list)
                self.send_list = ""

    def update_game_state(self, msg):
        self.update_messages.append(msg)
        
    """
        Format:
        'map_name,type(player/mob),id,pos_x,pos_y,hp'
    """
    def add_to_send_list(self,data):
        self.send_list += data + ";"

    def send_to_server(self, data):
        if self.connected:
            return self.network.send(data[:-1])
        return None

    def quit(self):
        self.send_to_server("remove," + self.current_map.name + "," + str(self.player.id) + ";")
        self.network.end_session()
        pg.quit()
        sys.exit()

    def update(self):
        messages, peer_ids = self.network.getMessages()
        for peer_id in peer_ids:
            if peer_id not in self.known_peers:
                self.known_peers.append(peer_id)
        for msg in messages:
            for updateString in msg.split(";"):
                parts = updateString.split(",")
                if len(parts) <= 2:
                    self.add_to_send_list(self.player.create_message_to_server())
                elif parts[0] == "remove":
                    if self.current_map.name == parts[1]:
                        existingPlayer = list(filter(lambda player: player.id == int(parts[2]), self.other_players))
                        if len(existingPlayer) > 0:
                            existingPlayer[0].kill()
                elif parts[0] == "remove_spell":
                    if self.current_map.name == parts[1]:
                        existingSpell = list(filter(lambda spell: spell.id == int(parts[3]) and spell.player_id == int(parts[2]), self.other_spells))
                        if len(existingSpell) > 0:
                            print("killing")
                            existingSpell[0].kill()
                elif parts[0] == "dead":
                    if self.current_map.name == parts[1]:
                        existingMob = list(filter(lambda mob: mob.id == int(parts[2]), self.mobs))
                        if len(existingMob) > 0:
                            existingMob.dieing = True
                            existingMob.die_animation()
                elif parts[0] == "damage":
                    if self.current_map.name == parts[1]:
                        existingMob = list(filter(lambda mob: mob.id == int(parts[2]), self.mobs))
                        if len(existingMob) > 0:
                            existingMob[0].hit_points -= int(float(parts[3]))
                            existingMob[0].total_slow *= float(parts[4])
                            existingMob[0].update_hp_bar()
                            if existingMob[0].hit_points <= 0:
                                existingMob[0].dieing = True
                                existingMob[0].die_animation()
                else:
                    if parts[1] == "player":
                        if parts[0] != self.current_map.name:
                            players = list(filter(lambda player: player.id == int(parts[2]), self.other_players))
                            for player in players:
                                player.kill()

                    if self.current_map.name == parts[0]:
                        if parts[1] == "mob":
                            existingMob = list(filter(lambda mob: mob.id == int(parts[2]), self.mobs))
                            if len(existingMob) > 0:
                                mob = existingMob[0]
                                mob.hit_points = int(parts[3])
                                mob.pos = vec(round(float(parts[4])), round(float(parts[5])))
                                mob.way = vec(round(float(parts[6])), round(float(parts[7])))
                                mob.image_index = int(parts[8])
                        elif parts[1] == "player":
                            existingPlayer = list(filter(lambda player: player.id == int(parts[2]), self.other_players))
                            player = None
                            needs_update = False
                            if len(existingPlayer) > 0:
                                player = existingPlayer[0]
                                needs_update = True
                            else:
                                player = OtherPlayer(self, round(float(parts[7])), round(float(parts[8])), int(parts[2]))
                                self.network.send_to_peer(self.player.create_message_to_server() + "," + str(self.player.pos.x) + "," + str(self.player.pos.y), int(parts[2]))
                            player.vel = vec(round(float(parts[3])), round(float(parts[4])))
                            player.map = parts[0]
                            player.hit_points = int(float(parts[5]))
                            player.max_hit_points = int(float(parts[6]))
                            player.way = vec(round(float(parts[7])), round(float(parts[8])))
                            player.image_index = int(parts[9])
                            if parts[10] != "none":
                                player.weapon = parts[10]
                            else:
                                player.weapon = None
                            player.body = parts[11]
                            player.feet = parts[12]
                            player.hands = parts[13]
                            player.eyes = parts[14]
                            player.hair = parts[15]
                            if len(parts) > 17:
                                player.pos = vec(round(float(parts[16])), round(float(parts[17])))
                            player.update_hp_bar()
                            if needs_update:
                                player.update_images()
                            player.ready = True
                        elif parts[1] == "spell":
                            existingSpell = list(filter(lambda spell: spell.id == int(parts[3]) and spell.player_id == int(parts[2]), self.other_spells))
                            spell = None
                            if len(existingSpell) > 0:
                                spell = existingSpell[0]
                            else:
                                spell = OtherSpell(self, float(parts[4]), float(parts[5]), round(float(parts[6])), round(float(parts[7])), parts[9], int(parts[3]), int(parts[2]))
                            spell.pos = vec(round(float(parts[4])), round(float(parts[5])))
                            spell.hit = (parts[8] == "True")
        self.update_messages = []
        # update portion of the game loop
        self.players.update()
        if self.break_update_loop:
            self.break_update_loop = False
            return
        self.other_players.update()
        self.mobs.update()
        self.spells.update()
        self.messages.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img_under, self.camera.apply_rect(self.map_rect))
        for sprite in self.items:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.mobs:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.players:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.other_players:
            if sprite.map == self.current_map.name:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.spells:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.other_spells:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.messages:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.screen.blit(self.map_img_over, self.camera.apply_rect(self.map_rect))
        self.screen.blit(self.player.statbar.image, self.player.statbar.rect)
        self.screen.blit(self.player.skillsGUI.image, self.player.skillsGUI.rect)
        if self.discussion_handler.discussion_open:
            self.screen.blit(self.discussion_handler.comment.image, self.discussion_handler.comment.pos)
        if self.player.open_dialog != None:
            self.screen.blit(self.player.open_dialog.get_image(), self.player.open_dialog.get_rect())
        if self.error_message.open:
            self.screen.blit(self.error_message.image, self.error_message.rect)

        pg.display.flip()
        
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_m:
                    self.main_menu()
                    return
                if event.key == pg.K_SPACE:
                    if self.error_message.open:
                        self.error_message.open = False
                        return
                    if self.player.open_dialog != None:
                        self.player.handle_key_pressed(event.key)
                        return
                    elif not self.discussion_handler.discussion_open:
                        collides_with = self.player.collide_with_beebo()
                        if collides_with:
                            comment = collides_with.get_comment()
                            if isinstance(comment, Buyer):
                                self.player.open_sell_dialog(comment)
                            else:
                                self.discussion_handler.set_comment(collides_with.get_comment())
                            if self.discussion_handler.comment != None:
                                self.player.wait = True
                        collides_with_item = self.player.collide_with_item()
                        if collides_with_item:
                            self.player.pick_item(collides_with_item)
                        collides_with_treasure = self.player.collide_with_treasure()
                        if collides_with_treasure:
                            if not collides_with_treasure.name in self.opened_treasures:
                                collides_with_treasure.open_treasure()
                        collides_with_friendly_mob = self.player.collide_with_friendly_mob()
                        if collides_with_friendly_mob:
                            collides_with_friendly_mob.space_action()
                    elif self.discussion_handler.discussion_open:
                        self.discussion_handler.comment.space_pressed(self.discussion_handler)
                if not self.error_message.open:
                    if self.discussion_handler.discussion_open:
                        if isinstance(self.discussion_handler.comment, Store) or isinstance(self.discussion_handler.comment, QuestDialog):
                            if event.key in [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN]:
                                self.discussion_handler.comment.change_active(event.key)
                    if self.player.open_dialog != None and event.key != pg.K_SPACE:
                        self.player.handle_key_pressed(event.key) 
                    if event.key == pg.K_b:
                        self.player.open_backpack()
                    if event.key == pg.K_g:
                        self.player.open_equipped()
                    if event.key == pg.K_q:
                        self.player.hit()
    
    def toJSON(player):
        return jsonpickle(player)
        # return json.dumps(player, default=lambda o: vars2(o), sort_keys=True, indent=4)
        
# create the game object
g = Game()
while True:
    g.new()
    g.run()