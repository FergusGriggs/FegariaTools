# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
from widget import *
import game_data


class EntityTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Entity Tool"
        self.entity_type = "Entity"
        self.xml_group_name = "entities"
        self.xml_type_name = "entity"

        self.set_xml_data_root()

        self.icon = commons.et_icon_small
        self.accent_col = commons.entity_tool_col

        super().init()

    def set_xml_data_root(self):
        self.xml_data_root = game_data.entity_data

    def export_tool_data(self):
        game_data.save_entity_data()

    def reload_tool_data(self):
        game_data.load_entity_data()

    def widget_altered(self, widget):
        super().widget_altered(widget)
