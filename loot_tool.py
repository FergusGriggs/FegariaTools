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
        self.entity_type = "Loot"
        self.xml_data_root = game_data.loot_data
        self.xml_group_name = "lootgroups"
        self.xml_type_name = "loot"

        self.icon = commons.lt_icon_small
        self.accent_col = commons.loot_tool_col

        super().init()
