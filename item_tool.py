# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
import game_data


class ItemTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Item Tool"
        self.icon = commons.it_icon_small

        super().init()
