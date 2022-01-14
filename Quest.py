import pygame as pg
from os import path
from settings import *
from helpers import *
from SpriteSheet import *

class Quest:

    def __init__(self, quest_id):
        self.quest_id = quest_id
        self.progress = 0
        