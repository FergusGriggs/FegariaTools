# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
import game_data


class WorldGenTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "World Gen Tool"
        self.entity_type = "World Gen"
        self.xml_data_root = game_data.world_gen_data
        self.xml_group_name = "world_gens"
        self.xml_type_name = "world_gen"

        self.icon = commons.wgt_icon_small
        self.accent_col = commons.world_gen_tool_col

        super().init()
