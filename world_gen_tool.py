# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
from widget import *
import game_data


class WorldGenTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "World Gen Tool"
        self.entity_type = "Gen Type"
        self.xml_group_name = "world_gens"
        self.xml_type_name = "world_gen"

        self.set_xml_data_root()

        self.icon = commons.wgt_icon_small
        self.accent_col = commons.world_gen_tool_col

        super().init()

    def set_xml_data_root(self):
        self.xml_data_root = game_data.world_gen_data

    def export_tool_data(self):
        game_data.save_world_gen_data()

    def reload_tool_data(self):
        game_data.load_world_gen_data()

    def widget_altered(self, widget):
        super().widget_altered(widget)
