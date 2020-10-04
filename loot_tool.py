# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
import game_data


class LootTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Loot Tool"
        self.icon = commons.lt_icon_small

        super().init()
