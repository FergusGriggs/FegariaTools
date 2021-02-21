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
        self.entity_type = "Structure"
        self.xml_data_root = game_data.structure_data
        self.xml_group_name = "structures"
        self.xml_type_name = "structure"

        self.icon = commons.st_icon_small
        self.accent_col = commons.structure_tool_col

        super().init()
