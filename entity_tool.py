# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
import game_data


class EntityTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Entity Tool"
        self.icon = commons.et_icon_small

        super().init()
