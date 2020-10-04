# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
import game_data


class StructureTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Structure Tool"
        self.icon = commons.st_icon_small

        super().init()
