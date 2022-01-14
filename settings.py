# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 14:04:25 2019

@author: Mika Sipilä
"""
import pygame as pg
from os import path
#import ctypes
vec = pg.math.Vector2

WHITE = (255,255,255)
BLACK = (0,0,0)
DARKGREY = (40,40,40)
LIGHTGREY = (100,100,100)
LIGHTERGREY = (200,200,200)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0, 0, 255)

WIDTH = 20*40
HEIGHT = 20*30
MARGIN = 50
MARGIN_LEFT = 40
MARGIN_BOT = 53
FPS = 60
TITLE = ""
BGCOLOR = LIGHTGREY

TILESIZE = 32
HIT_COOLDOWN = 1

PLAYER_HIT_RECT = pg.Rect(0, 0, 50, 50)
GREEN_MOB_HIT_RECT = pg.Rect(0,0,40,40)
PLAYER_SPEED = 200
MOB_SPEED = 50
RUN_MULTIPLIER = 2
HERO_IMG_STANDING = 'standing_hero.png'
HERO_IMG_WALKING1 = 'walking_hero1.png'
HERO_IMG_WALKING2 = 'walking_hero2.png'
HERO_IMG_HIT = 'hitting_hero_with_steel_spear.png'
DISCUSSION_BOX = 'comment.png'
MENU_BOX = 'menu.png'
IMAGE_UPDATE_FREQUENCY = 14

pg.init()
HEADER_FONT = pg.font.SysFont('calibri', 30)
SUBHEADER_FONT = pg.font.SysFont('calibri', 24)
BODY_FONT = pg.font.SysFont('calibri', 18)
BODY_FONT_SMALL = pg.font.SysFont('calibri', 12)
#ctypes.windll.user32.SetProcessDPIAware()
#true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
pg.display.set_mode((WIDTH, HEIGHT))
from helpers import resource_path
GOLD_IMG = pg.image.load(resource_path('img/' + 'price.png')).convert_alpha()
STRENGHT_IMG = pg.image.load(resource_path('img/' + 'strength.png')).convert_alpha()
AGILITY_IMG = pg.image.load(resource_path('img/' + 'agility.png')).convert_alpha()
FORTUNE_IMG = pg.image.load(resource_path('img/' + 'fortune.png')).convert_alpha()
FIRE_SPELL_IMG = pg.image.load(resource_path('img/' + 'fire_spell.png')).convert_alpha()
FIRE_SPELL_HIT_IMG = pg.image.load(resource_path('img/' + 'fire_spell_hit.png')).convert_alpha()

ITEMS = {
        'grape': {
                "file": 'grape',
                "name": 'Grape',
                "amount": 1,
                "type": 'other_item',
                'price': 0,
                'level': 1, 
                'only_once': False,
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'daisy': {
                "file": 'daisy',
                "name": 'Daisy',
                "amount": 1,
                "type": 'other_item',
                'price': 0,
                'level': 1,
                'only_once': True,
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'secret-room1-key': {
                'file': 'key',
                'name': "The first secret key",
                'amount': 1,
                'level': 1,
                'type': 'other_item',
                'only_once': False,
                'price': 0,
                "amount": 1,
                "requirements": [],
                "is_sellable": False
        },
        'apple': {
                "name": "Apple",
                "file": "apple",
                "hp": 5,
                "price": 3,
                "level": 1,
                "type": "consumable",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'apple_pie': {
                "name": "Apple Pie",
                "file": "apple_pie",
                "hp": 40,
                "price": 5,
                "level": 1,
                "amount": 1,
                "type": "consumable",
                "requirements": [
                        {
                                "name": "Apple",
                                "count": 10
                        }
                ],
                "is_sellable": True
        },
        'small_hp_potion': {
                "name": "Small health potion",
                "file": "small_hp_potion",
                "hp": 10,
                "price": 10,
                "level": 1,
                "type": "consumable",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        }, 
        'normal_hp_potion': {
                "name": "Normal health potion",
                "file": "small_hp_potion",
                "hp": 40,
                "price": 80,
                "level": 1,
                "type": "consumable",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        }, 
        'wool': {
                "name": "Wool",
                "file": "wool",
                "price": 3,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'chicken_egg': {
                "name": "Chicken egg",
                "file": "chicken_egg",
                "price": 2,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'cooked_chicken_egg': {
                "name": "Cooked chicken egg",
                "file": "chicken_egg",
                "price": 3,
                "level": 1,
                "type": "consumable",
                "hp": 10,
                "amount": 1,
                "requirements": [
                        {
                                "name": "Chicken egg",
                                "count": 1
                        }
                ],
                "is_sellable": True
        },
        'omelet': {
                "name": "Omelet",
                "file": "omelet",
                "price": 15,
                "level": 1,
                "type": "consumable",
                "hp": 30,
                "amount": 1,
                "requirements": [
                        {
                                "name": "Chicken egg",
                                "count": 5
                        }
                ],
                "is_sellable": True
        },
        'scissors': {
                "name": "Scissors",
                "file": "scissors",
                "price": 200,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": False
        },
        'red_slime': {
                "name": "Red Slime",
                "file": "red_slime",
                "price": 0,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'yellow_slime': {
                "name": "Yellow Slime",
                "file": "yellow_slime",
                "price": 0,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'blue_slime': {
                "name": "Blue Slime",
                "file": "blue_slime",
                "price": 0,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        
        'dotted_slime': {
                "name": "Dotted Slime",
                "file": "dotted_slime",
                "price": 0,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'red_gem': {
                "name": "Red gem",
                "file": "red_gem",
                "price": 20,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'blue_gem': {
                "name": "Blue gem",
                "file": "blue_gem",
                "price": 20,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'green_gem': {
                "name": "Green gem",
                "file": "green_gem",
                "price": 20,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'green_spider_leg': {
                "name": "Green Spider Leg",
                "file": "green_spider_leg",
                "price": 10,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'red_spider_leg': {
                "name": "Red Spider Leg",
                "file": "red_spider_leg",
                "price": 10,
                "level": 1,
                "type": "other_item",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'potion_of_fortune': {
                "name": "Potion of Fortune",
                "file": "potion_of_fortune",
                "hp": 0,
                "effects": [{'effect': 'fortune', 'time': 60, 'amount': 5}],
                "price": 150,
                "level": 1,
                "type": "consumable",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        # 'basic_axe': {
                    #    "file": "basic_axe",
                    #    "name": "Steel axe",
                    #    "damage": 10,
                    #    "speed": 1,
                    #    "price": 100,
                    #    "level": 1,
                    #    "strength": 1,
                    #    "agility": 1,
                    #    "fortune": 1,
                    #    "type": "weapon",
                    #    "amount": 1,
                    #    "requirements": []
                    #},
        # WEAPONS
        'steel_sword': {
                        "file": "steel_sword",
                        "name": "Steel sword",
                        "damage": 10,
                        "speed": 1,
                        "price": 100,
                        "level": 1,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "weapon",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'bronze_sword': {
                        "file": "bronze_sword",
                        "name": "Bronze sword",
                        "damage": 25,
                        "speed": 1,
                        "price": 1000,
                        "level": 7,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "weapon",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'mighty_sword': {
                "file": "mighty_sword",
                "name": "Mighty sword",
                "damage": 22,
                "speed": 1.2,
                "price": 1000,
                "level": 8,
                "strength": 0,
                "agility": 0,
                "fortune": 0,
                "type": "weapon",
                "amount": 1,
                "requirements": [],
                "is_sellable": True
        },
        'silver_sword': {
                        "file": "silver_sword",
                        "name": "Silver sword",
                        "damage": 30,
                        "speed": 1.1,
                        "price": 2500,
                        "level": 13,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "weapon",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'golden_sword': {
                        "file": "golden_sword",
                        "name": "Golden sword",
                        "damage": 40,
                        "speed": 1.2,
                        "price": 7500,
                        "level": 20,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "weapon",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'mystic_sword': {
                        "file": "mystic_sword",
                        "name": "Mystic sword",
                        "damage": 50,
                        "speed": 1.3,
                        "price": 15500,
                        "level": 27,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "weapon",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'sword_of_ancient_gods': {
                        "file": "sword_of_ancient_gods",
                        "name": "Sword of Ancient Gods",
                        "damage": 100,
                        "speed": 1.7,
                        "price": 150000,
                        "level": 50,
                        "strength": 10,
                        "agility": 10,
                        "fortune": 10,
                        "type": "weapon",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'pink_sword': {
                        "file": "pink_sword",
                        "name": "Pink Sword",
                        "damage": 50,
                        "speed": 2,
                        "price": 25000,
                        "level": 50,
                        "strength": 0,
                        "agility": 20,
                        "fortune": 0,
                        "type": "weapon",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'steel_spear': {
                        "file": "steel_spear",
                        "name": "Steel spear",
                        "damage": 6,
                        "speed": 1.5,
                        "price": 100,
                        "level": 1,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "weapon",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        #BOOTS
        'leather_boots': {
                        "file":"leather_boots",
                        "name": "Leather boots",
                        "defence": 2,
                        "price": 75,
                        "level": 1,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "boots",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'red_leather_boots': {
                        "file":"red_leather_boots",
                        "name": "Red leather boots",
                        "defence": 3,
                        "price": 150,
                        "level": 5,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "boots",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'boots_of_swiftness': {
                        "file": 'boots_of_swiftness',
                        "name": "Boots of swiftness",
                        "defence": 4,
                        "price": 800,
                        "level": 10,
                        "strength": 0,
                        "agility": 2,
                        "fortune": 0,
                        "type": "boots",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'boots_of_wisdom': {
                        "file": 'boots_of_wisdom',
                        "name": "Boots of wisdom",
                        "defence": 4,
                        "price": 800,
                        "level": 10,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 2,
                        "type": "boots",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'steel_boots': {
                        "file": 'steel_boots',
                        "name": "Steel boots",
                        "defence": 7,
                        "price": 800,
                        "level": 10,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "boots",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'golden_boots': {
                        "file": 'golden_boots',
                        "name": "Golden boots",
                        "defence": 15,
                        "price": 2800,
                        "level": 25,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "boots",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'boots_of_lizard_skin': {
                        "file": 'boots_of_lizard_skin',
                        "name": "Boots of Lizard skin",
                        "defence": 5,
                        "price": 2000,
                        "level": 20,
                        "strength": 1,
                        "agility": 1,
                        "fortune": 1,
                        "type": "boots",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'leather_gloves': {
                        "file":"leather_gloves",
                        "name": "Leather gloves",
                        "defence": 2,
                        "price": 150,
                        "level": 1,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "gloves",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'red_leather_gloves': {
                        "file":"red_leather_gloves",
                        "name": "Leather gloves",
                        "defence": 4,
                        "price": 300,
                        "level": 5,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "gloves",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'steel_gloves': {
                        "file":"steel_gloves",
                        "name": "Steel gloves",
                        "defence": 6,
                        "price": 700,
                        "level": 10,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "gloves",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'steel_gloves': {
                        "file":"steel_gloves",
                        "name": "Steel gloves",
                        "defence": 6,
                        "price": 700,
                        "level": 10,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "gloves",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'bronze_gloves': {
                        "file":"bronze_gloves",
                        "name": "Bronze gloves",
                        "defence": 8,
                        "price": 1500,
                        "level": 15,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "gloves",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'silver_gloves': {
                        "file":"silver_gloves",
                        "name": "Silver gloves",
                        "defence": 10,
                        "price": 2100,
                        "level": 20,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "gloves",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'golden_gloves': {
                        "file":"golden_gloves",
                        "name": "Golden gloves",
                        "defence": 13,
                        "price": 3000,
                        "level": 25,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "gloves",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'mystic_gloves': {
                        "file":"mystic_gloves",
                        "name": "Mystic gloves",
                        "defence": 20,
                        "price": 5000,
                        "level": 30,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "gloves",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        # PANTS
        'leather_pants': {
                        "file":"leather_pants",
                        "name": "Leather pants",
                        "defence": 4,
                        "price": 300,
                        "level": 1,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "pants",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'red_leather_pants': {
                        "file":"leather_pants",
                        "name": "Leather pants",
                        "defence": 6,
                        "price": 700,
                        "level": 5,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "pants",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'steel_pants': {
                        "file":"steel_pants",
                        "name": "Steel pants",
                        "defence": 9,
                        "price": 1400,
                        "level": 10,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "pants",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'bronze_pants': {
                        "file":"bronze_pants",
                        "name": "Bronze pants",
                        "defence": 12,
                        "price": 2200,
                        "level": 15,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "pants",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'silver_pants': {
                        "file":"silver_pants",
                        "name": "Silver pants",
                        "defence": 17,
                        "price": 3900,
                        "level": 20,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "pants",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'golden_pants': {
                        "file":"golden_pants",
                        "name": "Golden pants",
                        "defence": 22,
                        "price": 6000,
                        "level": 25,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "pants",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'mystic_pants': {
                        "file":"mystic_pants",
                        "name": "Mystic pants",
                        "defence": 27,
                        "price": 10500,
                        "level": 30,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "pants",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        # CHESTPLATES
        'leather_chestplate': {
                        "file":"leather_chestplate",
                        "name": "Leather chestplate",
                        "defence": 5,
                        "price": 600,
                        "level": 1,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "chestplate",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'red_leather_chestplate': {
                        "file":"red_leather_chestplate",
                        "name": "Red leather chestplate",
                        "defence": 9,
                        "price": 1300,
                        "level": 5,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "chestplate",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'steel_chestplate': {
                        "file":"steel_chestplate",
                        "name": "Steel chestplate",
                        "defence": 12,
                        "price": 2500,
                        "level": 10,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "chestplate",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'bronze_chestplate': {
                        "file":"bronze_chestplate",
                        "name": "Bronze chestplate",
                        "defence": 17,
                        "price": 3900,
                        "level": 20,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "chestplate",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'silver_chestplate': {
                        "file":"silver_chestplate",
                        "name": "Silver chestplate",
                        "defence": 21,
                        "price": 5500,
                        "level": 20,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "chestplate",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'golden_chestplate': {
                        "file":"golden_chestplate",
                        "name": "Golden chestplate",
                        "defence": 25,
                        "price": 7500,
                        "level": 25,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "chestplate",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'mystic_chestplate': {
                        "file":"mystic_chestplate",
                        "name": "Mystic chestplate",
                        "defence": 30,
                        "price": 12000,
                        "level": 30,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "chestplate",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        # RINGS
        'basic_ring': {
                        "file":"basic_ring",
                        "name": "Basic ring",
                        "defence": 1,
                        "price": 40,
                        "level": 1,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "ring",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'ring_of_swiftness': {
                        "file": 'ring_of_swiftness',
                        "name": "Ring of swiftness",
                        "defence": 2,
                        "price": 500,
                        "level": 10,
                        "strength": 0,
                        "agility": 1,
                        "fortune": 0,
                        "type": "ring",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'ring_of_wisdom': {
                        "file": 'boots_of_wisdom',
                        "name": "Boots of wisdom",
                        "defence": 2,
                        "price": 500,
                        "level": 10,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 1,
                        "type": "ring",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'ring_of_power': {
                        "file": 'ring_of_wisdom',
                        "name": "Ring of power",
                        "defence": 2,
                        "price": 500,
                        "level": 10,
                        "strength": 1,
                        "agility": 0,
                        "fortune": 0,
                        "type": "ring",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'ring_of_ancient_gods': {
                        "file": 'ring_of_ancient_gods',
                        "name": "Ring of ancient gods",
                        "defence": 10,
                        "price": 50000,
                        "level": 50,
                        "strength": 5,
                        "agility": 5,
                        "fortune": 5,
                        "type": "ring",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        
        # HELMETS
        'leather_helmet': {
                        "file":"leather_helmet",
                        "name": "Leather helmet",
                        "defence": 2,
                        "price": 300,
                        "level": 1,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "helmet",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'red_leather_helmet': {
                        "file":"red_leather_helmet",
                        "name": "Red leather helmet",
                        "defence": 5,
                        "price": 700,
                        "level": 5,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "helmet",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'steel_helmet': {
                        "file":"steel_helmet",
                        "name": "Steel helmet",
                        "defence": 7,
                        "price": 1200,
                        "level": 10,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "helmet",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'bronze_helmet': {
                        "file":"bronze_helmet",
                        "name": "Bronze helmet",
                        "defence": 10,
                        "price": 2400,
                        "level": 15,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "helmet",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'silver_helmet': {
                        "file":"silver_helmet",
                        "name": "Silver helmet",
                        "defence": 15,
                        "price": 4100,
                        "level": 15,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "helmet",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'golden_helmet': {
                        "file":"golden_helmet",
                        "name": "Golden helmet",
                        "defence": 20,
                        "price": 7000,
                        "level": 25,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "helmet",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'mystic_helmet': {
                        "file":"mystic_helmet",
                        "name": "Mystic helmet",
                        "defence": 26,
                        "price": 9000,
                        "level": 30,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "helmet",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        # CLOAKS
        'leather_cloak': {
                        "file":"leather_cloak",
                        "name": "Leather cloak",
                        "defence": 2,
                        "price": 400,
                        "level": 3,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "cloak",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'mystic_cloak': {
                        "file":"mystic_cloak",
                        "name": "Mystic cloak",
                        "defence": 35,
                        "price": 16000,
                        "level": 30,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "cloak",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'cloak_of_ancient_gods': {
                        "file":"cloak_of_ancient_gods",
                        "name": "The cloak of Ancient Gods",
                        "defence": 50,
                        "price": 100000,
                        "level": 50,
                        "strength": 10,
                        "agility": 10,
                        "fortune": 10,
                        "type": "cloak",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'cloak_of_swiftness': {
                        "file":"cloack_of_swiftness",
                        "name": "The cloak of swiftness",
                        "defence": 5,
                        "price": 1000,
                        "level": 10,
                        "strength": 0,
                        "agility": 3,
                        "fortune": 0,
                        "type": "cloak",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'cloak_of_power': {
                        "file":"cloack_of_power",
                        "name": "The cloak of power",
                        "defence": 5,
                        "price": 1000,
                        "level": 10,
                        "strength": 3,
                        "agility": 0,
                        "fortune": 0,
                        "type": "cloak",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'cloak_of_wisdom': {
                        "file":"cloack_of_wisdom",
                        "name": "The cloak of wisdom",
                        "defence": 5,
                        "price": 1000,
                        "level": 10,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 3,
                        "type": "cloak",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },
        'golden_cloak': {
                        "file":"golden_cloak",
                        "name": "Golden cloak",
                        "defence": 20,
                        "price": 10000,
                        "level": 25,
                        "strength": 0,
                        "agility": 0,
                        "fortune": 0,
                        "type": "cloak",
                        "amount": 1,
                        "requirements": [],
                        "is_sellable": True
                    },

        
        'wool_boots': {
                "file": "wool_boots",
                "name": "Wool boots",
                "defence": 2,
                "price": 100,
                "level": 5,
                "strength": 0,
                "agility": 1,
                "fortune": 0,
                "type": "boots",
                "amount": 1,
                "requirements": [
                        {
                                'name': 'Wool',
                                'count': 20
                        }
                ],
                "is_sellable": True
        },
        'wool_shirt': {
                "file": "wool_shirt",
                "name": "Wool shirt",
                "defence": 3,
                "price": 300,
                "level": 5,
                "strength": 0,
                "agility": 2,
                "fortune": 0,
                "type": "chestplate",
                "amount": 1,
                "requirements": [
                        {
                                'name': 'Wool',
                                'count': 50
                        }
                ],
                "is_sellable": True
        },
        'wool_pants': {
                "file": "wool_pants",
                "name": "Wool pants",
                "defence": 2,
                "price": 200,
                "level": 5,
                "strength": 0,
                "agility": 2,
                "fortune": 0,
                "type": "pants",
                "amount": 1,
                "requirements": [
                        {
                                'name': 'Wool',
                                'count': 40
                        }
                ],
                "is_sellable": True
        },
}

LOOTS = {
        'grape_loot': [
                { 
                        'item': ITEMS['grape'],
                        'prob': 0.5,
                },
        ],
        'tier1': [
                {
                        'item': ITEMS['steel_sword'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['steel_spear'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['leather_boots'],
                        'prob': 0.01,
                },
                {
                        'item': ITEMS['basic_ring'],
                        'prob': 0.01,
                },
                {
                        'item': ITEMS['leather_chestplate'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['leather_helmet'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['leather_gloves'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['leather_pants'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['leather_cloak'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['small_hp_potion'],
                        'prob': 0.07
                },
                {
                        'item': ITEMS['normal_hp_potion'],
                        'prob': 0.03
                },
        ],
        'tier2': [
                {
                        'item': ITEMS['bronze_sword'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['red_leather_boots'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['ring_of_swiftness'],
                        'prob': 0.001,
                },
                {
                        'item': ITEMS['ring_of_power'],
                        'prob': 0.001,
                },
                {
                        'item': ITEMS['ring_of_wisdom'],
                        'prob': 0.001,
                },
                {
                        'item': ITEMS['red_leather_chestplate'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['red_leather_helmet'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['red_leather_gloves'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['red_leather_pants'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['leather_cloak'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['small_hp_potion'],
                        'prob': 0.05
                },
                {
                        'item': ITEMS['normal_hp_potion'],
                        'prob': 0.05
                },
        ],
        'tier3': [
                {
                        'item': ITEMS['silver_sword'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['steel_spear'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['steel_boots'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['ring_of_swiftness'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['ring_of_power'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['ring_of_wisdom'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['steel_chestplate'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['steel_helmet'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['steel_gloves'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['steel_pants'],
                        'prob': 0.005,
                },
                {
                        'item': ITEMS['cloak_of_wisdom'],
                        'prob': 0.001,
                },
                {
                        'item': ITEMS['cloak_of_power'],
                        'prob': 0.001,
                },
                {
                        'item': ITEMS['cloak_of_swiftness'],
                        'prob': 0.001,
                },
                {
                        'item': ITEMS['small_hp_potion'],
                        'prob': 0.03
                },
                {
                        'item': ITEMS['normal_hp_potion'],
                        'prob': 0.07
                },
        ],
        
}

MOBS = {
        'green_mob': {
                'name': 'green_mob',
                'stand_frames': 'mob_standing.png',
                'walk_frames': 'mob_standing.png',
                'hit_frames': 'mob_hit.png',
                'hp': 30,
                'damage': 5,
                'defence': 3,
                'exp': 10,
                'gold': 8,
                'quest_drops': {
                },
                'drops': LOOTS['grape_loot'],
                'no_hit': False,
                'hit_rect': pg.Rect(0,0,40,40),
                'walk_speed': 50,
                'hit_speed': 1,
        },
        'red_slime': {
                'name': 'red_slime',
                'stand_frames': 'red_slime_walking.png',
                'walk_frames': 'red_slime_walking.png',
                'hit_frames': 'red_slime_hit.png',
                'hp': 50,
                'damage': 16,
                'defence': 5,
                'exp': 25,
                'gold': 20,
                'quest_drops': {
                        'slime_quest': [
                                { 
                                        'item': ITEMS['red_slime'],
                                        'prob': 1,
                                },
                        ]
                },
                'drops': LOOTS['tier1'] + [{'item': ITEMS['red_gem'], 'prob': 0.5}],
                'no_hit': False,
                'hit_rect': pg.Rect(0,0,50,50),
                'walk_speed': 70,
                'hit_speed': 1,
        },
        'yellow_slime': {
                'name': 'yellow_slime',
                'stand_frames': 'yellow_slime_walking.png',
                'walk_frames': 'yellow_slime_walking.png',
                'hit_frames': 'yellow_slime_hit.png',
                'hp': 50,
                'damage': 18,
                'defence': 3,
                'exp': 25,
                'gold': 20,
                'quest_drops': {
                        'slime_quest': [
                                { 
                                        'item': ITEMS['yellow_slime'] ,
                                        'prob': 1,
                                },
                        ]
                },
                'drops': LOOTS['tier1'] + [{'item': ITEMS['green_gem'], 'prob': 0.5}],
                'no_hit': False,
                'hit_rect': pg.Rect(0,0,50,50),
                'walk_speed': 70,
                'hit_speed': 1,
        },
        'blue_slime': {
                'name': 'blue_slime',
                'stand_frames': 'blue_slime_walking.png',
                'walk_frames': 'blue_slime_walking.png',
                'hit_frames': 'blue_slime_hit.png',
                'hp': 50,
                'damage': 14,
                'defence': 7,
                'exp': 25,
                'gold': 20,
                'quest_drops': {
                        'slime_quest': [
                                { 
                                        'item': ITEMS['blue_slime'],
                                        'prob': 1,
                                },
                        ]
                },
                'drops': LOOTS['tier1'] + [{'item': ITEMS['blue_gem'], 'prob': 0.5}],
                'no_hit': False,
                'hit_rect': pg.Rect(0,0,50,50),
                'walk_speed': 70,
                'hit_speed': 1,
        },
        'dotted_slime': {
                'name': 'dotted_slime',
                'stand_frames': 'dotted_slime_walking.png',
                'walk_frames': 'dotted_slime_walking.png',
                'hit_frames': 'dotted_slime_hit.png',
                'hp': 70,
                'damage': 20,
                'defence': 8,
                'exp': 45,
                'gold': 50,
                'quest_drops': {
                        'slime_quest': [
                                { 
                                        'item': ITEMS['dotted_slime'],
                                        'prob': 1,
                                },
                        ]
                },
                'drops': LOOTS['tier2'] + [{'item': ITEMS['red_gem'], 'prob': 0.2}, {'item': ITEMS['blue_gem'], 'prob': 0.2}, {'item': ITEMS['green_gem'], 'prob': 0.2}],
                'no_hit': False,
                'hit_rect': pg.Rect(0,0,50,50),
                'walk_speed': 70,
                'hit_speed': 1,
        },
        'horror-bubble': {
                'name': 'horror-bubble',
                'stand_frames': 'horror_bubble_standing.png',
                'walk_frames': 'horror_bubble_standing.png',
                'hit_frames': 'horror_bubble_hit.png',
                'hp': 5000,
                'damage': 500,
                'defence': 100,
                'exp': 4000,
                'gold': 1000,
                'quest_drops': {
                },
                'drops': LOOTS['tier3'],
                'no_hit': False,
                'hit_rect': pg.Rect(0,0,40,40),
                'walk_speed': 50,
                'hit_speed': 1,
        },
        'green-spider': {
                'name': 'green-spider',
                'stand_frames': 'spider_stand.png',
                'walk_frames': 'spider_walk.png',
                'hit_frames': 'spider_hit.png',
                'hp': 100,
                'damage': 20,
                'defence': 10,
                'exp': 130,
                'gold': 80,
                'quest_drops': {},
                'drops': LOOTS['tier2'] + [{'item': ITEMS['green_spider_leg'], 'prob': 1}],
                'no_hit': False,
                'hit_rect': pg.Rect(0,0,40,40),
                'walk_speed': 100,
                'hit_speed': 1,
        },
        'red_spider': {
                'name': 'red_spider',
                'stand_frames': 'red_spider_stand.png',
                'walk_frames': 'red_spider_walk.png',
                'hit_frames': 'red_spider_hit.png',
                'hp': 120,
                'damage': 28,
                'defence': 10,
                'exp': 180,
                'gold': 100,
                'quest_drops': {},
                'drops': LOOTS['tier2'] + [{'item': ITEMS['red_spider_leg'], 'prob': 1}],
                'no_hit': False,
                'hit_rect': pg.Rect(0,0,40,40),
                'walk_speed': 100,
                'hit_speed': 1,
        },
        'spider_boss': {
                'name': 'spider_boss',
                'stand_frames': 'spider_boss_stand.png',
                'walk_frames': 'spider_boss_walk.png',
                'hit_frames': 'spider_boss_hit.png',
                'hp': 500,
                'damage': 40,
                'defence': 12,
                'exp': 500,
                'gold': 300,
                'quest_drops': {},
                'drops': LOOTS['tier3'],
                'no_hit': False,
                'hit_rect': pg.Rect(0,0,60,60),
                'walk_speed': 200,
                'hit_speed': 1.4,
        },

        # Friendly mobs
        'pig': {
                'name': 'pig',
                'stand_frames': 'pig_standing.png',
                'walk_frames': 'pig_walking.png',
                'hp': 30,
                'defence': 1,
                'exp': 0,
                'gold': 0,
                'quest_drops': {},
                'drops': [],
                'action': None,
                'hit_rect': pg.Rect(0,0,40,40),
                'follows': True,
                'walk_speed': 70,                
        },
        'sheep': {
                'name': 'sheep',
                'stand_frames': 'sheep_standing.png',
                'walk_frames': 'sheep_walking.png',
                'hp': 30,
                'defence': 1,
                'exp': 0,
                'gold': 0,
                'quest_drops': {},
                'drops': [],
                'action': {
                        'name': 'shear the sheep',
                        'item_needed': 'Scissors',
                        'drop': ITEMS['wool']
                },
                'hit_rect': pg.Rect(0,0,40,40),
                'follows': False,
                'walk_speed': 70,
        },
        'chicken': {
                'name': 'chicken',
                'stand_frames': 'chicken_standing.png',
                'walk_frames': 'chicken_walking.png',
                'hp': 10,
                'defence': 1,
                'exp': 0,
                'gold': 0,
                'quest_drops': {},
                'drops': [],
                'action': {
                        'name': 'get the chicken egg',
                        'item_needed': None,
                        'drop': ITEMS['chicken_egg']
                },
                'hit_rect': pg.Rect(0,0,20,20),
                'follows': False,
                'walk_speed': 70,
        },
}

HIT_SPELLS = {
        'fire_spell1': {
                'id': 'fire_spell1',
                'name': 'Fire Spell',
                'file': 'fire_spell',
                'hit_file': 'fire_spell_hit',
                'damage': 20,
                'strength_needed': 5,
                'agility_needed': 0,
                'fortune_needed': 0,
                'price': 800,
                'slow': 1,
                'cooldown': 4,
                'effect_time': 0,
                'dot': 0,
                'type': 'spell',
                'level': 5,
                'requirements': [],
                'needed': [{"name": "Red gem", "amount": 2}],
                'effect': "Pure damage",
                'is_sellable': False
        },
        'ice_spell1': {
                'id': 'ice_spell1',
                'name': 'Ice Spell',
                'file': 'ice_spell',
                'hit_file': 'ice_spell_hit',
                'damage': 5,
                'strength_needed': 0,
                'agility_needed': 5,
                'fortune_needed': 0,
                'price': 800,
                'slow': 1.5,
                'cooldown': 5,
                'effect_time': 5,
                'dot': 0,
                'type': 'spell',
                'level': 5,
                'requirements': [],
                'needed': [{"name": "Blue gem", "amount": 2}],
                'effect': "Slows enemy by 50%",
                'is_sellable': False
        },
        'poison_spell1': {
                'id': 'poison_spell1',
                'name': 'Poison spell',
                'file': 'poison_spell',
                'hit_file': 'poison_spell_hit',
                'damage': 5,
                'strength_needed': 0,
                'agility_needed': 0,
                'fortune_needed': 5,
                'price': 800,
                'slow': 1,
                'cooldown': 5,
                'effect_time': 5,
                'dot': 5,
                'type': 'spell',
                'level': 5,
                'requirements': [],
                'needed': [{"name": "Green gem", "amount": 2}],
                'effect': "5 damage per second for 5 seconds",
                'is_sellable': False
        }
}

MAX_SPELLS_PER_LEVEL = {
        6: 1,
        10: 2,
        20: 3,
        40: 4,
        60: 5,
        100: 6
}

SPECIAL_TREASURES = ["secret-corridor2-treasure5", "apple_tree"]

SPECIAL_TREASURE_DROPS = {
        'secret-corridor2-treasure5': ['mighty-sword'],
        'apple_tree': ['apple']
}

CONTINUING_TREASURES = ["apple_tree"]
SELLERS = ["weapon_seller", "armor_seller", "store_seller", "bakery-beebo", "seed_seller", "crafting_beebo", "mage_beebo", "spider-beebo"]
BUYERS = ["seller-beebo1", "buyer-beebo2"]

ARMOR_TYPES = ["boots", "chestplate", "plate", "gloves", "pants", "ring", "cloak", "helmet"]

SHOPS = {
        "weapon_seller": [
                # ITEMS['basic_axe],
                ITEMS['steel_sword'],
                ITEMS['steel_spear']],
        "armor_seller": [
                ITEMS['leather_boots'],
                ITEMS['leather_gloves'],
                ITEMS['leather_pants'],
                ITEMS['leather_chestplate'],
                ITEMS['basic_ring'],
                ITEMS['leather_cloak']
        ],
        "store_seller": [
                    ITEMS['small_hp_potion']
                ],
        "bakery-beebo": [
                ITEMS['apple_pie'],
                ITEMS['omelet'],
                ITEMS['cooked_chicken_egg']
        ],
        "seed_seller": [
                #ITEMS['scissors']
        ],
        "crafting_beebo": [
                ITEMS['wool_boots'],
                ITEMS['wool_pants'],
                ITEMS['wool_shirt'],
        ],
        "mage_beebo": [
                ITEMS['normal_hp_potion'],
                HIT_SPELLS['fire_spell1'],
                HIT_SPELLS['ice_spell1'],
                HIT_SPELLS['poison_spell1'],
                ITEMS['red_gem'],
                ITEMS['blue_gem'],
                ITEMS['green_gem'],
        ],
        "spider-beebo": [
                ITEMS['normal_hp_potion'],
                ITEMS['potion_of_fortune'],
                ITEMS['red_gem'],
                ITEMS['blue_gem'],
                ITEMS['green_gem'],
                ITEMS['sword_of_ancient_gods']
        ]
}

HEAD_LINES = {
        "weapon_seller": "Weapon store",
        "armor_seller": "Armor store",
        "store_seller": "Potion store",
        "bakery-beebo": "Bakery",
        "seed_seller": "Garden store",
        "crafting_beebo": "Crafting store",
        "mage_beebo": "Magic store",
        "spider-beebo": "Potion store",
        }
        
    