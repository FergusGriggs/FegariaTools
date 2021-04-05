# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
from widget import *
import game_data


class AITool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "AI Tool"
        self.entity_type = "AI"
        self.xml_group_name = "ais"
        self.xml_type_name = "ai"

        self.set_xml_data_root()

        self.icon = commons.at_icon_small
        self.accent_col = commons.ai_tool_col

        super().init()

    def set_xml_data_root(self):
        self.xml_data_root = game_data.ai_data

    def export_tool_data(self):
        game_data.save_ai_data()

    def reload_tool_data(self):
        game_data.load_ai_data()

    def widget_altered(self, widget):
        super().widget_altered(widget)
