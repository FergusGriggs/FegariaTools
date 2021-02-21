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
        self.entity_type = "Recipe"
        self.xml_data_root = game_data.crafting_data
        self.xml_group_name = "crafting_recipes"
        self.xml_type_name = "crafting_recipe"

        self.icon = commons.ct_icon_small
        self.accent_col = commons.crafting_tool_col

        super().init()
