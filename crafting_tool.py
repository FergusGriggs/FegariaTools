# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
import game_data


class CraftingTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Crafting Tool"
        self.icon = commons.ct_icon_small

        super().init()
