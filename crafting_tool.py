# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
from widget import *
import game_data


class CraftingTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Crafting Tool"
        self.entity_type = "Recipe"
        self.xml_group_name = "crafting_recipes"
        self.xml_type_name = "crafting_recipe"

        self.set_xml_data_root()

        self.icon = commons.ct_icon_small
        self.accent_col = commons.crafting_tool_col

        super().init()

    def set_xml_data_root(self):
        self.xml_data_root = game_data.crafting_data

    def export_tool_data(self):
        game_data.save_crafting_data()

    def reload_tool_data(self):
        game_data.load_crafting_data()

    def widget_altered(self, widget):
        super().widget_altered(widget)
